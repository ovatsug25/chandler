
__revision__  = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2003-2004 Open Source Applications Foundation"
__license__   = "http://osafoundation.org/Chandler_0.1_license_terms.htm"

from threading import currentThread
from datetime import timedelta
from time import time, sleep

from chandlerdb.item.c import CItem, Nil, Default, isitem
from chandlerdb.util.c import isuuid, HashTuple
from chandlerdb.persistence.c import DBLockDeadlockError

from repository.item.RefCollections import RefList, TransientRefList
from repository.item.Indexed import Indexed
from repository.item.Sets import AbstractSet
from repository.persistence.RepositoryError \
     import RepositoryError, MergeError, VersionConflictError
from repository.persistence.RepositoryView \
     import RepositoryView, OnDemandRepositoryView
from repository.persistence.Repository import Repository
from repository.persistence.DBLob import DBLob
from repository.persistence.DBRefs import DBRefList, DBChildren, DBNumericIndex
from repository.persistence.DBItemIO import DBItemWriter


class DBRepositoryView(OnDemandRepositoryView):

    def openView(self):

        self._log = set()
        self._indexWriter = None

        super(DBRepositoryView, self).openView()

    def _logItem(self, item):

        if super(DBRepositoryView, self)._logItem(item):
            self._log.add(item)
            return True
        
        return False

    def dirtyItems(self):

        return iter(self._log)

    def hasDirtyItems(self):

        return len(self._log) > 0

    def dirlog(self):

        for item in self._log:
            print item.itsPath

    def cancel(self):

        refCounted = self.isRefCounted()

        for item in self._log:
            item.setDirty(0)
            item._unloadItem(not item.isNew(), self, False)

        self._instanceRegistry.update(self._deletedRegistry)
        self._log.update(self._deletedRegistry.itervalues())
        self._deletedRegistry.clear()
        self.cancelDelete()

        for item in self._log:
            if not item.isNew():
                self.logger.debug('reloading version %d of %s',
                                  self._version, item)
                self.find(item._uuid)

        self._log.clear()

        if self.isDirty():
            self._roots._clearDirties()
            self.setDirty(0)

        self.prune(10000)

    def queryItems(self, kind=None, attribute=None):

        store = self.store
        
        for itemReader in store.queryItems(self, self._version,
                                           kind and kind.itsUUID,
                                           attribute and attribute.itsUUID):
            uuid = itemReader.getUUID()
            if uuid not in self._deletedRegistry:
                # load and itemReader, trick to pass reader directly to find
                item = self.find(uuid, itemReader)
                if item is not None:
                    yield item

    def queryItemKeys(self, kind=None, attribute=None):

        store = self.store
        
        for uuid in store.queryItemKeys(self, self._version,
                                        kind and kind.itsUUID,
                                        attribute and attribute.itsUUID):
            if uuid not in self._deletedRegistry:
                yield uuid

    def kindForKey(self, uuid):

        if uuid in self._registry:
            return self[uuid].itsKind

        uuid = self.store.kindForKey(self, self.itsVersion, uuid)
        if uuid is not None:
            return self[uuid]

        return None

    def searchItems(self, query, attribute=None, load=True):

        if attribute is not None:
            uAttr = attribute.itsUUID
        else:
            uAttr = None

        for uItem, uAttr in self.store.searchItems(self, self.itsVersion,
                                                   query, uAttr):
            item = self.find(uItem, load)
            if item is not None:
                yield item, self[uAttr]

    def _createRefList(self, item, name, otherName,
                       persisted, readOnly, new, uuid):

        if persisted:
            return DBRefList(self, item, name, otherName, readOnly, new, uuid)
        else:
            return TransientRefList(item, name, otherName, readOnly)

    def _createChildren(self, parent, new):

        return DBChildren(self, parent, new)

    def _createNumericIndex(self, **kwds):

        return DBNumericIndex(self, **kwds)
    
    def _registerItem(self, item):

        super(DBRepositoryView, self)._registerItem(item)
        if item.isDirty():
            self._log.add(item)

    def _unregisterItem(self, item, reloadable):

        super(DBRepositoryView, self)._unregisterItem(item, reloadable)
        if item.isDirty():
            self._log.remove(item)

    def _getLobType(self):

        return DBLob

    def _startTransaction(self, nested=False):

        return self.store.startTransaction(self, nested)

    def _commitTransaction(self, status):

        if self._indexWriter is not None:
            self.store._index.commitIndexWriter(self._indexWriter)
            self._indexWriter = None
            
        self.store.commitTransaction(self, status)

    def _abortTransaction(self, status):

        if self._indexWriter is not None:
            try:
                self.store._index.abortIndexWriter(self._indexWriter)
            except:
                pass
                #self.logger.exception('Ignorable exception while closing indexWriter during _abortTransaction')
            self._indexWriter = None
            
        self.store.abortTransaction(self, status)

    def _getIndexWriter(self):

        if self._indexWriter is None:
            store = self.store
            if not store._ramdb and store.txn is None:
                raise RepositoryError, "Can't index outside transaction"
            self._indexWriter = store._index.getIndexWriter()

        return self._indexWriter

    def _dispatchHistory(self, history, refreshes, oldVersion, newVersion):

        refs = self.store._refs
        watcherDispatch = self._watcherDispatch

        def dirtyNames():
            if kind is None:
                names = ()
            else:
                names = kind._nameTuple(dirties)
            if status & CItem.KDIRTY:
                names += ('itsKind',)
            return names

        for uItem, version, uKind, status, uParent, pKind, dirties in history:

            if not (pKind is None or pKind == DBItemWriter.NOITEM):
                kind = self.find(pKind)
                if kind is not None:
                    kind.extent._collectionChanged('refresh', 'collection',
                                                   'extent', uItem)

            kind = self.find(uKind)
            names = None
            if kind is not None:
                kind.extent._collectionChanged('refresh', 'collection',
                                               'extent', uItem)
                
                dispatch = self.findValue(uItem, 'watcherDispatch', None)
                if dispatch:
                    isNew = (status & CItem.NEW) != 0
                    for attribute, watchers in dispatch.iteritems():
                        if watchers:
                            if attribute is None:  # item watchers
                                if names is None:
                                    names = dirtyNames()
                                for watcher, watch, methodName in watchers:
                                    watcher = self[watcher.itsUUID]
                                    getattr(watcher, methodName)('refresh', uItem, names)
                            elif isNew or attribute in dirties:
                                value = self.findValue(uItem, attribute, None)
                                if not isuuid(value):
                                    if isinstance(value, RefList):
                                        value = value.uuid
                                    else:
                                        continue
                                for uRef in refs.iterHistory(self, value, version - 1, version, True):
                                    if uRef in refreshes:
                                        self.invokeWatchers(watchers, 'refresh', 'collection', uItem, attribute, uRef)

                for name in kind._iterNotifyAttributes():
                    value = self.findValue(uItem, name, None)
                    if isuuid(value):
                        if kind.getAttribute(name).c.cardinality != 'list':
                            continue
                        refsIterator = refs.iterKeys(self, value, version)
                    elif isinstance(value, RefList):
                        refsIterator = value.iterkeys()
                    else:
                        continue
                    otherName = kind.getOtherName(name, None)
                    for uRef in refsIterator:
                        dispatch = self.findValue(uRef, 'watcherDispatch', None)
                        if dispatch:
                            watchers = dispatch.get(otherName, None)
                            if watchers:
                                self.invokeWatchers(watchers, 'changed', 'notification', uRef, otherName, uItem)

            if watcherDispatch and uItem in watcherDispatch:
                watchers = watcherDispatch[uItem].get(None)
                if watchers:
                    if names is None:
                        names = dirtyNames()
                    for watcher, watch, methodName in list(watchers):
                        watcher = self.find(watcher)
                        if watcher is not None:
                            getattr(watcher, methodName)('refresh', uItem, names)

    def _dispatchChanges(self, changes):

        for item, version, status, literals, references in changes:

            kind = item.itsKind
            uItem = item.itsUUID
            if kind is not None:
                kind.extent._collectionChanged('changed', 'notification',
                                               'extent', uItem)

                for name in kind._iterNotifyAttributes():
                    value = getattr(item, name, None)
                    if value is not None and isinstance(value, RefList):
                        otherName = value._otherName
                        for uRef in value.iterkeys():
                            dispatch = self.findValue(uRef, 'watcherDispatch', None)
                            if dispatch:
                                watchers = dispatch.get(otherName, None)
                                if watchers:
                                    self.invokeWatchers(watchers, 'changed', 'notification', uRef, otherName, uItem)
    
    def refresh(self, mergeFn=None, version=None, notify=True):

        if not self._status & RepositoryView.REFRESHING:
            try:
                self._status |= RepositoryView.REFRESHING
                while True:
                    try:
                        txnStatus = self._startTransaction(False)
                        self._refresh(mergeFn, version, notify)
                    except DBLockDeadlockError:
                        self.logger.info('%s retrying refresh aborted by deadlock (thread: %s)', self, currentThread().getName())
                        self._abortTransaction(txnStatus)
                        sleep(1)
                        continue
                    except:
                        self._abortTransaction(txnStatus)
                        raise
                    else:
                        self._abortTransaction(txnStatus)
                        return
            finally:
                self._status &= ~RepositoryView.REFRESHING

        else:
            self.logger.warning('%s: skipping recursive refresh', self)

    def _refresh(self, mergeFn=None, version=None, notify=True):

        store = self.store
        if not version:
            newVersion = store.getVersion()
        else:
            newVersion = min(long(version), store.getVersion())
        
        refCounted = self.isRefCounted()

        def _refresh(items):
            for item in items():
                item._unloadItem(refCounted or item.isPinned(), self, False)
            for item in items():
                if refCounted or item.isPinned():
                    if item.isSchema():
                        self.find(item.itsUUID)
            for item in items():
                if refCounted or item.isPinned():
                    self.find(item.itsUUID)

        if newVersion > self._version:
            history = []
            refreshes = set()
            deletes = set()
            merges = {}
            unloads = {}
            dangling = []

            self._refreshItems(self._version, newVersion,
                               history, refreshes, merges, unloads, deletes)
            oldVersion = self._version
            self._version = newVersion
            _refresh(unloads.itervalues)

            if merges:
                newChanges = {}
                changes = {}
                indexChanges = {}

                def _unload(keys):
                    for uItem in keys():
                        item = self.find(uItem)
                        item.setDirty(0)
                        item._unloadItem(True, self, False)

                try:
                    self.recordChangeNotifications()

                    for uItem, (dirty, uParent, dirties) in merges.iteritems():
                        item = self.find(uItem, False)
                        newDirty = item.getDirty()
                        _newChanges = {}
                        _changes = {}
                        _indexChanges = {}
                        newChanges[uItem] = (newDirty, _newChanges)
                        changes[uItem] = (dirty, _changes)
                        self._collectChanges(item, newDirty,
                                             dirty, HashTuple(dirties),
                                             oldVersion, newVersion,
                                             _newChanges, _changes,
                                             _indexChanges)
                        if _indexChanges:
                            indexChanges[uItem] = _indexChanges

                except:
                    self.discardChangeNotifications()
                    self._version = oldVersion
                    _refresh(unloads.itervalues)
                    raise

                try:
                    _unload(merges.iterkeys)

                    for uItem, (dirty, uParent, dirties) in merges.iteritems():
                        item = self.find(uItem)
                        newDirty, _newChanges = newChanges[uItem]
                        dirty, _changes = changes[uItem]
                        self._applyChanges(item, newDirty,
                                           dirty, HashTuple(dirties),
                                           oldVersion, newVersion,
                                           _newChanges, _changes, mergeFn,
                                           dangling)
                    self._applyIndexChanges(indexChanges, deletes)
                    for uItem, name, uRef in dangling:
                        item = self.find(uItem)
                        if item is not None:
                            item._references._removeRef(name, uRef)

                except:
                    self.discardChangeNotifications()
                    self._version = oldVersion
                    _refresh(unloads.itervalues)

                    _unload(merges.iterkeys)
                    deletes.clear()
                    del dangling[:]

                    for uItem, (dirty, uParent, dirties) in merges.iteritems():
                        item = self.find(uItem)
                        newDirty, _newChanges = newChanges[uItem]
                        self._applyChanges(item, newDirty, 0, (),
                                           oldVersion, newVersion,
                                           _newChanges, None, None, None)
                    self._applyIndexChanges(indexChanges, deletes)
                    raise

                else:
                    self.playChangeNotifications()

            if notify:
                before = time()
                self._dispatchHistory(history, refreshes,
                                      oldVersion, newVersion)
                count = self.dispatchNotifications()
                duration = time() - before
                if duration > 1.0:
                    self.logger.warning('%s %d notifications ran in %s',
                                        self, len(history) + count,
                                        timedelta(seconds=duration))
            else:
                self.flushNotifications()

            self.prune(10000)

        elif newVersion == self._version:
            if notify:
                self.dispatchNotifications()
            else:
                self.flushNotifications()

        elif newVersion < self._version:
            self.cancel()
            refCounted = self.isRefCounted()
            unloads = [item for item in self._registry.itervalues()
                       if item._version > newVersion]
            self._version = newVersion
            _refresh(unloads.__iter__)
            self.flushNotifications()

    def commit(self, mergeFn=None, notify=True):

        if self._status & RepositoryView.COMMITTING:
            self.logger.warning('%s: skipping recursive commit', self)
        elif len(self._log) + len(self._deletedRegistry) > 0:
            try:
                release = False
                release = self._acquireExclusive()
                self._status |= RepositoryView.COMMITTING
                
                store = self.store
                before = time()

                size = 0L
                txnStatus = 0
                lock = None

                def finish(commit):
                    if txnStatus:
                        if commit:
                            self._commitTransaction(txnStatus)
                        else:
                            self._abortTransaction(txnStatus)
                    return store.releaseLock(lock), 0
        
                while True:
                    try:
                        while True:
                            self.refresh(mergeFn, None, notify)
                            lock = store.acquireLock()
                            newVersion = store.getVersion()
                            if newVersion > self.itsVersion:
                                lock = store.releaseLock(lock)
                            else:
                                break

                        if self.isDeferringDelete():
                            self.logger.info('%s effecting deferred deletes', self)
                            self.effectDelete()

                        count = len(self._log) + len(self._deletedRegistry)
                        if count > 500:
                            self.logger.info('%s committing %d items...',
                                             self, count)

                        if count > 0:
                            txnStatus = self._startTransaction(True)
                            if txnStatus == 0:
                                raise AssertionError, 'no transaction started'

                            newVersion = store.nextVersion()

                            itemWriter = DBItemWriter(store)
                            for item in self._log:
                                size += self._saveItem(item, newVersion,
                                                       itemWriter)
                            for item in self._deletedRegistry.itervalues():
                                size += self._saveItem(item, newVersion,
                                                       itemWriter)
                            if self.isDirty():
                                size += self._roots._saveValues(newVersion)

                        lock, txnStatus = finish(True)
                        break

                    except DBLockDeadlockError:
                        self.logger.info('%s retrying commit aborted by deadlock (thread: %s)', self, currentThread().getName())
                        lock, txnStatus = finish(False)
                        sleep(1)
                        continue

                    except Exception, e:
                        self.logger.warning('%s commit aborted by error: %s',
                                            self, e)
                        lock, txnStatus = finish(False)
                        raise

                self._version = newVersion
                
                if self._log:
                    for item in self._log:
                        item._version = newVersion
                        item.setDirty(0, None)
                        item._status &= ~(CItem.NEW | CItem.MERGED)
                    self._log.clear()

                    if self.isDirty():
                        self._roots._clearDirties()
                        self.setDirty(0)

                if self._deletedRegistry:
                    self._deletedRegistry.clear()

                after = time()

                if count > 0:
                    duration = after - before
                    try:
                        iSpeed = "%d items/s" % round(count / duration)
                        dSpeed = "%d kbytes/s" % round((size >> 10) / duration)
                    except ZeroDivisionError:
                        iSpeed = dSpeed = 'speed could not be measured'

                    self.logger.info('%s committed %d items (%d kbytes) in %s, %s (%s)', self, count, size >> 10, timedelta(seconds=duration), iSpeed, dSpeed)

            finally:
                self._status &= ~RepositoryView.COMMITTING
                if release:
                    self._releaseExclusive()

    def _saveItem(self, item, newVersion, itemWriter):

        if self.isDebug():
            self.logger.debug('saving version %d of %s',
                              newVersion, item.itsPath)

        if item.isDeleted() and item.isNew():
            return 0
                    
        return itemWriter.writeItem(item, newVersion)

    def mapChanges(self, freshOnly=False):

        if freshOnly:
            if self._status & RepositoryView.FDIRTY:
                self._status &= ~RepositoryView.FDIRTY
            else:
                return

        for item in list(self._log):   # self._log may change while looping
            status = item._status
            if not freshOnly or freshOnly and status & CItem.FDIRTY:
                if freshOnly:
                    status &= ~CItem.FDIRTY
                    item._status = status

                if item.isDeleted():
                    yield (item, item._version, status, [], [])
                elif item.isNew():
                    yield (item, item._version, status,
                           item._values.keys(),
                           item._references.keys())
                else:
                    yield (item, item._version, status,
                           item._values._getDirties(), 
                           item._references._getDirties())
    
    def mapHistory(self, fromVersion=-1, toVersion=0, history=None):

        if history is None:
            store = self.store
            if fromVersion == -1:
                fromVersion = self._version
            if toVersion == 0:
                toVersion = store.getVersion()
            history = store._items.iterHistory(self, fromVersion, toVersion)

        for uItem, version, uKind, status, uParent, pKind, dirties in history:
            kind = self.find(uKind)
            if not (pKind is None or pKind == DBItemWriter.NOITEM):
                prevKind = self.find(pKind)
            else:
                prevKind = None
            values = []
            references = []
            if kind is not None:
                for name, attr, k in kind.iterAttributes():
                    if name in dirties:
                        if kind.getOtherName(name, None, None) is not None:
                            references.append(name)
                        else:
                            values.append(name)
            yield uItem, version, kind, status, values, references, prevKind

    def _refreshItems(self, oldVersion, toVersion,
                      history, refreshes, merges, unloads, deletes):

        for args in self.store._items.iterHistory(self, oldVersion, toVersion):
            uItem, version, uKind, status, uParent, prevKind, dirties = args

            history.append(args)
            refreshes.add(uItem)

            if status & CItem.DELETED:
                deletes.add(uItem)

            item = self.find(uItem, False)
            if item is not None:
                if item.isDirty():
                    oldDirty = status & CItem.DIRTY
                    if uItem in merges:
                        od, x, d = merges[uItem]
                        merges[uItem] = (od | oldDirty, uParent,
                                         d.union(dirties))
                    else:
                        merges[uItem] = (oldDirty, uParent, set(dirties))

                elif item.itsVersion < version:
                    unloads[uItem] = item

            elif uItem in self._deletedRegistry:
                kind = self.find(uKind, False)
                if kind is None:
                    self._e_1_delete(uItem, uKind, oldVersion, version)
                else:
                    self._e_1_delete(uItem, kind, oldVersion, version)

    def _collectChanges(self, item, newDirty, dirty, dirties,
                        version, newVersion,
                        newChanges, changes, indexChanges):

        CDIRTY = CItem.CDIRTY
        NDIRTY = CItem.NDIRTY
        RDIRTY = CItem.RDIRTY
        VDIRTY = CItem.VDIRTY

        if newDirty & CDIRTY:
            children = item._children
            newChanges[CDIRTY] = dict(children._iterChanges())
            if dirty & CDIRTY:
                changes[CDIRTY] = dict(children._iterHistory(version, newVersion))
            else:
                changes[CDIRTY] = {}

        if newDirty & NDIRTY:
            newChanges[NDIRTY] = (item.itsParent.itsUUID, item.itsName,
                                  item.isDeferred())

        if newDirty & RDIRTY:
            newChanges[RDIRTY] = _newChanges = {}
            changes[RDIRTY] = _changes = {}
            item._references._collectChanges(self, RDIRTY, dirties,
                                             _newChanges, _changes,
                                             indexChanges, version, newVersion)
                
        if newDirty & VDIRTY:
            newChanges[VDIRTY] = _newChanges = {}
            item._references._collectChanges(self, VDIRTY, dirties,
                                             _newChanges, None, indexChanges,
                                             version, newVersion)
            item._values._collectChanges(self, VDIRTY, dirties,
                                         _newChanges, None, indexChanges,
                                         version, newVersion)

    def _applyChanges(self, item, newDirty, dirty, dirties,
                      version, newVersion, newChanges, changes, mergeFn,
                      dangling):

        CDIRTY = CItem.CDIRTY
        NDIRTY = CItem.NDIRTY
        RDIRTY = CItem.RDIRTY
        VDIRTY = CItem.VDIRTY

        def ask(reason, name, value):
            mergedValue = Default
            if mergeFn is not None:
                mergedValue = mergeFn(reason, item, name, value)
            if mergedValue is Default:
                if hasattr(type(item), 'onItemMerge'):
                    mergedValue = item.onItemMerge(reason, name, value)
                if mergedValue is Default:
                    self._e_1_overlap(reason, item, name)
            return mergedValue

        if newDirty & CDIRTY:
            if changes is None:
                if item._children is None:
                    item._children = self._createChildren(item, True)
                item._children._applyChanges(newChanges[CDIRTY], ())
            else:
                item._children._applyChanges(newChanges[CDIRTY],
                                             changes[CDIRTY])
            dirty &= ~CDIRTY
            newDirty &= ~CDIRTY
            item._status |= (CItem.CMERGED | CDIRTY)

        if newDirty & NDIRTY:
            newParent, newName, isDeferred = newChanges[NDIRTY]
            if dirty & NDIRTY:
                if newName != item.itsName:
                    newName = ask(MergeError.RENAME, 'itsName', newName)
                if newParent != item.itsParent.itsUUID:
                    newParent = ask(MergeError.MOVE, 'itsParent',
                                    self.find(newParent)).itsUUID
            if newName != item.itsName:
                item._name = newName
            if newParent != item.itsParent.itsUUID:
                item._parent = self[newParent]
            dirty &= ~NDIRTY
            newDirty &= ~NDIRTY
            if isDeferred:
                item._status |= (CItem.NMERGED | CItem.DEFERRED | NDIRTY)
            else:
                item._status |= (CItem.NMERGED | NDIRTY)

        if newDirty & RDIRTY:
            item._references._applyChanges(self, RDIRTY, dirties, ask,
                                           newChanges, changes, dangling)
            dirty &= ~RDIRTY
            newDirty &= ~RDIRTY
            item._status |= (CItem.RMERGED | RDIRTY)

        if newDirty & VDIRTY:
            item._references._applyChanges(self, VDIRTY, dirties, ask,
                                           newChanges, None, dangling)
            item._values._applyChanges(self, VDIRTY, dirties, ask, newChanges)
            dirty &= ~VDIRTY
            newDirty &= ~VDIRTY
            item._status |= (CItem.VMERGED | VDIRTY)

        if dirty and newDirty:
            raise VersionConflictError, (item, newDirty, dirty)

        self.logger.info('%s merged %s with newer versions, merge status: 0x%0.8x', self, item.itsPath, (item._status & CItem.MERGED))

    def _applyIndexChanges(self, indexChanges, deletes):

        for uItem, _indexChanges in indexChanges.iteritems():
            item = self.find(uItem, False)
            if item is None and uItem not in deletes:
                raise AssertionError, (uItem, "item not found")
            for name, __indexChanges in _indexChanges.iteritems():
                getattr(item, name)._applyIndexChanges(self, __indexChanges,
                                                       deletes)

    def _e_1_delete(self, uItem, uKind, oldVersion, newVersion):

        raise MergeError, ('delete', uItem, 'item %s was deleted in this version (%d) but has later changes in version (%d) where it is of kind %s' %(uItem, oldVersion, newVersion, uKind), MergeError.CHANGE)

    def _e_1_name(self, list, key, newName, name):
        raise MergeError, ('name', type(self).__name__, 'element %s renamed to %s and %s' %(key, newName, name), MergeError.RENAME)

    def _e_2_name(self, list, key, newKey, name):
        raise MergeError, ('name', type(list).__name__, 'element %s named %s conflicts with element %s of same name' %(newKey, name, key), MergeError.NAME)

    def _e_2_move(self, list, key):
        raise MergeError, ('move', type(list).__name__, 'removed element %s was modified in other view' %(key), MergeError.MOVE)

    def _e_1_overlap(self, code, item, name):
        
        raise MergeError, ('callback', item, 'merging values for %s on %s failed because no merge callback was defined or because the merge callback(s) punted' %(name, item._repr_()), code)

    def _e_2_overlap(self, code, item, name):

        raise MergeError, ('bug', item, 'merging refs is not implemented, attribute: %s' %(name), code)

    def _e_3_overlap(self, code, item, name):

        raise MergeError, ('bug', item, 'this merge not implemented, attribute: %s' %(name), code)

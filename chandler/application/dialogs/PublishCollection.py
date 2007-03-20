#   Copyright (c) 2003-2006 Open Source Applications Foundation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


# The collection publishing dialog
# Invoke using the ShowPublishDialog( ) method.

import wx
import logging
import os, sys
from application import schema, Globals
from osaf import sharing
from util import task, viewpool
from i18n import ChandlerMessageFactory as _
from osaf.pim import Remindable, EventStamp
from TurnOnTimezones import ShowTurnOnTimezonesDialog, PUBLISH
import zanshin
from osaf.activity import *

logger = logging.getLogger(__name__)

MAX_UPDATE_MESSAGE_LENGTH = 55

class PublishCollectionDialog(wx.Dialog):

    def __init__(self, parent, title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE,
                 resources=None, view=None, collection=None,
                 publishType='collection', modal=True,
                 name=None):

        wx.Dialog.__init__(self, parent, -1, title, pos, size, style)
        self.resources = resources
        self.view = view
        self.parent = parent
        self.collection = collection    # The collection to share
        self.modal = modal
        self.publishType = publishType
        self.name = name

        self.mySizer = wx.BoxSizer(wx.VERTICAL)

        # Turn on timezones
        notCancelled = ShowTurnOnTimezonesDialog(self, view, modal=True,
                                                 state=PUBLISH)
        if notCancelled == False:
            self.OnCancel(None)
            return

        # Is this collection already shared?

        isShared = sharing.isShared(collection)

        if not isShared:       # Not yet shared, show "Publish"
            self.mainPanel = self.resources.LoadPanel(self,
                                                      "PublishCollection")
            self.buttonPanel = self.resources.LoadPanel(self,
                                                        "PublishButtonsPanel")
        else:                           # Already shared, show "Manage"
            self.mainPanel = self.resources.LoadPanel(self, "ManageCollection")
            self.buttonPanel = self.resources.LoadPanel(self,
                                                        "ManageButtonsPanel")


        # Create/Hide the status panel that appears when there is text to
        # display
        self.statusPanel = self.resources.LoadPanel(self, "StatusPanel")
        self.statusPanel.Hide()
        self.textStatus = wx.xrc.XRCCTRL(self, "TEXT_STATUS")

        self.updatePanel = self.resources.LoadPanel(self, "UpdatePanel")
        self.updatePanel.Hide()
        self.textUpdate = wx.xrc.XRCCTRL(self, "TEXT_UPDATE")
        self.gauge = wx.xrc.XRCCTRL(self, "GAUGE")
        self.gauge.SetRange(100)

        # Fit all the pieces together
        self.mySizer.Add(self.mainPanel, 0, wx.GROW|wx.ALL, 5)
        self.mySizer.Add(self.buttonPanel, 0, wx.GROW|wx.ALL, 5)
        self.SetSizer(self.mySizer)
        self.mySizer.SetSizeHints(self)
        self.mySizer.Fit(self)

        if not isShared:       # Not yet shared, show "Publish"
            self.ShowPublishPanel()
        else:                           # Already shared, show "Manage"
            self.ShowManagePanel()


    def ShowPublishPanel(self):
        # "Publish" mode -- i.e., the collection has not yet been shared

        self.Bind(wx.EVT_BUTTON, self.OnPublish, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=wx.ID_CANCEL)

        collName = self.collection.displayName

        self.currentAccount = schema.ns('osaf.sharing',
            self.view).currentSharingAccount.item

        # Populate the listbox of sharing accounts
        self.accounts = self._getSharingAccounts()
        self.accountsControl = wx.xrc.XRCCTRL(self, "CHOICE_ACCOUNT")
        self.accountsControl.Clear()

        for account in self.accounts:
            newIndex = self.accountsControl.Append(account.displayName)
            self.accountsControl.SetClientData(newIndex, account)
            if account is self.currentAccount:
                self.accountsControl.SetSelection(newIndex)

        self.Bind(wx.EVT_CHOICE,
                  self.OnChangeAccount,
                  id=wx.xrc.XRCID("CHOICE_ACCOUNT"))

        if self.publishType == 'collection': #freebusy doesn't need these
            wx.xrc.XRCCTRL(self, "TEXT_COLLNAME").SetLabel(collName)
            self.CheckboxShareAlarms = wx.xrc.XRCCTRL(self, "CHECKBOX_ALARMS")
            self.CheckboxShareAlarms.SetValue(False)
            self.CheckboxShareStatus = wx.xrc.XRCCTRL(self, "CHECKBOX_STATUS")
            self.CheckboxShareStatus.SetValue(False)
            self.CheckboxShareTriage = wx.xrc.XRCCTRL(self, "CHECKBOX_TRIAGE")
            self.CheckboxShareTriage.SetValue(False)
            self.CheckboxShareReply = wx.xrc.XRCCTRL(self, "CHECKBOX_REPLY")
            self.CheckboxShareReply.SetValue(False)

        self.SetDefaultItem(wx.xrc.XRCCTRL(self, "wxID_OK"))


    def ShowManagePanel(self):
        # "Manage" mode -- i.e., the collection has already been shared

        self.Bind(wx.EVT_BUTTON, self.OnManageDone, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=wx.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.OnCopy,
                  id=wx.xrc.XRCID("BUTTON_CLIPBOARD"))
        self.Bind(wx.EVT_BUTTON, self.OnUnPubSub,
                  id=wx.xrc.XRCID("BUTTON_UNPUBLISH"))

        name = self.collection.displayName
        wx.xrc.XRCCTRL(self, "TEXT_MANAGE_COLLNAME").SetLabel(name)

        share = sharing.getShare(self.collection)
        if share.conduit.account:
            name = share.conduit.account.displayName
        else:
            name = u"(via ticket)"
        wx.xrc.XRCCTRL(self, "TEXT_ACCOUNT").SetLabel(name)


        self.UnPubSub = wx.xrc.XRCCTRL(self, "BUTTON_UNPUBLISH")

        share = sharing.getShare(self.collection)
        if sharing.isSharedByMe(share):
            self.UnPubSub.SetLabel("Unpublish")
        else:
            self.UnPubSub.SetLabel("Unsubscribe")


        self.CheckboxShareAlarms = wx.xrc.XRCCTRL(self, "CHECKBOX_ALARMS")
        self.CheckboxShareAlarms.Enable(True)
        self.CheckboxShareStatus = wx.xrc.XRCCTRL(self, "CHECKBOX_STATUS")
        self.CheckboxShareStatus.Enable(True)
        self.CheckboxShareTriage = wx.xrc.XRCCTRL(self, "CHECKBOX_TRIAGE")
        self.CheckboxShareTriage.Enable(True)
        self.CheckboxShareReply = wx.xrc.XRCCTRL(self, "CHECKBOX_REPLY")
        self.CheckboxShareReply.Enable(True)

        if isinstance(share.conduit, sharing.RecordSetConduit):
            self.originalFilters = set(share.conduit.filters)

        else:
            self.originalFilterAttributes = list(share.filterAttributes)

        self._loadAttributeFilterState(share)

        self.SetDefaultItem(wx.xrc.XRCCTRL(self, "wxID_OK"))

    def OnChangeAccount(self, evt):
        self._hideStatus()

        accountIndex = self.accountsControl.GetSelection()
        account = self.accountsControl.GetClientData(accountIndex)
        self.currentAccount = account



    def OnManageDone(self, evt):

        for share in sharing.SharedItem(self.collection).shares:
            self._saveAttributeFilterState(share)

        if self.modal:
            self.EndModal(False)
        self.Destroy()

        share = sharing.getShare(self.collection)
        needsSync = False
        if isinstance(share.conduit, sharing.RecordSetConduit):
            if share.conduit.filters != self.originalFilters:
                needsSync = True
        else:
            if share.filterAttributes != self.originalFilterAttributes:
                needsSync = True

        if needsSync:
            self.view.commit()
            sharing.scheduleNow(self.view, collection=share.contents,
                                forceUpdate=True)


    def _loadAttributeFilterState(self, share):

        if isinstance(share.conduit, sharing.RecordSetConduit):

            self.CheckboxShareAlarms.SetValue('cid:reminders-filter@osaf.us'
                not in share.conduit.filters)
            self.CheckboxShareStatus.SetValue('cid:event-status-filter@osaf.us'
                not in share.conduit.filters)
            self.CheckboxShareTriage.SetValue('cid:triage-filter@osaf.us'
                not in share.conduit.filters)
            self.CheckboxShareReply.SetValue('cid:needs-reply-filter@osaf.us'
                not in share.conduit.filters)

        else:
            # @@@ Jeffrey: Needs updating for new reminders?
            self.CheckboxShareAlarms.SetValue(Remindable.reminders.name
                not in share.filterAttributes)
            self.CheckboxShareStatus.SetValue(EventStamp.transparency.name
                not in share.filterAttributes)
            self.CheckboxShareTriage.SetValue('_triageStatus'
                not in share.filterAttributes)


    def _getAttributeFilterState(self):
        attrs = []
        if self.publishType == 'collection':

            if isinstance(self.currentAccount, sharing.CosmoAccount):
                attrs = set()
                if not self.CheckboxShareAlarms.GetValue():
                    attrs.add('cid:reminders-filter@osaf.us')
                if not self.CheckboxShareStatus.GetValue():
                    attrs.add('cid:event-status-filter@osaf.us')
                if not self.CheckboxShareTriage.GetValue():
                    attrs.add('cid:triage-filter@osaf.us')
                if not self.CheckboxShareReply.GetValue():
                    attrs.add('cid:needs-reply-filter@osaf.us')

            else:
                # @@@ Jeffrey: Needs updating for new reminders?
                if not self.CheckboxShareAlarms.GetValue():
                    attrs.append(Remindable.reminders.name)
                if not self.CheckboxShareStatus.GetValue():
                    attrs.append(EventStamp.transparency.name)
                if not self.CheckboxShareTriage.GetValue():
                    attrs.append('_triageStatus')
                    attrs.append('_triageStatusChanged')
                    attrs.append('doAutoTriageOnDateChange')
        return attrs


    def _saveAttributeFilterState(self, share):

        if isinstance(share.conduit, sharing.RecordSetConduit):

            if not self.CheckboxShareAlarms.GetValue():
                if 'cid:reminders-filter@osaf.us' not in share.conduit.filters:
                    share.conduit.filters.add('cid:reminders-filter@osaf.us')
            else:
                if 'cid:reminders-filter@osaf.us' in share.conduit.filters:
                    share.conduit.filters.remove('cid:reminders-filter@osaf.us')

            if not self.CheckboxShareStatus.GetValue():
                if 'cid:event-status-filter@osaf.us' not in share.conduit.filters:
                    share.conduit.filters.add('cid:event-status-filter@osaf.us')
            else:
                if 'cid:event-status-filter@osaf.us' in share.conduit.filters:
                    share.conduit.filters.remove('cid:event-status-filter@osaf.us')

            if not self.CheckboxShareTriage.GetValue():
                if 'cid:triage-filter@osaf.us' not in share.conduit.filters:
                    share.conduit.filters.add('cid:triage-filter@osaf.us')
            else:
                if 'cid:triage-filter@osaf.us' in share.conduit.filters:
                    share.conduit.filters.remove('cid:triage-filter@osaf.us')

            if not self.CheckboxShareReply.GetValue():
                if 'cid:needs-reply-filter@osaf.us' not in share.conduit.filters:
                    share.conduit.filters.add('cid:needs-reply-filter@osaf.us')
            else:
                if 'cid:needs-reply-filter@osaf.us' in share.conduit.filters:
                    share.conduit.filters.remove('cid:needs-reply-filter@osaf.us')

        else:
            # @@@ Jeffrey: Needs updating for new reminders?
            if not self.CheckboxShareAlarms.GetValue():
                if Remindable.reminders.name not in share.filterAttributes:
                    share.filterAttributes.append(Remindable.reminders.name)
            else:
                if Remindable.reminders.name in share.filterAttributes:
                    share.filterAttributes.remove(Remindable.reminders.name)

            if not self.CheckboxShareStatus.GetValue():
                if EventStamp.transparency.name not in share.filterAttributes:
                    share.filterAttributes.append(EventStamp.transparency.name)
            else:
                if EventStamp.transparency.name in share.filterAttributes:
                    share.filterAttributes.remove(EventStamp.transparency.name)

            if not self.CheckboxShareTriage.GetValue():
                if '_triageStatus' not in share.filterAttributes:
                    share.filterAttributes.append('_triageStatus')
                    share.filterAttributes.append('_triageStatusChanged')
                    share.filterAttributes.append('doAutoTriageOnDateChange')
            else:
                if '_triageStatus' in share.filterAttributes:
                    share.filterAttributes.remove('_triageStatus')
                    share.filterAttributes.remove('_triageStatusChanged')
                    share.filterAttributes.remove('_doAutoTriageOnDateChange')

            # Make sure no matter what we keep filtering out the attributes that
            # never belong in the XML fork of a CalDAV share:
            if EventStamp.allDay.name in share.filterAttributes:
                # this is such an XML fork
                for attr in sharing.CALDAVFILTER:
                    if attr not in share.filterAttributes:
                        share.filterAttributes.append(attr)




    def _updateCallback(self, activity, *args, **kwds):
        wx.GetApp().PostAsyncEvent(self.updateCallback, activity, *args, **kwds)

    def updateCallback(self, activity, *args, **kwds):

        if 'msg' in kwds:
            msg = kwds['msg'].replace('\n', ' ')
            # @@@MOR: This is unicode unsafe:
            if len(msg) > MAX_UPDATE_MESSAGE_LENGTH:
                msg = "%s..." % msg[:MAX_UPDATE_MESSAGE_LENGTH]
            self._showUpdate(msg)
        if 'percent' in kwds:
            percent = kwds['percent']
            if percent is None:
                self.gauge.Pulse()
            else:
                self.gauge.SetValue(percent)

    def _shutdownInitiated(self):
        if self.modal:
            self.EndModal(False)
        self.Destroy()

    def OnPublish(self, evt):
        self.PublishCollection()

    def PublishCollection(self):
        # Publish the collection

        # Update the UI by disabling/hiding various panels, and swapping in a
        # new set of buttons
        self.mainPanel.Enable(False)
        self.buttonPanel.Hide()
        self.mySizer.Detach(self.buttonPanel)
        self.buttonPanel = self.resources.LoadPanel(self,
                                                    "PublishingButtonsPanel")
        self.mySizer.Add(self.buttonPanel, 0, wx.GROW|wx.ALL, 5)
        publishingButton = wx.xrc.XRCCTRL(self, "BUTTON_PUBLISHING")
        publishingButton.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.OnStopPublish, id=wx.ID_CANCEL)

        self._clearStatus()
        self._resize()
        wx.Yield()

        attrsToExclude = self._getAttributeFilterState()
        accountIndex = self.accountsControl.GetSelection()
        account = self.accountsControl.GetClientData(accountIndex)

        class ShareTask(task.Task):

            def __init__(task, view, account, collection, activity):
                super(ShareTask, task).__init__(view)
                task.accountUUID = account.itsUUID
                task.collectionUUID = collection.itsUUID
                task.activity = activity

            def error(task, err):
                self._shareError(err)
                self.done = True
                self.success = False

            def success(task, result):
                self._finishedShare(result)
                self.done = True
                self.success = True

            def shutdownInitiated(task, arg):
                self._shutdownInitiated()

            def run(task):

                account = task.view.find(task.accountUUID)
                collection = task.view.find(task.collectionUUID)

                msg = _(u"Publishing collection to server...")
                task.callInMainThread(self._showStatus, msg)

                if self.publishType == 'freebusy':
                    displayName = u"%s FreeBusy" % account.username
                else:
                    displayName = self.collection.displayName

                if self.name:
                    displayName = self.name

                shares = sharing.publish(collection, account,
                                         attrsToExclude=attrsToExclude,
                                         displayName=displayName,
                                         publishType=self.publishType,
                                         activity=task.activity)

                shareUUIDs = [item.itsUUID for item in shares]
                return shareUUIDs

        # Run this in its own background thread
        self.view.commit()
        self.taskView = viewpool.getView(self.view.repository)
        self.activity = Activity("Publish: %s" % self.collection.displayName)
        self.currentTask = ShareTask(self.taskView, account, self.collection,
            self.activity)
        self.listener = Listener(activity=self.activity,
            callback=self._updateCallback)
        self.activity.started()
        self.done = False
        self.currentTask.start(inOwnThread=True)

    def _shareError(self, err):

        viewpool.releaseView(self.taskView)

        if not isinstance(err, ActivityAborted):
            self.activity.failed(exception=err)
        self.listener.unregister()

        # Display the error
        self._hideUpdate()
        logger.error("Failed to publish collection.")
        try:
            if isinstance(err, zanshin.error.ConnectionError):
                logger.error("Connection error during publish")

                # Note: do not localize the 'startswith' strings -- these need
                # to match twisted error messages:
                if err.message.startswith("DNS lookup failed"):
                    msg = _(u"Unable to look up server address via DNS")
                elif err.message.startswith("Connection was refused"):
                    msg = _(u"Connection refused by server")
                else:
                    msg = err.message
            else:
                msg = err

            self._showStatus(_(u"\nSharing error:\n%(error)s\n") %
                {'error': msg})

        except Exception, e:
            logger.exception("Error displaying exception")
            self._showStatus(_(u"\nSharing error:\n(Can't display error message;\nSee chandler.log for more details)\n"))
        # self._showStatus("Exception:\n%s" % traceback.format_exc(10))

        # Re-enable the main panel and switch back to the "Share" button
        self.mainPanel.Enable(True)
        self.buttonPanel.Hide()
        self.mySizer.Detach(self.buttonPanel)
        self.buttonPanel = self.resources.LoadPanel(self,
                                                    "PublishButtonsPanel")
        self.mySizer.Add(self.buttonPanel, 0, wx.GROW|wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.OnPublish, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=wx.ID_CANCEL)
        self._resize()

        return False

    def _finishedShare(self, shareUUIDs):

        viewpool.releaseView(self.taskView)

        self.activity.completed()
        self.listener.unregister()

        # Pull in the changes from sharing view
        self.view.refresh(lambda code, item, attr, val: val)


        self._showStatus(_(u" Done\n"))
        self._hideUpdate()

        if self.publishType == 'freebusy':
            share = sharing.getFreeBusyShare(self.collection)
        else:
            share = sharing.getShare(self.collection)

        urls = sharing.getUrls(share)
        if len(urls) == 1:
            self._showStatus(u"%s\n" % urls[0])
        else:
            if self.publishType != 'freebusy':
                self._showStatus(u"View and Edit: %s\n" % urls[0])
            self._showStatus(u"View-only: %s\n" % urls[1])

        self.buttonPanel.Hide()
        self.mySizer.Detach(self.buttonPanel)
        self.buttonPanel = self.resources.LoadPanel(self,
                                                    "PublishedButtonsPanel")
        self.mySizer.Add(self.buttonPanel, 0, wx.GROW|wx.ALL, 5)

        self.Bind(wx.EVT_CLOSE,  self.OnPublishDone)
        self.Bind(wx.EVT_BUTTON, self.OnPublishDone, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCopy,
                  id=wx.xrc.XRCID("BUTTON_CLIPBOARD"))
        self._resize()

        return True

    def OnStopPublish(self, evt):
        self.activity.abortRequested = True

    def OnCancel(self, evt):
        if self.modal:
            self.EndModal(False)
        self.Destroy()

    def OnPublishDone(self, evt):
        if self.modal:
            self.EndModal(False)
        self.Destroy()

    def OnUnPubSub(self, evt):
        share = sharing.getShare(self.collection)
        if sharing.isSharedByMe(share):
            sharing.unpublish(self.collection)
        else:
            sharing.unsubscribe(self.collection)
        if self.modal:
            self.EndModal(False)
        self.Destroy()

    def OnCopy(self, evt):
        gotClipboard = wx.TheClipboard.Open()
        if gotClipboard:
            if self.publishType == 'freebusy':
                share = sharing.getFreeBusyShare(self.collection)
            else:
                share = sharing.getShare(self.collection)
            urls = sharing.getUrls(share)
            if len(urls) == 1:
                urlString = urls[0]
            elif self.publishType == 'freebusy':
                urlString = urls[1]
            else:
                urlString = "Read-write: %s\nRead-only: %s\n" % (urls[0],
                                                                 urls[1])
            wx.TheClipboard.SetData(wx.TextDataObject(unicode(urlString)))
            wx.TheClipboard.Close()

    def _clearStatus(self):
            self.textStatus.SetLabel(u"")

    def _showStatus(self, msg):
        if not self.statusPanel.IsShown():
            self.mySizer.Insert(1, self.statusPanel, 0, wx.GROW, 5)
            self.statusPanel.Show()
        self.textStatus.SetLabel("%s%s" % (self.textStatus.GetLabel(), msg))
        # self.textStatus.ShowPosition(self.textStatus.GetLastPosition())
        self._resize()
        # @@@MOR wx.Yield()

    def _hideStatus(self):
        self._clearStatus()
        if self.statusPanel.IsShown():
            self.statusPanel.Hide()
            self.mySizer.Detach(self.statusPanel)
            self._resize()
            wx.Yield()
        pass

    def _showUpdate(self, text):
        if not self.updatePanel.IsShown():
            self.mySizer.Add(self.updatePanel, 0, wx.GROW, 5)
            self.updatePanel.Show()

        self.textUpdate.SetLabel(text)
        self._resize()

    def _hideUpdate(self):
        if self.updatePanel.IsShown():
            self.updatePanel.Hide()
            self.mySizer.Detach(self.updatePanel)
            self._resize()

    def _resize(self):
        self.mySizer.Layout()
        self.mySizer.SetSizeHints(self)
        self.mySizer.Fit(self)

    def _getSharingAccounts(self):
        #XXX [i18n] Should this be a localized PyICU sort?
        return sorted(
            sharing.SharingAccount.iterItems(self.view),
            key = lambda x: x.displayName.lower()
        )

type_to_xrc_map = {'collection' :
                   ('PublishCollection.xrc', _(u"Publish")),
                   'freebusy'   :
                   ('PublishFreeBusy.xrc', _(u"Publish Free/Busy Calendar"))}

def ShowPublishDialog(parent, view=None, collection=None,
                      publishType = 'collection', modal=False, name=None):
    filename, title = type_to_xrc_map[publishType]
    xrcFile = os.path.join(Globals.chandlerDirectory,
                           'application', 'dialogs', filename)
    #[i18n] The wx XRC loading method is not able to handle raw 8bit paths
    #but can handle unicode
    xrcFile = unicode(xrcFile, sys.getfilesystemencoding())
    resources = wx.xrc.XmlResource(xrcFile)
    win = PublishCollectionDialog(parent,
                                  title,
                                  resources=resources,
                                  view=view,
                                  collection=collection,
                                  publishType=publishType,
                                  modal=modal,
                                  name=name)
    win.CenterOnScreen()
    if modal:
        return win.ShowModal()
    else:
        win.Show()
        return win

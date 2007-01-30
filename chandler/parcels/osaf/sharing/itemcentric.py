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

from osaf import pim
import eim, eimml, translator, shares, errors
import logging

logger = logging.getLogger(__name__)


__all__ = [
    'inbound',
    'outbound',
    'outboundDeletion',
]


# Item-centric peer-to-peer sharing

def inbound(rv, peer, text, allowDeletion=False, debug=False):

    # At some point, which serializer and translator to use should be
    # configurable
    serializer = eimml.EIMMLSerializer # only using class methods
    trans = translator.PIMTranslator(rv)

    inbound, extra = serializer.deserialize(text)

    # Only one recordset is allowed
    if len(inbound) != 1:
        raise errors.MalformedData(_("Only one recordset allowed"))

    peerRepoId = extra.get('repo', None)
    peerItemVersion = int(extra.get('version', '-1'))

    uuid, rsExternal = inbound.items()[0]

    item = rv.findUUID(uuid)

    if rsExternal is not None:

        if item is not None: # Item already exists
            if not pim.has_stamp(item, shares.SharedItem):
                shares.SharedItem(item).add()
            shared = shares.SharedItem(item)
            state = getPeerState(shared, peer)
            rsInternal= eim.RecordSet(trans.exportItem(item))

        else: # Item doesn't exist yet
            state = shares.State(itsView=rv, peer=peer)
            rsInternal = eim.RecordSet()

        if peerRepoId != state.peerRepoId:
            # This update is not from the peer repository we last saw.
            # Treat the update is entirely new
            state.clear()
            state.peerRepoId = peerRepoId

        if 0 < peerItemVersion <= state.peerItemVersion:
            # If we're using a null repository view (like during doctesting)
            # the item versions are stuck at zero, so ignore versions less
            # than 1
            raise errors.OutOfSequence("Update %d arrived after %d" %
                (peerItemVersion, state.peerItemVersion))

        state.peerItemVersion = peerItemVersion

        dSend, dApply, pending = state.merge(rsInternal, rsExternal,
            send=False, receive=True, uuid=uuid, debug=debug)

        if dApply:
            if debug: print "Applying:", uuid, dApply
            trans.importRecords(dApply)

        item = rv.findUUID(uuid)
        if item is not None and item.isLive():
            if not pim.has_stamp(item, shares.SharedItem):
                shares.SharedItem(item).add()
            shared = shares.SharedItem(item)
            if not hasattr(shared, 'states'):
                shared.states = []
            if state not in shared.states:
                shared.states.append(state, peer.itsUUID.str16())

    else: # Deletion

        # Remove the state
        if pim.has_stamp(item, shares.SharedItem):
            shared = shares.SharedItem(item)
            if hasattr(shared, 'states'):
                state = shared.states.getByAlias(peer.itsUUID.str16())
                if state is not None:
                    shared.states.remove(state)
                    state.delete(True)

        # Remove the item (if allowed)
        if allowDeletion:
            if debug: print "Deleting item:", uuid
            item.delete(True)
            item = None

    return item



def outbound(rv, peer, item, debug=False):

    # At some point, which serializer and translator to use should be
    # configurable
    serializer = eimml.EIMMLSerializer # only using class methods
    trans = translator.PIMTranslator(rv)

    uuid = item.itsUUID.str16()
    rsInternal = eim.RecordSet(trans.exportItem(item))

    if not pim.has_stamp(item, shares.SharedItem):
        shares.SharedItem(item).add()

    shared = shares.SharedItem(item)
    state = getPeerState(shared, peer)

    # Abort if pending

    # Repository identifier:
    if rv.repository is not None:
        repoId = rv.repository.getSchemaInfo()[0].str16()
    else:
        repoId = ""

    text = serializer.serialize({uuid : rsInternal}, "item", repo=repoId,
        version=str(item.itsVersion))

    if debug: print "Text:", text

    return text




def outboundDeletion(rv, peer, uuid, debug=False):

    # At some point, which serializer and translator to use should be
    # configurable
    serializer = eimml.EIMMLSerializer # only using class methods

    return serializer.serialize({ uuid : None }, "item")



def getPeerState(item, peer, create=True):

    state = None
    if hasattr(item, 'states'):
        state = item.states.getByAlias(peer.itsUUID.str16())
    if state is None and create:
        state = shares.State(itsView=item.itsItem.itsView, peer=peer)
    return state


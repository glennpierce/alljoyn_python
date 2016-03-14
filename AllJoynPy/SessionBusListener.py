# Copyright Glenn Pierce. All rights reserved.
#
#    Permission to use, copy, modify, and/or distribute this software for any
#    purpose with or without fee is hereby granted, provided that the above
#    copyright notice and this permission notice appear in all copies.
#
#    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import BusListener, SessionListener, SessionPortListener


class SessionBusListener(object):
    def __init__(self, context=None):
        self.sessionListener = SessionListener.SessionListener(context=context)
        self.busListener = BusListener.BusListener(context=context)
        self.sessionPortListener = SessionPortListener.SessionPortListener(context=context)

        self.sessionListener.OnSessionLostCallBack = self.OnSessionLostCallBack
        self.sessionListener.OnSessionMemberAddedCallback = self.OnSessionMemberAddedCallback
        self.sessionListener.OnSessionMemberRemovedCallBack = self.OnSessionMemberRemovedCallBack

        self.busListener.OnListenerRegisteredCallBack = self.OnListenerRegisteredCallBack
        self.busListener.OnListenerUnregisteredCallback = self.OnListenerUnregisteredCallback
        self.busListener.OnFoundAdvertisedNameCallBack = self.OnFoundAdvertisedNameCallBack
        self.busListener.OnLostAdvertisedNameCallBack = self.OnLostAdvertisedNameCallBack
        self.busListener.OnNameOwnerChangedCallBack = self.OnNameOwnerChangedCallBack
        self.busListener.OnBusStoppingCallBack = self.OnBusStoppingCallBack
        self.busListener.OnBusDisconnectedCallBack = self.OnBusDisconnectedCallBack
        self.busListener.OnPropertyChangedCallBack = self.OnPropertyChangedCallBack

        self.sessionPortListener.OnAcceptSessionJoinerCallBack = self.OnAcceptSessionJoinerCallBack
        self.sessionPortListener.OnSessionJoinedCallback = self.OnSessionJoinedCallback

    # SessionListener Callbacks

    def OnSessionLostCallBack(self, context, sessionId, reason):
        pass

    def OnSessionMemberAddedCallback(self, context, sessionId, uniqueName):
        pass

    def OnSessionMemberRemovedCallBack(self, context, sessionId, uniqueName):
        pass

    # BusListener Callbacks

    def OnListenerRegisteredCallBack(self, context, bus):
        pass

    def OnListenerUnregisteredCallback(self, context):
        pass

    def OnFoundAdvertisedNameCallBack(self, context, name, transport, name_prefix):
        pass

    def OnLostAdvertisedNameCallBack(self, context, name, transport, name_prefix):
        pass

    def OnNameOwnerChangedCallBack(self, context, bus_name, previous_owner, new_owner):
        pass

    def OnBusStoppingCallBack(self, context):
        pass

    def OnBusDisconnectedCallBack(self, context):
        pass

    def OnPropertyChangedCallBack(self, context, property_name, property_value):
        pass

    # SessionPortListener Callbacks

    def OnAcceptSessionJoinerCallBack(self, context, session_port, joiner, opts):
        pass

    def OnSessionJoinedCallback(self, context, session_port, session_id, joiner):
        pass

#   Copyright (c) 2003-2008 Open Source Applications Foundation
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


import wx
import threading
from i18n import ChandlerMessageFactory as _
from osaf.activity import *


def Show(activity, parent=None, makeAuxiliary=lambda parent:None):
    win = ProgressFrame(parent, -1, activity.title,
        size=(300,100), style=wx.DEFAULT_FRAME_STYLE,
        activity=activity, makeAuxiliary=makeAuxiliary)
    win.CenterOnParent()
    win.Show()
    return win



class ProgressFrame(wx.Frame):

    def __init__(self, *args, **kwds):
        self.activity = kwds.pop('activity')
        auxiliary = kwds.pop('makeAuxiliary')

        super(ProgressFrame, self).__init__(*args, **kwds)
        self.listener = Listener(activity=self.activity, callback=self.callback)

        self.panel = wx.Panel(self, -1)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.gaugeCtrl = wx.Gauge(self.panel, -1, size=(300,10))
        self.sizer.Add(self.gaugeCtrl, 0,
            wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.gaugeCtrl.Pulse()

        self.msgCtrl = wx.StaticText(self.panel, -1, "")
        self.sizer.Add(self.msgCtrl, 0, wx.ALIGN_LEFT|wx.ALL, 5)

        self.auxiliary = auxiliary(self.panel)
        if self.auxiliary is not None:
            self.sizer.Add(self.auxiliary, 0,
                wx.EXPAND|wx.ALIGN_TOP|wx.ALL, 12)

        self.cancelCtrl = wx.Button(self.panel, wx.ID_CANCEL)
        self.sizer.Add(self.cancelCtrl, 0, wx.ALIGN_LEFT|wx.ALL, 5)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=wx.ID_CANCEL)

        self.panel.SetSizer(self.sizer)
        self.panel.Layout()
        self.sizer.Fit(self)

        self.cancel = False

    def OnCloseWindow(self, event):
        self.listener.unregister()
        self.Destroy()

    def OnCancel(self, event):
        self.cancel = True

    def callback(self, activity, *args, **kwds):
        # Can be called from any thread; will call _callback in main thread

        if threading.currentThread().getName() != "MainThread":
            wx.GetApp().PostAsyncEvent(self._callback, activity, *args, **kwds)
        else:
            self._callback(activity, *args, **kwds)

        return self.cancel


    def _callback(self, activity, *args, **kwds):
        # Must be called in main thread

        if 'status' in kwds:
            status = kwds['status']
            if status in (STATUS_ABORTED, STATUS_FAILED, STATUS_COMPLETE):
                self.OnCloseWindow(None)
                return

        self.updateWidget(activity, *args, **kwds)

    def updateWidget(self, activity, *args, **kwds):
        if 'msg' in kwds:
            self.msgCtrl.SetLabel(kwds['msg'])

        if 'percent' in kwds:
            percent = kwds['percent']
            if percent is None:
                self.gaugeCtrl.Pulse()
            else:
                self.gaugeCtrl.SetValue(percent)

        wx.GetApp().Yield(True)

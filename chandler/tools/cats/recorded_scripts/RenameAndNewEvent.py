import wx, osaf
from osaf.framework.script_recording.script_lib import ProcessEvent, VerifyOn

def run():
    VerifyOn ()
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_DOWN, 'sentTo':'Sidebar'}, {'m_leftDown':True, 'm_x':65, 'm_y':14})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_UP, 'sentTo':'Sidebar', 'newFocusWindow':-218, 'newFocusWindowClass':wx.Window}, {'m_x':65, 'm_y':14})    
    ProcessEvent (wx.MouseEvent, {'associatedBlock':'SidebarContainer', 'eventType':wx.EVT_LEFT_DOWN, 'sentTo':'SidebarContainer'}, {'m_leftDown':True, 'm_x':81, 'm_y':171})
    ProcessEvent (wx.MouseEvent, {'associatedBlock':'SidebarContainer', 'eventType':wx.EVT_LEFT_UP, 'sentTo':'SidebarContainer'}, {'m_x':80, 'm_y':338})
    ProcessEvent (wx.CommandEvent, {'associatedBlock':'ApplicationBarEventButton', 'eventType':wx.EVT_MENU, 'sentTo':'ApplicationBar'}, {})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_DOWN, 'sentTo':'DashboardSummaryView'}, {'m_leftDown':True, 'm_x':261, 'm_y':25})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_UP, 'sentTo':'DashboardSummaryView'}, {'m_x':261, 'm_y':25})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_DCLICK, 'sentTo':'DashboardSummaryView'}, {'m_leftDown':True, 'm_x':261, 'm_y':25})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_UP, 'sentTo':'__FocusWindow__', 'selectionRange': (0,29), 'newFocusWindow':-299, 'newFocusWindowClass':osaf.framework.attributeEditors.AETypeOverTextCtrl.AENonTypeOverTextCtrl}, {'m_x':74, 'm_y':5})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'DashboardSummaryView', 'newFocusWindow':-224, 'newFocusWindowClass':wx.Window, 'lastWidgetValue':u'Play around with the Calendar'}, {'m_rawCode':16, 'm_keyCode':306, 'm_shiftDown':True, 'm_x':261, 'm_y':25, 'UnicodeKey':16})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'DashboardSummaryView'}, {'m_rawCode':84, 'm_keyCode':84, 'm_shiftDown':True, 'm_x':261, 'm_y':25, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'DashboardSummaryView'}, {'m_rawCode':84, 'm_keyCode':84, 'm_shiftDown':True, 'm_x':261, 'm_y':25, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'newFocusWindow':-299, 'newFocusWindowClass':osaf.framework.attributeEditors.AETypeOverTextCtrl.AENonTypeOverTextCtrl}, {'m_rawCode':16, 'm_keyCode':306, 'm_shiftDown':True, 'm_x':76, 'm_y':7, 'UnicodeKey':16})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Play around with the Calendar'}, {'m_rawCode':16, 'm_keyCode':306, 'm_shiftDown':True, 'm_x':76, 'm_y':7, 'UnicodeKey':16})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Play around with the Calendar'}, {'m_rawCode':16, 'm_keyCode':306, 'm_shiftDown':True, 'm_x':76, 'm_y':7, 'UnicodeKey':16})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Play around with the Calendar'}, {'m_rawCode':84, 'm_keyCode':84, 'm_shiftDown':True, 'm_x':76, 'm_y':7, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Play around with the Calendar'}, {'m_rawCode':84, 'm_keyCode':84, 'm_shiftDown':True, 'm_x':76, 'm_y':7, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'T'}, {'m_rawCode':69, 'm_keyCode':69, 'm_x':76, 'm_y':7, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'T'}, {'m_rawCode':101, 'm_keyCode':101, 'm_x':76, 'm_y':7, 'UnicodeKey':101})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Te'}, {'m_rawCode':83, 'm_keyCode':83, 'm_x':76, 'm_y':7, 'UnicodeKey':83})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Te'}, {'m_rawCode':115, 'm_keyCode':115, 'm_x':76, 'm_y':7, 'UnicodeKey':115})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Tes'}, {'m_rawCode':84, 'm_keyCode':84, 'm_x':76, 'm_y':7, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Tes'}, {'m_rawCode':116, 'm_keyCode':116, 'm_x':76, 'm_y':7, 'UnicodeKey':116})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test'}, {'m_rawCode':49, 'm_keyCode':49, 'm_x':76, 'm_y':7, 'UnicodeKey':49})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test'}, {'m_rawCode':49, 'm_keyCode':49, 'm_x':76, 'm_y':7, 'UnicodeKey':49})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_DOWN, 'sentTo':'Sidebar', 'lastWidgetValue':u'Test1'}, {'m_leftDown':True, 'm_x':118, 'm_y':157})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_UP, 'sentTo':'Sidebar', 'newFocusWindow':-224, 'newFocusWindowClass':wx.Window}, {'m_x':118, 'm_y':157})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_DCLICK, 'sentTo':'Sidebar'}, {'m_leftDown':True, 'm_x':118, 'm_y':157})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_UP, 'sentTo':'Sidebar', 'newFocusWindow':-310, 'newFocusWindowClass':wx.Window}, {'m_x':118, 'm_y':157})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'newFocusWindow':-314, 'newFocusWindowClass':osaf.framework.attributeEditors.AETypeOverTextCtrl.AENonTypeOverTextCtrl}, {'m_rawCode':16, 'm_keyCode':306, 'm_shiftDown':True, 'm_x':96, 'm_y':25, 'UnicodeKey':16})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Untitled'}, {'m_rawCode':84, 'm_keyCode':84, 'm_shiftDown':True, 'm_x':96, 'm_y':25, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Untitled'}, {'m_rawCode':84, 'm_keyCode':84, 'm_shiftDown':True, 'm_x':96, 'm_y':25, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'T'}, {'m_rawCode':69, 'm_keyCode':69, 'm_x':96, 'm_y':25, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'T'}, {'m_rawCode':101, 'm_keyCode':101, 'm_x':96, 'm_y':25, 'UnicodeKey':101})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Te'}, {'m_rawCode':83, 'm_keyCode':83, 'm_x':96, 'm_y':25, 'UnicodeKey':83})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Te'}, {'m_rawCode':115, 'm_keyCode':115, 'm_x':96, 'm_y':25, 'UnicodeKey':115})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Tes'}, {'m_rawCode':84, 'm_keyCode':84, 'm_x':96, 'm_y':25, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Tes'}, {'m_rawCode':116, 'm_keyCode':116, 'm_x':96, 'm_y':25, 'UnicodeKey':116})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test'}, {'m_rawCode':50, 'm_keyCode':50, 'm_x':96, 'm_y':25, 'UnicodeKey':50})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test'}, {'m_rawCode':50, 'm_keyCode':50, 'm_x':96, 'm_y':25, 'UnicodeKey':50})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test2'}, {'m_rawCode':9, 'm_keyCode':9, 'm_x':96, 'm_y':25, 'UnicodeKey':9})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_DOWN, 'sentTo':'TimedEvents', 'newFocusWindow':-219, 'newFocusWindowClass':wx.Window, 'lastWidgetValue':u'Test2'}, {'m_leftDown':True, 'm_x':261, 'm_y':139})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_UP, 'sentTo':'TimedEvents'}, {'m_x':261, 'm_y':139})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_DCLICK, 'sentTo':'TimedEvents', 'newFocusWindow':-310, 'newFocusWindowClass':wx.Window}, {'m_leftDown':True, 'm_x':261, 'm_y':139})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_UP, 'sentTo':'TimedEvents'}, {'m_x':261, 'm_y':139})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_DOWN, 'sentTo':'TimedEvents', 'newFocusWindow':-311, 'newFocusWindowClass':osaf.framework.blocks.calendar.CalendarCanvas.wxInPlaceEditor}, {'m_leftDown':True, 'm_x':268, 'm_y':147})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_UP, 'sentTo':'TimedEvents', 'newFocusWindow':-310, 'newFocusWindowClass':wx.Window}, {'m_x':268, 'm_y':147})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_DCLICK, 'sentTo':'TimedEvents'}, {'m_leftDown':True, 'm_x':268, 'm_y':147})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_UP, 'sentTo':'TimedEvents'}, {'m_x':268, 'm_y':147})
    ProcessEvent (wx.MouseEvent, {'associatedBlock':'NotesBlock', 'eventType':wx.EVT_LEFT_DOWN, 'sentTo':'NotesBlock', 'newFocusWindow':-311, 'newFocusWindowClass':osaf.framework.blocks.calendar.CalendarCanvas.wxInPlaceEditor}, {'m_leftDown':True, 'm_x':48, 'm_y':23})
    ProcessEvent (wx.MouseEvent, {'associatedBlock':'NotesBlock', 'eventType':wx.EVT_LEFT_UP, 'sentTo':'NotesBlock', 'selectionRange': (0,0), 'newFocusWindow':'NotesBlock', 'newFocusWindowClass':osaf.framework.attributeEditors.AETypeOverTextCtrl.AENonTypeOverTextCtrl, 'lastWidgetValue':u''}, {'m_x':48, 'm_y':23})
    ProcessEvent (wx.KeyEvent, {'associatedBlock':'NotesBlock', 'eventType':wx.EVT_KEY_DOWN, 'sentTo':'NotesBlock', 'lastWidgetValue':u''}, {'m_rawCode':84, 'm_keyCode':84, 'm_x':50, 'm_y':25, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'associatedBlock':'NotesBlock', 'eventType':wx.EVT_CHAR, 'sentTo':'NotesBlock', 'lastWidgetValue':u''}, {'m_rawCode':116, 'm_keyCode':116, 'm_x':50, 'm_y':25, 'UnicodeKey':116})
    ProcessEvent (wx.KeyEvent, {'associatedBlock':'NotesBlock', 'eventType':wx.EVT_KEY_DOWN, 'sentTo':'NotesBlock', 'lastWidgetValue':u't'}, {'m_rawCode':69, 'm_keyCode':69, 'm_x':50, 'm_y':25, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'associatedBlock':'NotesBlock', 'eventType':wx.EVT_CHAR, 'sentTo':'NotesBlock', 'lastWidgetValue':u't'}, {'m_rawCode':101, 'm_keyCode':101, 'm_x':50, 'm_y':25, 'UnicodeKey':101})
    ProcessEvent (wx.KeyEvent, {'associatedBlock':'NotesBlock', 'eventType':wx.EVT_KEY_DOWN, 'sentTo':'NotesBlock', 'lastWidgetValue':u'te'}, {'m_rawCode':83, 'm_keyCode':83, 'm_x':50, 'm_y':25, 'UnicodeKey':83})
    ProcessEvent (wx.KeyEvent, {'associatedBlock':'NotesBlock', 'eventType':wx.EVT_CHAR, 'sentTo':'NotesBlock', 'lastWidgetValue':u'te'}, {'m_rawCode':115, 'm_keyCode':115, 'm_x':50, 'm_y':25, 'UnicodeKey':115})
    ProcessEvent (wx.KeyEvent, {'associatedBlock':'NotesBlock', 'eventType':wx.EVT_KEY_DOWN, 'sentTo':'NotesBlock', 'lastWidgetValue':u'tes'}, {'m_rawCode':84, 'm_keyCode':84, 'm_x':50, 'm_y':25, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'associatedBlock':'NotesBlock', 'eventType':wx.EVT_CHAR, 'sentTo':'NotesBlock', 'lastWidgetValue':u'tes'}, {'m_rawCode':116, 'm_keyCode':116, 'm_x':50, 'm_y':25, 'UnicodeKey':116})
    ProcessEvent (wx.KeyEvent, {'associatedBlock':'NotesBlock', 'eventType':wx.EVT_KEY_DOWN, 'sentTo':'NotesBlock', 'lastWidgetValue':u'test'}, {'m_rawCode':51, 'm_keyCode':51, 'm_x':50, 'm_y':25, 'UnicodeKey':51})
    ProcessEvent (wx.KeyEvent, {'associatedBlock':'NotesBlock', 'eventType':wx.EVT_CHAR, 'sentTo':'NotesBlock', 'lastWidgetValue':u'test'}, {'m_rawCode':51, 'm_keyCode':51, 'm_x':50, 'm_y':25, 'UnicodeKey':51})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_DOWN, 'sentTo':'TimedEvents', 'lastWidgetValue':u'test3'}, {'m_leftDown':True, 'm_x':298, 'm_y':178})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_UP, 'sentTo':'TimedEvents'}, {'m_x':298, 'm_y':178})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_DCLICK, 'sentTo':'TimedEvents', 'newFocusWindow':-310, 'newFocusWindowClass':wx.Window}, {'m_leftDown':True, 'm_x':298, 'm_y':178})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_UP, 'sentTo':'__FocusWindow__', 'selectionRange': (0,9), 'newFocusWindow':-311, 'newFocusWindowClass':osaf.framework.blocks.calendar.CalendarCanvas.wxInPlaceEditor}, {'m_x':40, 'm_y':23})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'New Event'}, {'m_rawCode':84, 'm_keyCode':84, 'm_x':40, 'm_y':23, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'New Event'}, {'m_rawCode':116, 'm_keyCode':116, 'm_x':40, 'm_y':23, 'UnicodeKey':116})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u't'}, {'m_rawCode':69, 'm_keyCode':69, 'm_x':40, 'm_y':23, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u't'}, {'m_rawCode':101, 'm_keyCode':101, 'm_x':40, 'm_y':23, 'UnicodeKey':101})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'te'}, {'m_rawCode':83, 'm_keyCode':83, 'm_x':40, 'm_y':23, 'UnicodeKey':83})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'te'}, {'m_rawCode':115, 'm_keyCode':115, 'm_x':40, 'm_y':23, 'UnicodeKey':115})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'tes'}, {'m_rawCode':84, 'm_keyCode':84, 'm_x':40, 'm_y':23, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'tes'}, {'m_rawCode':116, 'm_keyCode':116, 'm_x':40, 'm_y':23, 'UnicodeKey':116})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'test'}, {'m_rawCode':52, 'm_keyCode':52, 'm_x':40, 'm_y':23, 'UnicodeKey':52})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'test'}, {'m_rawCode':52, 'm_keyCode':52, 'm_x':40, 'm_y':23, 'UnicodeKey':52})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_DOWN, 'sentTo':'TimedEvents', 'lastWidgetValue':u'test4'}, {'m_leftDown':True, 'm_x':302, 'm_y':101})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_UP, 'sentTo':'TimedEvents', 'newFocusWindow':-310, 'newFocusWindowClass':wx.Window}, {'m_x':302, 'm_y':101})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_DCLICK, 'sentTo':'TimedEvents'}, {'m_leftDown':True, 'm_x':302, 'm_y':101})
    ProcessEvent (wx.MouseEvent, {'eventType':wx.EVT_LEFT_UP, 'sentTo':'__FocusWindow__', 'selectionRange': (0,9), 'newFocusWindow':-311, 'newFocusWindowClass':osaf.framework.blocks.calendar.CalendarCanvas.wxInPlaceEditor}, {'m_x':44, 'm_y':9})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'New Event'}, {'m_rawCode':84, 'm_keyCode':84, 'm_x':44, 'm_y':9, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'New Event'}, {'m_rawCode':116, 'm_keyCode':116, 'm_x':44, 'm_y':9, 'UnicodeKey':116})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u't'}, {'m_rawCode':69, 'm_keyCode':69, 'm_x':44, 'm_y':9, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u't'}, {'m_rawCode':101, 'm_keyCode':101, 'm_x':44, 'm_y':9, 'UnicodeKey':101})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'te'}, {'m_rawCode':83, 'm_keyCode':83, 'm_x':44, 'm_y':9, 'UnicodeKey':83})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'te'}, {'m_rawCode':115, 'm_keyCode':115, 'm_x':44, 'm_y':9, 'UnicodeKey':115})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'tes'}, {'m_rawCode':84, 'm_keyCode':84, 'm_x':44, 'm_y':9, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'tes'}, {'m_rawCode':116, 'm_keyCode':116, 'm_x':44, 'm_y':9, 'UnicodeKey':116})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'test'}, {'m_rawCode':53, 'm_keyCode':53, 'm_x':44, 'm_y':9, 'UnicodeKey':53})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'test'}, {'m_rawCode':53, 'm_keyCode':53, 'm_x':44, 'm_y':9, 'UnicodeKey':53})
    ProcessEvent (wx.MouseEvent, {'associatedBlock':'EditAllDay', 'eventType':wx.EVT_LEFT_DOWN, 'sentTo':'EditAllDay', 'lastWidgetValue':u'test5'}, {'m_leftDown':True, 'm_x':10, 'm_y':14})
    ProcessEvent (wx.MouseEvent, {'associatedBlock':'EditAllDay', 'eventType':wx.EVT_LEFT_UP, 'sentTo':'EditAllDay', 'newFocusWindow':'EditAllDay', 'newFocusWindowClass':osaf.framework.attributeEditors.AttributeEditors.AECheckBox, 'lastWidgetValue':False}, {'m_x':10, 'm_y':14})
    ProcessEvent (wx.CommandEvent, {'associatedBlock':'EditAllDay', 'eventType':wx.EVT_CHECKBOX, 'sentTo':'EditAllDay', 'lastWidgetValue':True}, {})

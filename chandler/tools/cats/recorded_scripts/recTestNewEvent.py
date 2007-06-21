import wx, osaf
from osaf.framework.script_recording.script_lib import ProcessEvent, VerifyOn

def run():
    #ignore this test on windows because it catches Bug#9061: beep when title too long in lozenges (ws Need a different set of flags for the lozenge editor)
    if wx.Platform == '__WXMSW__':
        return
    VerifyOn ()
    ProcessEvent (wx.CommandEvent, {'associatedBlock':'ApplicationBarEventButton', 'eventType':wx.EVT_MENU, 'sentTo':'ApplicationBar'}, {})
    ProcessEvent (wx.CommandEvent, {'associatedBlock':'NewCollectionItem', 'eventType':wx.EVT_MENU, 'sentTo':'MainFrame'}, {})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'newFocusWindow':-309, 'newFocusWindowClass':osaf.framework.attributeEditors.AETypeOverTextCtrl.AENonTypeOverTextCtrl}, {'m_rawCode':84, 'm_keyCode':84, 'm_x':222, 'm_y':28, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Untitled'}, {'m_rawCode':116, 'm_keyCode':116, 'm_x':222, 'm_y':28, 'UnicodeKey':116})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u't'}, {'m_rawCode':69, 'm_keyCode':69, 'm_x':222, 'm_y':28, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u't'}, {'m_rawCode':101, 'm_keyCode':101, 'm_x':222, 'm_y':28, 'UnicodeKey':101})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'te'}, {'m_rawCode':83, 'm_keyCode':83, 'm_x':222, 'm_y':28, 'UnicodeKey':83})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'te'}, {'m_rawCode':115, 'm_keyCode':115, 'm_x':222, 'm_y':28, 'UnicodeKey':115})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'tes'}, {'m_rawCode':84, 'm_keyCode':84, 'm_x':222, 'm_y':28, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'tes'}, {'m_rawCode':116, 'm_keyCode':116, 'm_x':222, 'm_y':28, 'UnicodeKey':116})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'test'}, {'m_rawCode':16, 'm_keyCode':306, 'm_shiftDown':True, 'm_x':222, 'm_y':28, 'UnicodeKey':16})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'test'}, {'m_rawCode':78, 'm_keyCode':78, 'm_shiftDown':True, 'm_x':222, 'm_y':28, 'UnicodeKey':78})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'test'}, {'m_rawCode':78, 'm_keyCode':78, 'm_shiftDown':True, 'm_x':222, 'm_y':28, 'UnicodeKey':78})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'testN'}, {'m_rawCode':69, 'm_keyCode':69, 'm_x':222, 'm_y':28, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'testN'}, {'m_rawCode':101, 'm_keyCode':101, 'm_x':222, 'm_y':28, 'UnicodeKey':101})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'testNe'}, {'m_rawCode':87, 'm_keyCode':87, 'm_x':222, 'm_y':28, 'UnicodeKey':87})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'testNe'}, {'m_rawCode':119, 'm_keyCode':119, 'm_x':222, 'm_y':28, 'UnicodeKey':119})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'testNew'}, {'m_rawCode':16, 'm_keyCode':306, 'm_shiftDown':True, 'm_x':222, 'm_y':28, 'UnicodeKey':16})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'testNew'}, {'m_rawCode':69, 'm_keyCode':69, 'm_shiftDown':True, 'm_x':222, 'm_y':28, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'testNew'}, {'m_rawCode':69, 'm_keyCode':69, 'm_shiftDown':True, 'm_x':222, 'm_y':28, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'testNewE'}, {'m_rawCode':86, 'm_keyCode':86, 'm_x':222, 'm_y':28, 'UnicodeKey':86})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'testNewE'}, {'m_rawCode':118, 'm_keyCode':118, 'm_x':222, 'm_y':28, 'UnicodeKey':118})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'testNewEv'}, {'m_rawCode':69, 'm_keyCode':69, 'm_x':222, 'm_y':28, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'testNewEv'}, {'m_rawCode':101, 'm_keyCode':101, 'm_x':222, 'm_y':28, 'UnicodeKey':101})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'testNewEve'}, {'m_rawCode':78, 'm_keyCode':78, 'm_x':222, 'm_y':28, 'UnicodeKey':78})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'testNewEve'}, {'m_rawCode':110, 'm_keyCode':110, 'm_x':222, 'm_y':28, 'UnicodeKey':110})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'testNewEven'}, {'m_rawCode':84, 'm_keyCode':84, 'm_x':222, 'm_y':28, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'testNewEven'}, {'m_rawCode':116, 'm_keyCode':116, 'm_x':222, 'm_y':28, 'UnicodeKey':116})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'testNewEvent'}, {'m_rawCode':9, 'm_keyCode':9, 'm_x':222, 'm_y':28, 'UnicodeKey':9})
    ProcessEvent (wx.CommandEvent, {'associatedBlock':'NewEventItem', 'eventType':wx.EVT_MENU, 'sentTo':'MainFrame', 'newFocusWindow':-219, 'newFocusWindowClass':wx.Window, 'lastWidgetValue':u'testNewEvent'}, {})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'newFocusWindow':-305, 'newFocusWindowClass':wx.Window}, {'m_rawCode':16, 'm_keyCode':306, 'm_shiftDown':True, 'm_x':167, 'm_y':689, 'UnicodeKey':16})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__'}, {'m_rawCode':84, 'm_keyCode':84, 'm_shiftDown':True, 'm_x':167, 'm_y':689, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__'}, {'m_rawCode':84, 'm_keyCode':84, 'm_shiftDown':True, 'm_x':167, 'm_y':689, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'newFocusWindow':-306, 'newFocusWindowClass':osaf.framework.blocks.calendar.CalendarCanvas.wxInPlaceEditor}, {'m_rawCode':69, 'm_keyCode':69, 'm_x':-162, 'm_y':-496, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'T'}, {'m_rawCode':101, 'm_keyCode':101, 'm_x':-162, 'm_y':-496, 'UnicodeKey':101})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Te'}, {'m_rawCode':83, 'm_keyCode':83, 'm_x':-162, 'm_y':-496, 'UnicodeKey':83})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Te'}, {'m_rawCode':115, 'm_keyCode':115, 'm_x':-162, 'm_y':-496, 'UnicodeKey':115})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Tes'}, {'m_rawCode':84, 'm_keyCode':84, 'm_x':-162, 'm_y':-496, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Tes'}, {'m_rawCode':116, 'm_keyCode':116, 'm_x':-162, 'm_y':-496, 'UnicodeKey':116})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test'}, {'m_rawCode':32, 'm_keyCode':32, 'm_x':-162, 'm_y':-496, 'UnicodeKey':32})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test'}, {'m_rawCode':32, 'm_keyCode':32, 'm_x':-162, 'm_y':-496, 'UnicodeKey':32})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test '}, {'m_rawCode':78, 'm_keyCode':78, 'm_x':-162, 'm_y':-496, 'UnicodeKey':78})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test '}, {'m_rawCode':110, 'm_keyCode':110, 'm_x':-162, 'm_y':-496, 'UnicodeKey':110})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test n'}, {'m_rawCode':69, 'm_keyCode':69, 'm_x':-162, 'm_y':-496, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test n'}, {'m_rawCode':101, 'm_keyCode':101, 'm_x':-162, 'm_y':-496, 'UnicodeKey':101})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test ne'}, {'m_rawCode':87, 'm_keyCode':87, 'm_x':-162, 'm_y':-496, 'UnicodeKey':87})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test ne'}, {'m_rawCode':119, 'm_keyCode':119, 'm_x':-162, 'm_y':-496, 'UnicodeKey':119})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new'}, {'m_rawCode':32, 'm_keyCode':32, 'm_x':-162, 'm_y':-496, 'UnicodeKey':32})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new'}, {'m_rawCode':32, 'm_keyCode':32, 'm_x':-162, 'm_y':-496, 'UnicodeKey':32})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new '}, {'m_rawCode':69, 'm_keyCode':69, 'm_x':-162, 'm_y':-496, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new '}, {'m_rawCode':101, 'm_keyCode':101, 'm_x':-162, 'm_y':-496, 'UnicodeKey':101})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new e'}, {'m_rawCode':86, 'm_keyCode':86, 'm_x':-162, 'm_y':-496, 'UnicodeKey':86})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new e'}, {'m_rawCode':118, 'm_keyCode':118, 'm_x':-162, 'm_y':-496, 'UnicodeKey':118})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new ev'}, {'m_rawCode':69, 'm_keyCode':69, 'm_x':-162, 'm_y':-496, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new ev'}, {'m_rawCode':101, 'm_keyCode':101, 'm_x':-162, 'm_y':-496, 'UnicodeKey':101})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new eve'}, {'m_rawCode':78, 'm_keyCode':78, 'm_x':-162, 'm_y':-496, 'UnicodeKey':78})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new eve'}, {'m_rawCode':110, 'm_keyCode':110, 'm_x':-162, 'm_y':-496, 'UnicodeKey':110})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new even'}, {'m_rawCode':84, 'm_keyCode':84, 'm_x':-162, 'm_y':-496, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new even'}, {'m_rawCode':116, 'm_keyCode':116, 'm_x':-162, 'm_y':-496, 'UnicodeKey':116})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event'}, {'m_rawCode':32, 'm_keyCode':32, 'm_x':-162, 'm_y':-496, 'UnicodeKey':32})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event'}, {'m_rawCode':32, 'm_keyCode':32, 'm_x':-162, 'm_y':-496, 'UnicodeKey':32})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event '}, {'m_rawCode':67, 'm_keyCode':67, 'm_x':-162, 'm_y':-496, 'UnicodeKey':67})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event '}, {'m_rawCode':99, 'm_keyCode':99, 'm_x':-162, 'm_y':-496, 'UnicodeKey':99})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event c'}, {'m_rawCode':82, 'm_keyCode':82, 'm_x':-162, 'm_y':-496, 'UnicodeKey':82})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event c'}, {'m_rawCode':114, 'm_keyCode':114, 'm_x':-162, 'm_y':-496, 'UnicodeKey':114})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event cr'}, {'m_rawCode':69, 'm_keyCode':69, 'm_x':-162, 'm_y':-496, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event cr'}, {'m_rawCode':101, 'm_keyCode':101, 'm_x':-162, 'm_y':-496, 'UnicodeKey':101})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event cre'}, {'m_rawCode':65, 'm_keyCode':65, 'm_x':-162, 'm_y':-496, 'UnicodeKey':65})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event cre'}, {'m_rawCode':97, 'm_keyCode':97, 'm_x':-162, 'm_y':-496, 'UnicodeKey':97})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event crea'}, {'m_rawCode':84, 'm_keyCode':84, 'm_x':-162, 'm_y':-496, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event crea'}, {'m_rawCode':116, 'm_keyCode':116, 'm_x':-162, 'm_y':-496, 'UnicodeKey':116})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event creat'}, {'m_rawCode':69, 'm_keyCode':69, 'm_x':-162, 'm_y':-496, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event creat'}, {'m_rawCode':101, 'm_keyCode':101, 'm_x':-162, 'm_y':-496, 'UnicodeKey':101})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event create'}, {'m_rawCode':8, 'm_keyCode':8, 'm_x':-162, 'm_y':-496, 'UnicodeKey':8})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event create'}, {'m_rawCode':8, 'm_keyCode':8, 'm_x':-162, 'm_y':-496, 'UnicodeKey':8})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event creat'}, {'m_rawCode':73, 'm_keyCode':73, 'm_x':-162, 'm_y':-496, 'UnicodeKey':73})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event creat'}, {'m_rawCode':105, 'm_keyCode':105, 'm_x':-162, 'm_y':-496, 'UnicodeKey':105})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event creati'}, {'m_rawCode':79, 'm_keyCode':79, 'm_x':-162, 'm_y':-496, 'UnicodeKey':79})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event creati'}, {'m_rawCode':111, 'm_keyCode':111, 'm_x':-162, 'm_y':-496, 'UnicodeKey':111})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event creatio'}, {'m_rawCode':78, 'm_keyCode':78, 'm_x':-162, 'm_y':-496, 'UnicodeKey':78})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event creatio'}, {'m_rawCode':110, 'm_keyCode':110, 'm_x':-162, 'm_y':-496, 'UnicodeKey':110})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event creation'}, {'m_rawCode':9, 'm_keyCode':9, 'm_x':-162, 'm_y':-496, 'UnicodeKey':9})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test new event creation'}, {'m_rawCode':9, 'm_keyCode':9, 'm_x':-162, 'm_y':-496, 'UnicodeKey':9})

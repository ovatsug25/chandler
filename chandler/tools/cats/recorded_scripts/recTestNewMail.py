import wx, osaf
from osaf.framework.script_recording.script_lib import ProcessEvent, VerifyOn

def run():
    if wx.Platform == '__WXGTK__':
        return
    
    VerifyOn ()
    ProcessEvent (wx.CommandEvent, {'associatedBlock':'NewCollectionItem', 'eventType':wx.EVT_MENU, 'sentTo':'MainFrame'}, {})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'newFocusWindow':-309, 'newFocusWindowClass':osaf.framework.attributeEditors.AETypeOverTextCtrl.AENonTypeOverTextCtrl}, {'m_rawCode':16, 'm_keyCode':306, 'm_shiftDown':True, 'm_x':129, 'm_y':-132, 'UnicodeKey':16})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Untitled'}, {'m_rawCode':84, 'm_keyCode':84, 'm_shiftDown':True, 'm_x':129, 'm_y':-132, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Untitled'}, {'m_rawCode':84, 'm_keyCode':84, 'm_shiftDown':True, 'm_x':129, 'm_y':-132, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'T'}, {'m_rawCode':69, 'm_keyCode':69, 'm_x':129, 'm_y':-132, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'T'}, {'m_rawCode':101, 'm_keyCode':101, 'm_x':129, 'm_y':-132, 'UnicodeKey':101})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Te'}, {'m_rawCode':83, 'm_keyCode':83, 'm_x':129, 'm_y':-132, 'UnicodeKey':83})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Te'}, {'m_rawCode':115, 'm_keyCode':115, 'm_x':129, 'm_y':-132, 'UnicodeKey':115})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Tes'}, {'m_rawCode':84, 'm_keyCode':84, 'm_x':129, 'm_y':-132, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Tes'}, {'m_rawCode':116, 'm_keyCode':116, 'm_x':129, 'm_y':-132, 'UnicodeKey':116})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test'}, {'m_rawCode':16, 'm_keyCode':306, 'm_shiftDown':True, 'm_x':129, 'm_y':-132, 'UnicodeKey':16})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test'}, {'m_rawCode':78, 'm_keyCode':78, 'm_shiftDown':True, 'm_x':129, 'm_y':-132, 'UnicodeKey':78})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'Test'}, {'m_rawCode':78, 'm_keyCode':78, 'm_shiftDown':True, 'm_x':129, 'm_y':-132, 'UnicodeKey':78})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'TestN'}, {'m_rawCode':69, 'm_keyCode':69, 'm_x':129, 'm_y':-132, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'TestN'}, {'m_rawCode':101, 'm_keyCode':101, 'm_x':129, 'm_y':-132, 'UnicodeKey':101})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'TestNe'}, {'m_rawCode':87, 'm_keyCode':87, 'm_x':129, 'm_y':-132, 'UnicodeKey':87})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'TestNe'}, {'m_rawCode':119, 'm_keyCode':119, 'm_x':129, 'm_y':-132, 'UnicodeKey':119})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'TestNew'}, {'m_rawCode':16, 'm_keyCode':306, 'm_shiftDown':True, 'm_x':129, 'm_y':-132, 'UnicodeKey':16})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'TestNew'}, {'m_rawCode':77, 'm_keyCode':77, 'm_shiftDown':True, 'm_x':129, 'm_y':-132, 'UnicodeKey':77})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'TestNew'}, {'m_rawCode':77, 'm_keyCode':77, 'm_shiftDown':True, 'm_x':129, 'm_y':-132, 'UnicodeKey':77})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'TestNewM'}, {'m_rawCode':65, 'm_keyCode':65, 'm_x':129, 'm_y':-132, 'UnicodeKey':65})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'TestNewM'}, {'m_rawCode':97, 'm_keyCode':97, 'm_x':129, 'm_y':-132, 'UnicodeKey':97})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'TestNewMa'}, {'m_rawCode':73, 'm_keyCode':73, 'm_x':129, 'm_y':-132, 'UnicodeKey':73})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'TestNewMa'}, {'m_rawCode':105, 'm_keyCode':105, 'm_x':129, 'm_y':-132, 'UnicodeKey':105})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'TestNewMai'}, {'m_rawCode':76, 'm_keyCode':76, 'm_x':129, 'm_y':-132, 'UnicodeKey':76})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'TestNewMai'}, {'m_rawCode':108, 'm_keyCode':108, 'm_x':129, 'm_y':-132, 'UnicodeKey':108})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'__FocusWindow__', 'lastWidgetValue':u'TestNewMail'}, {'m_rawCode':13, 'm_keyCode':13, 'm_x':129, 'm_y':-132, 'UnicodeKey':13})
    ProcessEvent (wx.MouseEvent, {'associatedBlock':'ApplicationBar', 'eventType':wx.EVT_LEFT_DOWN, 'sentTo':'ApplicationBar', 'newFocusWindow':-219, 'newFocusWindowClass':wx.Window, 'lastWidgetValue':u'TestNewMail'}, {'m_leftDown':True, 'm_x':67, 'm_y':17})
    ProcessEvent (wx.MouseEvent, {'associatedBlock':'ApplicationBar', 'eventType':wx.EVT_LEFT_UP, 'sentTo':'ApplicationBar'}, {'m_x':67, 'm_y':17})
    ProcessEvent (wx.CommandEvent, {'associatedBlock':'ApplicationBarMailButton', 'eventType':wx.EVT_MENU, 'sentTo':'ApplicationBar'}, {})
    ProcessEvent (wx.CommandEvent, {'associatedBlock':'NewMessageItem', 'eventType':wx.EVT_MENU, 'sentTo':'MainFrame', 'newFocusWindow':-313, 'newFocusWindowClass':wx.Window}, {})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'newFocusWindow':-412, 'newFocusWindowClass':osaf.framework.attributeEditors.DragAndDropTextCtrl.DragAndDropTextCtrl}, {'m_rawCode':84, 'm_keyCode':84, 'm_x':-363, 'm_y':-23, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'Untitled'}, {'m_rawCode':116, 'm_keyCode':116, 'm_x':-363, 'm_y':-23, 'UnicodeKey':116})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u't'}, {'m_rawCode':69, 'm_keyCode':69, 'm_x':-363, 'm_y':-23, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u't'}, {'m_rawCode':101, 'm_keyCode':101, 'm_x':-363, 'm_y':-23, 'UnicodeKey':101})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'te'}, {'m_rawCode':83, 'm_keyCode':83, 'm_x':-363, 'm_y':-23, 'UnicodeKey':83})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'te'}, {'m_rawCode':115, 'm_keyCode':115, 'm_x':-363, 'm_y':-23, 'UnicodeKey':115})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'tes'}, {'m_rawCode':84, 'm_keyCode':84, 'm_x':-363, 'm_y':-23, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'tes'}, {'m_rawCode':116, 'm_keyCode':116, 'm_x':-363, 'm_y':-23, 'UnicodeKey':116})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test'}, {'m_rawCode':32, 'm_keyCode':32, 'm_x':-363, 'm_y':-23, 'UnicodeKey':32})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test'}, {'m_rawCode':32, 'm_keyCode':32, 'm_x':-363, 'm_y':-23, 'UnicodeKey':32})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test '}, {'m_rawCode':78, 'm_keyCode':78, 'm_x':-363, 'm_y':-23, 'UnicodeKey':78})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test '}, {'m_rawCode':110, 'm_keyCode':110, 'm_x':-363, 'm_y':-23, 'UnicodeKey':110})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test n'}, {'m_rawCode':69, 'm_keyCode':69, 'm_x':-363, 'm_y':-23, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test n'}, {'m_rawCode':101, 'm_keyCode':101, 'm_x':-363, 'm_y':-23, 'UnicodeKey':101})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test ne'}, {'m_rawCode':87, 'm_keyCode':87, 'm_x':-363, 'm_y':-23, 'UnicodeKey':87})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test ne'}, {'m_rawCode':119, 'm_keyCode':119, 'm_x':-363, 'm_y':-23, 'UnicodeKey':119})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new'}, {'m_rawCode':32, 'm_keyCode':32, 'm_x':-363, 'm_y':-23, 'UnicodeKey':32})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new'}, {'m_rawCode':32, 'm_keyCode':32, 'm_x':-363, 'm_y':-23, 'UnicodeKey':32})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new '}, {'m_rawCode':77, 'm_keyCode':77, 'm_x':-363, 'm_y':-23, 'UnicodeKey':77})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new '}, {'m_rawCode':109, 'm_keyCode':109, 'm_x':-363, 'm_y':-23, 'UnicodeKey':109})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new m'}, {'m_rawCode':65, 'm_keyCode':65, 'm_x':-363, 'm_y':-23, 'UnicodeKey':65})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new m'}, {'m_rawCode':97, 'm_keyCode':97, 'm_x':-363, 'm_y':-23, 'UnicodeKey':97})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new ma'}, {'m_rawCode':73, 'm_keyCode':73, 'm_x':-363, 'm_y':-23, 'UnicodeKey':73})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new ma'}, {'m_rawCode':105, 'm_keyCode':105, 'm_x':-363, 'm_y':-23, 'UnicodeKey':105})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mai'}, {'m_rawCode':76, 'm_keyCode':76, 'm_x':-363, 'm_y':-23, 'UnicodeKey':76})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mai'}, {'m_rawCode':108, 'm_keyCode':108, 'm_x':-363, 'm_y':-23, 'UnicodeKey':108})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail'}, {'m_rawCode':32, 'm_keyCode':32, 'm_x':-363, 'm_y':-23, 'UnicodeKey':32})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail'}, {'m_rawCode':32, 'm_keyCode':32, 'm_x':-363, 'm_y':-23, 'UnicodeKey':32})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail '}, {'m_rawCode':67, 'm_keyCode':67, 'm_x':-363, 'm_y':-23, 'UnicodeKey':67})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail '}, {'m_rawCode':99, 'm_keyCode':99, 'm_x':-363, 'm_y':-23, 'UnicodeKey':99})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail c'}, {'m_rawCode':82, 'm_keyCode':82, 'm_x':-363, 'm_y':-23, 'UnicodeKey':82})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail c'}, {'m_rawCode':114, 'm_keyCode':114, 'm_x':-363, 'm_y':-23, 'UnicodeKey':114})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail cr'}, {'m_rawCode':69, 'm_keyCode':69, 'm_x':-363, 'm_y':-23, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail cr'}, {'m_rawCode':101, 'm_keyCode':101, 'm_x':-363, 'm_y':-23, 'UnicodeKey':101})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail cre'}, {'m_rawCode':65, 'm_keyCode':65, 'm_x':-363, 'm_y':-23, 'UnicodeKey':65})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail cre'}, {'m_rawCode':97, 'm_keyCode':97, 'm_x':-363, 'm_y':-23, 'UnicodeKey':97})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail crea'}, {'m_rawCode':84, 'm_keyCode':84, 'm_x':-363, 'm_y':-23, 'UnicodeKey':84})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail crea'}, {'m_rawCode':116, 'm_keyCode':116, 'm_x':-363, 'm_y':-23, 'UnicodeKey':116})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail creat'}, {'m_rawCode':69, 'm_keyCode':69, 'm_x':-363, 'm_y':-23, 'UnicodeKey':69})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail creat'}, {'m_rawCode':101, 'm_keyCode':101, 'm_x':-363, 'm_y':-23, 'UnicodeKey':101})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail create'}, {'m_rawCode':8, 'm_keyCode':8, 'm_x':-363, 'm_y':-23, 'UnicodeKey':8})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail create'}, {'m_rawCode':8, 'm_keyCode':8, 'm_x':-363, 'm_y':-23, 'UnicodeKey':8})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail creat'}, {'m_rawCode':73, 'm_keyCode':73, 'm_x':-363, 'm_y':-23, 'UnicodeKey':73})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail creat'}, {'m_rawCode':105, 'm_keyCode':105, 'm_x':-363, 'm_y':-23, 'UnicodeKey':105})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail creati'}, {'m_rawCode':79, 'm_keyCode':79, 'm_x':-363, 'm_y':-23, 'UnicodeKey':79})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail creati'}, {'m_rawCode':111, 'm_keyCode':111, 'm_x':-363, 'm_y':-23, 'UnicodeKey':111})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_KEY_DOWN, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail creatio'}, {'m_rawCode':78, 'm_keyCode':78, 'm_x':-363, 'm_y':-23, 'UnicodeKey':78})
    ProcessEvent (wx.KeyEvent, {'eventType':wx.EVT_CHAR, 'sentTo':'HeadlineBlock', 'lastWidgetValue':u'test new mail creatio'}, {'m_rawCode':110, 'm_keyCode':110, 'm_x':-363, 'm_y':-23, 'UnicodeKey':110})

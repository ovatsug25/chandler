""" Classes used for Calendar parcel kinds
"""

__revision__  = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2003 Open Source Applications Foundation"
__license__   = "http://osafoundation.org/Chandler_0.1_license_terms.htm"

import repository.parcel.Parcel as Parcel
import repository.item.Item as Item

import OSAF.contentmodel.ContentModel as ContentModel
import application.Globals as Globals

import mx.DateTime as DateTime


class CalendarParcel(Parcel.Parcel):

    def __init__(self, name, parent, kind):
        Parcel.Parcel.__init__(self, name, parent, kind)

    def _setUUIDs(self):
        calendarEventKind = self.find('CalendarEvent')
        CalendarParcel.calendarEventKindID = calendarEventKind.getUUID()

        locationKind = self.find('Location')
        CalendarParcel.locationKindID = locationKind.getUUID()
        
        calendarKind = self.find('Calendar')
        CalendarParcel.calendarKindID = calendarKind.getUUID()
        
        recurrenceKind = self.find('RecurrencePattern')
        CalendarParcel.recurrencePatternKindID = recurrenceKind.getUUID()
        
        reminderKind = self.find('Reminder')
        CalendarParcel.reminderKindID = reminderKind.getUUID()

    def onItemLoad(self):
        super(CalendarParcel, self).onItemLoad()
        self._setUUIDs()

    def startupParcel(self):
        Parcel.Parcel.startupParcel(self)
        self._setUUIDs()

    def getCalendarEventKind(cls):
        assert cls.calendarEventKindID, "CalendarParcel not yet loaded"
        return Globals.repository[cls.calendarEventKindID]

    getCalendarEventKind = classmethod(getCalendarEventKind)

    def getLocationKind(cls):
        assert cls.locationKindID, "CalendarParcel not yet loaded"
        return Globals.repository[cls.locationKindID]

    getLocationKind = classmethod(getLocationKind)

    def getCalendarKind(cls):
        assert cls.calendarKindID, "CalendarParcel not yet loaded"
        return Globals.repository[cls.calendarKindID]

    getCalendarKind = classmethod(getCalendarKind)

    def getRecurrencePatternKind(cls):
        assert cls.recurrencePatternKindID, "CalendarParcel not yet loaded"
        return Globals.repository[cls.recurrencePatternKindID]

    getRecurrencePatternKind = classmethod(getRecurrencePatternKind)

    def getReminderKind(cls):
        assert cls.reminderKindID, "CalendarParcel not yet loaded"
        return Globals.repository[cls.reminderKindID]

    getReminderKind = classmethod(getReminderKind)


    # The parcel knows the UUIDs for the Kinds, once the parcel is loaded
    calendarEventKindID = None
    locationKindID = None
    calendarKindID = None
    recurrencePatternKindID = None
    reminderKindID = None

class CalendarEvent(ContentModel.ContentItem):

    def __init__(self, name=None, parent=None, kind=None):
        if not kind:
            kind = CalendarParcel.getCalendarEventKind()
        ContentModel.ContentItem.__init__(self, name, parent, kind)
        self.startTime = DateTime.now()
        self.endTime = DateTime.now()
        self.participants = []
        self.whoAttribute = "participants"
        self.aboutAttribute = "headline"
        self.dateAttribute = "startTime"

    def GetDuration(self):
        """Returns an mxDateTimeDelta, None if no startTime or endTime"""
        
        if (self.hasAttributeValue("startTime") and
            self.hasAttributeValue("endTime")):
            return self.endTime - self.startTime
        else:
            return None

    def SetDuration(self, dateTimeDelta):
        """Set duration of event, expects value to be mxDateTimeDelta
        
        endTime is updated based on the new duration, startTime remains fixed
        """
        if (self.startTime != None):
            self.endTime = self.startTime + dateTimeDelta

    duration = property(GetDuration, SetDuration,
                                doc="mxDateTimeDelta: the length of an event")

    def ChangeStart(self, dateTime):
        """Change the start time without changing the duration.

        Setting startTime directly will effectively change the duration,
        because the endTime is not affected. This method changes the endTime"""

        duration = self.duration
        self.startTime = dateTime
        self.endTime = self.startTime + duration


class Location(Item.Item):
    def __init__(self, name=None, parent=None, kind=None):
        if not parent:
            parent = ContentModel.ContentModel.getContentItemParent()
        if not kind:
            kind = CalendarParcel.getLocationKind()
        Item.Item.__init__(self, name, parent, kind)
        

class Calendar(Item.Item):
    def __init__(self, name=None, parent=None, kind=None):
        if not parent:
            parent = ContentModel.ContentModel.getContentItemParent()
        if not kind:
            kind = CalendarParcel.getCalendarKind()
        Item.Item.__init__(self, name, parent, kind)

class RecurrencePattern(Item.Item):
    def __init__(self, name=None, parent=None, kind=None):
        if not parent:
            parent = ContentModel.ContentModel.getContentItemParent()
        if not kind:
            kind = CalendarParcel.getRecurrencePatternKind()
        Item.Item.__init__(self, name, parent, kind)

class Reminder(Item.Item):
    def __init__(self, name=None, parent=None, kind=None):
        if not parent:
            parent = ContentModel.ContentModel.getContentItemParent()
        if not kind:
            kind = CalendarParcel.getReminderKind()
        Item.Item.__init__(self, name, parent, kind)

#   Copyright (c) 2004-2007 Open Source Applications Foundation
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


__parcel__ = "osaf.framework.blocks"

from chandlerdb.util.c import Nil
from application import schema
from application.Application import mixinAClass
from i18n import ChandlerMessageFactory as _
import Block as Block
import logging
import wx
import os


class RefCollectionDictionary(schema.Item):
    """
    Provides dictionary access to a reference collection attribute
    L{RefList<repository.item.RefCollections.RefList>}.

    The attribute that contains the reference collection is determined
    through attribute indirection using the collectionSpecifier attribute.

    The "itsName" property of the items in the reference collection
    is used for the dictionary lookup by default.  You can override
    the name accessor if you want to use something other than
    itsName to key the items in the collection.
    """

    def itemNameAccessor(self, item):
        """
        Name accessor used for RefCollectionDictionary
        subclasses can override this method if they want to
        use something other than the itsName property to
        determine item names.

        @param item: The item whose name we want.
        @type item: C{item}
        @return: A C{immutable} for the key into the collection
        """
        return item.itsName or item.itsUUID.str64()

    def getCollectionSpecifier(self):
        """
        Determines which attribute to use for the collectionSpecifier.

        Subclasses can override this method if they want to
        use something other than collectionSpecifier,
        which is typlically set up to redirect to the actual
        attribute that contains the collection.

        @return: A C{String} for the name of the collection attribute
        """
        raise NotImplementedError, (type(self), 'getCollectionSpecifier')

    def _index(self, key):
        """
        Returns a tuple with the item refered to by the key, and the
        collection.

        @param key: The key used for lookup into the ref collection.
        @type key: C{immutable}, typically C{String} or C{int}
        @return: A C{Tuple} containing C{(item, collection)} or raises an
                 exception if not found.
        """
        coll = getattr(self, self.getCollectionSpecifier())
        if isinstance (key, int):
            if key >= 0:
                i = coll.first ()
                next = coll.next
            else:
                i = coll.last ()
                next = coll.previous
                key = -key
            for index in xrange (key):
                i = next (i)
        else:
            i = coll.getByAlias(key)
        return (i, coll)

    def index(self, key):
        """
        Returns the item refered to by the key.

        @param key: The key used for lookup into the ref collection.
        @type key: C{immutable}, typically C{String}
        @return: C{item} if found, or C{None} if not found.
        """
        try:
            i, coll = self._index(key)
            return i
        except KeyError:
            return None

    def __iter__(self):
        """
        Returns an iterator to the collection attribute.
        """
        return iter(getattr(self, self.getCollectionSpecifier()))

    def __len__(self):
        """
        @return: C{int} length of the collection attribute.
        """
        # In case our collection doesn't exist return zero
        return len(getattr(self, self.getCollectionSpecifier(), Nil))

    def has_key(self, key):
        """
        @param key: The key used for lookup into the ref collection.
        @type key: C{immutable}, typically C{String}
        @return: C{True} if found, or {False} if not found.
        """
        return self.index(key) != None

    def __contains__(self, item):
        """
        @param item: An item to find in the ref collection.
        @type item: C{item}
        @return: C{True} if found, or {False} if not found.
        """
        coll = getattr(self, self.getCollectionSpecifier())
        return coll.get(item.itsUUID) != None

    def __getitem__(self, key):
        """
        Return the item associated with the key from the ref collection attribute.

        @param key: The key used for lookup into the ref collection.
        @type key: C{immutable}, typically C{String}
        @return: C{item} if found, or raises an exception.
        """
        return self._index(key)[0]

    def __setitem__(self, key, value):
        """
        Replace the item associated with the key from the ref collection
        attribute.

        Note that the new item may have a different key, but it will be
        placed in the same position in the ref collection, and the keyed
        item will be removed.

        @param key: The key used for position lookup into the ref collection.
        @type key: C{immutable}, typically C{String}
        @param value: The C{item} to place into the ref collection.
        @type value: C{item}
        """
        itemIndex, coll = self._index(key) # find the keyed item
        self.insert(itemIndex, value) # insert before
        if itemIndex is not None:
            coll.remove(itemIndex) # remove keyed original

    def insert(self, index, item):
        """
        Insert item before index in our ref collection.

        @param index: The position used for insertion into the ref collection.
        @type index: C{item} that exists in the ref collection, or C{None} to append.
        @param item: The C{item} to insert before C{index} in the ref collection.
        @type item: C{item}
        """

        coll = getattr(self, self.getCollectionSpecifier())
        if index is None:
            afterItem = coll.last()
        else:
            afterItem = coll.previous(index)

        coll.insertItem (item, afterItem)
        coll.setAlias(item, self.itemNameAccessor(item))

    def insertAfter(self, index, item):
        """
        Insert item after index in our ref collection.

        @param index: The position used for insertion into the ref collection.
        @type index: C{item} that exists in the ref collection.
        @param item: The C{item} to insert before C{index} in the ref collection.
        @type item: C{item}
        """

        coll = getattr(self, self.getCollectionSpecifier())

        coll.insertItem (item, index)
        coll.setAlias(item, self.itemNameAccessor(item))

    def __delitem__(self, key):
        """
        Delete the keyed item from our ref collection.

        @param key: The key used for item location in the ref collection.
                    Throws an exception if there is no item associated with the key.
        @type key: C{immutable}, typically C{String}
        """
        itemIndex, coll = self._index(key)
        coll.remove(itemIndex)
        
    def next(self, item):
        coll = getattr(self, self.getCollectionSpecifier())
        return coll.next (item)

class DynamicBlock(schema.Item):
    """
    Mixin class for any Dynamic Block, both DynamicContainers
    and DynamicChild blocks.

    You should mix this class into a Block
    """
    def isDynamicChild (self):
        return False

    def isDynamicContainer (self):
        return False

    def appendDynamicBlocks (self, blockList):
        """
        Uniquely insert all dynamic blocks recursively to blockList
        preserving the order of the items.

        Note that items need to be inserted at the beginning, because
        we are scanning the tree from the bottom up, and tend to find
        the dynamic additions first, and the static definitions last.

        We want the static definitions to come first because the dynamic
        additions override them.
        """
        method = getattr (type (self), "isDynamicContainer", None)
        if method is not None:
            isContainer = method (self)
            # dynamicChildren with with operation = "None" are treated as static items.
            try:
                i = blockList.index (self)
            except ValueError:
                blockList.insert (0, self)
            else:
                blockList[i:i+1] = (self,)
            if isContainer:
                for child in self.childBlocks:
                    child.appendDynamicBlocks (blockList)

    def buildDynamicList (self):
        """
        Build a list of dynamic blocks found starting at self,
        moving up through the static hierarchy, and tunnelling down
        inside all dynamic branches found.

        We need all Dynamic Containers, and all Dynamic Children
        that have an itemLocation specified.

        @return: The list of all Dynamic Blocks.
        """
        blockList = []
        block = self
        while block is not None:
            for child in block.childBlocks:
                method = getattr (type (child), "appendDynamicBlocks", None)
                if method is not None:
                    method (child, blockList)
            block = block.parentBlock
        return blockList

    def rebuildContainers(self, containers):
        """
        Scan for dynamic containers, registering them in the containers list.
        Returns the block list of all dynamic blocks found.

        @param containers: The containers dictionary.
        @type containers: C{dict} to put all DynamicContainer blocks into.
        @return: The list of all Dynamic Blocks.
        """
        blockList = self.buildDynamicList ()
        for block in blockList:
            if block.isDynamicContainer ():
                # initialize dynamic children starting with the static hierarchy
                block.populateFromStaticChildren ()
                containers [block.blockName] = block
        return blockList

    def rebuildChildren(self, containers, blockList):
        """
        Scan for dynamic children, find their parent, and attach them
        appropriately to the parent.dynamicChildren attribute.

        @param containers: The containers dictionary.
        @type containers: C{dict} to put all DynamicContainer blocks into.
        @param blockList: The list of all Dynamic blocks to consider.
        @type blockList: C{list} of DynamicBlock objects.
        """
        for child in blockList:
            # pick up children
            if child.isDynamicChild ():
                """
                Use location to look up the container that
                contains the entry or container.

                If you get an exception here, it's probably because
                the name of the location isn't the name of an existing
                bar.

                Use 'MenuBar' for the Menu Bar.
                """
                operation = child.operation
                locationName = getattr (child, 'location', None)

                if operation != 'None' or locationName is not None:
                    if locationName is None:
                        locationName = child.parentBlock.blockName
                    bar = containers [locationName]
    
                    assert child in bar or not bar.has_key (child.blockName), "Child name is already in toolbar"
                    if operation != 'None':
                        if operation == 'InsertAfter':
                            # find its position (or None) and insert there (or at the end)
                            i = bar.index (child.itemLocation)
                            bar.insertAfter (i, child)
                        elif operation == 'InsertBefore':
                            i = bar.index (child.itemLocation)
                            bar.insert (i, child)
                        elif operation == 'Replace':
                            bar[child.itemLocation] = child
                        elif operation == 'Delete':
                            # If you get an exception here, it's probably because
                            # you're trying to remove a bar item that doesn't exist.
                            del bar[child.itemLocation]

    def synchronizeDynamicBlocks (self):
        """
        synchronizeDynamicBlocks rebuilds the dynamic
        container hierarchy based on the blocks it finds in
        a root section of the static block hierarchy and then
        calls synchronizeWidget on each container.

        Dynamic associations between blocks are done by blockName,
        which must be unique.  Upon exit all DynamicContainer
        blocks found will have references to all dynamicChildren
        found, and those blocks will have an inverse reference
        to their dynamicParent.

        The rebuild is done starting at the specified block,
        moving up to the parentBlock, repeating this process
        until reaching the root of the hierarchy.  If we find
        any dynamic block at any point in the traversal we
        scan down through all of its children recursively
        as long as dynamic blocks are found.

        DynamicContainers and their dynamicChildren are
        identified by their itemName rather than their UUIDs,
        to make it easy for third party parcels to add menus.

        This requires all container names to be unique
        and all names of dynamicChildren to be unique within
        their container.

        @param self: The starting block for the scan.
        @type self: C{DynamicBlock}
        """

        containers = {}
        """
        Rebuild the dynamic container hierarchy.

        First establish all containers, then insert their children
        so the block declarations can be order-independent.
        """
        allDynamic = self.rebuildContainers (containers)
        self.rebuildChildren (containers, allDynamic)

        """
        Now that the we have the new dynamic structure,
        update the blocks that have changed and call synchronizeWidget
        on them so they know to redraw.
        """
        for bar in containers.values():
            """
            Can't call synchronizeWidget because IgnoreSynchronizeWidget
            is true because we're in Tab's synchronizeWidget.
            """
            bar.synchronizeWidget()

        # Since menus have changed, we need to reissue UpdateUI events
        wx.GetApp().needsUpdateUI = True


class operationEnumType(schema.Enumeration):
      values = "None", "InsertAfter", "InsertBefore", "Replace", "Delete"


class DynamicChild(DynamicBlock):
    """
    Dynamic Children are built dynamically when the Active View changes.

    They include MenuItems, Menus, and ToolbarItems.
    Used as a mixin class for other blocks.
    """

    dynamicParent = schema.One(defaultValue = None)
    title = schema.One(schema.Text)
    operation = schema.One(operationEnumType, defaultValue = 'None')
    location = schema.One(schema.Text)
    itemLocation = schema.One(schema.Text, defaultValue = u'')
    helpString = schema.One(schema.Text, defaultValue = u'')

    def isDynamicChild (self):
        return True

class DynamicContainer(RefCollectionDictionary, DynamicBlock):
    """
    A block whose children are built dynamically, when the
    Active View changes.

    This list of children is in "dynamicChildren" and the
    back pointer is in "dynamicParent".
    """

    dynamicChildren = schema.Sequence(
        inverse = DynamicChild.dynamicParent, initialValue = [],
    )

    schema.addClouds(
        copying = schema.Cloud(byCloud = [dynamicChildren])
    )

    def getCollectionSpecifier(self):

        return 'dynamicChildren'

    def itemNameAccessor(self, item):
        """
        Use blockName for the accessor.
        """
        return item.blockName

    def isDynamicContainer (self):
        return True

    def populateFromStaticChildren (self):
        # copy our static children as a useful starting point
        self.dynamicChildren.clear ()
        for block in self.childBlocks:
            self[block.blockName] = block

    def ensureDynamicChildren (self):
        """
        Make sure we have a DynamicChildren hierarchy, since all my
        subclasses use that hierarchy when they synchronize.

        If there is no DynamicChildren built, then initialize it from
        the childBlocks hierarchy.
        """
        if not self.dynamicChildren:
            self.populateFromStaticChildren()

class wxMenuItem (wx.MenuItem):
    def __init__(self, style, *arguments, **keywords):
        # unpack the style arguments, wx expects them separately
        arguments = style + arguments
        super (wxMenuItem, self).__init__ (*arguments, **keywords)

    def OnInit(self):
        if hasattr(self.blockItem, 'icon'):
            app = wx.GetApp()
            uncheckedbitmap = \
                app.GetImage(self.blockItem.icon + ".png")
            if uncheckedbitmap:
                if '__WXMAC__' in wx.PlatformInfo:
                    # the mac already shows checkmarks next to menu
                    # items, so we just use the regular bitmap here
                    checkedbitmap = uncheckedbitmap
                else:
                    checkedbitmap = \
                        app.GetImage(self.blockItem.icon + "Checked.png")
                    if not checkedbitmap:
                        checkedbitmap = uncheckedbitmap
                self.SetBitmaps(checkedbitmap, uncheckedbitmap)

    def __cmp__ (self, other):
        """
        Shouldn't be needed, but wxWidgets will return it's internal
        wx.MenuItem when you ask for a menu item, instead of the wxMenuItem
        subclass that we supply to wx.  So we use this compare to test if
        the two instances are really the same thing.

        Note: @@@DLD - remove when wx.MenuItem subclasses are returned by wx.
        """
        try:
            if self.this == other.this:
                return 0
            else:
                return -1
        except AttributeError:
            raise NotImplementedError

    def Destroy(self):
        Block.Block.wxOnDestroyWidget (self)
        # Remove the menu item from it's menu if it's still in the menu
        menu = self.GetMenu()
        if menu and menu.FindItemById (self.GetId()):
            menu.RemoveItem (self)
        del self

    def wxSynchronizeWidget(self):
        # placeholder in case Menu Items change
        pass

    @classmethod
    def CalculateWXStyle(cls, block):
        parentWidget = block.dynamicParent.widget
        if block.menuItemKind == "Separator":
            id = wx.ID_SEPARATOR
            kind = wx.ITEM_SEPARATOR
            style = (parentWidget, id, "", "", kind, None)
        else:
            id = block.getWidgetID()
            if block.menuItemKind == "Normal":
                kind = wx.ITEM_NORMAL
            elif block.menuItemKind == "Check":
                kind = wx.ITEM_CHECK
            elif block.menuItemKind == "Radio":
                kind = wx.ITEM_RADIO
            else:
                assert (False)
            title = block.title
            if len (block.accel) > 0:
                title = title + '\t' + block.accel

            """
            When inserting ourself into a MenuItem, we must actually
            insert ourself into the submenu of that MenuItem.
            """
            if isinstance (parentWidget, wxMenu):
                style = (parentWidget, id, title, block.helpString, kind, None)
            else:
                assert isinstance (parentWidget, wxMenuItem)
                submenu = block.GetSubMenu()
                assert submenu
                style = (None, id, title, block.helpString, kind, submenu)
        return style

    def setMenuItem (self, newItem, oldItem, index):
        subMenu = self.GetSubMenu()
        assert isinstance (subMenu, wxMenu)
        subMenu.setMenuItem(newItem, oldItem, index)

    def getMenuItems(self):
        wxMenuObject = self.GetSubMenu()
        assert isinstance (wxMenuObject, wxMenu)
        return wxMenuObject.GetMenuItems()

class wxMenu(wx.Menu):
    def __init__(self, *arguments, **keywords):
        super (wxMenu, self).__init__ (*arguments, **keywords)

    def wxSynchronizeWidget(self):
        self.blockItem.synchronizeItems()

    def Destroy(self):
        Block.Block.wxOnDestroyWidget (self)
        parentMenu = self.GetParent()
        if parentMenu is not None:
            for item in parentMenu.GetMenuItems():
                if item.GetSubMenu() is self:
                    super (wxMenu, parentMenu).DestroyItem (item)
                    break
        else:
            menuBar = self.GetMenuBar()
            if menuBar:
                for index in xrange (menuBar.GetMenuCount()):
                    if menuBar.GetMenu (index) == self:
                        menuBar.Remove (index)
                        del self
                        break

    def __cmp__ (self, other):
        """
        CPIA and wxWidgets have different ideas about how submenus work.

        In CPIA a menu can appear in the menu bar, or inside another menu.

        In wxWidgets, only a MenuItem can appear in a Menu, and you have to
        get the "subMenu" out of the MenuItem to deal with it as a Menu.

        This method lets us compare a CPIA wxMenu widget with a wx.MenuItem
        and they will be the same if the wx.MenuItem has the right subMenu.
        """
        # self is a CPIA wxMenu.  "other" could be a wx.MenuItem
        try:
            # the menu is in the sub-menu of the item
            subMenu = other.GetSubMenu ()
        except AttributeError:
            pass # wasn't a wx.MenuItem
        else:
            # check if it actually had a submenu
            if subMenu is not None:
                other = subMenu # use the submenu for the compare
        if self is other:
            return 0 # they matched
        else:
            return -1

    """
    wxWindows doesn't implement convenient methods for dealing
    with menus, so we'll write our own: getMenuItems, removeItem
    and setMenuItem.
    """
    def getMenuItems (self):
        return self.GetMenuItems()

    def removeItem (self, index, oldItem):
        oldMenuItem = self.RemoveItem (oldItem)
        oldMenuItem.thisown = False

    def setMenuItem (self, newItem, oldItem, index):
        # set the menu item, replacing an old one if specified
        # the widget stays attached to the block until the block is destroyed
        itemsInMenu = self.GetMenuItemCount()
        assert (index <= itemsInMenu)
        if oldItem is not None:
            assert index < itemsInMenu, "index out of range replacing menu item"
            self.removeItem (index, oldItem)
        if isinstance (newItem.widget, wxMenuItem):
            success = self.InsertItem (index, newItem.widget)
            assert success, "error inserting menu item"
            """
            Disable menus by default. If they have an event then they will
            be enabled by an UpdateUIEvent or our command dispatch in Application.py
            """
            self.Enable (newItem.widget.GetId(), False)
        else:
            self.InsertMenu (index, 0, newItem.title, newItem.widget, newItem.helpString)

class wxMenuBar (wx.MenuBar):
    def Destroy(self):
        """
        We need to override Destroy to remove the MenuBar from mainFrame.

        We don't need to call wxOnDestroyWidget since wxMenuBar is a
        subclass of wxWindow, which sends a EVT_WINDOW_DESTROY which
        ends up calling wxOnDestroyWidget for us.

        Overriding __del__ doesn't work here since calling SetMenuBar (None)
        when the menuBar is being destroyed causes the application to crash --
        probably because wxWidgets tries to access the MenuBar when it's
        almost already deleted. Overriding Destroy catches the menuBar
        before it's deleted instead of just before it's disposed.
        """
        self.blockItem.getFrame().SetMenuBar(None)
        super (wxMenuBar, self).Destroy()

    def wxSynchronizeWidget(self):
        self.blockItem.synchronizeItems()

    """
    wxWindows doesn't implement convenient menthods for dealing
    with menus, so we'll write our own: getMenuItems, removeItem
    and setMenuItem.
    """
    def getMenuItems (self):
        menuList = []
        for index in xrange (self.GetMenuCount()):
            menuList.append (self.GetMenu (index))
        return menuList

    def removeItem (self, index, oldItem):
        oldMenu = self.Remove (index)

    def setMenuItem (self, newItem, oldItem, index):
        itemsInMenu = self.GetMenuCount()
        assert (index <= itemsInMenu)
        title = newItem.title
        # operating within the current list?
        if index < itemsInMenu:
            # check if the new item is already installed, and remove it first
            if newItem.widget in self.getMenuItems (): # invokes wxMenu.__cmp__
                self.removeItem (index, newItem.widget)
            # if there's an old item present, replace it, else just insert
            if oldItem is not None:
                oldMenu = self.Replace (index, newItem.widget, title)
                assert oldMenu is oldItem
            else:
                self.Insert (index, newItem.widget, title)
        else:
            # beyond list, add to the end
            success = self.Append (newItem.widget, title)
            assert success


class menuItemKindEnumType(schema.Enumeration):
      values = "Normal", "Separator", "Check", "Radio"

class MenuItem (Block.Block, DynamicChild):

    menuItemKind = schema.One(menuItemKindEnumType, initialValue = 'Normal')
    accel = schema.One(schema.Text, initialValue = u'')
    event = schema.One(Block.BlockEvent, inverse = Block.BlockEvent.menusForEvent)
    schema.addClouds(
        copying = schema.Cloud(byRef = [event])
    )
    icon = schema.One(schema.Text)
    toggleTitle = schema.One(schema.Text, initialValue = u'')

    def instantiateWidget (self):
        # We'll need a dynamicParent's widget in order to instantiate
        assert (isinstance(self.dynamicParent.widget, wxMenu))
        return wxMenuItem(style=wxMenuItem.CalculateWXStyle(self))

class MenuBar (Block.Block, DynamicContainer):
    def instantiateWidget (self):
        self.ensureDynamicChildren ()
        return wxMenuBar()


    def synchronizeItems(self):
        """
        Install the menus into supplied menu list, and submenus
        into their menu items.
        Used for both Menus and MenuBars.
        """
        menuList = self.widget.getMenuItems () # keep track of menus here

        index = 0 # cur menu item index
        # for each new menu
        for menuItem in self.dynamicChildren:
            # ensure that the menuItem has been instantiated
            if not hasattr (menuItem, "widget"):
                # @@@DLD - use framework block/widget linkage
                widget = menuItem.instantiateWidget()
                menuItem.widget = widget
                widget.blockItem = menuItem
                # We need to call wxSynchronizeWidget here instead of synchronizeWidget
                # becuase syncrhonizeItems is called from synchronizeWidget
                widget.wxSynchronizeWidget()

            # get the current item installed in the menu, if any
            if len(menuList) != 0:
                curItem = menuList.pop(0)
            else:
                curItem = None

            # current and new items match?
            if curItem is None or menuItem.widget != curItem: # invokes our __cmp__

                # is the new item already somewhere in our menu?
                if menuItem.widget in menuList: # invokes our __cmp__
                    # yes, rip out existing items till we get to our new item
                    while menuItem.widget != curItem:
                        self.widget.removeItem (index, curItem)
                        curItem = menuList.pop(0)
                        # until we get to the matching item
                else:
                    # no, we're inserting a new item
                    self.widget.setMenuItem (menuItem, None, index)
                    if curItem is not None:
                        menuList.insert (0, curItem) # put the cur item back, we didn't use it
            index += 1

        # remove any remaining items in the menu
        for oldItem in menuList:
            self.widget.removeItem (index, oldItem)
            index += 1

class Menu (MenuBar, DynamicChild):
    def instantiateWidget (self):
        self.ensureDynamicChildren ()
        return wxMenu()

"""
Toolbar classes.
"""

class wxToolbar (Block.BaseWidget, wx.ToolBar):
    def __init__(self, *arguments, **keywords):
        super (wxToolbar, self).__init__ (*arguments, **keywords)
        # keep track of ToolbarItems so we can tell when/how they change in synchronize
        self.toolItemList = [] # non-persistent list
        self.renderItems = False # controls whether toolbar items are rendered

    def wxSynchronizeWidget(self):
        super (wxToolbar, self).wxSynchronizeWidget()
        self.SetToolBitmapSize((self.blockItem.toolSize.width, self.blockItem.toolSize.height))
        self.SetToolSeparation(self.blockItem.separatorWidth)

        colorStyle = self.blockItem.colorStyle
        if colorStyle is not None:
            self.SetBackgroundColour(colorStyle.backgroundColor.wxColor())
            self.SetForegroundColour(colorStyle.foregroundColor.wxColor())

        dynamicChildren = self.blockItem.dynamicChildren
        index = 0
        for old, new in map (None, self.toolItemList, dynamicChildren):
            if old is not new:
                break
            index += 1
        else:
            return

        for block in self.toolItemList [index:]:
            widget = getattr (block, "widget", None)
            if widget is not None:
                block.onDestroyWidget()
            self.DeleteToolByPos (index)
        
        self.toolItemList = self.toolItemList [0:index]
        
        self.renderItems = True
        try:
            while new is not None:
                new.render()
                new = dynamicChildren.next (new)
        finally:
            self.renderItems = False
        
        # draw the bar, and we're done.
        self.Realize()

    def _item_named (self, toolbarItemName):
        for toolbarItem in self.blockItem.dynamicChildren:
            if getattr(toolbarItem, 'blockName', None) == toolbarItemName:
                return toolbarItem
        return None

    def pressed (self, toolbarItem = None, name=''):
        # return the state of the toolbarItem, or item located by toolbarName
        if toolbarItem is None:
            toolbarItem = self._item_named (name)
        return self.GetToolState(toolbarItem.toolID)

    def press (self, toolbarItem = None, name=''):
        # post the event for the toolbarItem, or toolbarItem located by name
        if toolbarItem is None:
            toolbarItem = self._item_named (name)
        return Block.Block.post(toolbarItem.event, {}, toolbarItem)

class wxToolbarItemMixin (object):
    """
    Toolbar Tool Widget mixin, for various items that can appear in a Toolbar.

    ToolbarItems are a CPIA concept, that are roughly equivalent to the
    wx object ToolbarTool.  In CPIA, ToolbarItems are children of Toolbars,
    (both regular childBlocks and dynamicChildren).  But in wxWidgets,
    a ToolbarTool is not a child of the Toolbar, instead it's added to
    the Toolbar with a special method call (either DoAddTool or AddControl).

    Because of this, destroying the Toolbar won't automatically destroy
    the widgets associated with each ToolbarItem since they are not
    children of the Toolbar from the wx perspective.  Luckily, about the
    only time we destroy the Toolbar is when we call wxSynchronizeWidget
    on it, so we can handle it specially.  At that time we explicitly
    call the onDestroy method on each ToolbarItem to unhook that
    block from its widget.
    """
    def Destroy(self):
        # toolbar items that are now wx.Windows need to have their blocks destroyed
        # menually. wx.Windows' destructions are caught by the application, which
        # handles their blocks' destruction.
        if not isinstance(self, wx.Window):
            Block.Block.wxOnDestroyWidget (self)
        
        parent = self.blockItem.dynamicParent
        if parent is None:
            parent = self.blockItem.parentBlock
        parent.widget.DeleteTool(self.GetId())

    def wxSynchronizeWidget(self):
        """
        Currently, we only synchronize radio buttons, eventually we
        need to synchronize other kinds, e.g. Text, Combo, and Choice types.
        """
        block = self.blockItem
        if block.toolbarItemKind == "Radio":
            selected = getattr (block, "selected", None)
            if selected is True:
                self.GetToolBar().ToggleTool (self.GetId(), True)

    def IsShown (self):
        # Since wx.ToolbarTools are not real widgets, they don't support IsShown,
        #  so we'll provide a stub for CPIA.
        return True

    def OnSetTextEvent (self, event):
        """
        wxToolbarItems don't properly handle setting the text of buttons, on
        updateUIEvents, so we'll handle it here.
        """
        self.SetLabel (event.GetText())
        if getattr(self, 'GetToolBar', None) is not None:
            # text fields in the toolbar do not have a GetToolBar() method
            self.GetToolBar().Realize()

    def SetToolbarItemBitmap(self, bitmapName):
        # get the named bitmap
        bitmap = wx.GetApp().GetImage(bitmapName)
        if bitmap is not None and getattr(self, 'GetToolBar', None) is not None:
            toolbar = self.GetToolBar()
            toolbar.SetToolNormalBitmap(self.GetId(), bitmap)
            toolbar.Realize()

    def selectTool(self):
        """
        Persist state of ToolbarItems. Currently limited to radio buttons,
        eventually we need to synchronize other kinds, e.g. Text, Combo, and
        Choice types.
        """
        block = self.blockItem
        if block.toolbarItemKind == "Radio":
            children = [child for child in block.parentBlock.childBlocks]
            blockIndex = children.index (block)
            """
            Unselect all the items in the radio group before this toolbar item.
            """
            index = blockIndex - 1
            while index >= 0 and children [index].toolbarItemKind == "Radio":
                children [index].selected = False
                children [index].synchronizeWidget()
                index -= 1
            """
            Select this toolbar item.
            """
            children [blockIndex].selected = True
            children [blockIndex].synchronizeWidget()

            """
            Unselect all the items in the radio group after this toolbar item.
            """
            index = blockIndex + 1
            while index < len (children) and children [index].toolbarItemKind == "Radio":
                children [index].selected = False
                children [index].synchronizeWidget()
                index += 1

    def OnToolEvent (self, event):
        self.selectTool()
        event.Skip()

from osaf.framework.blocks.Styles import ColorStyle
from osaf.pim.structs import SizeType

class Toolbar(Block.RectangularChild, DynamicContainer):

    colorStyle = schema.One(ColorStyle, defaultValue = None)
    toolSize = schema.One(SizeType)
    separatorWidth = schema.One(schema.Integer, initialValue = 5)
    buttons3D = schema.One(schema.Boolean, initialValue = False)
    buttonsLabeled = schema.One(schema.Boolean, initialValue = False)
    mainFrameToolbar = schema.One(schema.Boolean, defaultValue = False)
    schema.addClouds(
        copying = schema.Cloud(byRef=[colorStyle])
    )

    def instantiateWidget (self):
        self.ensureDynamicChildren ()
        heightGutter = self.buttonsLabeled and 23 or 6
        parentWidget = self.parentBlock.widget
        toolbar = wxToolbar(parentWidget,
                            self.getWidgetID(),
                            wx.DefaultPosition,
                            (-1, self.toolSize.height+heightGutter),
                            style=self.calculate_wxStyle())
        # set the tool bitmap size right away
        toolbar.SetToolBitmapSize((self.toolSize.width, self.toolSize.height))
        return toolbar

    def calculate_wxStyle (self):
        style = wx.TB_HORIZONTAL | wx.TB_MAC_NATIVE_SELECT
        if self.buttons3D:
            style |= wx.TB_3DBUTTONS
        else:
            style |= wx.TB_FLAT
        if self.buttonsLabeled:
            style |= wx.TB_TEXT
        return style

    def pressed (self, toolbarItem=None, name=''):
        # return the state of the toolbarItem, or toolbarItem located by name
        return self.widget.pressed (toolbarItem, name)

    def press (self, toolbarItem = None, name=''):
        # post the event for the toolbarItem, or toolbarItem located by name
        return self.widget.press (toolbarItem, name)

class wxTextCtrl(wx.TextCtrl):
    """
    """
    def onDestroyWidget(self, *arguments, **keywords):
        super (wxTextCtrl, self).onDestroyWidget(*arguments, **keywords)

    def onDestroy(self, event):
        super (wxTextCtrl, self).onDestroy(event)

class toolbarItemKindEnumType(schema.Enumeration):
    values = "Button", "Separator", "Radio", "QuickEntry"

class ToolbarItem(Block.Block, DynamicChild):
    """
    Item, e.g. button, that lives in a Toolbar.
    """
    prototype = schema.One(
        Block.Block, doc = 'The prototype block to be placed in the Toolbar',
    )
    selected = schema.One(schema.Boolean)

    toggle = schema.One(
        schema.Boolean,
        doc = 'For Buttons, makes it stay pressed down until pressed again.',
        initialValue = False,
    )
    bitmap = schema.One(schema.Text)
    disabledBitmap = schema.One(schema.Text)
    event = schema.One(Block.BlockEvent)
    toolbarItemKind = schema.One(toolbarItemKindEnumType)

    text = schema.One(schema.Text) # optional text for the toolbar item, e.g. QuickEntry text
    lastText = schema.One(schema.Text) # optional lastText for the toolbar item, e.g. QuickEntry last search
    size = schema.One(SizeType) # optional size used in QuickEntry

    schema.addClouds(
        copying = schema.Cloud(byRef=[prototype], byCloud=[event])
    )

    def instantiateWidget (self):
        def getBitmaps (self):
            app = wx.GetApp()
            bitmap = app.GetImage (self.bitmap)
            disabledBitmap = getattr (self, 'disabledBitmap', wx.NullBitmap)
            if disabledBitmap is not wx.NullBitmap:
                disabledBitmap = app.GetImage (disabledBitmap)
            return bitmap, disabledBitmap

        tool = None
        # Don't render unless our toolbar wants items rendered
        toolbar = self.dynamicParent.widget
        if toolbar.renderItems:

            id = self.getWidgetID()
            self.toolID = id
            # Bug 4090 - long help never appears in the status bar
            # for this reason I'm putting the longhelp into shorthelp too.
            shortHelp = self.helpString
            longHelp = self.helpString
    
            # First consider toolBarItems that don't have tools
            if self.toolbarItemKind == 'Separator':
                toolbar.AddSeparator()
            else:
                # Next consider toolBarItems that aren't controls
                if (self.toolbarItemKind == 'Button' or
                    self.toolbarItemKind == 'Radio'):
        
                    bitmap, disabledBitmap = getBitmaps (self)
                    if self.toggle:
                        theKind = wx.ITEM_CHECK
                    elif self.toolbarItemKind == 'Radio':
                        theKind = wx.ITEM_RADIO
                    else:
                        theKind = wx.ITEM_NORMAL
        
                    tool = toolbar.DoAddTool (id,
                                              self.title,
                                              bitmap,
                                              disabledBitmap,
                                              kind = theKind,
                                              shortHelp = shortHelp,
                                              longHelp = longHelp)
                    # add toolbarMixin, so it has the extra methods needed for Bind.
                    mixinAClass (tool, 'osaf.framework.blocks.MenusAndToolbars.wxToolbarItemMixin')
                    toolbar.SetToolLongHelp(id, longHelp)
                    toolbar.Bind (wx.EVT_TOOL, tool.OnToolEvent, id=id)
                else:
                    # Finally consider toolBarItems that are controls
                    if self.toolbarItemKind == 'QuickEntry':
                        tool = wxQuickEntry (toolbar,
                                             id,
                                             "",
                                             wx.DefaultPosition,
                                             size = (self.size.width, self.size.height),
                                             style = wx.TE_PROCESS_ENTER)
                        toolbar.AddControl (tool)
                    assert tool is not None, "unknown toolbarItemKind"
            toolbar.toolItemList.append (self)
        
        return tool

class wxQuickEntry (wxToolbarItemMixin, wx.SearchCtrl):
    """
    The order of superclasses is important. If it's wx.SearchCtrl, wxToolbarItemMixin
    Mac crashes in the destructor of the toolbar when it calls Realize
    """
    def __init__(self, parent, id, title, position, **keywords):
        super (wxQuickEntry, self).__init__ (parent, id, title, position, **keywords)
        self.ShowSearchButton(False)
        self.ShowHideCancelButton()
        self.SetDescriptiveText(_(u'Create new item'))
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnCancelButton)
        self.Bind(wx.EVT_TEXT_ENTER, wx.GetApp().OnCommand)
        self.Bind(wx.EVT_TEXT, self.OnUpdateButtons)
                  
    def OnCancelButton (self, event):
        block = self.blockItem
        block.post (block.event, {"cancelClicked": True}, sender = block)

    def wxSynchronizeWidget(self):
        super (wxQuickEntry, self).wxSynchronizeWidget()
        self.SetValue (self.blockItem.text)
        self.ShowHideCancelButton()
        
    def ShowHideCancelButton(self):
        self.ShowCancelButton( self.GetValue() != "" )

    def OnUpdateButtons(self, event):
        self.ShowHideCancelButton()
        

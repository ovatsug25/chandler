#   Copyright (c) 2003-2007 Open Source Applications Foundation
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

"""
Unit tests for kinds
"""

import os, unittest
from cStringIO import StringIO

from chandlerdb.util.RepositoryTestCase import RepositoryTestCase
from chandlerdb.item.Item import Item
from chandlerdb.item.ItemIO import XMLItemWriter
from chandlerdb.util.SAX import XMLPrettyGenerator, XMLGenerator
from chandlerdb.schema.Attribute import Attribute
from chandlerdb.schema.Kind import Kind

class KindTest(RepositoryTestCase):
    """ Test Kinds  """

    def setUp(self):
        super(KindTest, self).setUp()

        view = self.view
        self.kind = view.findPath("//Schema/Core/Kind")
        self.itemKind = view.findPath("//Schema/Core/Item")
        self.attrKind = self.itemKind.itsParent['Attribute']

        self.kind1 = self.kind.newItem('kind1', view)
        self.kind1.addValue('superKinds', self.itemKind)
        self.kind1Attr1 = Attribute('k1a1', view, self.attrKind)
        self.kind1Attr1.cardinality = 'list'
        self.kind1Attr1.otherName = 'owner'
        self.kind1.addValue('attributes', self.kind1Attr1, alias='k1a1')

        kind1Attr1Bad = Attribute('k1a1bad', self.kind1, self.attrKind)
        kind1Attr1Bad.cardinality = 'list'
        kind1Attr1Bad.otherName = 'owner'
        try:
            self.kind1.addValue('attribute', kind1Attr1Bad, alias='k1a1bad')
        except AttributeError:
            pass
        
        self.kind2 = self.kind.newItem('kind2', self.kind1)
        self.kind2.addValue('superKinds', self.itemKind)
        self.kind2.addValue('attributes', self.kind1Attr1, alias='k1a1')
        self.kind2Attr2 = Attribute('k2a2', view, self.attrKind)
        self.kind2Attr2.cardinality = 'list'
        self.kind2.addValue('attributes', self.kind2Attr2, alias='k2a2')
    
    def testBasic(self):
        """ Test basic Kind methods """
        kindClass = self.kind.getItemClass()
        itemKindClass = self.itemKind.getItemClass()
        self.assertEquals(kindClass.__name__,"Kind")
        self.assertEquals(itemKindClass.__name__,"Item")

    def testGetAttribute(self):
        """ Test getAttribute and has Attribute """
        
        # an attribute that is a child but not on the atts list should
        # not be returned
        try:
            self.kind1.getAttribute('k1a1bad')            
            self.assert_(False)
        except AttributeError:
            pass

        self.assert_(not self.kind1.hasAttribute('k1a1bad'))

        # basic getAttribute and hasAttribute
        self.assert_(self.kind1.hasAttribute('k1a1'))
        self.assert_(self.kind1.getAttribute('k1a1') is self.kind1Attr1)

        # add an inherited attribute, kind2 inherits from kind1
        self.kind2.addValue('superKinds', self.kind1)

        # retrieve an inherited attribute
        self.assert_(self.kind2.hasAttribute('k1a1'))
        self.assert_(self.kind2.getAttribute('k1a1') is not None)

    def testIsAlias(self):
        """ A kind is not an alias """
        self.assert_(not self.kind1.isAlias())
    
    def testIsKindOf(self):
        """ Test IsKindOf on multiple super kinds """
        # make kind2 a subkind of kind1
        self.kind2.addValue('superKinds', self.kind1)
        self.assert_(self.kind2.isKindOf(self.itemKind))
        self.assert_(self.kind2.isKindOf(self.kind1))

    def testToXML(self):
        """ Non realistic test of toXML """

        out = StringIO()
        generator = XMLPrettyGenerator(XMLGenerator(out))
        itemWriter = XMLItemWriter(generator)
        generator.startDocument()
        itemWriter.writeItem(self.kind, self.kind.getVersion())
        generator.endDocument()
        xml = out.getvalue()
        out.close()

        self.failIf(xml is None)
        
    def testRekinding(self):
        # rekind an item
        
        view = self.view
        item = self.kind2.newItem('item', view)
        item.k2a2 = 'foo'
        self.assert_(item.k2a2 == 'foo')
        self.assert_(item.getAttributeAspect('k1a1', 'cardinality') == 'list')

        item.itsKind = self.kind1
        self.assert_(not item.hasLocalAttributeValue('k2a2'))
        self.assert_(item.getAttributeAspect('k1a1', 'cardinality') == 'list')


if __name__ == "__main__":
#    import hotshot
#    profiler = hotshot.Profile('/tmp/TestItems.hotshot')
#    profiler.run('unittest.main()')
#    profiler.close()
    unittest.main()
        

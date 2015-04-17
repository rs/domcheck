# -*- coding: utf-8 -*-

import unittest
from domcheck.strategies import search_meta_tag


class TestMetaSearch(unittest.TestCase):
    def test_basic(self):
        self.assertTrue(search_meta_tag('<meta name="foo" content="bar"></head>', 'foo', 'bar'))

    def test_xhtml(self):
        self.assertTrue(search_meta_tag('<meta name="foo" content="bar"/></head>', 'foo', 'bar'))

    def test_multispaces(self):
        self.assertTrue(search_meta_tag('<meta name="foo"  content="bar"   /></head>', 'foo', 'bar'))

    def test_singlequote(self):
        self.assertTrue(search_meta_tag('<meta name=\'foo\' content=\'bar\'></head>', 'foo', 'bar'))

    def test_inverted_attrs(self):
        self.assertTrue(search_meta_tag('<meta content="bar" name="foo"></head>', 'foo', 'bar'))
        self.assertTrue(search_meta_tag('<meta content=\'bar\' name=\'foo\'></head>', 'foo', 'bar'))

    def test_out_of_head(self):
        self.assertFalse(search_meta_tag('</head><meta content=\'bar\' name=\'foo\'>', 'foo', 'bar'))
        self.assertFalse(search_meta_tag('</head><meta content=\'bar\' name=\'lol\'>', 'foo', 'bar'))

    def test_non_matching_quotes(self):
        self.assertFalse(search_meta_tag('<meta name="foo\' content="bar"></head>', 'foo', 'bar'))
        self.assertFalse(search_meta_tag('<meta name="foo" content=\'bar"></head>', 'foo', 'bar'))
        self.assertFalse(search_meta_tag('<meta content="bar\' content="foo"></head>', 'foo', 'bar'))
        self.assertFalse(search_meta_tag('<meta content="bar" content=\'foo"></head>', 'foo', 'bar'))

if __name__ == '__main__':
    unittest.main()

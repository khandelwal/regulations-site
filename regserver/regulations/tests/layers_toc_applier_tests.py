from unittest import TestCase

from regulations.generator.layers.toc_applier import *


class TableOfContentsLayerTest(TestCase):

    def test_section(self):
        toc = TableOfContentsLayer(None)
        el = {}
        toc.section(el, {'index': ['1']})
        self.assertEqual({}, el)

        toc.section(el, {'index': ['1', '2', '3']})
        self.assertEqual({}, el)

        toc.section(el, {'index': ['1', 'B']})
        self.assertEqual({}, el)

        toc.section(el, {'index': ['1', 'Interpretations']})
        self.assertEqual({}, el)

        toc.section(el, {'index': ['1', '2'], 'title': '1.2 - Awesome'})
        self.assertEqual(el, {
            'is_section': True,
            'section_id': '1-2',
            'label': '1.2',
            'sub_label': 'Awesome'
        })

        toc.section(el, {'index': ['2', '1'], 'title': '2.1Sauce'})
        self.assertEqual(el, {
            'is_section': True,
            'section_id': '2-1',
            'label': '2.1',
            'sub_label': 'Sauce'
        })

    def test_appendix_supplement(self):
        toc = TableOfContentsLayer(None)
        el = {}
        toc.appendix_supplement(el, {'index': ['1']})
        self.assertEqual({}, el)

        toc.appendix_supplement(el, {'index': ['1', '2', '3']})
        self.assertEqual({}, el)

        toc.appendix_supplement(el, {'index': ['1', 'B', '3']})
        self.assertEqual({}, el)

        toc.appendix_supplement(el, {'index': ['1', 'Interpretations', '3']})
        self.assertEqual({}, el)

        toc.appendix_supplement(el, {
            'index': ['1', 'B'],
            'title': 'Appendix B - Bologna'})
        self.assertEqual(el, {
            'is_appendix': True,
            'label': 'Appendix B',
            'sub_label': 'Bologna',
            'section_id': '1-B'
        })

        el = {}
        toc.appendix_supplement(el, {
            'index': ['1', 'Interp'],
            'title': 'Supplement I to 8787 - I am Iron Man'})
        self.assertEqual(el, {
            'is_supplement': True,
            'label': 'Supplement I to 8787',
            'sub_label': 'I am Iron Man',
            'section_id': '1-Interp'
        })

    def test_apply_layer_url(self):
        toc = TableOfContentsLayer({'100': [
            {'title': '100.1 Intro', 'index': ['100', '1']}]})

        result = toc.apply_layer('100')
        self.assertEqual('#100-1', result[1][0]['url'])

        toc.sectional = True
        toc.version = 'verver'
        result = toc.apply_layer('100')
        self.assertEqual('/regulation/100-1/verver#100-1', result[1][0]['url'])

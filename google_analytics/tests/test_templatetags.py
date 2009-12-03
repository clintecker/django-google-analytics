from django.test import TestCase
from django import template

from django.contrib.sites.models import Site

from google_analytics.templatetags import analytics 

class ParserTest(TestCase):

    def setUp(self):
        self.parser = "unused"
        #################################
        # Pathological case - Do not test
        #self.token_null = template.Token(template.TOKEN_BLOCK, "")
        #################################

        self.token_noarg = template.Token(template.TOKEN_BLOCK, "test")
        self.token_onearg = template.Token(template.TOKEN_BLOCK, "test 'UA-888888-1'")
        self.token_twoarg = template.Token(template.TOKEN_BLOCK, "test 'UA-888888-1' 'UA-999999-2'")
        self.site = Site.objects.get_current()

    def test_setup(self):
        self.assert_(True)

    def test_basic_return(self):
        node = analytics.do_get_analytics(self.parser, self.token_noarg)
        self.assertTrue(isinstance(node, template.Node))

    def _test_null_node_template(self):
        node = analytics.do_get_analytics(self.parser, self.token_null)
        self.assertEqual(node.template_name, 'google_analytics/_template.html')

    def test_noarg_node_template(self):
        node = analytics.do_get_analytics(self.parser, self.token_noarg)
        self.assertEqual(node.template_name, 'google_analytics/test_template.html')
    
    def test_onearg_node_template(self):
        node = analytics.do_get_analytics(self.parser, self.token_onearg)
        self.assertEqual(node.template_name, 'google_analytics/test_template.html')
    
    def test_twoarg_node_exception(self):
        self.assertRaises(template.TemplateSyntaxError, analytics.do_get_analytics, self.parser, self.token_twoarg)

    def test_noarg_site(self):
        """If no access code is provided, the site will be set to the currently active site"""
        node = analytics.do_get_analytics(self.parser, self.token_noarg)
        self.assertEqual(node.site, self.site)

    def test_onearg_site(self):
        """If an access code is provided, the site will not be set"""
        node = analytics.do_get_analytics(self.parser, self.token_onearg)
        self.assertEqual(node.site, None)

class NodeTest(TestCase):
    def setUp(self):
        self.node_noarg = analytics.AnalyticsNode()
        self.node_code = analytics.AnalyticsNode(code='UA-999999-1')
        self.node_explicit_template = analytics.AnalyticsNode(code='UA-999999-1', template_name='google_analytics/test_template.html')
        self.node_site = analytics.AnalyticsNode(site=None, template_name='google_analytics/test_template.html')
        self.node_code_and_site = analytics.AnalyticsNode(site=None, code='UA-999999-1', template_name='google_analytics/test_template.html')

    def test_default_template_name(self):
        self.assertEqual(self.node_noarg.template_name, 'google_analytics/analytics_template.html')

    def test_explicit_template_name(self):
        self.assertEqual(self.node_explicit_template.template_name, 'google_analytics/test_template.html')
        
    def test_noarg_code_name(self):
        self.assertEqual(self.node_noarg.code, None)

    def test_explicit_code_name(self):
        self.assertEqual(self.node_code.code, 'UA-999999-1')

    def _pending_test_site_code_name(self):
        """This test needs more set-up, not yet implented"""

    def _pending_test_explicit_code_overrides_site(self):
        """This test needs more set-up, not yet implented"""
       

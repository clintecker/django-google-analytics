from django.test import TestCase

from django import template
from django.contrib.sites.models import Site
from google_analytics.models import Analytics
from google_analytics.templatetags import analytics 

code7 = 'UA-777777-3' # for fixture-based codes
code9 = 'UA-999999-1' # for explicit codes

class ParserTest(TestCase):
    """Test parsing of template tokens"""

    fixtures = ['analytics_test']

    def setUp(self):
        self.parser = "unused"
        #################################
        # Pathological case - Do not test
        #self.token_null = template.Token(template.TOKEN_BLOCK, "")
        #################################

        self.token_noarg = template.Token(template.TOKEN_BLOCK, "test")
        self.token_onearg = template.Token(template.TOKEN_BLOCK, "test '%s'" % code9)
        self.token_twoarg = template.Token(template.TOKEN_BLOCK, "test '%s' '%s'" % (code9, code7))
        self.site = Site.objects.get_current()

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
    """Test set-up and rendering of AnalyticsNodes"""

    fixtures = ['analytics_test']
    
    def setUp(self):
        self.site = Site.objects.get_current()
        self.node_noarg = analytics.AnalyticsNode()
        self.node_code = analytics.AnalyticsNode(code=code9)
        self.node_explicit_template = analytics.AnalyticsNode(code=code9, template_name='google_analytics/test_template.html')
        self.node_site = analytics.AnalyticsNode(site=self.site, template_name='google_analytics/test_template.html')
        self.node_code_and_site = analytics.AnalyticsNode(site=self.site, code=code9, template_name='google_analytics/test_template.html')

    def test_fixture(self):
        """Fixtures have been loaded"""
        self.assertNotEqual(Analytics.objects.count(), 0)

    def test_default_template_name(self):
        self.assertEqual(
                self.node_code.template_name, 
                'google_analytics/analytics_template.html'
        )

    def test_explicit_code_name(self):
        self.assertEqual(self.node_code.code, code9)
        self.assertTrue(code9 in self.node_code.render(template.Context()))

    def test_noarg_code_name(self):
        """If the node is constructed with no code and no site, it will return
        an empty string"""
        self.assertEqual(self.node_noarg.code, None)
        self.assertEqual(self.node_noarg.render(template.Context()), "")

    def test_explicit_template_name(self):
        self.assertEqual(
                self.node_explicit_template.template_name, 
                'google_analytics/test_template.html'
        )
        self.assertEqual(
                self.node_explicit_template.render(template.Context()).strip(),
                'Tracking code: %s' % code9 
        )

    def test_defined_site(self):
        self.assertEqual(self.node_site.site, self.site)
        self.assertEqual(self.node_site.code, None)
        self.assertEqual(
                self.node_site.render(template.Context()).strip(),
                'Tracking code: %s' % code7
        )

    def test_site_overrides_explicit_code(self):
        """If both code and site are set, the site code will override the 
        explicitly set code.  This is contrary to how the tag works, but
        the parser never passes this combination of arguments."""

        self.assertEqual(self.node_code_and_site.code, code9)
        self.assertEqual(self.node_code_and_site.site, self.site)
        self.assertEqual(
                self.node_code_and_site.render(template.Context()).strip(),
                'Tracking code: %s' % code7 
        )
    
       

Google Analytics for Django Projects
====================================

I manage a lot of Django projects that present slightly-different forms to 
users depending on the site/domain they're visiting.  There's also a bunch of 
custom submission code that differs from form to form, but that's neither here
nor there.

I need different Google Analytics codes depending on the sites and after 
sticking these tags into every single template, I thought it would be cool to 
be able to manage these Google analytics accounts from the Django admin page. 
I also added a mode of operation that excludes the admin interface altogether 
(you can just use the template tag)


## Two modes of operation ##

### Administering and associating codes with Django `Sites` framework ###

1. Add the `google_analytics` application to your `INSTALLED_APPS` section of your `settings.py`.  This mode requires that you be using the Django sites framework too, so make sure you have that set up as well.
2. Add `GOOGLE_ANALYTICS_MODEL = True` to your `settings.py` 
3. Run a `./manage.py syncdb` to add the database tables
4. Go to your project's admin page (usually `/admin/`) and click into a site objects
5. You'll now see a new field under the normal site information called "Analytics Code". In this box you put your unique analytics code for your project's domain.  It looks like `UA-xxxxxx-x` and save the site.
6. In your base template (usually a `base.html`) insert this tag at the very top: `{% load analytics %}`
7. In the same template, insert the following code right before the closing body tag: `{% analytics %}`

### Just using the template tag ###


1. Add the `google_analytics` application to your `INSTALLED_APPS` section of your `settings.py`.
2. In your base template, usually a `base.html`, insert this tag at the very top: `{% load analytics %}`
3. In the same template, insert the following code right before the closing body tag: `{% analytics "UA-xxxxxx-x" %}` the `UA-xxxxxx-x` is a unique Google Analytics code for you domain when you sign up for a new account.


## Asynchronous Tracking ##

Google's recent asynchronous tracking API is also supported, as of v0.2.  To use it,
simply call the templatetag `{% analytics_async %}` in the document head instead
of calling `{% analytics %}` just before the end of the body.  You can also use
`{% analytics_async "UA-xxxxxx-x" %}` as with the old templatetags.

This is being added as an option rather than a replacement for two reasons:

1. Google recommends the Asynchronous Tracking snippet goes in the <head> tag, while
   the old snippet goes at the end of the <body> tag, so as not to disrupt page loading.
   Therefore it is not a drop in replacement in your template
2. The new snippet is reported to [break sites that have a comment before the head tag](http://www.stevesouders.com/blog/2009/12/01/google-analytics-goes-async/#comment-1171). 
   Adding the asynchronous tracking to existing code would cause backwards 
   incompatiblity.

## Tracking Page-Load Time ##

Google has added [page-load tracking](http://www.google.com/support/analyticshelp/bin/answer.py?hl=en&answer=1205784&topic=1120718).
To use this feature add the following to your settings file:

    GOOGLE_ANALYTICS_TRACK_PAGE_LOAD_TIME = True

## Supporting other tracking methods ##

Sometimes, the built-in code snippets are not sufficient for what you want to
do with Google Analytics.  You might need to use different access methods,
or to support more complex Google Analytics functionality.  Fortunately, using 
different code snippets is dead easy, and there are two ways to do it.


### Overriding the analytics template ###

The easiest way is to override the `'google_analytics/analytics_template.html'`
template in a template directory that gets loaded before the one in the 
`google_analytics` app.  


### Registering a new analytics tag ###

You may want to keep the existing snippets around, while adding a new method.
Perhaps some of your pages need one snippet, but other pages need a different
one.  In this case all you have to do is register a new tag in your tag 
library using `do_get_analytics` like so:

    from django import template
    from google_analytics.templatetags import analytics

    register = template.Library()
    register.tag('my_analytics', analytics.do_get_analytics)
    
Then create a template at `'google_analytics/%(tag_name)s_template.html'`. 
In this case the template name would be 
`'google_analytics/my_analytics_template.html'`.  Pass the variable 
`{{ analytics_code }}` to the template wherever you need it.

The new tag will have all the same properties as the default tag, supporting
site-based analytics codes, as well as explicitly defined codes.

The best way to do this is to create a tiny app just for this purpose, so 
you don't have to modify the code in `google_analytics`.  Just put the above
code in `[app_name]/templatetags/[tag_library_name].py`.  Then put your 
template in `[app_name]/templates/google_analytics/[template_name]`.  If your 
app is named `my_analytics_app`, your tag library is named `more_analytics`,
and your tag is registered as `my_analytics`, the resulting app will have a 
directory structure like this:

    my_analytics_app/
    +-- templatetags/
    |   +-- __init__.py
    |   \-- more_analytics.py
    \-- templates/
         \-- google_analytics/
             \-- my_analytics_template.html
         
Finally, add `'my_analytics_app'` to `INSTALLED_APPS` in your `settings.py` file.  Your new tag is 
ready to go.  To use the tag, put `{% load more_analytics %}` at the head of 
your template.  You can now access the `{% my_analytics %}` tag the same way 
you would use `{% analytics %}`.


## License ##

The MIT License

Copyright (c) 2009 Clint Ecker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

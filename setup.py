from distutils.core import setup

setup(name='google_analytics',
      version='0.2',
      description='A simple Django application to integrate Google Analytics into your projects',
      author='Clint Ecker',
      author_email='me@clintecker.com',
      url='http://github.com/clintecker/django-google-analytics/tree/master',
      packages=['google_analytics','google_analytics.templatetags',],
      package_data={'google_analytics': ['templates/google_analytics/*.html']},
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
      )

Django.SphinxCMS
================

Initial features
----------------

* Control via manage.py command line.
* Clone Sphinx repos for example from Github.
* Build pages based on Django templates.
* Publish as static files in the look and feel of the webpage.

Configuration of the document root
----------------------------------

The DOCS_ROOT and DOCS_URS settings should be in your project's `settings.py`::

    DOCS_URL = '/docs/'
    DOCS_ROOT = os.path.join(BASE_DIR, 'public', 'docs')

Then in the project's `urls.py` file::

    from django.urls import re_path
    from django.views.static import serve
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns += [
        re_path(r'^docs/(?P<path>.*)', serve, {'document_root': settings.DOCS_ROOT})
    ] + static(settings.DOCS_URL, document_root=settings.DOCS_ROOT)

License
=======

MIT

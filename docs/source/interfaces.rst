Interfaces
==========

There is a search interface open to all, an editing interface to be used by
contributors for editing and creating ISTC records and an admin interface
used by British Library staff only.

Access to the editing interface is controlled by ``istcAuthStore`` and new
users can be added by BL staff via the admin interface (create general user).
If requested they can also be added using the run script using the flag
``-adduser``

Access to the admin interface is controlled by ``istcSuperAuthStore`` and new
users can be added by BL staff via the admin interface (create Administrative
user). If requested they can also be added using the ``run.py`` script using
the flag ``-addsuperuser``

The SRU interface is turned on and has a filter in place so that private
location data is not provided. Filter is based on the Cheshire3 Transformer
``sruOutgoingTxr`` configured using XSLT ``sruOut.xsl``.

Once script controls the loading of all three databases. There are individual
flags too if you want to do them separately::

    python run.py -load



The HTML Folder - An Explanation
--------------------------------

Because of the restrictions of the BL style guide there are lots and lots of
HTML pages which make up the basic page structure.

There are two main template files:

1. baseTemplate.html
2. printTemplate.html

These contain the basic header and footer stuff (one in colour one B&W). Each
has a place holder for content and the colour one (because it is used for
everything for display on screen) also has a place holder for navigation.

All the *Nav.html files in the html folder do the navigation and breadcrumb
trail for the various different main pages.

The remainder are various menu's and other files read by the handlers to
create the pages needed.



.. ISTC documentation master file, created by
   sphinx-quickstart on Sat Jun 15 14:05:14 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ISTC's documentation!
================================

Contents:

.. toctree::
   :maxdepth: 2

   install
   search
   interfaces
   xslt
   common


Overview
--------

Database holding ISTC records and hosted on behalf of the British Library
<http://istc.bl.uk>. Our BL contact is John Goldfinch (john.goldfinch@bl.uk)

The application consists of three Cheshire3 databases. 

1. The main database (id = db_istc) holds ISTC bibliographical records in
   MARC21XML.

2. The Bibliographical database (id = db_refs) holds key value pair style
   data for short bibliographical codes used in field 510 of the MARC records
   and their full details. Not all 510 entries are the short version. Rarely
   used bibliographical references will occur in full in the MARC record and
   not appear in this database. This mainly makes display and search a little
   tricky.

3. The USA Locations database (id = db_usa) holds key value pair style data
   for USA location codes and their full details. In this case ALL USA
   location entries occur in the MARC records using the code.


Authors (of the Documentation)
------------------------------

2009-11-18
    Catherine Smith

2013-06-15
    John Harrison


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


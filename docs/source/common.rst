Common Tasks
============


Instructions For Tasks You Might Be Asked To Carry Out


Add locations from a new country to editor and display
------------------------------------------------------

1. add the data to the records (``dataCleaning/addAustrian.py`` is an example
   of how this was done for Austrian data)

2. add new field to the following indexes (``configs.d/indexes.xml``)

   #. ``idx-kwd-location``
   #. ``idx-location``
   #. ``idx-location-private``

3. add to the following xsl stylesheets
   #. ``recordDisplay.xsl`` -- copy version for another country and change
      the tag number the country name and all variables of the form v[number]
      and l[number] to the next unique number (note they are not necessarily
      numbered in the order they appear)
			-- also add to list of tags in the if statement in the first line of the 'locations' template
   #. ``istcForm.xsl`` -- Inside <div id="holdingscontainer"> add to the list of <option> tags and then later there is a choose statement with all of the location tags listed
			the new tag needs adding here and the further down there are some method calls to accesspointlist so copy an existing one
			change the tags numbers.
			Further down is the template called accesspointstring here there are two long choose statements which need the new tag 
			adding to the list.
4 - add to the following javascript files
		a - searchForm.js - add to locList array
5 - in ISTCextensions in code directory add to dictionary in LocCountriesNormalizer
6 - in dataRequest.html add to option list


Change the German Data 
----------------------

This is a fairly regular job as the German contributors have a different system which provides an export of their location data for us to upload.
It has been agreed with John Goldfinch that all future exports of this data will be supplied to us in the form found in dataCleaning/newGermanData.txt. 
The file should follow this layout exactly and should be in unicode. If not you can send it back to John Goldfinch and ask him to change it.

The script dataCleaning/changeGerman.py actually makes the changes to the data. There is one flag in the script which determines whether private data is 
to be kept or whether all German locations should be deleted. keepPrivate = True will retain any locations marked as private set to False it will delete all of
them. NB it only deletes German locations for those files which have new entries in the provided data. Before you do this make sure the editing store has been
cleared (see below).


Change the links to different catalogues from the record display
================================================================

BSB-Ink reference links are done in the python handler with the place holder being added by the xslt. This is because the URLs are not completely formulaic
so the data is taken from the 530 u field if there is data there and if not follows a formular.

Other links (GW) are done in the recordDisplay xslt.

The links from the Koninklijke Bibliotheek notes are also done in the recordDisplay xslt.


Print the full ISTC to pdf
==========================

This takes a very long time during which you must not restart apache on the machine it is running on as the XSLT needs to 
access the server to pull in the US data. The script is data_requests/printToPDF.py


Recreate USA data from files
============================

There is a script for this (dataCleaning/createUsaData.py) works on data in the format of dataCleaning/newusadata.csv.


Recreate Bibliographical data from files
========================================

There is a script for this (dataCleaning/createBiblioData.py) works on data in the format of dataCleaning/newBiblioData.txt


Clear the editing store
=======================

Sometimes they will want all the things currently in the editing store deleted. You will also want to do this before making any changes to the live data so that
things in the editing store don't overwrite your changes.

python run.py -clearEditingStore


Cengage Data Request
====================

I have sent an export sample of 20 records containing Cengage Learning Microfiche data to the BL for approval by Cengage. If John Goldfinch comes back saying 
they want to go ahead with all of the data the script is in data_requests/cengageData.py and will just need the 20 record restriction taken off and then should
be ready to go.


Other scripts that might be useful in case the same or similar requests come up again
====================================================================================

1 - bsbConcordance.py - creates a list of BSB-Ink numbers matched with their corresponding ISTC numbers.
2 - germansinglelib.py - prints out certain fields of all records which only have one German location which is not Munich ordered by location and then ISTC#

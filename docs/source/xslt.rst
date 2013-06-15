XSLT
====

Some potentially useful remarks
-------------------------------

There are a few generally useful XSL/Cheshire3 Transformers here which you
might need if you are asked to write other scripts for the ISTC.

``indentingTxr`` or ``reindent.xsl``
    properly indents the XML - useful for all writing out to file

``filterTxr`` or ``filterMarcFields.xsl``
    filters out the fields usually required when supplying data for data
    requests

``toTextTxr`` or ``toMARCTxt.xsl``
    produces MARC Aleph output as text for printing etc (``toAlephTxr`` or
    ``toAleph.xsl`` does the same but in html for screen display)

``dataTransformer`` or ``toMarcXml.xsl``
    is not used any more but was used to turn the data from Cheshire2's MARC
    record format to MARC21XML may be useful in other projects moving MARC
    records from Cheshire2 to Cheshire3 so kept for that reason only. 

``recordDisplay.xsl``
    This is a very complex XSLT because it is the basis of four different
    transformers which deal with the various methods of outputting the data
    from the search screen, the screen, email, print and save. Theoretically
    no changes will be needed to this file but at least if they are you will
    only have to make them once even if the structure is a bit complicated to
    figure out at first.

    The nasty looking text in this file is actually the set up for the RTF
    output file used for emailing and saving. The code comes from the template
    called ``outputTemplate.txt`` in the ``www/istc`` directory. This is a
    file created in RTF and then saved as text so that you can find the header
    and footer and all the stuff that formats each entry. It's not pretty but
    it does do the job. No changes should be required but if they are then
    basically you make the changes to the RTF using open office and a few
    records and then cut and paste the formatting stuff from around the data
    into the XSLT at the relevant points. Any changes at all usually mean
    copying everything back in to the XSLT even if its really minor because a
    the beginning seems always to be affected.

Bibliographical references (the full version) and USA locs are added in the
python handler code and replace place holders set up in the XSLT.

``printAll.xsl`` is similar to ``recordDisplay.xsl`` but deals with the
transformation of the record in ``reportLabDocumentFactory`` for the PDF
output options available from the admin menu. It is a much simpler file and
rather than using a placeholder for USA locations it retrieves them live from
the XSLT. 

This method was attempted for the record display on the screen but it cannot
return the document quickly enough, and results in Python errors. Here it is
necessary because the transformation has to happen in a single process without
using Python as it is actually part of a ``documentFactory``.


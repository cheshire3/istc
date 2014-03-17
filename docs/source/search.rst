Searching and Indexes
=====================

Generally straight forward there is a ZeeRex mapping.

Slight oddities with use of pass-through indexes and some which are searched
in pairs all described below.

USA locations use regular pass through indexes.

Biblical references indexes use special ISTC extension pass through indexes
because of the special structure needed for returning the data (due to spaces
in the codes). 

``norzig.posessingInstitution`` (locations) searches general locations and
the USA locations index.

``istc.referencedBy`` (bibliographical references) searches both the
abbreviations and the full references.



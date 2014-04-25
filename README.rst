ISTC
====

25th April 2014 (2014-04-25)


Description
-----------

Cheshire3 databases and applications supporting the British Library
Incunabula Short-Title Catalogue


Authors
-------

Cheshire3 Team at the `University of Liverpool`_:

* Catherine Smith
* **John Harrison** john.harrison@liv.ac.uk

(Current maintainer in **bold**)


Latest Version
--------------

Source code is under version control and available from:

http://github.com/cheshire3/istc

Development in the GitHub repository will follow (at least to begin with)
Vincent Driessen's branching model, and use `git-flow`_ to facilitate this.
For full details of the model, see:

http://nvie.com/posts/a-successful-git-branching-model/

Accordingly, the ``master`` branch is stable and contains the most recent
release of the software; development should take place in (or by creating a
new ``feature/...`` branch from) the ``develop`` branch.


Documentation
-------------

HTML documentation can be generate using the command::

    python setup.py build_sphinx


The generated HTML documentation can then be found in docs/build/html/.

All scripts intended for use by administrative users should return help when
passed the `--help` option.


Licensing
---------

Copyright © 2009-2014, the `University of Liverpool`_.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
- Neither the name of the `University of Liverpool`_ nor the names of its
  contributors may be used to endorse or promote products derived from this
  software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


.. Links
.. _Python: http://www.python.org/
.. _`University of Liverpool`: http://www.liv.ac.uk
.. _`Cheshire3`: http://cheshire3.org
.. _`Cheshire3 Information Framework`: http://cheshire3.org
.. _WSGI: http://wsgi.org
.. _`git-flow`: https://github.com/nvie/gitflow
.. _`SRU`: http://www.loc.gov/standards/sru/
.. _`OAI-PMH`: http://www.openarchives.org/pmh/
.. _`XSLT`: http://www.w3.org/TR/xslt

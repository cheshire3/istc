#
# Script:   istcLocalConfig.py
# Version:   0.1
# Description:
#            Customisable elements for ISTC
#
# Language:  Python
# Author:    Catherine Smith <catherine.smith@liv.ac.uk>
# Date:      25 June 2009
#
# Copyright: &copy; University of Liverpool 2009
#
# Version History:
# 0.01 - 13/04/2005 - JH - Basic configurable elements coded by John
#
#
# Changes to original:
# You should make a note of any changes that you make to the originally distributed file here.
# This will make it easier to remeber which fields need to be modified next time you update the software.
#
#
#

import os

from pkg_resources import Requirement, resource_filename

from istcHtmlFragments import *

# Path to Cheshire Root - i.e. where Cheshire3 was installed
try:
    cheshirePath = resource_filename(Requirement.parse('istc'), '')
except:
    # Cheshire3 not yet installed; maybe in a source distro/repo checkout
    # Assume local directory
    cheshirePath = os.path.expanduser('~/istc')

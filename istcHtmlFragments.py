#
# Script:     htmlFragments.py
# Version:    0.01
# Description:
#            HTML fragments used by Cheshire for Archives
#
# Language:  Python
# Author:    John Harrison <john.harrison@liv.ac.uk>
# Date:      3 January 2007
#
# Copyright: &copy; University of Liverpool 2005-2007
#
# Version History:
# 0.01 - 03/01/2006 - JH - HTML Fragments migrated from localConfig.py
#
# NB:
# - If you are not experieced in editing HTML you are advised not to edit any of the HTML fragments
# - Modifying placeholder words (block caps enclosed in '%' e.g. %TITLE%) WILL SERIOUSLY affect the functionality of the system.
#
# Changes to original:
# You should make a note of any changes that you make to the originally distributed file here.
# This will make it easier to remeber which fields need to be modified next time you update the software.
#
#
#
#


new_user_template = u'''
<config type="user" id="%USERNAME%">
  <objectType>user.SimpleUser</objectType>
  <username>%USERNAME%</username>
  <flags>
    <flag>
      <object>recordStore</object>
      <value>c3r:administrator</value>     
    </flag>

    <flag>
      <object>istcAuthStore</object>
        <value>info:srw/operation/2/retrieve</value>     
    </flag>
    <flag>
      <object>istcAuthStore</object>
        <value>info:srw/operation/1/replace</value>     
    </flag>
  </flags>
</config>'''

new_superuser_template = u'''
<config type="user" id="%USERNAME%">
  <objectType>user.SimpleUser</objectType>
  <username>%USERNAME%</username>
  <flags>
    <flag>
      <object/>
      <value>c3r:administrator</value>
    </flag>
  </flags>
</config>'''




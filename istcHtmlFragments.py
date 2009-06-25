# Just the user templates for creating users.

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




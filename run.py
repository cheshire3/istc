#!/home/cheshire/install/bin/python -i
# -*- coding: iso-8859-1 -*-

import time, sys, os
sys.path.insert(1,'/home/cheshire/cheshire3/code')

import cheshire3

from cheshire3.web import www_utils
from cheshire3.web.www_utils import *
from cheshire3.baseObjects import Session
from cheshire3.server import SimpleServer
from cheshire3.document import StringDocument

import getpass
from crypt import crypt


cheshirePath = "/home/cheshire"

# Build environment...
session = Session()
serv = SimpleServer(session, cheshirePath + "/cheshire3/configs/serverConfig.xml")
session.database = 'db_istc'
db = serv.get_object(session, 'db_istc')
lgr = db.get_path(session, 'defaultLogger')
parser = db.get_object(session, 'LxmlParser')


if '-refs' in sys.argv or '-load' in sys.argv:
    session.database = 'db_refs'
    db = serv.get_object(session, 'db_refs')
    defpath = db.get_path(session, "defaultPath")
    df = db.get_object(session, 'refsDocumentFactory')
    
    start = time.time()
    # build necessary objects
    flow = db.get_object(session, 'refsBuildIndexWorkflow')
    df.load(session)
    lgr.log_info(session, 'Loading references...' )

    flow.process(session, df)
    (mins, secs) = divmod(time.time() - start, 60)
    (hours, mins) = divmod(mins, 60)
    lgr.log_info(session, 'Loading, Indexing complete (%dh %dm %ds)' % (hours, mins, secs))



if '-usa' in sys.argv or '-load' in sys.argv:
    
    session.database = 'db_usa'
    db = serv.get_object(session, 'db_usa')
    defpath = db.get_path(session, "defaultPath")
    df = db.get_object(session, 'usaDocumentFactory')
    
    start = time.time()
    # build necessary objects
    flow = db.get_object(session, 'usaBuildIndexWorkflow')
    df.load(session)
    lgr.log_info(session, 'Loading usa locations...' )

    flow.process(session, df)
    (mins, secs) = divmod(time.time() - start, 60)
    (hours, mins) = divmod(mins, 60)
    lgr.log_info(session, 'Loading, Indexing complete (%dh %dm %ds)' % (hours, mins, secs))



if '-records' in sys.argv or '-load' in sys.argv:
    session.database = 'db_istc'
    db = serv.get_object(session, 'db_istc')
    defpath = db.get_path(session, "defaultPath")
    
    start = time.time()
    # build necessary objects
    flow = db.get_object(session, 'buildIndexWorkflow')
    baseDocFac = db.get_object(session, 'istcDocumentFactory')
    baseDocFac.load(session, defpath + "/data/", codec='utf-8')
    lgr.log_info(session, 'Loading files from %s...' % (baseDocFac.dataPath))
    try:
        flow.process(session, baseDocFac)
    except:
        raise
    (mins, secs) = divmod(time.time() - start, 60)
    (hours, mins) = divmod(mins, 60)
    lgr.log_info(session, 'Loading, Indexing complete (%dh %dm %ds)' % (hours, mins, secs))






if ('-adduser' in sys.argv):
    session.database = 'db_istc'
    db = serv.get_object(session, 'db_istc')
    authStore = db.get_object(session, 'istcAuthStore')
    
    un = raw_input('Please enter a username: ')
    if not un: inputError('You must enter a username for this user.')
    pw = getpass.getpass('Please enter a password for this user: ')
    if not (pw and len(pw)): inputError('You must enter a password for this user.')
    pw2 = getpass.getpass('Please re-enter the password to confirm: ')
    if pw != pw2: inputError('The two passwords submitted did not match. Please try again.')
    rn = raw_input('Real name of this user (not mandatory): ')
    addy = raw_input('Email address for this user (not mandatory): ')
    xml = read_file('xsl/admin.xml').replace('%USERNAME%', un)
    for k,v in {'%password%': crypt(pw, pw[:2]), '%realName%': rn, '%email%': addy}.iteritems():
        if v and len(v):
            xml = xml.replace(k, '\n  <%s>%s</%s>' % (k[1:-1],v,k[1:-1]))
        else:
            xml = xml.replace(k, '')
    doc = StringDocument(xml)
    rec = parser.process_document(session, doc)
    id = rec.process_xpath(session, '/config/@id')[0]
    rec.id = id
    authStore.store_record(session, rec)
    authStore.commit_storing(session)
    try:
        user = authStore.fetch_object(session, id)
    except c3errors.FileDoesNotExistException:
        print 'ERROR: User not successfully created. Please try again.'
    else:
        print 'OK: Username and passwords set for this user'
    #print user
    sys.exit()  
    
if ('-addsuperuser' in sys.argv):
    session.database = 'db_istc'
    db = serv.get_object(session, 'db_istc')
    superAuthStore = db.get_object(session, 'istcSuperAuthStore')
    
    un = raw_input('Please enter a username: ')
    if not un: inputError('You must enter a username for this user.')
    pw = getpass.getpass('Please enter a password for this user: ')
    if not (pw and len(pw)): inputError('You must enter a password for this user.')
    pw2 = getpass.getpass('Please re-enter the password to confirm: ')
    if pw != pw2: inputError('The two passwords submitted did not match. Please try again.')
    rn = raw_input('Real name of this user (not mandatory): ')
    addy = raw_input('Email address for this user (not mandatory): ')
    xml = read_file('xsl/admin.xml').replace('%USERNAME%', un)
    for k,v in {'%password%': crypt(pw, pw[:2]), '%realName%': rn, '%email%': addy}.iteritems():
        if v and len(v):
            xml = xml.replace(k, '\n  <%s>%s</%s>' % (k[1:-1],v,k[1:-1]))
        else:
            xml = xml.replace(k, '')
    doc = StringDocument(xml)
    rec = parser.process_document(session, doc)
    id = rec.process_xpath(session, '/config/@id')[0]
    rec.id = id
    superAuthStore.store_record(session, rec)
    superAuthStore.commit_storing(session)
    try:
        user = superAuthStore.fetch_object(session, id)
    except c3errors.FileDoesNotExistException:
        print 'ERROR: User not successfully created. Please try again.'
    else:
        print 'OK: Username and passwords set for this user'
    #print user
    sys.exit()  
       







        

        

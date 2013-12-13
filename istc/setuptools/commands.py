"""Setuptools command sub-classes."""
from __future__ import with_statement

import os
import re
import sys
import shutil
import inspect

from os.path import expanduser, abspath, dirname, join, exists
from pkg_resources import normalize_path

from setuptools import Command
from setuptools.command import develop as _develop
from setuptools.command import install as _install

from cheshire3.exceptions import ConfigFileException
from cheshire3.internal import cheshire3Home, cheshire3Root
from cheshire3.server import SimpleServer
from cheshire3.session import Session

from istc.setuptools.exceptions import *


class unavailable_command(Command):
    """Sub-class commands that we don't want to make available."""

    description = "Command is not appropriate for this package"
    user_options = []
    boolean_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        raise NotImplementedError(self.description)


class c3_command(Command):
    """Base Class for custom commands."""

    user_options = [
    ]

    def initialize_options(self):
        self.with_httpd = None

    def finalize_options(self):
        if self.with_httpd is not None:
            self.with_httpd = normalize_path(expanduser(self.with_httpd))

    def apply_config_templates(self):
        """Read config template(s), make subs, write config file(s)."""
        global distropath

        def apply_config_tmpl(path):
            "Subroutine to turn templates into configs"
            global distropath
            # Read in template
            with open(path + '.tmpl', 'r') as fh:
                config = fh.read()
            # Make replacements
            config = re.sub('type="defaultPath">~/istc/(.*?)</',
                            r'type="defaultPath">{0}/\1</'.format(distropath),
                            config
                            )
            # Write finished config file
            with open(path, 'w') as fh:
                fh.write(config)

        # ISTC Database
        apply_config_tmpl(join(distropath,
                               'dbs',
                               'istc',
                               'config.xml')
                          )
        # Refs Database
        apply_config_tmpl(join(distropath,
                               'dbs',
                               'istc',
                               'configRefs.xml')
                          )
        # USA Database
        apply_config_tmpl(join(distropath,
                               'dbs',
                               'istc',
                               'configUsa.xml')
                          )


class develop(_develop.develop, c3_command):

    user_options = _develop.develop.user_options + c3_command.user_options

    def initialize_options(self):
        _develop.develop.initialize_options(self)
        c3_command.initialize_options(self)

    def finalize_options(self):
        _develop.develop.finalize_options(self)
        c3_command.finalize_options(self)

    def install_for_development(self):
        global distropath, server, session
        # Carry out normal procedure
        _develop.develop.install_for_development(self)
        # Use config templates to generate configs
        self.apply_config_templates()
        # Tell the server to register the config file
        try:
            server.register_databaseConfigFile(session, join(distropath,
                                                             'dbs',
                                                             'istc',
                                                             'config.xml'))
        except ConfigFileException as e:
            if e.reason.startswith("Database with id 'db_istc' is already "
                                   "registered."):
                # Existing install / development install
                raise DevelopException("Package is already installed. To "
                                       "install in 'develop' mode you must "
                                       "first run the 'uninstall' command.")
        else:
            server.register_databaseConfigFile(session, join(distropath,
                                                             'dbs',
                                                             'istc',
                                                             'configRefs.xml'))
            server.register_databaseConfigFile(session, join(distropath,
                                                             'dbs',
                                                             'istc',
                                                             'configUsa.xml'))

    def uninstall_link(self):
        global server, session
        # Carry out normal procedure
        _develop.develop.uninstall_link(self)
        # Unregister the database by deleting
        # Cheshire3 database config plugin
        serverDefaultPath = server.get_path(session,
                                            'defaultPath',
                                            cheshire3Root)
        userSpecificPath = join(expanduser('~'), '.cheshire3-server')
        pluginPath = os.path.join('configs', 'databases', 'db_istc.xml')
        if exists(join(serverDefaultPath, pluginPath)):
            os.remove(join(serverDefaultPath, pluginPath))
            os.remove(join(serverDefaultPath,
                           'configs',
                           'databases',
                           'db_refs.xml'))
            os.remove(join(serverDefaultPath,
                           'configs',
                           'databases',
                           'db_usa.xml'))
        elif exists(os.path.join(userSpecificPath, pluginPath)):
            os.remove(os.path.join(userSpecificPath, pluginPath))
            os.remove(join(userSpecificPath,
                           'configs',
                           'databases',
                           'db_refs.xml'))
            os.remove(join(userSpecificPath,
                           'configs',
                           'databases',
                           'db_usa.xml'))
        else:
            server.log_error(session, "No database plugin file")


class install(_install.install, c3_command):

    user_options = _install.install.user_options + c3_command.user_options

    def initialize_options(self):
        _install.install.initialize_options(self)
        c3_command.initialize_options(self)

    def finalize_options(self):
        _install.install.finalize_options(self)
        c3_command.finalize_options(self)

    def run(self):
        # Carry out normal procedure
        _install.install.run(self)
        # Use config templates to generate configs
        self.apply_config_templates()
        # Install Cheshire3 database config plugin
        # Tell the server to register the config file
        try:
            server.register_databaseConfigFile(session, join(distropath,
                                                             'dbs',
                                                             'istc',
                                                             'config.xml'))
        except ConfigFileException as e:
            if e.reason.startswith("Database with id 'db_istc' is already "
                                   "registered."):
                # Existing install / development install
                raise InstallException("Package is already installed. To "
                                       "install you must first run the "
                                       "'uninstall' command.")
        else:
            server.register_databaseConfigFile(session, join(distropath,
                                                             'dbs',
                                                             'istc',
                                                             'configRefs.xml'))
            server.register_databaseConfigFile(session, join(distropath,
                                                             'dbs',
                                                             'istc',
                                                             'configUsa.xml'))


class upgrade(_install.install, c3_command):
    # Extremely experimental and untested...

    user_options = _install.install.user_options + c3_command.user_options

    def initialize_options(self):
        _install.install.initialize_options(self)
        c3_command.initialize_options(self)

    def finalize_options(self):
        _install.install.finalize_options(self)
        c3_command.finalize_options(self)

    def run(self):
        # Carry out normal procedure
        _install.install.run(self)
        # Use config templates to generate configs
        self.apply_config_templates()
        # Upgrade database directory
        subpath = join('cheshire3',
                       'dbs',
                       'istc')
        shutil.copytree(join(distropath, 'dbs', 'istc'),
                        join(cheshire3Home, subpath),
                        symlinks=False,
                        ignore=shutil.ignore_patterns(".git*",
                                                      "*.pyc",
                                                      "PyZ3950_parsetab.py*",
                                                      "*.bdb",
                                                      "*.log")
                        )
        # Upgrade to web app directory
        subpath = join('cheshire3',
                       'www',
                       'istc'
                       )
        shutil.copytree(join(distropath, 'www'),
                        join(cheshire3Home, subpath),
                        symlinks=False,
                        ignore=shutil.ignore_patterns(".git*",
                                                      "*.pyc",
                                                      "PyZ3950_parsetab.py*",
                                                      "*.bdb",
                                                      "*.log"
                                                      )
                        )


class uninstall(c3_command):

    description = "Uninstall Cheshire3 for ISTC"

    def run(self):
        if self.with_httpd is not None:
            # Uninstall Apache HTTPD mods
            self.uninstall_apache_mods()
        # Unregister the database by deleting
        # Cheshire3 database config plugin
        serverDefaultPath = server.get_path(session,
                                            'defaultPath',
                                            cheshire3Root)
        userSpecificPath = join(expanduser('~'), '.cheshire3-server')
        pluginPath = os.path.join('configs', 'databases', 'db_istc.xml')
        if exists(join(serverDefaultPath, pluginPath)):
            os.remove(join(serverDefaultPath, pluginPath))
            os.remove(join(serverDefaultPath,
                           'configs',
                           'databases',
                           'db_refs.xml'))
            os.remove(join(serverDefaultPath,
                           'configs',
                           'databases',
                           'db_usa.xml'))
        elif exists(os.path.join(userSpecificPath, pluginPath)):
            os.remove(os.path.join(userSpecificPath, pluginPath))
            os.remove(join(userSpecificPath,
                           'configs',
                           'databases',
                           'db_refs.xml'))
            os.remove(join(userSpecificPath,
                           'configs',
                           'databases',
                           'db_usa.xml'))
        else:
            server.log_error(session, "No database plugin file")


# Inspect to find current path
modpath = inspect.getfile(inspect.currentframe())
moddir = dirname(modpath)
distropath = abspath(join(moddir, '..', '..'))
serverConfig = os.path.join(cheshire3Root,
                            'configs',
                            'serverConfig.xml')
session = Session()
server = SimpleServer(session, serverConfig)

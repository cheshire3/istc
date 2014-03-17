Install
=======


Cheshire3 Packages Required
---------------------------

The application needs ``base``, ``web``, ``sql`` and ``formats`` packages
from Cheshire3 as well as this ``istc`` package which contains a few
extensions and specialist normalizers etc. It also needs True Type Fonts
installed on the server in order for the pdf output options in the admin
menu to work (instructions for installing TTF on linux are below).


Installing TTF on Linux
-----------------------

For Fedora 9 or later which no longer have the rpm for chkfontpath used by the
straight sourceforge download:

http://corefonts.sourceforge.net/msttcorefonts-2.0-1.spec

The version here has removed the need for that file.

As the user who installed Cheshire3 and will run the ISTC::

    $ wget http://pfrields.fedorapeople.org/packages/SPECS/msttcorefonts-2.0-1.1.spec
    $ rpmbuild -bb msttcorefonts-2.0-1.1.spec 

    $ sudo rpm -ivh /home/cheshire/rpmbuild/RPMS/noarch/msttcorefonts-2.0-1.1.noarch.rpm


At the second stage you may need to install ``cabextract`` and ``ttmkfdir``::

    sudo yum install cabextract
    sudo yum install ttmkfdir


Monthly CRON Job On The Server
------------------------------

The CRON job is programmed to run using ``crontab`` to run once a month and
the script itself is here::

    /home/cheshire/copyISTClogs.sh


This copies the log files for the previous month to the BritLib user for the
BL webteam to download and also backs up the data to a network storage device.


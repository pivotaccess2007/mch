**Edit a file, create a new file, and clone from Bitbucket in under 2 minutes**

When you're done, you can delete the content in this README and update the file with details for others getting started with your repository.

*We recommend that you open this README in another tab as you perform the tasks below. You can [watch our video](https://youtu.be/0ocf7u76WSo) for a full demo of all the steps in this tutorial. Open the video in a new tab to avoid leaving Bitbucket.*

---

## Edit a file

You’ll start by editing this README file to learn how to edit a file in Bitbucket.

1. Click **Source** on the left side.
2. Click the README.md link from the list of files.
3. Click the **Edit** button.
4. Delete the following text: *Delete this line to make a change to the README from Bitbucket.*
5. After making your change, click **Commit** and then **Commit** again in the dialog. The commit page will open and you’ll see the change you just made.
6. Go back to the **Source** page.

---

## Create a file

Next, you’ll add a new file to this repository.

1. Click the **New file** button at the top of the **Source** page.
2. Give the file a filename of **contributors.txt**.
3. Enter your name in the empty file space.
4. Click **Commit** and then **Commit** again in the dialog.
5. Go back to the **Source** page.

Before you move on, go ahead and explore the repository. You've already seen the **Source** page, but check out the **Commits**, **Branches**, and **Settings** pages.

---

## Clone a repository

Use these steps to clone from SourceTree, our client for using the repository command-line free. Cloning allows you to work on your files locally. If you don't yet have SourceTree, [download and install first](https://www.sourcetreeapp.com/). If you prefer to clone from the command line, see [Clone a repository](https://confluence.atlassian.com/x/4whODQ).

1. You’ll see the clone button under the **Source** heading. Click that button.
2. Now click **Check out in SourceTree**. You may need to create a SourceTree account or log in.
3. When you see the **Clone New** dialog in SourceTree, update the destination path and name if you’d like to and then click **Clone**.
4. Open the directory you just created to see your repository’s files.

Now that you're more familiar with your Bitbucket repository, go ahead and add a new file locally. You can [push your change back to Bitbucket with SourceTree](https://confluence.atlassian.com/x/iqyBMg), or you can [add, commit,](https://confluence.atlassian.com/x/8QhODQ) and [push from the command line](https://confluence.atlassian.com/x/NQ0zDQ).



INSTALLATION:
====================
NOTE
=====
 $ : means normal user 
 # : means superuser
============================
DEPENDENCIES
============
The system has been so far tested within the following environment
==================================================================
UBUNTU 16.04 ... both server and desktop version
Python 2.7.12
Virtualenv 15.1.0
====================================================================

INSTALL
==========
PIP
====
Reference
==========
https://pip.pypa.io/en/stable/
====================================================
$ sudo apt-get install python-pip
$ sudo pip install -U pip


FIX ERROR: 
======================
$ sudo dpkg-reconfigure locales

choose "all locales", and then the default locale to "en_US.UTF-8" 

VIRTUALENV
============
Reference
==========
https://virtualenv.pypa.io/en/stable/
====================================================

$ sudo pip install virtualenv


CREATE COUNTRY BASE DEPENDENCIES - RWANDA ENVIRONMENT
======================================================
# virtualenv rwanda
# cd rwanda 
# source bin/activate
(rwanda) root@RapidSMS:/livemas/mch/rwanda# mkdir mch
(rwanda) root@RapidSMS:/livemas/mch/rwanda# cd mch/
(rwanda) root@RapidSMS:/livemas/mch/rwanda/mch# ls
(rwanda) root@RapidSMS:/livemas/mch/rwanda/mch# mkdir src
(rwanda) root@RapidSMS:/livemas/mch/rwanda/mch# cd src/
(rwanda) root@RapidSMS:/livemas/mch/rwanda/mch/src# mkdir com
(rwanda) root@RapidSMS:/livemas/mch/rwanda/mch/src# cd com/
(rwanda) root@RapidSMS:/livemas/mch/rwanda/mch/src/com# mkdir rwanda
(rwanda) root@RapidSMS:/livemas/mch/rwanda/mch/src/com# cd rwanda/
(rwanda) root@RapidSMS:/livemas/mch/rwanda/mch/src/com/rwanda# mkdir mch
(rwanda) root@RapidSMS:/livemas/mch/rwanda/mch/src/com/rwanda# cd mch/
(rwanda) root@RapidSMS:/livemas/mch/rwanda/mch/src/com/rwanda/mch# 

(rwanda) root@RapidSMS:/livemas/mch/rwanda/mch# mkdir requirements
(rwanda) root@RapidSMS:/livemas/mch/rwanda/mch# pip install -r requirements/base.txt

=========================================================================
FIX psycopg (Error: You need to install postgresql-server-dev-X.Y for building a server-side extension or libpq-dev for building a client-side application.)
======================
$ sudo apt-get install libpq-dev

===========================================
FIX EnvironmentError: mysql_config not found
==============================================
$ sudo apt-get install libmysqlclient-dev

FIX __main__.ConfigurationError: Could not run curl-config: [Errno 2] No such file or directory
==================================================================================================
$ sudo apt-get install libcurl4-openssl-dev

RMQ:
===============================================================================================================================================
Installing collected packages: cherrypy, nose, django-nose, psycopg2, markupsafe, Jinja2, zope.interface, twisted, Django, djtables, djappsettings, RapidSMS, MySQL-python, unicodecsv, xlrd, xlwt, six, hl7, pycurl, python-dateutil, django-piston, django-admin-flexselect, xlsxwriter
Successfully installed Django-1.4.2 Jinja2-2.7.2 MySQL-python-1.2.3 RapidSMS-0.10.0 cherrypy-3.5.0 django-admin-flexselect-0.4.1 django-nose-1.4.3 django-piston-0.2.3 djappsettings-0.4.0 djtables-0.1.2 hl7-0.3.3 markupsafe-1.0 nose-1.3.7 psycopg2-2.5.3 pycurl-7.43.0 python-dateutil-2.5.3 six-1.11.0 twisted-14.0.2 unicodecsv-0.9.4 xlrd-0.9.0 xlsxwriter-0.8.6 xlwt-0.7.4 zope.interface-4.4.3

===============================================================================================================================================
TO LIST DIRECTORIES
=====================
$ sudo apt-get install tree
===================================================================================================
$ tree -a
$ tree -d

===============================

DELETE TABLE WITH FOREIGN KEYS
===============================

This might be useful to someone ending up here from a search. Make sure you're trying to drop a table and not a view.

SET foreign_key_checks = 0;
-- Drop tables
drop table ...
-- Drop views
drop view ...
SET foreign_key_checks = 1;

SET foreign_key_checks = 0 is to set foreign key checks to off and then SET foreign_key_checks = 1 is to set foreign key checks back on. While the checks are off the tables can be dropped, the checks are then turned back on to keep the integrity of the table structure.

==============================================================================================================================================



CHW LOGIN
=============
A CHW is uniquely identified by hi national_id
A CHW cannot be assigned a telephone being owned by another one in the system, and who is still active from that connected telephone number
Hence national is not updated from frontend, and when updating by assigning a telephone currently active, means you are deativating the existing user with that same number.


INDEX
===========
e.g:
CREATE INDEX CONCURRENTLY nid_pre_index ON pregnancy (national_id, lmp);

CREATE INDEX CONCURRENTLY nid_bir_index ON birth (national_id, child_number, birth_date);

CREATE INDEX CONCURRENTLY nid_cbn_index ON nutrition (national_id, child_number, birth_date);

CREATE INDEX CONCURRENTLY nid_dth_index ON death (national_id);

CREATE INDEX CONCURRENTLY nid_red_index ON redalert (national_id);

CREATE INDEX CONCURRENTLY nid_rar_index ON redresult (national_id);

CREATE INDEX CONCURRENTLY nid_anc_index ON ancvisit (national_id);

CREATE INDEX CONCURRENTLY nid_risk_index ON risk (national_id);

CREATE INDEX CONCURRENTLY nid_pnc_index ON pncvisit (national_id);

CREATE INDEX CONCURRENTLY nid_nbc_index ON nbcvisit (child_pk);

DROP INDEX nid_index;

The use of index should be used carefully to improve performance.

=======================
WSGI installation
========================
1. Install LAMP

2. Run the following command

sudo apt-get install libapache2-mod-wsgi


=================
KANNEL
============================
1. Install
sudo apt-get install kannel

2. Configure 
=======================================

Celery
==================
To increase performance of SMS:
===================================
1. Install RabbitMQ
=============================

sudo apt-get install rabbitmq-server

2. Install and configure celery
================================

pip install celery==3.1.23
pip install django-celery==3.0.0


Read docs on how to setup celery and RabbitMQ



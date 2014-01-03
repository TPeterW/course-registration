course-registration
===================

A script that can automate course registration within some Bannerweb-based systems.  Based on that of Middlebury College.

Usage
-----

Configure the hardcoded values (date of registration, term to register for, and CRNs to register for) within course-registration.py and then run the script.  Note that you may need to install a few Python libraries if you don't already have them installed -- this script depends on getpass, mechanize, time, datetime, and BeautifulSoup.
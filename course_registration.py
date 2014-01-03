"""
course_registration.py

Prompts the user for a Middlebury College BannerWeb 
ID number and PIN, accesses the Registration section,
and interfaces with it to select the desired term and
submit all desired CRNs at 7AM on the desired date.

Created by Daniel Trauner on 2013-11-09.
Copyright (c) 2013 Daniel Trauner. All rights reserved.
"""

from getpass import getpass
import mechanize as m
import time as t
from datetime import datetime, timedelta
from BeautifulSoup import BeautifulSoup


# begin helper methods

def term_to_termcode(term):
	"""
	Translates a human-readable term i.e. "Fall 2010"
	into the "termcode" parameter that the Middlebury 
	Course Catalog database URL uses.
	"""
	normalized_term = term.strip().lower()
	season, year = normalized_term.split(' ')[0], normalized_term.split(' ')[1]
	
	if season == 'winter' or season == 'jterm' or season == 'j-term':
		season = '1'
	elif season == 'spring':
		season = '2'
	elif season == 'summer':
		season = '6'
	elif season == 'fall':
		season = '9'
	else:
		season = 'UNKNOWN'
		print 'Error in determining the season of the given term!'

	if 'practice' in normalized_term:
		season += '3'
	else:
		season += '0'
	
	return year + season

def wait_until_7am(date):
	"""
	When called, delays the script until 7AM on the
	given date (day of registration) where date is a
	string of the form "MM/DD/YYYY".
	"""
	# get current time and user's supplied date
	now = datetime.now()
	user_date = datetime.strptime(date, '%m/%d/%Y')

	registration = now.replace(year=user_date.year, month=user_date.month, day=user_date.day, hour=7, minute=0, second=0, microsecond=0)

	time_diff = registration - now

	while registration > now:
		now = datetime.now()
		time_diff = registration - now
		if registration > now:
			remaining = datetime(1,1,1) + time_diff if time_diff else datetime(0,0,0)
			print chr(27) + "[2J"
			print("%02d:%02d:%02d:%02d until registration (%s @ 7AM)..." % (remaining.day - 1, remaining.hour, remaining.minute, remaining.second, date))
			if time_diff < timedelta(seconds=10):
				t.sleep(0.001)
			else:
				t.sleep(1)

def check_bw_credentials(user_id, user_pin):
	"""
	Checks whether or not the given user_id and
	user_pin are valid credentials for the
	Middlebury College BannerWeb system.
	"""
	print '\nValidating credentials...\n'
	br = m.Browser()
	br.open('https://ssb.middlebury.edu/PNTR/twbkwbis.P_WWWLogin?')

	br.select_form('loginform')
	uid = br.form.find_control('sid')
	pin = br.form.find_control('PIN')

	uid.value = user_id
	pin.value = user_pin

	response = br.submit()

	valid = False if br.geturl() == 'https://ssb.middlebury.edu/PNTR/twbkwbis.P_ValLogin' else True

	print chr(27) + "[2J"

	return valid

def register(user_id, user_pin, term_code, crn_list):
	"""
	Logs in using the account with id num user_id_num and
	pin user_pin into Middlebury College's Bannerweb, 
	navigates to the course registration page for the
	given term_code, and enters and submits the CRNs
	in crn_list.
	"""
	print '\nOpening BannerWeb with a Mechanize browser...\n'
	br = m.Browser()
	br.open('https://ssb.middlebury.edu/PNTR/twbkwbis.P_WWWLogin?')

	br.select_form('loginform')
	uid = br.form.find_control('sid')
	pin = br.form.find_control('PIN')

	uid.value = user_id
	pin.value = user_pin

	print chr(27) + "[2J"
	print 'Logging into BannerWeb...\n'
	br.submit()
	
	br.open(br.find_link(text='Student Records & Registration').url)
	br.open(br.find_link(text='Registration').url)
	br.open(br.find_link(text='Register or Add/Drop Classes').url)

	br.form = list(br.forms())[1]
	term = br.form.find_control('term_in')
	term.value = [term_code]

	br.submit()

	print chr(27) + "[2J"
	print 'Entering in CRNs...\n'
	br.form = list(br.forms())[1]

	crn_fields = []
	for control in br.form.controls:
		if control.name == 'CRN_IN':
			crn_fields.append(control)

	all_crn_fields = crn_fields[1:]

	for i, field in enumerate(all_crn_fields):
		if i < len(crn_list):
			try:
				field.value = crn_list[i]
			except AttributeError:
				print 'Already registered for ' + crn_list[i] + '!'

	response = br.submit()

	print chr(27) + "[2J"
	soup = BeautifulSoup(response.read())

	print 'Succeeded in registering for the following courses:'
	print '-'*51
	successful_table = soup.findAll("table", {"class" : "datadisplaytable"})[0]
	successful_courses = [e.text for e in successful_table.findAll("td", {"class" : "dddefault"})]

	i = 3
	while i < len(successful_courses):
		print successful_courses[i], successful_courses[i+1], successful_courses[i+6]
		i += 10


	if soup.findAll("span", {"class" : "errortext"}):
		print '\nFailed to register for the following courses:'
		print '-'*45
		failed_table = soup.findAll("table", {"class" : "datadisplaytable"})[1]
		failed_courses = [e.text for e in failed_table.findAll("td", {"class" : "dddefault"})]

		i = 0
		while i < len(failed_courses):
			print failed_courses[i+2], failed_courses[i+3], failed_courses[i+8], '(' + failed_courses[i] + ')'
			i += 9

	print

	return len(successful_courses)/10

# begin main method

def main():
	#################################
	##### BEGIN CONFIG SECTION! #####
	#################################

	date_string = '01/01/1970' # date of registration
	term_string = 'Spring 1970' # term you're registering for
	crn_list = ['12345', '67890'] # list of CRNs to register for

	#################################
	#####  END CONFIG SECTION!  #####
	#################################
	
	# get user's info from them and login to bannerweb with it
	user_id = raw_input('Enter your Student ID Number: ')
	user_pin = getpass('Enter your Bannerweb PIN: ')

	while not check_bw_credentials(user_id, user_pin):
		print chr(27) + "[2J"
		print '\nInvalid BannerWeb ID or password.  Try again.\n'
		user_id = raw_input('Enter your Student ID Number: ')
		user_pin = getpass('Enter your Bannerweb PIN: ')

	# wait until 7AM on the specified registration day
	wait_until_7am(date_string)

	# continually try to register until at least one successful attempt has occurred
	registered_courses = 0
	i = 1
	while not registered_courses:
		# submit each crn in crn_list
		try:
			registered_courses = register(user_id, user_pin, term_to_termcode(term_string), crn_list)
		except:
			t.sleep(1) # don't look TOO robotic...
			i += 1
			print chr(27) + "[2J"
			print 'Something is wrong with BannerWeb!  Trying again (attempt #' + str(i) + ')...'

	print 'Registered for', registered_courses, 'courses in', i, 'attempt(s)!\n'

	print """
               __:.__
Calvin    |   (_:..'"=
  and     |    |:/ o o\         AHAH!
   Hobbes |    ;'-'   (_)     Spaceman Spiff      .
              '-._  ;-'        wins again !  _'._|\/:
              /:;  ;                .         '- '   /_
             /.; ; ;,                \__     _/,    "_<
            |;|..| ;|                       '._____  _)
            |.|.'| ||                     _ ___  _/ /
            |.|..| :/                    =uu\___`;--|
            \;|..|:':       _               _ _ ||_\|
         .. _||__|:\_\.''..' ) ___________ ( )_)||_||
   :....::''::/  |::;:|''| "/ /_=_=_=_=_=/ :_[__'_\3_)
    ''''      '-''-'-'.__)-'
		  """
	
if __name__ == "__main__":
	main()
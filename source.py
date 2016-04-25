# -*- coding: utf-8 -*-
"""
Modified on Mon Apr 25 2016

@modifier: Tao Peter Wang https://github.com/TPeterW
Based on:
@author: Daniel Trauner https://github.com/danielhtrauner

To register through bannerweb for Middlebury College
"""

from getpass import getpass
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import mechanize as m
import time, os, re, ConfigParser
from sys import exit

def main():    
    date_string = None              # date of registration
    term_string = None              # target_term
    time_string = '0700'            # 7am
    crn_list = []   # list of CRNs
    
    login_data = handle_login()
    uid =  login_data['sid']
    pin = login_data['PIN']
    
    # what a stupid name
    # get date and CRNs from user
    reg_data = handle_registration()
    date_string = reg_data['date']
    crn_string = reg_data['CRNs']
    term_string = reg_data['term']
    alt_pin = reg_data['apin']
    
    # find all crns
    crn_list = re.findall(re.compile(r'[0-9]{5}'), crn_string)
    
    print('''
      ___  _ _                                _ 
     / _ \| | |                              | |
    / /_\ \ | | ___  _ __  ___ ______ _   _  | |
    |  _  | | |/ _ \| '_ \/ __|______| | | | | |
    | | | | | | (_) | | | \__ \      | |_| | |_|
    \_| |_/_|_|\___/|_| |_|___/       \__, | (_)
                                       __/ |    
                                      |___/        
    ''')
    
    wait_until_time(date_string)
    
    # continually try to register until at least one successful has occurred
    registered_courses = 0
    attempt = 0
    
    while not registered_courses:
        # submit each crn in crn_list
        try:
            registered_courses = register(uid, pin, term_to_termcode(term_string), crn_list, alt_pin)
        except KeyboardInterrupt as e:
            print('\nBye!')
            exit(1)
        except Exception as e:
            try:
                time.sleep(1)   # don't look too robotic
                attempt += 1
                print('Something is wrong with Bannerweb! Trying again (attempt #' + str(i) + ')...')
            except KeyboardInterrupt:
                print('\nBye!')
                exit(1)
            except:
                pass
    
    print('Registered for ' + str(registered_courses) + ' courses in ' + str(attempt) + ' attempt(s)!\n')
    
    # for Windows only
    # raw_input('Press any key to exit...')
    
def handle_login():
    cfg = ConfigParser.ConfigParser()
    cfg.read('reg.ini')
    uid = None
    pin = None
    
    # configuration exists
    if os.path.isfile('reg.ini') and cfg.has_section('User'):
        cache_choice = raw_input('There are records of %s, do you want to load from this record? (y/n/d): ' % cfg.get('User', 'sid'))
        while not cache_choice.startswith('y') and not cache_choice.startswith('n') and not cache_choice.startswith('d') and not len(cache_choice) == 0:
            cache_choice = raw_input('Please indicate whether you want to load from saved record (y/n/d): ')
        
        if cache_choice.startswith('y') or len(cache_choice) == 0:
            print('\nCredentials Loaded\n')
            return {'sid':cfg.get('User', 'sid'), 'PIN':cfg.get('User', 'PIN')}
        if cache_choice.startswith('d'):
            print('\nCredentials Deleted\n')
            cfg.remove_section('User')
            if cfg.has_section('Reg'):
                cfg.remove_section('Reg')           # also part of user configuration
            temp = open('reg.ini', 'w')
            cfg.write(temp)
            temp.close()
        
    # either no configuration exists or user doesn't want to load this records
    uid = raw_input('Enter your 8-digit Student ID number: ')
    pin = getpass('Enter your Bannerweb PIN: ')
    
    try:
        while not check_bw_credentials(uid, pin):
            print('\nInvalid credentials. Please try again.\n')
            uid = raw_input('Enter your 8-digit Student ID number: ')
            pin = getpass('Enter your Bannerweb PIN: ')
    except KeyboardInterrupt as e:
        print(e.message)
        print('\nBye!')
        exit(1)
    except:
        print('Encountered error, because: ' + e.message)
        exit(1)
    
    # sid and pin both check out
    print('Credentials correct\n')
    iniFile = open('reg.ini', 'w')
    
    if not cfg.has_section('User'):         # first use
        cfg.add_section('User') 
    cfg.set('User', 'sid', uid)
    cfg.set('User', 'PIN', pin)
    cfg.write(iniFile)
    iniFile.close()
    
    return {'sid':uid, 'PIN':pin}


def handle_registration():
    cfg = ConfigParser.ConfigParser()
    cfg.read('reg.ini')
    
    if cfg.has_section('Reg'):
        date_string = cfg.get('Reg', 'date')
        cache_choice = raw_input('There is plan for registration on %s, do you want to continue with this plan? (y/n/d): ' % date_string)
        
        if cache_choice.startswith('y') or len(cache_choice) == 0:
            return {'date': date_string, 'CRNs':cfg.get('Reg', 'CRNs'), 'term':cfg.get('Reg', 'term'), 'apin':cfg.get('Reg', 'apin')}
        if cache_choice.startswith('d'):
            cfg.remove_section('Reg')
    
    # ask for date
    date_string = raw_input('Enter the correct date of your registration in the following format:\nMM/DD/YYYY\n')
    
    while not re.match(r'[0-9]{2}/[0-9]{2}/[0-9]{4}', date_string):
        date_string = raw_input('Please enter in the correct format:\nMM/DD/YYYY\n')
    
    # now ask user for CRNs
    crn_string = ''
    
    crn = raw_input('Please enter your course CRNs ONE BY ONE (q to quit): ')
    while not crn.startswith('q'):
        if re.match(r'[0-9]{5}$', crn):
            crn_string += crn + '\n'
            crn = raw_input('Please enter next one (q to quit): ')
        else:
            print('!!!')
            print('!!!')
            crn = raw_input('Please enter 5 digits (q to quit): ')

    # ask user for semester
    term_string = raw_input('\nPlease enter semester (eg. "Fall 2016"): ')
    while not re.match(r'spring|fall|autumn|summer|winter\s[0-9]{4}[\s*]', term_string.lower()):
        term_string = raw_input('Please enter in the correct format: ')
        
    # ask user for alternate pin
    alt_pin = raw_input('\nPlease enter your alternate PIN (press Enter if N/A): ')
    while not re.match(r'[0-9]{4}', alt_pin):
        if len(alt_pin) == 0:
            alt_pin = ''
            break
        else:
            alt_pin = raw_input('Please enter in the correct format: ')
    
    print('Registration saved\n')
    iniFile = open('reg.ini', 'wb')
    
    if not cfg.has_section('Reg'):
        cfg.add_section('Reg')
    cfg.set('Reg', 'date', date_string)
    cfg.set('Reg', 'CRNs', crn_string)
    cfg.set('Reg', 'term', term_string)
    cfg.set('Reg', 'apin', alt_pin)
    cfg.write(iniFile)
    iniFile.close()
    
    return {'date': date_string, 'CRNs': crn_string, 'term': term_string, 'apin': alt_pin}
        
          
def register(user_id, user_pin, term_code, crn_list, alt_pin):
    '''
    Log in again using uid and pin
    navigates to course registration page and submits
    '''
    print('\nOpening BannerWeb with emulated browser...\n')
    
    br = m.Browser()
    # br.set_debug_http(True)
    br.open('https://ssb.middlebury.edu/PNTR/twbkwbis.P_WWWLogin?')
    
    br.select_form('loginform')
    uid = br.form.find_control('sid')
    pin = br.form.find_control('PIN')
    
    uid.value = user_id
    pin.value = user_pin
    br.submit()
    
    br.open(br.find_link(text='Student Records & Registration').url)
    br.open(br.find_link(text='Registration').url)
    br.open(br.find_link(text='Register or Add/Drop Classes').url)
    
    # check whether alt_pin is ''
    if len(alt_pin) > 0:
        br.select_form(nr = 1)
        apin = br.form.find_control('pin')
        apin.value = alt_pin
        br.submit()
    else:
        print('No alternate pin found.')
    
    
    # now at term selection page
    br.form = list(br.forms())[1]       # find all input fields
    term = br.form.find_control('term_in')
    term.value = [term_code]
    br.submit()
    
    # now at registration page
    print('Registering according to CRNs')
    br.form = list(br.forms())[1]
    
    crn_fields = []
    for control in br.form.controls:
		if control.name == 'CRN_IN':
			crn_fields.append(control)
    
    all_crn_fields = crn_fields[1:]         # excluding the first one?
    
    # fill in the crns
    for i, field in enumerate(all_crn_fields):
        if i < len(crn_list):
            try:
                field.value = crn_list[i]
            except AttributeError:
                print('Cannot register for ' + crn_list[i] + '!')
    
    print       # empty line
    response = br.submit()
    
    soup = BeautifulSoup(response.read(), 'html.parser')
    
    print('You are currenly registered for these courses:')
    print('-'*51)
    successful_table = soup.find_all('table', {'class':'datadisplaytable'})[0]
    successful_courses = [e.text for e in successful_table.find_all('td', {'class':'dddefault'})]
    
    i = 3
    while i < len(successful_courses):
        print(successful_courses[i] + successful_courses[i + 1] + successful_courses[i + 6])
        i += 10
    
    if soup.find_all('span', {'class':'errortext'}):
        print('\nFailed to register for the following courses: ')
        print('-'*45)
        failed_table = soup.find_all("table", {"class" : "datadisplaytable"})[1]
        failed_courses = [e.text for e in failed_table.find_all("td", {"class" : "dddefault"})]
        
        i = 0
        while i < len(failed_courses):
            print(failed_courses[i + 2], failed_courses[i + 3], failed_courses[i + 8], '(' + failed_courses[i] + ')')
            i += 9
    
    print
    
    return len(successful_courses)/10


def wait_until_time(reg_date):
    '''
	When called, delays the script until 7AM on the
	given date (day of registration) where date is a
	string of the form "MM/DD/YYYY".
	'''
    # get current time and user supplied date
    now = datetime.now()
    user_date = datetime.strptime(reg_date, '%m/%d/%Y')
    
    registration = now.replace(
        year=user_date.year, 
        month=user_date.month, 
        day=user_date.day, 
        hour=7, 
        minute=0, 
        second=0, 
        microsecond=0)
    
    time_diff = registration - now
    
    while registration > now:
        now = datetime.now()
        time_diff = registration - now
        if registration > now:
            remaining = datetime(1,1,1) + time_diff if time_diff else datetime(0,0,0)
            print("%02d:%02d:%02d:%02d until registration (%s @ 7AM)..." % (
                        remaining.day - 1, 
                        remaining.hour, 
                        remaining.minute, 
                        remaining.second, 
                        reg_date))
            # remove the following 3 lines for Windows
            CURSOR_UP_ONE = '\x1b[1A'
            ERASE_LINE = '\x1b[2K'
            print(CURSOR_UP_ONE + CURSOR_UP_ONE + ERASE_LINE)
            try:
                if time_diff < timedelta(seconds=10):
                    time.sleep(0.001)
                else:
                    time.sleep(1)
            except KeyboardInterrupt:
                print('\nBye!\n')
                exit(1)


def term_to_termcode(term):
    '''
    Translates a human-readable term i.e. "Fall 2010"
	into the "termcode" parameter that the Middlebury 
	Course Catalog database URL uses.
    '''
    normalised_term = term.strip().lower()
    season = normalised_term.split(' ')[0]
    year = normalised_term.split(' ')[1]
      
    if season == 'winter' or season == 'jterm' or season == 'j-term':
        season = '1'
    elif season == 'spring':
        season = '2'
    elif season == 'summer':
        season = '6'
    elif season == 'fall' or season == 'autumn':
        season = '9'
    else:
        season = 'UNKNOWN'
        print('Couldn\'t determine season of the given term')
        
    if 'practice' in normalised_term:
        # practice round
        season += '3'
    else:
        # this is waaaaarrrrr
        season += '0'
    
    return year + season 
    

def check_bw_credentials(user_id, user_pin):
    '''
    checks validity of given uid and pin
    for Middlebury College Bannerweb system
    '''
    print ('\nValidating credentials...\n')
    br = m.Browser()
    # br.set_debug_http(True)
    br.open('https://ssb.middlebury.edu/PNTR/twbkwbis.P_WWWLogin?')
    
    br.select_form('loginform')
    uid = br.form.find_control('sid')
    pin = br.form.find_control('PIN')
    
    uid.value = user_id
    pin.value = user_pin
    
    response = br.submit()
    
    return br.geturl() != 'https://ssb.middlebury.edu/PNTR/twbkwbis.P_ValLogin'




if __name__ == "__main__":
	main()
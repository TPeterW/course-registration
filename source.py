#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import mechanicalsoup
from getpass import getpass

u_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5'

def main():
	sid = input('Please input your 8 digit student ID: ')
	pin = getpass('Please input password: ')

	crns = []
	crn = '11111'
	while crn != '00000':
		crn = input('Add crn of one course you want to register (00000 to finish adding): ')
		crns.append(crn)

	print(crns)
	return

	cookies = firstStep(sid, pin)

	lastStep(crns, cookies)

	return

def firstStep(sid, pin):
	session = requests.Session()
	resp = session.get('https://ssb-prod.ec.middlebury.edu/PNTR/twbkwbis.P_WWWLogin?')

	cookies = resp.cookies

	url = "https://ssb-prod.ec.middlebury.edu/PNTR/twbkwbis.P_ValLogin"

	payload = 'sid=' + sid + '&PIN=' + pin
	headers = {
		# 'cookie': cookie,
		'origin': "https://ssb-prod.ec.middlebury.edu",
		'accept-encoding': "gzip, deflate, br",
		'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
		'upgrade-insecure-requests': "1",
		'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3255.0 Safari/537.36",
		'content-type': "application/x-www-form-urlencoded",
		'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		'cache-control': "no-cache",
		'referer': "https://ssb-prod.ec.middlebury.edu/PNTR/twbkwbis.P_WWWLogin?",
		'connection': "keep-alive",
		'save-data': "on",
		'postman-token': "3e18124e-d775-573b-4c01-8eb77baf2f91"
		}

	resp = requests.request("POST", url, data=payload, headers=headers, cookies=cookies)

	with open('index.html', 'w') as outputfile:
		outputfile.write(resp.text)

	return resp.cookies

def lastStep(crns, cookies):
	rl = "https://ssb-prod.ec.middlebury.edu/PNTR/bwckcoms.P_Regs"

	payload = "term_in=201823&RSTS_IN=DUMMY&assoc_term_in=DUMMY&CRN_IN=DUMMY&start_date_in=DUMMY&end_date_in=DUMMY&SUBJ=DUMMY&CRSE=DUMMY&SEC=DUMMY&LEVL=DUMMY&CRED=DUMMY&GMOD=DUMMY&TITLE=DUMMY&MESG=DUMMY&REG_BTN=DUMMY&REG_BTN=Submit%2BChanges&regs_row=0&wait_row=0&add_row=10"

	headers = {
		# 'cookie': cookie,
		'origin': "https://ssb-prod.ec.middlebury.edu",
		'accept-encoding': "gzip, deflate, br",
		'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
		'upgrade-insecure-requests': "1",
		'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3260.0 Safari/537.36",
		'content-type': "application/x-www-form-urlencoded",
		'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		'cache-control': "no-cache",
		'referer': "https://ssb-prod.ec.middlebury.edu/PNTR/bwskfreg.P_AltPin",
		'connection': "keep-alive",
		'save-data': "on",
		'postman-token': "7c257d83-2f02-a8e6-20d2-f15c18a616d1"
	}

	for crn in crns:
		payload = 'term_in=201823&RSTS_IN=DUMMY&RSTS_IN=RW&assoc_term_in=DUMMY&assoc_term_in=&CRN_IN=DUMMY&CRN_IN=' + str(crn) + '&start_date_in=DUMMY&start_date_in=&end_date_in=DUMMY&end_date_in=&SUBJ=DUMMY&CRSE=DUMMY&SEC=DUMMY&LEVL=DUMMY&CRED=DUMMY&GMOD=DUMMY&TITLE=DUMMY&MESG=DUMMY&REG_BTN=DUMMY&REG_BTN=Submit%2BChanges&regs_row=0&wait_row=0&add_row=10'
		resp = requests.request("POST", url, data=payload, headers=headers, cookies=cookies)
		print(str(resp) + ' for %s' % str(crn))

	with open('register.html', 'w') as outputfile:
		outputfile.write(resp.text)

if __name__ == '__main__':
	main()

def unused():
	br = mechanicalsoup.StatefulBrowser(user_agent=u_agent)
	page = br.get('https://ssb-prod.ec.middlebury.edu/PNTR/twbkwbis.P_WWWLogin?')

	data = {'sid': sid, 'PIN': pin}
	resp = br.post('https://ssb-prod.ec.middlebury.edu/PNTR/twbkwbis.P_ValLogin', data)

	# menu before selecting terms
	resp = br.open('https://ssb-prod.ec.middlebury.edu/PNTR/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu')

	for link in br.links():
		if link.text == 'Register or Add/Drop Classes':
			resp = br.follow_link(link)
    
	# choose term
	# data = {'term_in': '201820'}
	# data = {'term_in': '201823'}
	# resp = br.post('https://ssb-prod.ec.middlebury.edu/PNTR/bwskfreg.P_AltPin', data)

	form = br.select_form(nr=1)
	# form.set_select({'term_in': '201820'})
	form.set_select({'term_in': '201823'})
	resp = br.submit_selected()


	# register now
	# crns = [21725, 21709, 22494]
	crns = [22494]

	cookie_str = ''
	for cookie in br.get_cookiejar():
		cookie_str += cookie.name + '=' + cookie.value + '; '

	lastStep(crns, cookie_str)

	with open('index.html', 'w') as outputfile:
		outputfile.write(resp.content.decode("utf-8"))

	br.close()

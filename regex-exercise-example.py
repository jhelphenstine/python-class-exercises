#! /usr/bin/env python


import re

#regex_file = '/root/regex-matchables.txt'
regex_file = 'regex-matchables.txt'


def IPaddress_regex(filename):
	IPaddress_pattern = re.compile("(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])")
	txtfile = open(filename, 'r')
	matches = IPaddress_pattern.findall(txtfile.read())
	txtfile.close()
	print(matches)
	return matches
	
IPaddress_regex(regex_file)


def Email_regex(filename):
	email_pattern = re.compile("\S+@\S+\.[a-zA-Z]{2,5}")
	txtfile = open(filename, 'r')
	matches = email_pattern.findall(txtfile.read())
	txtfile.close()
	print(matches)
	return matches

Email_regex(regex_file)


def Phone_regex(filename):
	phone_pattern = re.compile("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})")
	txtfile = open(filename, 'r')
	matches = phone_pattern.findall(txtfile.read())
	txtfile.close()
	print(matches)
	return matches

Phone_regex(regex_file)

	

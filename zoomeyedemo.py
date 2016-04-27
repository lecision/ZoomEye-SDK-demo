# coding: utf-8
# author: lecision
# datetime: 20160426
# 查询开放特定端口主机的ip地址以及所在位置
import os
import requests
import json

access_token = ''
ip_list = []
def login():
		user = raw_input('[-] input : username:')
		passwd = raw_input('[-] input : password:')
		data = {
			'username' : user,
			'password' : passwd
		}
		data_encoded = json.dumps(data)
		try:
				r = requests.post('http://api.zoomeye.org/user/login', data = data_encoded)
				r_decoded = json.loads(r.text)
				global access_token
				access_token = r_decoded['access_token']
		except Exception, e:
				print e
				print '[-] info : username or password is wrong, please try again'
				exit()

def saveStrToFile(file,str):
		with open(file,'w') as output:
				output.write(str)

def saveListToFile(file,list):
		s = '\n'.join(list)
		with open(file,'w') as output:
				output.write(s)

def apiTest():
		page = 1
		global access_token
		with open('access_token.txt','r') as input:
				access_token = input.read()
		port = raw_input('[-] input : port:')
		headers = {
						'Authorization' : 'JWT '  +  access_token
				}
		while(True):
				try:
						r = requests.get('http://api.zoomeye.org/host/search?query="port:'+ str(port) + '"&facet=app,os&page=' + str(page), 
										headers = headers)
						r_decoded = json.loads(r.text)
						for x in r_decoded['matches']:
								y = x['geoinfo']
								z = y['city']
								w = z['names']
								q = w['en']
								match = 'ip:' + x['ip'] + '     ' + 'city:' + q
								ip_list.append(match)
						print '[-] info : count' + str(page * 10)
				except Exception, e:
						if str(e.message) == 'matches':
								print '[-] info : account was break, excceeding the max limitations'
								break
						else:
								print '[-] info : ' + str(e.message)
				else:
						if page == 10:
								break
						page += 1
def zoomeyedemo():
		if not os.path.isfile('access_token.txt'):
				print '[-] info: access_token file is not exit, please login'
				login()
				saveStrToFile('access_token.txt', access_token)

		apiTest()
		saveListToFile('match.txt', ip_list)


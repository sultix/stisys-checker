#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import smtplib
from email.mime.text import MIMEText 
import json
from pathlib import Path
import requests
from bs4 import BeautifulSoup as bs

class Reader:

    PATH = 'results.json'
    CONST_COURSE_CELL = 1
    CONST_DATE_CELL = 5
    CONST_VALUE_CELL = 7

    user = None
    password = None
    toEmail = None
    fromEmail = None
    emailPassword = None
    results = {}

    def __init__(self, user, password, toEmail, fromEmail, emailPassword, smtpServer):
        self.user = user
        self.password = password
        self.toEmail = toEmail
        self.fromEmail = fromEmail
        self.emailPassword = emailPassword;
        self.smtpServer = smtpServer

    def start(self):
        initstate = not self.read()
        session = requests.Session()
        logouturl = 'https://stisys.haw-hamburg.de/logout.do'
        response = session.get(logouturl)
        print('logged out')

        loginurl = 'https://stisys.haw-hamburg.de/login.do'
        values = {'username': self.user,
                'password': self.password}
        response = session.post(loginurl, data=values)
        print('logged in')

        dataurl = 'https://stisys.haw-hamburg.de/viewExaminationData.do'
        response = session.get(dataurl)

        soup = bs(response.content, 'html.parser')
        print(soup.title.string)
        parent = soup.find(id='ergebnisuebersicht')
        tables = parent.find_all('table', class_='tablecontent')
        for table in tables:
            #read first set of values
            rows = table.find_all('tr', class_='tablecontentbacklight')
            self.addToDictionary(rows, initstate)
            #read second set of values
            rows = table.find_all('tr', class_='tablecontentbackdark')
            self.addToDictionary(rows, initstate)
        self.save()

    def addToDictionary(self, rows, initstate):
        for row in rows:
            cells = row.find_all('td')
            course = cells[self.CONST_COURSE_CELL].text
            date = cells[self.CONST_DATE_CELL].text
            result = cells[self.CONST_VALUE_CELL].text

            if date != '' and not initstate and self.genKey(course, date) not in self.results:
                print(course + ' - ' + date + ' ' + result)
                try:
                    toaddr = [self.toEmail]
                    msg =  MIMEText(course + ' - ' + date + ' ' + result)
                    msg['From'] = self.fromEmail
                    msg['To'] = self.toEmail
                    msg['Subject'] = "New Result from Stisys"

                    print("start sending email...")
                    server = smtplib.SMTP(self.smtpServer)
                    server.starttls()
                    server.login(self.fromEmail, self.emailPassword)
                    text = msg.as_string()
                    server.sendmail(self.fromEmail, toaddr, text)   
                    server.quit  
                    print("Successfully sent email")
                except smtplib.SMTPException as e:
                    print("Error: unable to send email\n" + str(e))

            if date != '':
                self.put(self.genKey(course,date),course, date)

    def genKey(self,course, date):
        return str(course + date)

    def put(self,key, course, date):
        self.results[key] = {'course': course, 'date': date}

    def getValue(self, course):
        if course in self.results:
            return self.results[course]
        else:
            return '';

    def save(self):
            with open(self.PATH, 'w') as outfile:
                json.dump(self.results, outfile)

    def read(self):
        print("start reading..")
        result = False
        conf_file = Path(self.PATH)
        if conf_file.is_file():
            with open(self.PATH) as json_data_file:
                self.results = json.load(json_data_file)
            result = True

        return result
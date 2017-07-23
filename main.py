#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from threading import Timer
import time
import sys
import getpass
from reader import Reader

class ReaderManager:

    user = None
    password = None
    email = None
    senderPassword = None
    senderEmail = None
    smtpServer = None
    repeatAfter = 3600
    conf = None

    def __init__(self, user, password, email, senderPassword, senderEmail, smtpServer, repeatAfter):
        self.user = user
        self.password = password
        self.email = email
        self.senderPassword = senderPassword
        self.senderEmail = senderEmail
        self.repeatAfter = repeatAfter

    def timeout(self):
        print("Start Check...")
        self.startTimer(int(self.repeatAfter))
        r = Reader(self.user, self.password, self.email, 
            self.senderEmail, self.senderPassword, self.smtpServer)
        r.start()

    def startTimer(self, repeatAfter):
        t = Timer(repeatAfter, self.timeout)
        t.start()

    def run(self): 
        self.timeout()

def main():
    print('Welcome to stisys checker ;) ')
    user = input('User: ')
    password = getpass.getpass()
    
    conf = readConf()

    email =  conf["email"]
    if email == '':
        email = input('email address: ')
        conf["email"] = email

    senderEmail = conf["sender.email"]
    if senderEmail == '':
        senderEmail = input('Email address for sending of results: ')
        conf["sender.email"] = senderEmail

    print('Configuration of smtp server for [' + senderEmail + ']')
    smtpServer = conf["smtpServer"]
    if conf["smtpServer"] == '':
        smtpServer = input('smtp server address: ')
        conf["smtpServer"] = smtpServer

    #set smt passwor
    senderPassword = getpass.getpass()

    repeatAfter = conf["repeatAfter"]
    if conf["repeatAfter"] == '':
        repeatAfter = input('repeat time in sec.: ')
        conf["repeatAfter"] = repeatAfter

    saveConf(conf)

    manager = ReaderManager(user, password, email, senderPassword, senderEmail, smtpServer, repeatAfter)
    manager.run()

def readConf():
    path = 'conf.json'
    conf_file = Path(path)
    if conf_file.is_file():
        with open(path) as json_data_file:
            return json.load(json_data_file)

    return None

def saveConf(conf):
    path = 'conf.json'
    with open(path, 'w') as outfile:
        json.dump(conf, outfile)

if __name__ == "__main__":
    main()
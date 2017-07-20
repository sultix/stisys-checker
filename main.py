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
    senderPassword = None
    conf = None

    def __init__(self, user, password, senderPassword, conf):
        self.user = user
        self.password = password
        self.senderPassword = senderPassword
        self.conf = conf

    def timeout(self):
        print("Start Check...")
        self.startTimer(int(self.conf["repeatAfter"]))
        r = Reader(self.user, self.password, self.conf["email"], 
            self.conf["sender.email"], self.senderPassword, self.conf["smtpServer"])
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

    senderEmail = ''
    if conf["sender.email"] == '':
        senderEmail = input('Email address for sending of results: ')
        conf["sender.email"] = senderEmail
    else:
        senderEmail = conf["sender.email"]

    print('Configuration of smtp server for [' + senderEmail + ']')
    if conf["smtpServer"] == '':
        smtpServer = input('smtp server address: ')
        conf["smtpServer"] = smtpServer

    saveConf(conf)

    #set smt passwor
    senderPassword = getpass.getpass()

    manager = ReaderManager(user, password, senderPassword, conf)
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
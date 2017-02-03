#-------------------------------------------------------------------------------
# Name:        oprepo Installer
# Author:      Ethan
# Copyright:   (c) Ethan 2017
#-------------------------------------------------------------------------------
import os, winshell
from win32com.client import Dispatch
import requests
import getpass
import time
from datetime import datetime, timedelta, date
import json
import base64
import sys
import zipfile

def askQuestion(question, default="yes"):
    valid = {"yes": True, "y": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

def main():
    installDirectory = r'C:\OPREPO'
    print "Welcome to the OPREPO installer!"
    if (askQuestion("Are you sure you want to install?")):
        print "Starting installer",
        time.sleep(.6)
        print ".",
        time.sleep(.6)
        print ".",
        time.sleep(.6)
        print "."
        time.sleep(.6)
        if not os.path.exists(installDirectory):
            print "directory does not exist"
            print "creating new directory..."
            os.mkdir(installDirectory)
            time.sleep(1)
            print "directory created successfully"
        else:
            print "directory already exists"
        time.sleep(.6)
        print "loading data",
        time.sleep(.7)
        print ".",
        time.sleep(.4)
        print ".",
        r = requests.Session()
        resp = r.get('http://localhost:3000/downloadclient').text
        j = json.loads(resp)
        print "."
        outzipfile = "out.zip"
        with open(outzipfile, "wb") as fh:
            fh.write(base64.decodestring(j['data']))
        fh.close()
        print j["response"]
        print "extracting files..."
        zfile = zipfile.ZipFile(outzipfile)
        zfile.extractall(r"C:\OPREPO")
        zfile.close()
        print "files extracted."
        print "deleting zip file..."
        os.remove(outzipfile)
        print "zip file deleted successfully"
        time.sleep(.6)
        print "loading updates",
        time.sleep(.7)
        print ".",
        time.sleep(.4)
        print ".",
        resp = r.get('http://localhost:3000/downloadupdate').text
        j = json.loads(resp)
        print "."
        outzipfile = "out.zip"
        with open(outzipfile, "wb") as fh:
            fh.write(base64.decodestring(j['data']))
        fh.close()
        print j["response"]
        print "extracting files..."
        zfile = zipfile.ZipFile(outzipfile)
        zfile.extractall(r"C:\OPREPO")
        zfile.close()
        print "files extracted."
        print "deleting zip file..."
        os.remove(outzipfile)
        print "zip file deleted successfully"
        if(askQuestion("Would you like to create a shortcut on the desktop?")):
            desktop = winshell.desktop()
            path = os.path.join(desktop, "oprepo.lnk")
            target = r"C:\OPREPO\oprepo.exe"
            wDir = r"C:\OPREPO"
            icon = r"C:\OPREPO\icon.ico"
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = wDir
            shortcut.IconLocation = icon
            shortcut.save()
    print "install complete!"
    pass

if __name__ == '__main__':
    main()

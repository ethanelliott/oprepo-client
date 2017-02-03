#-------------------------------------------------------------------------------
# Name:        oprepo generate install package
# Author:      Ethan
# Copyright:   (c) Ethan 2017
#-------------------------------------------------------------------------------
import os
import requests
import base64
import sys
import zipfile
import json

def main():
    print "generating new file data..."
    zf = zipfile.ZipFile('installer.zip', mode='w')
    zf.write('oprepo.exe')
    zf.write('icon.ico')
    zf.close()
    zf = zipfile.ZipFile('update.zip', mode='w')
    zf.write('update.exe')
    zf.close()
    with open('installer.zip', 'rb') as fin, open('output.txt', 'w') as fout:
        base64.encode(fin, fout)
    fin.close()
    fout.close()
    os.remove('installer.zip')
    with open('update.zip', 'rb') as fin, open('update.txt', 'w') as fout:
        base64.encode(fin, fout)
    fin.close()
    fout.close()
    os.remove('update.zip')
    with open('output.txt', 'r') as fin:
        c = fin.read()
        print c
        payload={"data":c}
        r = requests.Session()
        resp = r.post("http://localhost:3000/newclientupload", data=payload).text
        j = json.loads(resp)
        print j["response"]
    fin.close()
    with open('update.txt', 'r') as fin:
        c = fin.read()
        print c
        payload={"data":c}
        r = requests.Session()
        resp = r.post("http://localhost:3000/newclientinstaller", data=payload).text
        j = json.loads(resp)
        print j["response"]
    fin.close()
    os.remove('output.txt')
    os.remove('update.txt')
    print "done."

if __name__ == '__main__':
    main()

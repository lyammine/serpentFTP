import base64
import getpass
import os
import socket
import sys
import traceback

import paramiko

def Singleton(singleClass):
    if not singleClass._instance:
        singleClass._instance = singleClass()
    return singleClass._instance

class Connection:
    
    transport= None #ssh2 connection
    sftp= None #sftp client
    hostkeytype = None
    hostkey = None
    _instance = None

    def __init__(self, hostname=None, username=None, password=None):
        self.hostname = hostname
        self.username = username
        self.password = password
        
    def setConnectionParameters(self, hostname=None, username=None, password=None):
        self.hostname = hostname
        self.username = username
        self.password = password

    def getTransport(self):
        
        if self.transport is None:
            self.transport = paramiko.Transport((self.hostname, 22))
        return self.transport
    
    def getCwd(self):
        sftp = self.getSFTP()
        if sftp.getcwd() == None:
            sftp.chdir("/")
        return sftp.getcwd()
    
    def getListDir(self):
        sftp = self.getSFTP()
        return sftp.listdir()
    
    def chDir(self, dirPath):
        sftp = self.getSFTP()
        sftp.chdir(dirPath)
        
    
    def getSFTP(self):
        if self.transport is not None and self.sftp is None:
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        return self.sftp
    
    def validate(self):
        pass
    
    def connect(self):
        
        self.validate()
        self.getTransport()
        
        if self.transport is not None:
            self.transport.connect(username=self.username, password=self.password)
          
    #send a file of name "filename"
    def send(self, filename):
        
        sftp = self.getSFTP()
        
        try:
            data = open(file, 'rb').read()
            sftp.open(file, 'wb').write(data)

        except Exception, e:
            print '*** Caught exception: %s: %s' % (e.__class__, e)
            traceback.print_exc()
            try:
                self.close()
            except:
                pass
                
    #retrieve a file of name filename
    def retrieve(self, filename):
        
        sftp = self.getSFTP()
        
        try:
            data = sftp.open(file, 'rb').read()
            open(file, 'wb').write(data)
            
        except Exception, e:
            print '*** Caught exception: %s: %s' % (e.__class__, e)
            traceback.print_exc()
            
    def close(self):
        self.transfer.close()

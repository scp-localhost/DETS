#!/usr/bin/env python
# POC: perimeterPig.py
# Bluetooth (could be wifi) learner & listener
# Build Db of 'friends'
# Log or alert exceptions
#Author: scp
#import random #always, always import random...
#https://scapy.readthedocs.io/en/latest/layers/bluetooth.html#

from scapy.all import *
#import scapy
import time
import datetime
import sys
import os
import sqlite3
cwd = os.getcwd()

class pig():
  def __init__(a_pig, name = 'Napoleon', db = cwd+ '/data/Pig_Perimeter.db'):
    a_pig.name = name
    a_pig.ds = []
    a_pig.db = db
    a_pig.pcap = False
    a_pig.mens_rea = False
    a_pig.sql = ''
 
  def bbq(this_pig):#use this to show Pig state
    print('let\'s eat ',this_pig.name)
    
def setSniffOld():
  try:
    bt = scapy.all.BluetoothHCISocket(0)
    bt.sr(HCI_Hdr()/HCI_Command_Hdr()/HCI_Cmd_LE_Set_Scan_Enable(enable=True,filter_dups=False))
    bt.sniff(timeout=600,lfilter=lambda p: HCI_LE_Meta_Advertising_Reports in p,prn=packout)
  except Exception as bork:
    print ("Sniff/Scapy error...sound of things breaking ", bork , time.strftime('%X %x %Z'),'\n','=' * 50)

def setSniff():
  try:
    bt = scapy.all.BluetoothHCISocket(0)
    bt.sr(HCI_Hdr()/HCI_Command_Hdr()/HCI_Cmd_LE_Set_Scan_Enable(enable=True,filter_dups=False))
    bt.sniff(timeout=600,prn=packout)
  except Exception as bork:
    print ("Sniff/Scapy error...sound of things breaking ", bork , time.strftime('%X %x %Z'),'\n','=' * 50)

def packout(packet):#packet.show()
  a_pig = mainPig
  a_pig.ds = packet
  grind(a_pig)
    
def grind(this_pig):#this_pig.ds.show()
  if ('Complete list of 128-bit service UUIDs' in this_pig.ds):
    this_pig.ds.show()
  try:
    if(this_pig.ds['HCI header'].type==4):
      if(this_pig.ds.haslayer('LE Meta')):#trap(this_pig)
         if(this_pig.ds['LE Meta'].event==2):trap(this_pig)
      else:
        print('Event')
        this_pig.ds.show()
    elif(this_pig.ds['HCI header'].type==1):
      print('CMD')
      this_pig.ds.show()
  except Exception as bork:
    print("????", bork)

def trap(this_pig):#this_pig.ds.show()
  ar = this_pig.ds['Advertising Reports'][0]['Advertising Report']#print(ar.addr, str(ar.rssi))
  if 'the grass is green and the sun still shines':
    try:
      if 'write to db':
          keyDT = str(datetime.datetime.now())
          initQs = ['/*drop table if exists perimeter;*/'
              ,'create table if not exists perimeter (last_seen, MAC TEXT, rssi TEXT, relate TEXT, UNIQUE(MAC,rssi,relate) ON CONFLICT REPLACE)'
              ,'INSERT INTO perimeter VALUES ("'+keyDT+'","'+ar.addr+'","'+str(ar.rssi)+'","'+this_pig.name+'")'
              ,'/*SELECT distinct MAC FROM perimeter ORDER BY last_seen";*/'
              ]
          for sql in initQs:
              this_pig.sql = sql#print(this_pig.sql)
              dbLand(this_pig)#ds = this_pig.ds
    except Exception as bork:
      print ("DB error...sound of things breaking ", bork , time.strftime('%X %x %Z'),'\n','=' * 50)

def dbLand(this_pig):#import sqlite3#https://www.sqlite.org/inmemorydb.html
    conn = sqlite3.connect(this_pig.db)#You can also supply the special name :memory: to create a database in RAM.
    c = conn.cursor()
    c.execute(this_pig.sql)
    this_pig.ds = c.fetchall()
    conn.commit()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mainPig = pig(sys.argv[1])#used for db field flag
        mainPig.bbq()
    else :
        mainPig = pig('scan'+str(datetime.datetime.now()))
        mainPig.bbq()
    setSniff()

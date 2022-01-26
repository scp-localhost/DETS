#!/usr/bin/env python
# POC: perimeterPig.py
# Bluetooth & Wifi) learner & listener
# Build Db of 'friends'
# Log or alert exceptions
#Author: scp
#import random #always, always import random...
#https://scapy.readthedocs.io/en/latest/layers/bluetooth.html#
#sudo lsusb |grep Bluetooth && hcitool dev
from scapy.all import *#import scapy
import time
import datetime
import sys
import os
import sqlite3
from threading import Thread
import re
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import pandas as pd
import urllib.parse
cwd = os.getcwd()

hostName = "localhost"
serverPort = 60080
networks = pd.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto"])
networks.set_index("BSSID", inplace=True)# set the index BSSID (MAC address)

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

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
    
        if parsed_path.query=="json":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(json.loads(networks.to_json(orient="index"))), "utf-8"))
        else:
            parsed_path = urllib.parse.urlparse(self.path)
            message = sortNetDS()#message = 'query=%s' % parsed_path.query
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>perimeterPigWifi</title></head>", "utf-8"))
            self.wfile.write(bytes("<!--<p>Request: %s</p>-->" % self.path, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>" + message + "</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
            return
    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++
def setSniffWifi():
  try:
    sniff(prn=packout, iface=interface)# start sniffing
  except Exception as bork:
    print ("Sniff/Scapy error...sound of things breaking ", bork , time.strftime('%X %x %Z'),'\n','=' * 50)
    
def setSniffOld():
  try:
    bt = scapy.all.BluetoothHCISocket(1)
    bt.sr(HCI_Hdr()/HCI_Command_Hdr()/HCI_Cmd_LE_Set_Scan_Enable(enable=True,filter_dups=False))
    bt.sniff(timeout=600,lfilter=lambda p: HCI_LE_Meta_Advertising_Reports in p,prn=packout)
  except Exception as bork:
    print ("Sniff/Scapy error...sound of things breaking ", bork , time.strftime('%X %x %Z'),'\n','=' * 50)

def setSniffNu():
  try:
    bt = scapy.all.BluetoothHCISocket(1)
    #bt.sr(HCI_Hdr()/HCI_Command_Hdr()/HCI_Cmd_LE_Set_Scan_Enable(enable=True,filter_dups=False))
    bt.sniff(timeout=600,prn=packout)
  except Exception as bork:
    print ("Sniff/Scapy error...sound of things breaking ", bork , time.strftime('%X %x %Z'),'\n','=' * 50)


    
def grind(this_pig):#this_pig.ds.show()
  if ('Complete list of 128-bit service UUIDs' in this_pig.pcap):#???
    this_pig.pcap.show()
  try:
    if(this_pig.pcap.haslayer(Dot11Beacon)):
        bssid = this_pig.pcap[Dot11].addr2 if this_pig.pcap[Dot11].addr2 else "Null>"
        ssid = re.sub(r"(\u0000)", "Null>", this_pig.pcap[Dot11Elt].info.decode())        
        ssid = "<<Hidden>>" if len(this_pig.pcap[Dot11Elt].info.decode()) == 0 else ssid
        try: dbm_signal = str(this_pig.pcap.dBm_AntSignal)
        except: dbm_signal = "N/A"
        try:
            stats = this_pig.pcap[Dot11Beacon].network_stats()
            channel = str(stats.get("channel"))
            crypto = stats.get("crypto")
        except:
            channel = "?"
            crypto = "?"
    elif(this_pig.pcap['HCI header'].type==4):
      if(this_pig.pcap.haslayer('LE Meta')):#trap(this_pig)
         if(this_pig.pcap['LE Meta'].event==2):
           ar = this_pig.pcap['Advertising Reports'][0]['Advertising Report']
           bssid = ar.addr
           ssid = ar.addr
           dbm_signal = str(ar.rssi)
           channel = "channel"
           crypto = "crypto"
           networks.loc[bssid] = (ssid, dbm_signal, channel, crypto)
           this_pig.ds = (bssid, ssid, dbm_signal, channel, crypto)
           trap(this_pig)
      else:#More>>>>
        print('Event')
        this_pig.pcap.show()
    elif(this_pig.pcap['HCI header'].type==1):
      print('CMD')
      this_pig.pcap.show()
    else:
        bssid = "Unfiltered"
        ssid = "Borken"
        dbm_signal = "dbm_signal"
        channel = "channel"
        crypto = "crypto"
        this_pig.pcap.show()
    networks.loc[bssid] = (ssid, dbm_signal, channel, crypto)
    if not bssid == "Unfiltered":
        this_pig.ds = (bssid, ssid, dbm_signal, channel, crypto)
        trap(this_pig)
  except Exception as bork:
    print("????", bork)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

  

  
def callback(this_pig):
    if this_pig.pcap.haslayer(Dot11Beacon):
        bssid = this_pig.pcap[Dot11].addr2 if this_pig.pcap[Dot11].addr2 else "Null>"
        ssid = re.sub(r"(\u0000)", "Null>", this_pig.pcap[Dot11Elt].info.decode())        
        ssid = "<<Hidden>>" if len(this_pig.pcap[Dot11Elt].info.decode()) == 0 else ssid
        try: dbm_signal = str(this_pig.pcap.dBm_AntSignal)
        except: dbm_signal = "N/A"
        try:
            stats = this_pig.pcap[Dot11Beacon].network_stats()
            channel = str(stats.get("channel"))
            crypto = str(stats.get("crypto"))
        except:
            channel = "?"
            crypto = "?"
        networks.loc[bssid] = (ssid, dbm_signal, channel, crypto)
        this_pig.ds = (bssid, ssid, dbm_signal, channel, crypto)
        trap(this_pig)


def makeReq(url="http://127.0.0.1:"+str(serverPort)):
    r = requests.get(url)#print(r.text)
    j = r.json()
    df = pd.DataFrame.from_dict(j)
    print(df.to_json(orient="index"))


def setFlirt(nic='wlan0',m="managed"):
        r = "ifconfig "+ nic+ " down && iwconfig "+ nic+ " mode "+ m+ " && ifconfig "+ nic+ " up"
        return (r) #os.system(r) 

def prettyPig(up=True):# web server as thread
            web = Thread(target=svr)
            web.daemon = True
            if up: web.start()
            else: web.stop()
def svr():
    webServer = HTTPServer((hostName, serverPort), MyServer)#print("http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except Exception as bork:
        print ("Web error...sound of things breaking ", bork , time.strftime('%X %x %Z'),'\n','=' * 50)

def nakedPig(up=True):# web server as thread
            printer = Thread(target=print_all)# start the thread that prints all the networks
            printer.daemon = True
            if up: printer.start()
            else: printer.stop()

def print_all():
    while True:
        os.system("clear")
        result = networks.to_json(orient="index")#print(networks.sort_values(by=['dBm_Signal']))
        parsed = json.loads(result)
        print(result)
        time.sleep(0.5)

def hedyLamarr(up=True):# web server as thread
            channel_changer = Thread(target=change_channel)# start the channel changer
            channel_changer.daemon = True 
            if up: channel_changer.start()
            else: channel_changer.stop()

def change_channel(): # switch channel from 1 to 14 each 0.5s
    ch = 1
    while True:
        os.system(f"iwconfig {interface} channel {ch}")
        ch = ch % 13 + 1#ch = ch % 14 + 1 local limits!
        time.sleep(0.5)

#==============================================================================================
def sortNetDS():
    df = networks.sort_index(key=lambda x: x.str.lower())
    r = df.to_html()
    return (r)

def packout(packet):#packet.show() print(packet)
  a_pig = mainPig 
  a_pig.ds = packet
  a_pig.pcap = packet
  #callback(a_pig)#
  grind(a_pig)

def trap(this_pig):#this_pig.pcap.show()
  if 'the grass is green and the sun still shines':
    try:
      if 'write to db':
          keyDT = str(datetime.datetime.now())
          #drop(this_pig)
          initQs = ['/*drop table if exists perimeter;*/'
              ,'create table if not exists perimeter (last_seen, MAC TEXT, PUB TEXT, rssi TEXT, channel TEXT, crypto TEXT, proto TEXT, relate TEXT, UNIQUE(MAC,rssi,relate) ON CONFLICT REPLACE)'
              ,'INSERT INTO perimeter VALUES ("'+keyDT+'","'+this_pig.ds[0]+'","'+this_pig.ds[1]+'","'+this_pig.ds[2]+'","'+this_pig.ds[3]+'","'+this_pig.ds[4]+'","'+this_pig.proto+'","'+this_pig.name+'")'
              ,'/*SELECT distinct MAC FROM perimeter ORDER BY last_seen";*/'
              ]
          for sql in initQs:
              this_pig.sql = sql#print(this_pig.sql)
              dbLand(this_pig)#ds = this_pig.ds
    except Exception as bork:
      print ("DB error...sound of things breaking ", bork , time.strftime('%X %x %Z'),'\n','=' * 50)
      print(this_pig.sql)

def drop(this_pig):#this_pig.pcap.show()
  if 'the grass is green and the sun still shines':
    try:
      if 'write to db':
          initQs = ['drop table if exists perimeter;']
          for sql in initQs:
              this_pig.sql = sql#print(this_pig.sql)
              dbLand(this_pig)#ds = this_pig.ds
    except Exception as bork:
      print ("DB error...sound of things breaking ", bork , time.strftime('%X %x %Z'),'\n','=' * 50)
      print(this_pig.sql)

def dbLand(this_pig):#import sqlite3#https://www.sqlite.org/inmemorydb.html
    conn = sqlite3.connect(this_pig.db)#You can also supply the special name :memory: to create a database in RAM.
    c = conn.cursor()
    c.execute(this_pig.sql)
    this_pig.ds = c.fetchall()
    conn.commit()
    conn.close()

if __name__ == "__main__":
    mainPig = pig('scan'+str(datetime.datetime.now()))
    mainPig.bbq()
    #drop(mainPig)
    if len(sys.argv) > 1:
        interface = sys.argv[1]
        try:
            if not (interface=='1'):
                mainPig.proto='Wifi Dot11Beacon'
                os.system(setFlirt(interface,"monitor"))
                prettyPig()
                #nakedPig()
                hedyLamarr()
                setSniffWifi()#sniff(prn=packout, iface=interface)# start sniffing
            else:
                mainPig.proto='BTLE Advert'
                prettyPig()
                nakedPig()
                setSniffOld()

        except KeyboardInterrupt:
            pass
        if not (interface=='1'):os.system(setFlirt(interface))
    else :
        makeReq()

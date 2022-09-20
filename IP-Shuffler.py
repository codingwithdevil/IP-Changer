#! /usr/bin/env python2
"""
The IP-Shuffler tool is not Mine, All of its credits to ruped24 and its crew, I only maked it some changes
Combine toriptable2 & Tor_ip_switcher & added buttons for set (Tor Hash Password ,check ip, start 
tor , load , flush and refresh).
Useful for making any DoS attack look like a DDoS attack.
"""

from commands import getoutput
from json import load
from random import random
from ScrolledText import ScrolledText
from telnetlib import Telnet
from thread import start_new_thread
from time import localtime, sleep
from Tkinter import *
from tkMessageBox import showerror
from urllib2 import URLError, urlopen
from os import devnull
from os.path import isfile
from sys import exit, stdout
from time import sleep
from subprocess import call, check_call, CalledProcessError
from os.path import isfile, basename
from os import devnull
from sys import exit




class Switcher(Tk):
  
  def __init__(self):
    
    Tk.__init__(self)
    self.resizable(0, 0)
    self.title(string=".o0O| TOR IP Switcher Recoded by Devil |O0o.")
    self.local_dnsport = "53"  # DNSPort
    self.virtual_net = "10.0.0.0/10"  # VirtualAddrNetwork
    self.local_loopback = "127.0.0.1" # Local loopback
    self.non_tor_net = ["192.168.0.0/16", "172.16.0.0/12"]
    self.non_tor = ["127.0.0.0/9", "127.128.0.0/10", "127.0.0.0/8"]
    self.tor_uid = getoutput("id -ur debian-tor")  # Tor user uid
    self.trans_port = "9040"  # Tor port
    self.tor_config_file = '/etc/tor/torrc'
    
    self.torrc = r'''
## Inserted by %s for tor iptables rules set
## Transparently route all traffic thru tor on port %s
VirtualAddrNetwork %s
AutomapHostsOnResolve 1
TransPort %s
DNSPort %s
''' % (basename(__file__), self.trans_port, self.virtual_net,
       self.trans_port, self.local_dnsport)

    self.host = StringVar()
    self.port = IntVar()
    self.passwd = StringVar()
    self.time = DoubleVar()
    self.torpasswd = StringVar()
    

    self.host.set('localhost')
    self.port.set('9051')
    self.passwd.set('')
    self.time.set('30')
    self.torpasswd.set('')

    Label(self, text='Host:').grid(row=1, column=1, sticky=E)
    Label(self, text='Port:').grid(row=2, column=1, sticky=E)
    Label(self, text='Password:').grid(row=3, column=1, sticky=E)
    Label(self, text='Interval:').grid(row=4, column=1, sticky=E)
    Label(self, text='Set Tor password:').grid(row=5, column=1, sticky=E)
    
    Entry(self, textvariable=self.host).grid(row=1, column=2, columnspan=2)
    Entry(self, textvariable=self.port).grid(row=2, column=2, columnspan=2)
    Entry(self, textvariable=self.passwd, show='*').grid(
          row=3, column=2, columnspan=2)
    Entry(self, textvariable=self.time).grid(row=4, column=2, columnspan=2)
    Entry(self, textvariable=self.torpasswd, show='*').grid(
          row=5, column=2, columnspan=2)

    
    Button(self, text='Start', command=self.start).grid(row=6, column=1)
    Button(self, text='Stop', command=self.stop).grid(row=6, column=2)
    Button(self, text='Refresh', command=self.starttable_refresh).grid(row=6, column=3)
    Button(self, text='Set tor password', command=self.set_torpasswd).grid(row=6, column=4)
    Button(self, text='Start tor', command=self.start_tor).grid(row=6, column=5)
    Button(self, text='load', command=self.starttable_l).grid(row=6, column=6)
    Button(self, text='flush', command=self.starttable_f).grid(row=6, column=7)
    Button(self, text='ip', command=self.starttable_ip).grid(row=6, column=8)

    self.output = ScrolledText(
        self,
        foreground="white",
        background="black",
        highlightcolor="white",
        highlightbackground="purple",
        wrap=WORD,
        height=8,
        width=40)
    self.output.grid(row=1, column=4, rowspan=5, padx=4, pady=4)

  def start_tor(self):
    call(["service", "tor", "start"])
    self.write('Tor Started...')
  def set_torpasswd(self):
    passwd = self.torpasswd.get()
    if len(passwd) != 0:
      call(["service", "tor", "stop"])
      self.write('Setting password')
      hashpass = ''.join(
        getoutput('tor --hash-password "%s"' % ''.join(passwd)).split()[-1:])
      
      
      info = \
        """
        Gathering torrc config information
        """
      if isfile('/etc/tor/torrc'):
          self.write('hi')
          if 'HashedControlPassword' not in open('/etc/tor/torrc').read():
            self.write("[!] HashedControlPassword not in /etc/tor/torrc.")
          for i in info:
            sleep(.02)
            stdout.write(i)
            stdout.flush()
          
          call(["sed", "-i", "/ControlPort /s/^#//", "/etc/tor/torrc"])
          call(["sed", "-i", "/HashedControlPassword /s/^#//", "/etc/tor/torrc"])
          
          call([
              "sed",
              "-i",
              "s/^HashedControlPassword 16:.*[A-Z0-9]/HashedControlPassword %s/" %
              hashpass,
              "/etc/tor/torrc",
          ])
          
          if getoutput('pidof tor') == '':
              call(['kill', '-HUP', '$(pidof tor)' ], stderr=open(devnull, 'w'))
              self.write("Tor Config: Reloaded")
          else:
              self.write("Tor Daemon: Not running")
          self.write("ControlPort 9051: Enabled")   
          self.write("HashedControlPassword: Enabled" )
          self.write("/etc/tor/torrc: Updated successfully")
          self.write("Password set to: %s"%(passwd))
          self.write("HashedControlPassword: %s" % (hashpass))
          
      else:
          self.write("/etc/tor/torrc missing.")
          self.write('Check tor is installed')
          self.write('Password Setup Finished')
      
    else:
      self.write('Password is empty')
      self.write('Type password first')
      self.write('Then try again')
      

  def starttable_l(self):
    try:
        self.write("This may take Time")
        self.write('Please be patient..')
        
        if isfile(self.tor_config_file):
            if not 'VirtualAddrNetwork' in open(self.tor_config_file).read():
                with open(self.tor_config_file, 'a+') as torrconf:
                    torrconf.write(self.torrc)
        
        call(["iptables", "-F"])
        call(["iptables", "-t", "nat", "-F"])
        self.write('Flushing Complete')
      
        self.non_tor.extend(self.non_tor_net)

        
        fnull = open(devnull, 'w')
        try:
          tor_restart = check_call(
              ["service", "tor", "restart"],
                stdout=fnull, stderr=fnull)

          if tor_restart is 0:
            self.write("{0}".format(
                  "Anonymizer status [ON]"))
            self.get_ip()
        except CalledProcessError as err:
          self.write("[!] Command failed: %s" % ' '.join(err.cmd))

        # See https://trac.torproject.org/projects/tor/wiki/doc/TransparentProxy#WARNING
        # See https://lists.torproject.org/pipermail/tor-talk/2014-March/032503.html
        call(["iptables", "-I", "OUTPUT", "!", "-o", "lo", "!", "-d",
              self.local_loopback, "!", "-s", self.local_loopback, "-p", "tcp",
              "-m", "tcp", "--tcp-flags", "ACK,FIN", "ACK,FIN", "-j", "DROP"])
        call(["iptables", "-I", "OUTPUT", "!", "-o", "lo", "!", "-d",
              self.local_loopback, "!", "-s", self.local_loopback, "-p", "tcp",
              "-m", "tcp", "--tcp-flags", "ACK,RST", "ACK,RST", "-j", "DROP"])

        call(["iptables", "-t", "nat", "-A", "OUTPUT", "-m", "owner", "--uid-owner",
              "%s" % self.tor_uid, "-j", "RETURN"])
        call(["iptables", "-t", "nat", "-A", "OUTPUT", "-p", "udp", "--dport",
              self.local_dnsport, "-j", "REDIRECT", "--to-ports", self.local_dnsport])

        for net in self.non_tor:
          call(["iptables", "-t", "nat", "-A", "OUTPUT", "-d", "%s" % net, "-j",
                "RETURN"])

        call(["iptables", "-t", "nat", "-A", "OUTPUT", "-p", "tcp", "--syn", "-j",
              "REDIRECT", "--to-ports", "%s" % self.trans_port])

        call(["iptables", "-A", "OUTPUT", "-m", "state", "--state",
              "ESTABLISHED,RELATED", "-j", "ACCEPT"])

        for net in self.non_tor:
          call(["iptables", "-A", "OUTPUT", "-d", "%s" % net, "-j", "ACCEPT"])

        call(["iptables", "-A", "OUTPUT", "-m", "owner", "--uid-owner", "%s" %
              self.tor_uid, "-j", "ACCEPT"])
        call(["iptables", "-A", "OUTPUT", "-j", "REJECT"])

            
    except Exception as err:
        self.write("[!] Run as super user: %s" % err)

  def starttable_f(self):
    try:
        
        if isfile(self.tor_config_file):
            if not 'VirtualAddrNetwork' in open(self.tor_config_file).read():
                with open(self.tor_config_file, 'a+') as torrconf:
                    torrconf.write(self.torrc)
        
        call(["iptables", "-F"])
        call(["iptables", "-t", "nat", "-F"])
        self.write('Flush Complete')
        
    except Exception as err:
      try:
        self.write("[!] Run as super user: %s" % (err)) 
      except:
        print("[!] Run as super user: %s" % (err))

  def starttable_ip(self):
    try:
       
        if isfile(self.tor_config_file):
            if not 'VirtualAddrNetwork' in open(self.tor_config_file).read():
                with open(self.tor_config_file, 'a+') as torrconf:
                    torrconf.write(self.torrc)
        self.get_ip()
    except Exception as err:
      try:
        self.write("[!] Run as super user: %s" % (err)) 
      except:
        print("[!] Run as super user: %s" % (err))

  def starttable_refresh(self):
    try:
        
        if isfile(self.tor_config_file):
            if not 'VirtualAddrNetwork' in open(self.tor_config_file).read():
                with open(self.tor_config_file, 'a+') as torrconf:
                    torrconf.write(self.torrc)
        call(['kill', '-HUP', '%s' % getoutput('pidof tor')])
        self.get_ip()
    except Exception as err:
      try:
        self.write("[!] Run as super user: %s" % (err)) 
      except:
        print("[!] Run as super user: %s" % (err))
  

  def start(self):
    self.write('TOR Switcher starting.')
    self.ident = random()
    start_new_thread(self.newnym, ())

  def stop(self):
    try:
      self.write('TOR Switcher stopping.')
      self.write('Flushing..')
      call(["iptables", "-F"])
      call(["iptables", "-t", "nat", "-F"])
      self.write('Stoping Tor')
      call(["service", "tor", "stop"])
      self.write('Stoped ..')
    except:
      pass
    self.ident = random()

  def write(self, message):
    t = localtime()
    try:
      self.output.insert(END,
                         '[%02i:%02i:%02i] %s\n' % (t[3], t[4], t[5], message))
      self.output.yview(MOVETO, 1.0)
    except:
      print('[%02i:%02i:%02i] %s\n' % (t[3], t[4], t[5], message))

  def error(self):
    showerror('TOR IP Switcher', 'Tor daemon not running!')

  def newnym(self):
    key = self.ident
    host = self.host.get()
    port = self.port.get()
    passwd = self.passwd.get()
    interval = self.time.get()

    try:
      telnet = Telnet(host, port)
      if passwd == '':
        telnet.write("AUTHENTICATE\r\n")
      else:
        telnet.write("AUTHENTICATE \"%s\"\r\n" % (passwd))
      res = telnet.read_until('250 OK', 5)

      if res.find('250 OK') > -1:
        self.write('AUTHENTICATE accepted.')
      else:
        self.write('Control responded,' + "\n"
                   'Incorrect password: "%s"' % (passwd))
        key = self.ident + 1
        self.write('Quitting.')
    except Exception:
      self.write('There was an error!')
      self.error()
      key = self.ident + 1
      self.write('Quitting.')

    while key == self.ident:
      try:
        telnet.write("signal NEWNYM\r\n")
        res = telnet.read_until('250 OK', 5)
        if res.find('250 OK') > -1:
          try:
            my_new_ident = load(urlopen('https://check.torproject.org/api/ip'))['IP']
          except (URLError, ValueError):
            my_new_ident = getoutput('wget -qO - ifconfig.me')
          self.write('Your IP is %s' % (my_new_ident))
        else:
          key = self.ident + 1
          self.write('Quitting.')
        sleep(interval)
      except Exception as  ex:
        self.write('There was an error: %s.' % (ex))
        key = self.ident + 1
        self.write('Quitting.')

    try:
      telnet.write("QUIT\r\n")
      telnet.close()
    except:
      pass
   
  def get_ip(self):
    self.write("Getting public IP,")
    self.write('please wait...')
    retries = 0
    my_public_ip = None
    while retries < 12 and not my_public_ip:
      retries += 1
      try:
        my_public_ip = load(urlopen('https://check.torproject.org/api/ip'))['IP']
      except URLError:
        sleep(5)
        self.write("Still waiting for IP address...")
      except ValueError:
        break
    print
    if not my_public_ip:
      my_public_ip = getoutput('wget -qO - ifconfig.me')
    if not my_public_ip:
      exit("[!] Can't get public ip address!")
    self.write("Your IP is %s" %(my_public_ip))



if __name__ == '__main__':
  try:
    mw = Switcher()
    mw.mainloop()
    mw.stop()
  except KeyboardInterrupt:
    exit()

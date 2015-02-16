#!/usr/bin/env python


import sys
from sys import stdout
import csv  # Exporting and importing cracked aps
import os  # File management
from os import path
import time
import subprocess
from subprocess import Popen, PIPE, call
import re  # RegEx, Converting ESSID to filename
from PyQt4 import QtCore, QtGui
from signal import SIGINT, SIGTERM
import commands
import wifernGui
import interfaceGui

"""
    My first attempt at duplicating the fern-wifi-cracker and wifite programs
    with a Graphical Interface.
    A tall order and a long rood ahead but if you don't start you're never gone learn

"""




class wifern(QtGui.QMainWindow, wifernGui.Ui_mainwindow):
    'Main application class derived from WIfite and FERN-wifi-cracker thus wifern'

    def __init__(self, parent=None):
        super(wifern, self).__init__(parent)
        self.setupUi(self)
        if os.getuid() != 0:
            exit(1)
        self.working_dir()
        self.recs()
        self.wordlist = ''
        self.working_Dir = ''
        self.list_processes = []  # maybe list of proccesses to close on exit
        self.int_iface = ''
        self.before_intface = ('', '')
        self.mon_iface = ''
        self.adapters = []
        self.monitors = []
        self.connect(self.access_pointScan_Button, QtCore.SIGNAL("clicked()"), self.initscan)
        self.connect(self.dictionary_select_Button, QtCore.SIGNAL("clicked()"), self.opendict)
        self.connect(self.Get_Wordlist_Button, QtCore.SIGNAL("clicked()"), self.Sort_Wordlist)
        self.connect(self.Process_wordlist_Button, QtCore.SIGNAL("clicked()"), self.process_wordlist)
        self.wlan0_monitor_Button.setVisible(False)
        self.wlan1_monitor_button.setVisible(False)
        # self.Process_wordlist_Button.setEnabled(False)
        self.showlcd()
        self.connect(self.list_interfaces_Button, QtCore.SIGNAL("clicked()"), self.wireless_interface)
        self.connect(self.wlan0_monitor_Button, QtCore.SIGNAL('clicked()'), self.monitor_mode_enable)
        self.connect(self.start_wash_Button, QtCore.SIGNAL('clicked'), self.wash)

    def wireless_interface(self):

        self.int_iface = ''
        cmd = str(commands.getoutput('iwconfig'))
        if 'Mode:Managed' in cmd:
            regex = re.compile('wlan\d', re.IGNORECASE)
            self.adapters = regex.findall(cmd)
        if 'Mode:Monitor' in cmd:
            regex = re.compile('mon\d', re.IGNORECASE)
            self.monitors = regex.findall(cmd)
        if not (('Mode:Managed') or ('Mode:Monitor')) in cmd:
            text = ['No Interface']
            for i in text:
                self.adapters_comboBox.addItem(i)
        for adap in self.adapters:
            self.adapters_comboBox.addItem(adap)
            self.wlan0_monitor_Button.setVisible(True)
        for monit in self.monitors:
            self.monitors_comboBox.addItem(monit)
            self.wlan1_monitor_button.setVisible(True)
        print self.adapters, self.monitors          # remove after tests

    def monitor_mode_enable(self,):
        self.int_iface = str(self.adapters_comboBox.currentText())
        comm = str(commands.getoutput("ifconfig -a | awk '/HWaddr/ {print $1 " " $NF}'"))
        a = comm.splitlines()
        for word in a:
            wor_essid = word[:-17]
            wor_mac = word[-17:]
            if wor_essid == self.int_iface:                    ## TODO  Anonymize the original interface
                self.before_intface = wor_essid, wor_mac       ##       to avoid accidents
                print self.before_intface
        '''ifconfig wlan0 down
         hw ether 01:10:10:00:01:10
          ifconfig wlan0 up'''
        comma = str(commands.getoutput('airmon-ng start %s' %( self.int_iface)))
        if 'monitor mode enabled' in comma:
            reg = re.compile('mon\d', re.IGNORECASE)
            x_int = reg.findall(comma)
            for a, monitor in enumerate(x_int):
                self.mon_iface = monitor
                if self.mon_iface in self.monitors:
                    self.mon_iface = x_int[(a + 1) % len(x_int)]
                else:
                    self.monitors.append(self.mon_iface)
            if self.injection_working(self.mon_iface):          ## Check if injection is working
                if self.mon_iface in self.monitors:
                    self.monitors_comboBox.setItemText(0, self.mon_iface)    ####   fix ME   ####
                else:
                    self.monitors.append(self.mon_iface)
                    for monit in self.monitors:
                        self.monitors_comboBox.addItem(monit)
                        self.wlan1_monitor_button.setVisible(True)
            else:
                print('Injection NOT working')          ## Add instuctions to fix or buy other card
                                                        ## Disable(!!!!!) buttons

    def injection_working(self, mon_iface_check):
        cmd = str(commands.getoutput('aireplay-ng -9 %s'%(mon_iface_check)))
        if 'Injection is working!' in cmd:
                message = QtGui.QMessageBox.information(self, 'Injection', 'Injection on ' + mon_iface_check + ' is working!', QtGui.QMessageBox.Ok)
                return True
        else:
            return False


    def opendict(self):
        #################
        # Method works  #
        ################
        dict_open = QtGui.QFileDialog.getOpenFileName(self, 'Select Dictionary', '',
                                                'Text files (*.txt);; List files (*.lst)')
        if dict_open:
            filename = dict_open
            self.dict_file_path.setText(filename)
            self.wordlist = os.path.basename(str(filename))
            print self.wordlist                         #Delete after test
            self.dict_file_path.setEnabled(False)


    def washMonitorList(self):
        for m in self.monitors.index():
            if m >= 1:
                for i in self.monitors:
                    self.Monitor_select_comboBox.addItem(i)
            else:
                continue


    def working_dir(self):

        from tempfile import mkdtemp

        self.working_Dir = mkdtemp(prefix='wifern')
        if not self.working_Dir.endswith(os.sep):
            self.working_Dir += os.sep
        os.chdir(self.working_Dir)



    def initscan(self,):
        cmd = str(commands.getoutput('airodump-ng --ignore-negative-one --manufacturer -a --output-format csv -w wifern-dump %s'%(self.mon_iface)))




    def get_victim_list(self, csv_filename):
            if not os.path.exists(csv_filename):
                return [], []
            targets = []
            clients = []
            try:
                victim_clients = False
                with open(csv_filename, 'rb') as csvfile:
                    victimreader = csv.reader((line.replace('\0', '') for line in csvfile), delimiter=',')
                    for row in victimreader:
                        if len(row) < 2:
                            continue
                        if not victim_clients:
                            if len(row) < 14:
                                continue
                            if row[0].strip() == 'Station MAC':
                                victim_clients = True
                            if row[0].strip() == 'BSSID' or row[0].strip() == 'Station Mac':
                                continue
                            enc = row[5].strip()
                            wps = False
                            if enc.find('WPA') == -1 and enc.find('WEP') == -1:
                                continue
                            if self.RUN_CONFIG.WEP_DISABLE and enc.find('WEP') != -1:
                                continue
                            if self.RUN_CONFIG.WPA_DISABLE and self.RUN_CONFIG.WPS_DISABLE and enc.find('WPA') != -1:
                                continue
                            if enc == "WPA2WPA":
                                enc = "WPA2"
                                wps = True
                            power = int(row[8].strip())

                            essid = row[13].strip()
                            essidlen = int(row[12].strip())
                            essid = essid[:essidlen]
                            if power < 0: power += 100
                            t = Victim(row[0].strip(), power, row[10].strip(), row[3].strip(), enc, essid)
                            t.wps = wps
                            targets.append(t)
                        else:
                            if len(row) < 6:
                                continue
                            bssid = re.sub(r'[^a-zA-Z0-9:]', '', row[0].strip())
                            station = re.sub(r'[^a-zA-Z0-9:]', '', row[5].strip())
                            power = row[3].strip()
                            if station != 'notassociated':
                                c = Client(bssid, station, power)
                                clients.append(c)
            except IOError as e:
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
                return [], []
            return (targets, clients)


    def program_list(self, program):
            proc = Popen(['which', program], stdout=PIPE, stderr=PIPE)
            txt = proc.communicate()
            if txt[0].strip() == '' and txt[1].strip() == '':
                return False
            if txt[0].strip() != '' and txt[1].strip() == '':
                return True
            return not (txt[1].strip() == '' or txt[1].find('no %s in' % program) != -1)

    def reaver(self):
        print ('Hi')


    def wash(self):
        cmd = str(commands.getoutput('wash -i %s -C'%(self.mon_iface)))
        yolo = cmd.splitlines()
        print yolo
        time.sleep(7)

        try:
            os.kill(cmd.pid, SIGTERM)
        except OSError:
            pass
        except UnboundLocalError:
            pass

        row = 0
        col = 0
        self.wash_treewidget.setColumnCount(4)
        self.wash_treewidget.setColumnWidth(3,70)
        self.wash_treewidget.setRowCount(17)

    def recs(self):
        ####################
        #  Method works    #
        ####################
        row = 0
        col = 0
        self.my_tableWidget.setColumnCount(3)
        self.my_tableWidget.setColumnWidth(1,70)
        self.my_tableWidget.setColumnWidth(2,70)
        self.my_tableWidget.setRowCount(17)
        rec_progs = ['aircrack-ng', 'aireplay-ng', 'airodump-ng', 'airmon-ng', 'packetforge-ng',
                'iw', 'iwconfig', 'reaver', 'wash', 'mdk3', 'pyrit', 'ifconfig']
        for prog in rec_progs:
            if self.program_list(prog):
                x = QtGui.QTableWidgetItem()
                x.setFlags(QtCore.Qt.ItemIsEnabled)
                x.setCheckState(QtCore.Qt.Checked)
                y = QtGui.QTableWidgetItem()
                y.setFlags(QtCore.Qt.ItemIsEnabled)
                y.setCheckState(QtCore.Qt.Checked)
                row_item = QtGui.QTableWidgetItem(prog)
                self.my_tableWidget.setItem(row, col, row_item)
                self.my_tableWidget.setItem(row, 1, x)
                self.my_tableWidget.setItem(row, 2, y)
                row += 1
            else:
                x = QtGui.QTableWidgetItem()
                x.setFlags(QtCore.Qt.ItemIsEnabled)
                x.setCheckState(QtCore.Qt.Unchecked)
                y = QtGui.QTableWidgetItem()
                y.setFlags(QtCore.Qt.ItemIsEnabled)
                y.setCheckState(QtCore.Qt.Checked)     # add column with link to install or apt command
                row_item = QtGui.QTableWidgetItem(prog)
                self.my_tableWidget.setItem(row, col, row_item)
                self.my_tableWidget.setItem(row, 1, x)
                self.my_tableWidget.setItem(row, 2, y)
                row += 1



        not_rec_progs = ['bully', 'crunch', 'pw-inspector', 'oclhashcat', 'cudahashcat']
        not_rec_list = []
        for prog in not_rec_progs:
            if self.program_list(prog):
                x = QtGui.QTableWidgetItem()
                x.setFlags(QtCore.Qt.ItemIsEnabled)
                x.setCheckState(QtCore.Qt.Checked)
                y = QtGui.QTableWidgetItem()
                y.setFlags(QtCore.Qt.ItemIsEnabled)
                y.setCheckState(QtCore.Qt.Unchecked)
                row_item = QtGui.QTableWidgetItem(prog)
                self.my_tableWidget.setItem(row, col, row_item)
                self.my_tableWidget.setItem(row, 1, x)
                self.my_tableWidget.setItem(row, 2, y)
                row += 1
            else:
                x = QtGui.QTableWidgetItem()
                x.setFlags(QtCore.Qt.ItemIsEnabled)
                x.setCheckState(QtCore.Qt.Unchecked)
                y = QtGui.QTableWidgetItem()
                y.setFlags(QtCore.Qt.ItemIsEnabled)
                y.setCheckState(QtCore.Qt.Unchecked)
                row_item = QtGui.QTableWidgetItem(prog)
                self.my_tableWidget.setItem(row, col, row_item)
                self.my_tableWidget.setItem(row, 1, x)
                self.my_tableWidget.setItem(row, 2, y)
                row += 1



    def showlcd(self):
        time = QtCore.QTime.currentTime()
        text = time.toString('hh:mm')
        self.lcd_time_Number.display(text)


    def Sort_Wordlist(self):

        get_wordlist_for_sorting = QtGui.QFileDialog.getOpenFileName(self, 'Select Dictionary', '',
                                                'Text files (*.txt);; List files (*.lst)')
        if get_wordlist_for_sorting:
            filename = get_wordlist_for_sorting
            self.sort_wordlist_lineEdit.setText(filename)
            self.wordlist = filename
            self.sort_wordlist_lineEdit.setEnabled(False)

    def process_wordlist(self):
        cmd = ['cat ' + self.wordlist]

        if self.sort_checkBox.isChecked():
            cmd.append(' |' + ' sort')
            self.Process_wordlist_Button.setEnabled(True)
        if self.unique_checkBox.setCheckState(True):
            cmd.append(' |' + ' uniq')
            self.Process_wordlist_Button.setEnabled(True)
            ## cat words.txt | sort | uniq > dictionary.txt

        if self.pwinspector_checkBox.isChecked():
            cmd.append(' | ' + 'pw-inspector -m 8 -M 63')
            self.Process_wordlist_Button.setEnabled(True)
            ## pw-inspector -m 8 -M 63 > WPAwordlist.txt
        sort = Popen(cmd, stdout=PIPE, stderr=open(os.devnull, 'w'))


        ########################
        #  FIX ME              #
        ########################

class Interface:
    'Handles all the interface interactions'
    global wifern



class CapFile:
    'Holds data about an access points .cap file, including AP ESSID & BSSID'

    def __init__(self, filename, ssid, bssid):
        self.filename = filename
        self.ssid = ssid
        self.bssid = bssid


class Victim:
    'Contains information about the Access Poimt we are about to attack'

    def __init__(self, bssid, power, data, channel, encryption, essid, maker_model, wps):
        self.bssid = bssid
        self.power = power
        self.data = data
        self.channel = channel
        self.encryption = encryption
        self.essid = essid
        self.model = maker_model
        self.wps = wps
        self.wps = False  # Default to non-WPS-enabled router.
        self.key = ''

    def get_manufacturer(self):
        ##################
        # Method works   #
        ##################
        oui_path0 = '/etc/aircrack-ng/airodump-ng-oui.txt'
        oui_path1 = '/usr/local/etc/aircrack-ng/airodump-ng-oui.txt'
        oui_path2 = '/usr/share/aircrack-ng/airodump-ng-oui.txt'
        bssid = 'fc:bb:a1:35:f1:5g'
        partial_mac = ''


        try:
            oui_path = ''
            if os.path.exists(oui_path0):
                oui_path = oui_path0
            elif os.path.exists(oui_path1):
                oui_path = oui_path1
            elif os.path.exists(oui_path2):
                oui_path = oui_path2
            else:
                model = 'Not Available'

            with open(oui_path, 'r') as oui:
                db = oui.readlines()
            for line in db:
                oui_db = line.split()
                lookup_mac = oui_db[0].lower().replace('-', ':')
                partial_mac = bssid[:8]
                if lookup_mac == partial_mac:
                    self.model = ' '.join(oui_db[2:])
                    return model    # need to athached to client before record is displayed
        except IOError as a:
            print "I/O error({0}): {1}".format(a.errno, a.strerror)

class Tools:

    def __init__(self):

        print('')





class Client:
    'Contains information about the connected clients to the AP'
    def __init__(self, bssid, station, power, essid, encryption):
        self.bssid = bssid
        self.station = station
        self.power = power
        self.essid = essid
        self.encryption = encryption

    def vicscan(self, intface, bssid):
        self.bssid = Victim.bssid


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = wifern()
    form.show()
    sys.exit(app.exec_())



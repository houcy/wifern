#!/usr/bin/env python


import sys
from sys import stdout
import csv
import os
from os import path
import time
import subprocess
from subprocess import Popen, PIPE, call
import re
from PyQt4 import QtCore, QtGui
import multiprocessing
from signal import SIGINT, SIGTERM
import commands
import wifernGui
import interfaceGui
import sqlite3


"""
    My first attempt at duplicating the fern-wifi-cracker and wifite programs
    with a Graphical Interface.
    A tall order and a long rood ahead but if you don't start you're never gone learn

"""

wordlist_path = ''
wordlist = ''
list_processes = []  # maybe list of proccesses to close on exit
int_iface = ''
before_intface = ('', '')
after_intface = ('', '')
mon_iface = ''
adapters = []
monitors = []
WVList = []



class wifern(QtGui.QMainWindow, wifernGui.Ui_mainwindow):
    'Main application class derived from WIfite and FERN-wifi-cracker thus wifern'

    def __init__(self, parent=None):
        super(wifern, self).__init__(parent)
        self.setupUi(self)
        if os.getuid() != 0:
            exit(1)
        self.working_Dir = ''
        self.working_dir()
        self.recs()
        self.connect(self.access_pointScan_Button, QtCore.SIGNAL("clicked()"), self.initscan)
        self.connect(self.dictionary_select_Button, QtCore.SIGNAL("clicked()"), self.opendict)
        self.connect(self.Get_Wordlist_Button, QtCore.SIGNAL("clicked()"), self.Sort_Wordlist)
        self.connect(self.start_wash_Button, QtCore.SIGNAL("clicked()"), self.wash_call)
        self.connect(self.Process_wordlist_Button, QtCore.SIGNAL("clicked()"), self.process_wordlist)
        self.connect(self.list_interfaces_Button, QtCore.SIGNAL("clicked()"), self.wireless_interface)
        self.connect(self.wlan0_monitor_Button, QtCore.SIGNAL('clicked()'), self.monitor_mode_enable)
        self.connect(self.wlan1_monitor_button, QtCore.SIGNAL('clicked()'), self.UseThis)
        self.connect(self.Monitor_select_comboBox, QtCore.SIGNAL('clicked()'), self.washMonitorList)
        self.wlan0_monitor_Button.setVisible(False)
        self.wlan1_monitor_button.setVisible(False)
        self.start_wash_Button.setEnabled(False)
        self.Monitor_select_comboBox.setEnabled(False)
        self.showlcd()
        global stop
        stop = False


    def wireless_interface(self):
        conn=sqlite3.connect('attack_session.db')
        cursor = conn.cursor()
        global monitors, adapters
        # need to check if iwconfig exists (it should )
        cmd = str(commands.getoutput('iwconfig'))
        if 'Mode:Managed' in cmd:
            regex = re.compile('wlan\d', re.IGNORECASE)
            adapters = regex.findall(cmd)
        if 'Mode:Monitor' in cmd:
            regex = re.compile('mon\d', re.IGNORECASE)
            monitors = regex.findall(cmd)
        if not (('Mode:Managed') or ('Mode:Monitor')) in cmd:
            text = ['No Interface']
            for i in text:
                self.adapters_comboBox.addItem(i)
        if adapters:
            for adap in adapters:
                self.adapters_comboBox.addItem(adap)
                self.wlan0_monitor_Button.setVisible(True)
                int_iface = str(self.adapters_comboBox.currentText())
                comm = str(commands.getoutput("ifconfig -a | awk '/HWaddr/ {print $1 " " $NF}'"))
                a = comm.splitlines()
                for word in a:
                    wor_essid = word[:-17]
                    wor_mac = word[-17:]
                    if wor_essid == int_iface:                    ## TODO  Anonymize the original interface
                        before_intface = wor_essid, wor_mac
                        q = """insert into adapters(name, bssid, status) values(?,?,?)"""
                        cursor.execute(q,(wor_essid, wor_mac, 'before'))
                        conn.commit()
        else:
            return

        if monitors:
            for monit in monitors:
                self.monitors_comboBox.addItem(monit)
                self.wlan1_monitor_button.setVisible(True)
                comm = str(commands.getoutput("ifconfig -a | awk '/HWaddr/ {print $1 " " $NF}'"))
                a = comm.splitlines()
                for word in a:
                    wor_essid = word[:-47]
                    wor_mac = word[-47:-30]
                    wor_mac = wor_mac.replace('-', ':')
                    if wor_essid == monit:
                        b_m_intface = wor_essid, wor_mac
                        q = """insert into monitors(name, bssid) values(?,?)"""
                        cursor.execute(q,(wor_essid, wor_mac))
                        conn.commit()
        else:
            return

        cursor.close()
        conn.close()
        print adapters, monitors          # remove after tests

    def monitor_mode_enable(self,):
        conn=sqlite3.connect('attack_session.db')
        cursor = conn.cursor()
        int_iface = str(self.adapters_comboBox.currentText())
        print int_iface
        q = ("""select adapters.bssid from adapters where adapters.name = ?""")
        u = ("""select monitors.name from monitors where monitors.bssid = ?""")
        cursor.execute(q,(int_iface,));
        for row in cursor.fetchone():
            if row is not None:
                Mon_bss = str(row)
                try:
                    cursor.execute(u, ((Mon_bss).upper(),));
                    for arow in cursor.fetchone():
                        if arow is not None:
                            message = QtGui.QMessageBox.information(self, 'Select diferent adapter',int_iface + ' has already been put in monitor mode', QtGui.QMessageBox.Ok)
                except TypeError:
                    comm = str(commands.getoutput("ifconfig -a | awk '/HWaddr/ {print $1 " " $NF}'"))
                    a = comm.splitlines()
                    for word in a:
                        wor_essid = word[:-17]
                        wor_mac = word[-17:]
                    if wor_essid == int_iface:                    ## TODO  Anonymize the original interface
                        before_intface = wor_essid, wor_mac       ##       to avoid accidents
                        print before_intface                      ## Delete after test
                        '''ifconfig wlan0 down
                            ifconfig wlan0 hw ether 00:22:33:44:55:66
                        ifconfig wlan0 up'''
                    comma = str(commands.getoutput('airmon-ng start %s' %( int_iface)))
                    if 'monitor mode enabled' in comma:
                        reg = re.compile('mon\d', re.IGNORECASE)
                        x_int = reg.findall(comma)
                        for a, monitor in enumerate(x_int):
                            mon_iface = monitor
                            if mon_iface in monitors:
                                mon_iface = x_int[(a + 1) % len(x_int)]
                            else:
                                monitors.append(mon_iface)

                        if self.injection_working(mon_iface):          ## Check if injection is working
                            if mon_iface in monitors:
                                for monit in monitors:
                                    self.monitors_comboBox.addItem(monit)
                                    self.Monitor_select_comboBox.addItem(monit)
                                    self.wlan1_monitor_button.setVisible(True)
                            else:
                                monitors.append(mon_iface)
                                for monit in monitors:
                                    self.monitors_comboBox.addItem(monit)
                                    self.Monitor_select_comboBox.addItem(monit)
                                    self.wlan1_monitor_button.setVisible(True)
                        else:
                            print('Injection NOT working')          ## Add instuctions to fix or buy other card
                                                                    ## Disable(!!!!!) buttons



    def injection_working(self, mon_iface_check):  ## Make this method a thread
        cmd = ['aireplay-ng', '-9', mon_iface_check]
        cmd_inj = Popen(cmd, stdout=PIPE)
        for line in iter(cmd_inj.stdout.readline, ''):
            if 'Injection is working!' in line:
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
            self.wordlist_path = str(filename)                        #Delete after test
            self.dict_file_path.setEnabled(False)

    def UseThis(self):
        if self.monitors_comboBox.currentText() != '':
            self.mon_iface = self.monitors_comboBox.currentText()
            self.Monitor_select_comboBox.setEnabled(True)
            self.start_wash_Button.setEnabled(True)


    def washMonitorList(self):
        try:
            for i in self.monitors:
                self.Monitor_select_comboBox.addItem(i)
        except TypeError:
            print 'No Interface'



    def working_dir(self):
        from tempfile import mkdtemp

        self.working_Dir = mkdtemp(prefix='wifern')
        if not self.working_Dir.endswith(os.sep):
            self.working_Dir += os.sep
        os.chdir(self.working_Dir)
        conn=sqlite3.connect('attack_session.db')
        cursor = conn.cursor()
        cursor.execute("""create table reaver(bssid varchar PRIMARY KEY NOT NULL, \
        essid varchar, channel varchar, power varchar, locked char)""")
        cursor.execute("""create table victim(bssid varchar PRIMARY KEY NOT NULL, essid varchar, \
        power varchar, data varchar, channel int, encryption varchar,  maker_model varchar, wps bool)""")
        cursor.execute("""create table adapters(name varchar, bssid varchar, status varchar)""")
        cursor.execute("""create table monitors(name varchar, bssid varchar)""")
        cursor.execute("""create table recs(program_name varchar, available bool)""")
        conn.commit()
        cursor.close()
        conn.close()



    def initscan(self,):
        cmd = str(commands.getoutput('airodump-ng --ignore-negative-one --manufacturer -a --output-format csv -w wifern-dump %s'%(self.mon_iface)))
        # wait aprox 3 sec
        targets, clients = self.get_victim_list(wifern-dump.csv)


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
                            model = self.get_manufacturer(bssid)
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

    def wash_call(self):
        try:
            mon = str(self.mon_iface)
            proc = multiprocessing.Process(target=self.WashThread, args=(mon,))
            if self.start_wash_Button.text() == 'Start':
                self.start_wash_Button.setText('Stop')
                self.wash_run()
                proc.start()
                X = proc.pid
                xx = multiprocessing.active_children()
                print xx
            else:
                self.start_wash_Button.setText('Start')
                os.kill(int(X), SIGTERM)
                os.kill(P_pid, SIGTERM)
        except KeyboardInterrupt, SystemExit:
            os.kill(P_pid, SIGTERM)
        except OSError:
            pass
        except UnboundLocalError:
            pass
        finally:
            pass
    def wash_run(self):
        try:
            sqlite3.enable_shared_cache(True)
            conn=sqlite3.connect('attack_session.db')
            cursor = conn.cursor()
            my_row = 0
            col = 0
            self.wash_tableWidget.setColumnCount(4)
            self.wash_tableWidget.setColumnWidth(1,200)
            self.wash_tableWidget.setColumnWidth(2, 120)
            self.wash_tableWidget.setColumnWidth(4,30)
            self.wash_tableWidget.setColumnWidth(3,70)
            cursor.execute("""select bssid, essid, power, locked from reaver""")
            for row in cursor.fetchall():
                if row != None:
                    row_item = QtGui.QTableWidgetItem(row[0])
                    x = QtGui.QTableWidgetItem(row[1])
                    y = QtGui.QTableWidgetItem(row[2])
                    z = QtGui.QTableWidgetItem(row[3])
                    self.wash_tableWidget.setItem(my_row, col, row_item)
                    self.wash_tableWidget.setItem(my_row, 1, x)
                    self.wash_tableWidget.setItem(my_row, 2, y)
                    self.wash_tableWidget.setItem(my_row, 3, z)
                    row += 1
                    self.wash_tableWidget.setRowCount(row)

            cursor.close()
            conn.close()
        except:
            pass   # TODO errors here

    def recs(self):
        ####################
        #  Method works    #
        ####################
        conn=sqlite3.connect('attack_session.db')
        cursor = conn.cursor()
        row = 0
        col = 0
        self.my_tableWidget.setColumnCount(3)
        self.my_tableWidget.setColumnWidth(1,70)
        self.my_tableWidget.setColumnWidth(2,70)
        self.my_tableWidget.setRowCount(17)
        rec_progs = ['aircrack-ng', 'aireplay-ng', 'airodump-ng', 'airmon-ng', 'packetforge-ng',
                'iw', 'iwconfig', 'reaver', 'wash', 'mdk3', 'pyrit', 'ifconfig', 'sqlite3']
        for prog in rec_progs:
            if self.program_list(prog):
                q = """insert into recs(program_name, available) values(?,?)"""
                cursor.execute(q,(prog, True))
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
                q = """insert into recs(program_name, available) values(?,?)"""
                cursor.execute(q,(prog, False))
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
                q = """insert into recs(program_name, available) values(?,?)"""
                cursor.execute(q,(prog, True))
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
                q = """insert into recs(program_name, available) values(?,?)"""
                cursor.execute(q,(prog, False))
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
        conn.commit()
        cursor.close()
        conn.close()

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
            self.wordlist = os.path.basename(str(filename))
            self.wordlist_path = str(filename)
            self.sort_wordlist_lineEdit.setEnabled(False)

    def process_wordlist(self):

        cmd = ['cat '+ self.wordlist_path]

        if self.sort_checkBox.isChecked():
            cmd.append(' | sort')
            self.Process_wordlist_Button.setEnabled(True)
                                               ## Test
        if self.unique_checkBox.setCheckState(True):
            cmd.append(' | uniq')
            self.Process_wordlist_Button.setEnabled(True)
            ## cat words.txt | sort | uniq > dictionary.txt

        if self.pwinspector_checkBox.isChecked():
            cmd.append(' | pw-inspector -m 8 -M 63')
            self.Process_wordlist_Button.setEnabled(True)
        cmd.append(' > WPAwordlist.txt')
        foo = open('WPAwordlist.txt', 'w')
        print cmd
            ## pw-inspector -m 8 -M 63 > WPAwordlist.txt
        # comment for now
        sort = Popen(cmd, stdout=PIPE, stderr=open(os.devnull, 'w'))
        sort.wait()

        ########################
        #  FIX ME              #
        ########################

    def WashThread(self, device):
        sqlite3.enable_shared_cache(True)
        try:
            if device:
                conn=sqlite3.connect('attack_session.db')
                cmd = ['wash', '-C', '-i', device]
                wash_cmd = subprocess.Popen(cmd, stdout=PIPE)
                for line in iter(wash_cmd.stdout.readline, ''):
                    if line.strip() == '' or line.startswith('---'): continue
                    if line.startswith('Wash') or line.startswith('Copyright') or line.startswith('BSSID'): continue
                    line = line.strip()
                    Split = line.split()
                    b = Split[0]
                    e = str(' '.join(Split[5:]))
                    if len(e) == 0:
                        e = 'Hidden'
                    p = Split[2]
                    c = Split[1]
                    l = Split[4]
                    print b, e, c, p, l
                    q = """insert into reaver(bssid, essid, channel, power, locked) values(?,?,?.?,?)"""
                    conn.execute(q,(b, e, c, p, l,));
                    conn.commit()

            conn.close()
            P_pid = int(wash_cmd.pid)
            print P_pid
        except:
            pass


class CapFile:
    'Holds data about an access points .cap file, including AP ESSID & BSSID'

    def __init__(self, filename, ssid, bssid):
        self.filename = filename
        self.ssid = ssid
        self.bssid = bssid


class Victim():
    '''Contains information about the Access Poimt we are about to attack'''

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

    def get_manufacturer(self, bssid):  ##  TODO Add BSSID var to be processed
        ##################
        # Method works   #
        ##################
        oui_path0 = '/etc/aircrack-ng/airodump-ng-oui.txt'
        oui_path1 = '/usr/local/etc/aircrack-ng/airodump-ng-oui.txt'
        oui_path2 = '/usr/share/aircrack-ng/airodump-ng-oui.txt'
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



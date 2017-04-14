#!/usr/bin/env python
import os
from PyQt4 import QtCore, QtSql, QtGui
from subprocess import call
import multiprocessing
db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName("attack_session.db")
query = QtSql.QSqlQuery(db)


def working_dir():
    from tempfile import mkdtemp
    working__dir = mkdtemp(prefix='wifern')
    if not working__dir.endswith(os.sep):
        working__dir += os.sep
    os.chdir(working__dir)
    dBaseOpen()


def dBaseOpen():
    db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
    db.setDatabaseName('attack_session.db')
    db.open()
    if db.open():
        print 'I: Database connection was succesfull'
    if not db.open():
        QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"),
                                   QtGui.qApp.tr("Unable to establish a database connection.\n"
                                                 "This example needs SQLite support. Please read "
                                                 "the Qt SQL driver documentation for information "
                                                 "how to build it.\n\n"
                                                 "Click Cancel to exit."),
                                   QtGui.QMessageBox.Cancel)
        return False
    query = QtSql.QSqlQuery()
    query.exec_("create table reaver(bssid varchar(17) PRIMARY KEY NOT NULL, essid varchar(20), "
                "channel int, power int, locked varchar(3))")
    query.exec_("create table victim(bssid varchar(17) PRIMARY KEY NOT NULL, essid varchar(20), "
                "power int, data varchar(20), channel int, encryption varchar(7), "
                "maker_model varchar(40), wps varchar(3))")
    query.exec_("create table adapters (name varchar(8), bssid varchar(17), status varchar(7))")
    query.exec_("create table monitors (name varchar(8), bssid varchar(17))")
    query.exec_("create table recs (program_name varchar(20), available varchar(7))")
    query.exec_(
        "create table clients(bssid varchar(17), station varchar(17) references reaver (bssid), power int(3))")

    return True

def wifirefresh(self):
    self.wifi_model.setQuery("select * from victim", db)
    self.wifi_model.setHeaderData(0, QtCore.Qt.Horizontal, "BSSID")
    self.wifi_model.setHeaderData(1, QtCore.Qt.Horizontal, "ESSID")
    self.wifi_model.setHeaderData(2, QtCore.Qt.Horizontal, "Channel")
    self.wifi_model.setHeaderData(3, QtCore.Qt.Horizontal, "Encryption")
    self.wifi_model.setHeaderData(4, QtCore.Qt.Horizontal, "Cipher")
    self.wifi_model.setHeaderData(5, QtCore.Qt.Horizontal, "Authentication")
    self.wifi_model.setHeaderData(6, QtCore.Qt.Horizontal, "Power")
    self.wifi_model.setHeaderData(7, QtCore.Qt.Horizontal, "WPS")
    self.wifi_model.setHeaderData(8, QtCore.Qt.Horizontal, "Key")
    self.wifi_model.setHeaderData(9, QtCore.Qt.Horizontal, "Make/ Model")
    self.accessPointTable.setModel(self.wifi_model)
    self.accessPointTable.resizeColumnsToContents()

def wifi_window(self):
        try:
            mon = str(self.mon_iface)
            if self.access_pointScan_Button.text() == "Scan for Access Points":
                self.access_pointScan_Button.setText('Stop Scan')
                wifi = multiprocessing.Process(target=self.initscan, args=(mon,)).start()
                self.wifi_model = QtSql.QSqlQueryModel()
                self.wifi_model.setQuery("select * from victim", db)
                self.wifi_model.setHeaderData(0, QtCore.Qt.Horizontal, "BSSID")
                self.wifi_model.setHeaderData(1, QtCore.Qt.Horizontal, "ESSID")
                self.wifi_model.setHeaderData(2, QtCore.Qt.Horizontal, "Channel")
                self.wifi_model.setHeaderData(3, QtCore.Qt.Horizontal, "Encryption")
                self.wifi_model.setHeaderData(4, QtCore.Qt.Horizontal, "Cipher")
                self.wifi_model.setHeaderData(5, QtCore.Qt.Horizontal, "Authentication")
                self.wifi_model.setHeaderData(6, QtCore.Qt.Horizontal, "Power")
                self.wifi_model.setHeaderData(7, QtCore.Qt.Horizontal, "WPS")
                self.wifi_model.setHeaderData(8, QtCore.Qt.Horizontal, "Key")
                self.wifi_model.setHeaderData(9, QtCore.Qt.Horizontal, "Make/ Model")
                self.accessPointTable.setModel(self.wifi_model)
                self.accessPointTable.resizeColumnsToContents()
                self.file_Wifi = QtCore.QFileSystemWatcher()
                self.file_Wifi.addPath('attack_session.db')
                self.file_Wifi.fileChanged.connect(self.wifirefresh)
                if self.wifi_model.lastError().isValid():
                    print self.wifi_model.lastError()
            else:
                self.access_pointScan_Button.setText("Scan for Access Points")
                with open('extra1.txt', 'r') as fw:
                    Pid = int(fw.readline().strip())
                    os.kill(Pid, SIGINT)
        except AttributeError:
            message = QtGui.QMessageBox.information(self, 'Monitor Interface', 'You Must select a monitor Interface',
                                                    QtGui.QMessageBox.Ok)
        except OSError as e:
            print e.message
        except KeyboardInterrupt, SystemExit:
            os.kill(Pid, SIGTERM)


def close(self, QCloseEvent):
    print "Hi"
    query = QtSql.QSqlQuery(self.db)
    query.prepare("select name from monitors")
    query.exec_()
    query.next()
    while query.isValid():
        tempList = QtCore.QStringList()
        tempList.append(query.value(0).toString())
        for erase in tempList:
            call(['airmon-ng', 'stop', erase], stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))

    else:
        if os.path.exists(self.working_Dir):
            for f in os.listdir(self.working_Dir):
                os.remove(self.working_Dir + f)
        os.rmdir(self.working_Dir)
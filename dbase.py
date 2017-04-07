#!/usr/bin/env python
import os
from PyQt4 import QtCore, QtSql, QtGui
from subprocess import call


def working_dir():
    from tempfile import mkdtemp
    working_Dir = mkdtemp(prefix='wifern')
    if not working_Dir.endswith(os.sep):
        working_Dir += os.sep
    os.chdir(working_Dir)

def dBaseOpen():
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('attack_session.db')
    db.open()
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
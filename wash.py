import sqlite3
import subprocess
from PyQt4 import QtCore
from subprocess import Popen, PIPE, call

class wash_proccess():

    def wash(self, mon):
        proc = QtCore.QProcess()
        wash = 'wash'
        args = ['-i', mon]
        proc.start(wash, args)
        print(proc.waitForStarted())
        proc.closeWriteChannel()
        proc.setReadChannel(0)
        proc.waitForReadyRead()
        proc.readLineData()
        print(proc.readAllStandardOutput())


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


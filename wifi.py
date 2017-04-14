def get_victim_list(self, csv_filename):
    # Credit for this method goes to the wifite dev team.
    if not os.path.exists(csv_filename): return [], []
    victims = []
    clients = []
    try:
        victim_clients = False
        with open(csv_filename, 'rb') as csvfile:
            victimreader = csv.reader((line.replace('\0', '') for line in csvfile), delimiter=',')
            for row in victimreader:
                if len(row) < 2:
                    continue
                if not victim_clients:
                    if len(row) < 10:
                        continue
                    if row[0].strip() == 'Station MAC':
                        victim_clients = True
                    if row[0].strip() == 'BSSID' or row[0].strip() == 'Station Mac':
                        continue
                    enc = row[5].strip()
                    wps = False
                    if enc.find('OPN'): continue
                    if enc.find('WPA') == -1 and enc.find('WEP') == -1: continue
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
                    t.model = Victim.get_manufacturer(row[0].strip())
                    victims.append(t)
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
    return (victims, clients)


def initscan(self, iface):
    try:
        if iface:
            cmd = ['airodump-ng', '--output-format', 'csv', '--ignore-negative-one', '-w', 'wifern-dump', iface]
            wifi_cmd = Popen(cmd, stdout=PIPE)
            wi = str(wifi_cmd.pid)
            with open('extra1.txt', 'w') as fw:
                fw.write(wi)
                fw.close()
    except:
        pass

  def wifi_sort(self):
        query = QtSql.QSqlQuery(db)
        query.prepare("insert into victims")
        victims, clients = self.get_victim_list('wifern-dump.csv')
        if len(victims) < 1: self.wifi_sort()
        while t < len(victims):
            query.addBindValue(victims[i].bssid.lower())


def get_manufacturer(self, bssid):
    ##################
    # Method works   #
    ##################
    oui_path0 = '/etc/aircrack-ng/airodump-ng-oui.txt'
    oui_path1 = '/usr/local/etc/aircrack-ng/airodump-ng-oui.txt'
    oui_path2 = '/usr/share/aircrack-ng/airodump-ng-oui.txt'
    partial_mac = ''
    model = 'Not Available'

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
                model = ' '.join(oui_db[2:])

    except IOError as a:
        print "I/O error({0}): {1}".format(a.errno, a.strerror)
    except TypeError:
        model = 'Not Available'
    finally:
        return model  # needs to be attached to client before record is displayed

def get_manufacturer(self, bssid):
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
                return model  # need to athached to client before record is displayed
    except IOError as a:
        print "I/O error({0}): {1}".format(a.errno, a.strerror)

def MacGen(self):
    try:
        with open(os.path.expanduser('~') + '/wifern.txt', 'wb') as mac:
            for i in range(0, int(self.mac_gen_lineEdit.text())):
                x = self.randomMAC()
                y = self.get_manufacturer(x)
                print x
                mac.write(x + ',' + y + '\n')
    except ValueError:
        message = QtGui.QMessageBox.information(self, 'Wrong Value', 'Please enter a valid number',
                                                QtGui.QMessageBox.Ok)
        self.mac_gen_lineEdit.setText(" ")
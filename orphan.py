class Orphan:
    def __init__(self):
        self.station = []
        self.orphan_bssid = ''

    def aphistory(self, ap, orphan_bssid):
        self.station.append([ap, orphan_bssid])


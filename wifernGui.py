# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wifern.ui'
#
# Created: Fri Feb 27 14:47:49 2015
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_mainwindow(object):
    def setupUi(self, mainwindow):
        mainwindow.setObjectName(_fromUtf8("mainwindow"))
        mainwindow.resize(1339, 771)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mainwindow.sizePolicy().hasHeightForWidth())
        mainwindow.setSizePolicy(sizePolicy)
        mainwindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtGui.QWidget(mainwindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1331, 771))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setIconSize(QtCore.QSize(30, 30))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.home_tab = QtGui.QWidget()
        self.home_tab.setObjectName(_fromUtf8("home_tab"))
        self.verticalLayoutWidget = QtGui.QWidget(self.home_tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 1311, 721))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setStyleSheet(_fromUtf8(""))
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.my_tableWidget = QtGui.QTableWidget(self.groupBox)
        self.my_tableWidget.setGeometry(QtCore.QRect(0, 120, 271, 571))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.my_tableWidget.setFont(font)
        self.my_tableWidget.setStyleSheet(_fromUtf8("color:rgb(0, 109, 0)"))
        self.my_tableWidget.setFrameShape(QtGui.QFrame.StyledPanel)
        self.my_tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.my_tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.my_tableWidget.setObjectName(_fromUtf8("my_tableWidget"))
        self.my_tableWidget.setColumnCount(3)
        self.my_tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.my_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.my_tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.my_tableWidget.setHorizontalHeaderItem(2, item)
        self.groupBox_2 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(290, 0, 1001, 691))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.groupBox_3 = QtGui.QGroupBox(self.groupBox_2)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 20, 361, 161))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.Get_Wordlist_Button = QtGui.QPushButton(self.groupBox_3)
        self.Get_Wordlist_Button.setGeometry(QtCore.QRect(0, 20, 95, 31))
        self.Get_Wordlist_Button.setObjectName(_fromUtf8("Get_Wordlist_Button"))
        self.sort_wordlist_lineEdit = QtGui.QLineEdit(self.groupBox_3)
        self.sort_wordlist_lineEdit.setGeometry(QtCore.QRect(100, 20, 261, 31))
        self.sort_wordlist_lineEdit.setObjectName(_fromUtf8("sort_wordlist_lineEdit"))
        self.sort_checkBox = QtGui.QCheckBox(self.groupBox_3)
        self.sort_checkBox.setGeometry(QtCore.QRect(100, 60, 61, 26))
        self.sort_checkBox.setObjectName(_fromUtf8("sort_checkBox"))
        self.unique_checkBox = QtGui.QCheckBox(self.groupBox_3)
        self.unique_checkBox.setGeometry(QtCore.QRect(170, 60, 81, 26))
        self.unique_checkBox.setObjectName(_fromUtf8("unique_checkBox"))
        self.pwinspector_checkBox = QtGui.QCheckBox(self.groupBox_3)
        self.pwinspector_checkBox.setGeometry(QtCore.QRect(250, 60, 111, 26))
        self.pwinspector_checkBox.setObjectName(_fromUtf8("pwinspector_checkBox"))
        self.line = QtGui.QFrame(self.groupBox_3)
        self.line.setGeometry(QtCore.QRect(0, 80, 361, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.Process_wordlist_Button = QtGui.QPushButton(self.groupBox_3)
        self.Process_wordlist_Button.setGeometry(QtCore.QRect(0, 50, 95, 31))
        self.Process_wordlist_Button.setObjectName(_fromUtf8("Process_wordlist_Button"))
        self.label_2 = QtGui.QLabel(self.groupBox_3)
        self.label_2.setGeometry(QtCore.QRect(0, 90, 361, 61))
        self.label_2.setToolTip(_fromUtf8(""))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.groupBox_4 = QtGui.QGroupBox(self.groupBox_2)
        self.groupBox_4.setGeometry(QtCore.QRect(370, 0, 631, 321))
        self.groupBox_4.setStyleSheet(_fromUtf8(""))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.label_3 = QtGui.QLabel(self.groupBox_4)
        self.label_3.setGeometry(QtCore.QRect(60, 30, 131, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.wash_tableView = QtGui.QTableView(self.groupBox_4)
        self.wash_tableView.setGeometry(QtCore.QRect(60, 60, 561, 171))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.wash_tableView.setFont(font)
        self.wash_tableView.setAutoFillBackground(True)
        self.wash_tableView.setStyleSheet(_fromUtf8("color:rgb(0, 109, 0)"))
        self.wash_tableView.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed|QtGui.QAbstractItemView.SelectedClicked)
        self.wash_tableView.setDragDropOverwriteMode(False)
        self.wash_tableView.setAlternatingRowColors(True)
        self.wash_tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.wash_tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.wash_tableView.setGridStyle(QtCore.Qt.NoPen)
        self.wash_tableView.setSortingEnabled(True)
        self.wash_tableView.setObjectName(_fromUtf8("wash_tableView"))
        self.reaver_command_label = QtGui.QLabel(self.groupBox_4)
        self.reaver_command_label.setGeometry(QtCore.QRect(0, 268, 611, 31))
        self.reaver_command_label.setObjectName(_fromUtf8("reaver_command_label"))
        self.pushButton_6 = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_6.setGeometry(QtCore.QRect(70, 240, 91, 31))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.lcd_time_Number = QtGui.QLCDNumber(self.groupBox_4)
        self.lcd_time_Number.setGeometry(QtCore.QRect(510, 0, 111, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lcd_time_Number.setFont(font)
        self.lcd_time_Number.setStyleSheet(_fromUtf8("color:rgb(255, 0, 0)"))
        self.lcd_time_Number.setObjectName(_fromUtf8("lcd_time_Number"))
        self.layoutWidget = QtGui.QWidget(self.groupBox_4)
        self.layoutWidget.setGeometry(QtCore.QRect(190, 20, 225, 33))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.Monitor_select_comboBox = QtGui.QComboBox(self.layoutWidget)
        self.Monitor_select_comboBox.setObjectName(_fromUtf8("Monitor_select_comboBox"))
        self.horizontalLayout_2.addWidget(self.Monitor_select_comboBox)
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_2.addWidget(self.label_4)
        self.start_wash_Button = QtGui.QPushButton(self.layoutWidget)
        self.start_wash_Button.setObjectName(_fromUtf8("start_wash_Button"))
        self.horizontalLayout_2.addWidget(self.start_wash_Button)
        self.layoutWidget1 = QtGui.QWidget(self.groupBox_4)
        self.layoutWidget1.setGeometry(QtCore.QRect(190, 240, 429, 28))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.checkBox_4 = QtGui.QCheckBox(self.layoutWidget1)
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.horizontalLayout.addWidget(self.checkBox_4)
        self.checkBox_3 = QtGui.QCheckBox(self.layoutWidget1)
        self.checkBox_3.setStyleSheet(_fromUtf8("color:rgb(0, 109, 0)"))
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.horizontalLayout.addWidget(self.checkBox_3)
        self.checkBox_2 = QtGui.QCheckBox(self.layoutWidget1)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.horizontalLayout.addWidget(self.checkBox_2)
        self.checkBox = QtGui.QCheckBox(self.layoutWidget1)
        self.checkBox.setStyleSheet(_fromUtf8("color:rgb(0, 109, 0)"))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.horizontalLayout.addWidget(self.checkBox)
        self.Interface_groupBox = QtGui.QGroupBox(self.groupBox_2)
        self.Interface_groupBox.setGeometry(QtCore.QRect(10, 190, 331, 171))
        self.Interface_groupBox.setObjectName(_fromUtf8("Interface_groupBox"))
        self.wlan0_monitor_Button = QtGui.QPushButton(self.Interface_groupBox)
        self.wlan0_monitor_Button.setGeometry(QtCore.QRect(150, 70, 121, 31))
        self.wlan0_monitor_Button.setObjectName(_fromUtf8("wlan0_monitor_Button"))
        self.wlan1_monitor_button = QtGui.QPushButton(self.Interface_groupBox)
        self.wlan1_monitor_button.setGeometry(QtCore.QRect(150, 110, 121, 31))
        self.wlan1_monitor_button.setObjectName(_fromUtf8("wlan1_monitor_button"))
        self.list_interfaces_Button = QtGui.QPushButton(self.Interface_groupBox)
        self.list_interfaces_Button.setGeometry(QtCore.QRect(10, 20, 241, 31))
        self.list_interfaces_Button.setObjectName(_fromUtf8("list_interfaces_Button"))
        self.adapters_comboBox = QtGui.QComboBox(self.Interface_groupBox)
        self.adapters_comboBox.setGeometry(QtCore.QRect(10, 70, 131, 31))
        self.adapters_comboBox.setObjectName(_fromUtf8("adapters_comboBox"))
        self.monitors_comboBox = QtGui.QComboBox(self.Interface_groupBox)
        self.monitors_comboBox.setGeometry(QtCore.QRect(10, 110, 131, 31))
        self.monitors_comboBox.setObjectName(_fromUtf8("monitors_comboBox"))
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(10, 20, 271, 101))
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_2.addWidget(self.groupBox)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/home_tab/Home-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.home_tab, icon, _fromUtf8(""))
        self.wifi_tab = QtGui.QWidget()
        self.wifi_tab.setObjectName(_fromUtf8("wifi_tab"))
        self.access_pointScan_Button = QtGui.QPushButton(self.wifi_tab)
        self.access_pointScan_Button.setGeometry(QtCore.QRect(0, 10, 181, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.access_pointScan_Button.setFont(font)
        self.access_pointScan_Button.setObjectName(_fromUtf8("access_pointScan_Button"))
        self.accessPointTable = QtGui.QTableView(self.wifi_tab)
        self.accessPointTable.setGeometry(QtCore.QRect(0, 50, 1041, 611))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.accessPointTable.sizePolicy().hasHeightForWidth())
        self.accessPointTable.setSizePolicy(sizePolicy)
        self.accessPointTable.setStyleSheet(_fromUtf8("color:rgb(0, 109, 0)"))
        self.accessPointTable.setLineWidth(3)
        self.accessPointTable.setAlternatingRowColors(True)
        self.accessPointTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.accessPointTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.accessPointTable.setWordWrap(False)
        self.accessPointTable.setObjectName(_fromUtf8("accessPointTable"))
        self.EncryptionGroupBox = QtGui.QGroupBox(self.wifi_tab)
        self.EncryptionGroupBox.setGeometry(QtCore.QRect(1050, 50, 241, 71))
        self.EncryptionGroupBox.setObjectName(_fromUtf8("EncryptionGroupBox"))
        self.wep_radioButton = QtGui.QRadioButton(self.EncryptionGroupBox)
        self.wep_radioButton.setGeometry(QtCore.QRect(80, 30, 61, 26))
        self.wep_radioButton.setObjectName(_fromUtf8("wep_radioButton"))
        self.wpa_radioButton = QtGui.QRadioButton(self.EncryptionGroupBox)
        self.wpa_radioButton.setGeometry(QtCore.QRect(0, 30, 61, 26))
        self.wpa_radioButton.setObjectName(_fromUtf8("wpa_radioButton"))
        self.wps_radioButton = QtGui.QRadioButton(self.EncryptionGroupBox)
        self.wps_radioButton.setGeometry(QtCore.QRect(160, 30, 71, 26))
        self.wps_radioButton.setObjectName(_fromUtf8("wps_radioButton"))
        self.dictionary_groupBox = QtGui.QGroupBox(self.wifi_tab)
        self.dictionary_groupBox.setGeometry(QtCore.QRect(1050, 130, 241, 91))
        self.dictionary_groupBox.setObjectName(_fromUtf8("dictionary_groupBox"))
        self.dictionary_select_Button = QtGui.QPushButton(self.dictionary_groupBox)
        self.dictionary_select_Button.setGeometry(QtCore.QRect(110, 10, 121, 31))
        self.dictionary_select_Button.setObjectName(_fromUtf8("dictionary_select_Button"))
        self.dict_file_path = QtGui.QLineEdit(self.dictionary_groupBox)
        self.dict_file_path.setGeometry(QtCore.QRect(0, 50, 241, 31))
        self.dict_file_path.setObjectName(_fromUtf8("dict_file_path"))
        self.Clients_Groupbox = QtGui.QGroupBox(self.wifi_tab)
        self.Clients_Groupbox.setGeometry(QtCore.QRect(1050, 230, 231, 141))
        self.Clients_Groupbox.setObjectName(_fromUtf8("Clients_Groupbox"))
        self.Clients_View = QtGui.QScrollArea(self.Clients_Groupbox)
        self.Clients_View.setGeometry(QtCore.QRect(0, 20, 231, 121))
        self.Clients_View.setWidgetResizable(True)
        self.Clients_View.setObjectName(_fromUtf8("Clients_View"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 229, 119))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.Clients_View.setWidget(self.scrollAreaWidgetContents)
        self.toolbox_groupBox = QtGui.QGroupBox(self.wifi_tab)
        self.toolbox_groupBox.setGeometry(QtCore.QRect(1050, 390, 241, 171))
        self.toolbox_groupBox.setObjectName(_fromUtf8("toolbox_groupBox"))
        self.pushButton = QtGui.QPushButton(self.toolbox_groupBox)
        self.pushButton.setGeometry(QtCore.QRect(10, 60, 95, 31))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.label = QtGui.QLabel(self.toolbox_groupBox)
        self.label.setGeometry(QtCore.QRect(0, 20, 241, 41))
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton_2 = QtGui.QPushButton(self.toolbox_groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(110, 60, 95, 31))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.toolbox_groupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 90, 95, 31))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(self.toolbox_groupBox)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 120, 95, 31))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_5 = QtGui.QPushButton(self.toolbox_groupBox)
        self.pushButton_5.setGeometry(QtCore.QRect(110, 90, 95, 31))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/wifi_tab/WiFi.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.wifi_tab, icon1, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        mainwindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(mainwindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        mainwindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainwindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(mainwindow)

    def retranslateUi(self, mainwindow):
        mainwindow.setWindowTitle(QtGui.QApplication.translate("mainwindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("mainwindow", "Program List", None, QtGui.QApplication.UnicodeUTF8))
        item = self.my_tableWidget.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("mainwindow", "Program", None, QtGui.QApplication.UnicodeUTF8))
        item = self.my_tableWidget.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("mainwindow", "Available", None, QtGui.QApplication.UnicodeUTF8))
        item = self.my_tableWidget.horizontalHeaderItem(2)
        item.setText(QtGui.QApplication.translate("mainwindow", "Required", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("mainwindow", "Tools ", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("mainwindow", "Wordlist Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.Get_Wordlist_Button.setText(QtGui.QApplication.translate("mainwindow", "Get Wordlist", None, QtGui.QApplication.UnicodeUTF8))
        self.sort_checkBox.setToolTip(QtGui.QApplication.translate("mainwindow", "Sort the wordlist", None, QtGui.QApplication.UnicodeUTF8))
        self.sort_checkBox.setText(QtGui.QApplication.translate("mainwindow", "Sort", None, QtGui.QApplication.UnicodeUTF8))
        self.unique_checkBox.setToolTip(QtGui.QApplication.translate("mainwindow", "Unique the wordlist. Make sure only unique passwords are contained inside the list.", None, QtGui.QApplication.UnicodeUTF8))
        self.unique_checkBox.setText(QtGui.QApplication.translate("mainwindow", "Unique", None, QtGui.QApplication.UnicodeUTF8))
        self.pwinspector_checkBox.setToolTip(QtGui.QApplication.translate("mainwindow", "<html><head/><body><p>Save some extra time when attacking WPA systems(handshakes) by making sure that ONLY words of length 8 and greater are included.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pwinspector_checkBox.setText(QtGui.QApplication.translate("mainwindow", "Pw Inspector", None, QtGui.QApplication.UnicodeUTF8))
        self.Process_wordlist_Button.setText(QtGui.QApplication.translate("mainwindow", "Execute", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("mainwindow", "Please note that depending on the size of the wordlist these operations will take a long time to complete especially if they are combined ", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("mainwindow", "Reaver", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("mainwindow", "Monitor Interface", None, QtGui.QApplication.UnicodeUTF8))
        self.reaver_command_label.setText(QtGui.QApplication.translate("mainwindow", "Reaver command:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_6.setText(QtGui.QApplication.translate("mainwindow", "Start Reaver", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("mainwindow", "Wash", None, QtGui.QApplication.UnicodeUTF8))
        self.start_wash_Button.setText(QtGui.QApplication.translate("mainwindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_4.setText(QtGui.QApplication.translate("mainwindow", "--auto", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_3.setText(QtGui.QApplication.translate("mainwindow", "--dh-small", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_2.setText(QtGui.QApplication.translate("mainwindow", "--ignore-locks", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("mainwindow", "--no-associate", None, QtGui.QApplication.UnicodeUTF8))
        self.Interface_groupBox.setTitle(QtGui.QApplication.translate("mainwindow", "Available Interfaces", None, QtGui.QApplication.UnicodeUTF8))
        self.wlan0_monitor_Button.setText(QtGui.QApplication.translate("mainwindow", "<- Monitor Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.wlan1_monitor_button.setText(QtGui.QApplication.translate("mainwindow", "<- Use This", None, QtGui.QApplication.UnicodeUTF8))
        self.list_interfaces_Button.setText(QtGui.QApplication.translate("mainwindow", "List Wireless Interfaces", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("mainwindow", "This is a list of programs that are required for the application to run smothly and some programs that help you with diferent aspects of your network testing.", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.home_tab), QtGui.QApplication.translate("mainwindow", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.access_pointScan_Button.setText(QtGui.QApplication.translate("mainwindow", "Scan for Access Points", None, QtGui.QApplication.UnicodeUTF8))
        self.EncryptionGroupBox.setTitle(QtGui.QApplication.translate("mainwindow", "Encryption", None, QtGui.QApplication.UnicodeUTF8))
        self.wep_radioButton.setText(QtGui.QApplication.translate("mainwindow", "WEP", None, QtGui.QApplication.UnicodeUTF8))
        self.wpa_radioButton.setText(QtGui.QApplication.translate("mainwindow", "WPA", None, QtGui.QApplication.UnicodeUTF8))
        self.wps_radioButton.setText(QtGui.QApplication.translate("mainwindow", "WPS", None, QtGui.QApplication.UnicodeUTF8))
        self.dictionary_groupBox.setTitle(QtGui.QApplication.translate("mainwindow", "Dictionary", None, QtGui.QApplication.UnicodeUTF8))
        self.dictionary_select_Button.setText(QtGui.QApplication.translate("mainwindow", "Dictionary Select", None, QtGui.QApplication.UnicodeUTF8))
        self.Clients_Groupbox.setTitle(QtGui.QApplication.translate("mainwindow", "Clients", None, QtGui.QApplication.UnicodeUTF8))
        self.toolbox_groupBox.setTitle(QtGui.QApplication.translate("mainwindow", "ToolBox", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("mainwindow", "Aircrack-ng", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("mainwindow", "Select the tool you wood like to use to attack the access point(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("mainwindow", "Pyrit", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("mainwindow", "Reaver", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("mainwindow", "Mdk3", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("mainwindow", "Bully", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.wifi_tab), QtGui.QApplication.translate("mainwindow", "Wifi Attack", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("mainwindow", "Page", None, QtGui.QApplication.UnicodeUTF8))

import wifern_rc

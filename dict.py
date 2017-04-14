

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
        self.wordlist_path = str(filename)  # Delete after test
        self.dict_file_path.setEnabled(False)
    else:
        message = QtGui.QMessageBox.information(self, 'Select File', 'You must select a file', QtGui.QMessageBox.ok)

    def Sort_Wordlist(self):
        try:
            self.sort_wordlist_lineEdit.setText("")
            get_wordlist_for_sorting = QtGui.QFileDialog.getOpenFileName(self, 'Select Dictionary', '/root/',
                                                                         'Text files (*.txt);; List files (*.lst)')
            if get_wordlist_for_sorting:
                self.wordlist_save_button.setEnabled(True)
                filename = get_wordlist_for_sorting
                self.sort_wordlist_lineEdit.setText(filename)
                self.wordlist = os.path.basename(str(filename))
                self.wordlist_path = str(filename)
                self.sort_wordlist_lineEdit.setEnabled(False)
            else:
                self.sort_wordlist_lineEdit.setText("")
                self.Process_wordlist_Button.setEnabled(False)
                self.wordlist = ''
                self.wordlist_save_button.setEnabled(False)

        except:
            pass

    def saveWordlist(self):
        try:
            if self.saveLineEdit.text() != None:
                save_wordlist = QtGui.QFileDialog.getSaveFileName(self, 'Save Wordlist', '/root/',
                                                                  'Text Files (*.txt);;List Files (*.lst)')
                if save_wordlist:
                    self.savewordlist = save_wordlist
                    self.saveLineEdit.setText(self.savewordlist)
                    self.Process_wordlist_Button.setEnabled(True)
                else:
                    self.Process_wordlist_Button.setEnabled(False)
            else:
                save_wordlist = QtGui.QFileDialog.getSaveFileName(self, 'Save Wordlist', '/root/',
                                                                  'Text Files (*.txt);;List Files (*.lst)')
        except AttributeError:
            message = QtGui.QMessageBox.information(self, 'No Wordlist', 'You Must select a wordlist first',
                                                    QtGui.QMessageBox.Ok)

    def process_wordlist(self):
        try:
            if self.saveLineEdit.text() != None:
                self.wordlist_path == self.saveLineEdit.text()
            if self.sort_checkBox.isChecked() and not self.pwinspector_checkBox.isChecked():
                sort = Popen(['sort', '-u', self.wordlist_path, '-o', self.savewordlist], stdout=PIPE)
                ## sorts and stores unique occurrences
                self.Process_wordlist_Button.setEnabled(True)
            elif self.sort_checkBox.isChecked() and self.pwinspector_checkBox.isChecked():
                sort = Popen(['sort', '-u', self.wordlist_path], stdout=PIPE)
                pwi = Popen(['pw-inspector', '-m', '8', '-M', '63', '-o', self.savewordlist], stdin=sort.stdout,
                            stdout=PIPE)
                sort.stdout.close()

            elif self.pwinspector_checkBox.isChecked():
                cmd = Popen(['pw-inspector', '-i', self.wordlist_path, '-m', '8', '-M', '63', '-o', self.savewordlist])
        except:
            print 'Error'
            # p1 = Popen(["dmesg"], stdout=PIPE)
            # p2 = Popen(["grep", "hda"], stdin=p1.stdout, stdout=PIPE)
            # p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
            # output = p2.communicate()[0]
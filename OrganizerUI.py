import sys

from PyQt5.QtCore import Qt, QCoreApplication

import dataAccess

from PyQt5.QtWidgets import QWidget, QApplication, QTabWidget, QFormLayout, QLineEdit, QHBoxLayout, QRadioButton, \
    QLabel, QCheckBox, QPushButton, QTextEdit, QGridLayout, QDialog, QComboBox


class Organizer(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(550, 250, 800, 600)
        self.setWindowTitle('Organizer')

        layout = QFormLayout()

        self.tabWidget1 = QTabWidget()
        self.tabWidget2 = QTabWidget()

        layout.addRow(self.tabWidget1)
        layout.addRow(self.tabWidget2)

        self.showCompetition()
        self.eventUI()
        self.recordUI()

        self.setLayout(layout)
        # self.show()


    # tag 1 Competition
    def showCompetition(self):
        self.tab1 = QWidget()
        self.tabWidget1.addTab(self.tab1, "Competition")

        layout = QFormLayout()
        hbox = QHBoxLayout()
        t_cid = QTextEdit('cid')
        t_info = QTextEdit('info')
        t_cname = QTextEdit('cname')
        t_from = QTextEdit('from')
        t_to = QTextEdit('to')

        titles = []
        titles.append(t_cid)
        titles.append(t_info)
        titles.append(t_cname)
        titles.append(t_from)
        titles.append(t_to)

        t_cid.setFixedSize(50, 24)
        t_info.setFixedSize(250, 24)
        t_cname.setFixedSize(250, 24)
        t_from.setFixedSize(80, 24)
        t_to.setFixedSize(80, 24)

        for t in titles:
            t.setDisabled(True)
            hbox.addWidget(t)

        layout.addRow(hbox)

        self.competitions = []
        competitions = dataAccess.getCompetition()
        for c in competitions:
            gridlayout = QGridLayout()
            gridlayout.setSpacing(5)
            cid = QTextEdit(str(c[0]))
            info = QTextEdit(c[1])
            cname = QTextEdit(c[2])
            from_time = QTextEdit(c[3].strftime("%Y/%m/%d"))
            to_time = QTextEdit(c[4].strftime("%Y/%m/%d"))

            row = []
            row.append(cid)
            row.append(info)
            row.append(cname)
            row.append(from_time)
            row.append(to_time)

            self.competitions.append(row)

            cid.setFixedSize(50, 24)
            info.setFixedSize(250, 48)
            cname.setFixedSize(250, 48)
            from_time.setFixedSize(80,24)
            to_time.setFixedSize(80,24)

            i = 0
            for each in row:
                each.setDisabled(True)
                gridlayout.addWidget(each, 0, i)
                i = i + 1

            layout.addRow(gridlayout)

        self.changeBtn = QPushButton("change")
        self.changeBtn.clicked.connect(self.change)
        self.add = QPushButton("add")
        self.add.clicked.connect(self.addCompetition)
        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(self.changeBtn)
        hbox2.addWidget(self.add)
        hbox2.addStretch(1)

        layout.addRow(hbox2)
        self.tabWidget1.setTabText(0, 'Competition')
        self.tab1.setLayout(layout)

    def change(self):
        if self.changeBtn.text() == "change":
            for row in self.competitions:
                for each in row:
                    each.setDisabled(False)
            self.changeBtn.setText("save")
        else:
            self.changeCompetitionInfo()
            # for row in self.competitions:
            #     for each in row:
            #         each.setDisabled(True)
            self.tabWidget1.clear()
            self.showCompetition()
            self.tabWidget2.clear()
            self.eventUI()
            self.recordUI()
            self.changeBtn.setText("change")

    def addCompetition(self):
        dialog = QDialog()
        dialog.resize(400, 300)
        layout = QFormLayout()
        self.infoAddEdit = QLineEdit()
        self.cnameAddEdit = QLineEdit()
        self.from_timeAddEdit = QLineEdit()
        self.to_timeAddEdit = QLineEdit()
        button = QPushButton('add')
        button.clicked.connect(self.addBtn)
        button.clicked.connect(dialog.close)

        layout.addRow('info', self.infoAddEdit)
        layout.addRow('cname', self.cnameAddEdit)
        layout.addRow('from_time',self.from_timeAddEdit)
        layout.addRow('to_time', self.to_timeAddEdit)
        layout.addWidget(button)

        dialog.setLayout(layout)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def addBtn(self):
        info = self.infoAddEdit.text()
        cname = self.cnameAddEdit.text()
        from_time = self.from_timeAddEdit.text()
        to_time = self.to_timeAddEdit.text()
        # print(info, cname, from_time, to_time)
        dataAccess.addCompetition(info, cname, from_time, to_time)
        self.tabWidget1.clear()
        self.showCompetition()

    def changeCompetitionInfo(self):
        for c in self.competitions:
            cid = int(c[0].toPlainText())
            info = c[1].toPlainText()
            cname = c[2].toPlainText()
            from_time = c[3].toPlainText()
            to_time = c[4].toPlainText()

            dataAccess.changeCompetition(cid, info, cname, from_time, to_time)
            # print(cid, info, cname, from_time, to_time)

    # tag 1.1 Competition Event
    def getCompetitionNames(self):
        competitions = dataAccess.getCompetition()
        names = []
        for c in competitions:
            names.append(c[2])

        return names


    def eventUI(self):
        self.tab2 = QWidget()
        self.tabWidget2.addTab(self.tab2, "Events")
        layout = QFormLayout()

        self.eventComboBox = QComboBox()
        self.eventComboBox.addItem("select...")
        self.eventComboBox.addItems(self.getCompetitionNames())
        self.eventComboBox.setCurrentIndex(0)
        self.eventComboBox.currentIndexChanged.connect(self.showevent)
        layout.addRow('select a competition:', self.eventComboBox)

        hbox = QHBoxLayout()
        events = dataAccess.getEvents()
        self.checkBoxes = []
        for each in events:
            hbox.addStretch(1)
            checkBox = QCheckBox(each[1])
            self.checkBoxes.append(checkBox)
            hbox.addWidget(checkBox)
            checkBox.setDisabled(True)
        layout.addRow("Events:", hbox)

        self.eventsButton = QPushButton("change")
        self.eventsButton.clicked.connect(self.changeevents)
        layout.addWidget(self.eventsButton)

        self.tabWidget2.setTabText(1, 'Events')
        self.tab2.setLayout(layout)

    def changeevents(self):
        if self.eventsButton.text() == "change":
            for each in self.checkBoxes:
                each.setDisabled(False)
            self.eventsButton.setText("save")
        else:
            self.addEvent()
            self.deleteEvent()
            for each in self.checkBoxes:
                each.setDisabled(True)
            self.eventsButton.setText("change")


    def showevent(self, i):
        competition = self.eventComboBox.currentText()
        events = dataAccess.getCompetitionEvents(competition)
        for each in self.checkBoxes:
            each.setChecked(False)
            if each.text() in events:
                each.setChecked(True)

    def addEvent(self):
        competition = self.eventComboBox.currentText()
        events = dataAccess.getCompetitionEvents(competition)
        for each in self.checkBoxes:
            if each.isChecked() == True:
                if each.text() not in events:
                    dataAccess.addEvent(each.text(), competition)

    def deleteEvent(self):
        competition = self.eventComboBox.currentText()
        events = dataAccess.getCompetitionEvents(competition)
        for each in self.checkBoxes:
            if each.isChecked() == False:
                if each.text() in events:
                    dataAccess.deleteEvent(each.text(), competition)

    # tag 1.2 Competition Record
    def recordUI(self):
        self.tab3 = QWidget()
        self.tabWidget2.addTab(self.tab3, "Records")
        self.recordLayout = QFormLayout()

        self.recordComboBoxCom = QComboBox()
        self.recordComboBoxCom.addItem("select...")
        self.recordComboBoxCom.addItems(self.getCompetitionNames())
        self.recordComboBoxCom.setCurrentIndex(0)
        self.recordComboBoxCom.currentIndexChanged.connect(self.getShowCompetitionEvents)
        self.recordLayout.addRow('select a competition:', self.recordComboBoxCom)

        self.recordComboBoxEvent = QComboBox()
        self.recordComboBoxEvent.addItem("select...")
        self.recordComboBoxEvent.setCurrentIndex(0)
        self.recordComboBoxEvent.currentIndexChanged.connect(self.showCompetitionRecord)
        self.recordLayout.addRow('select an event:', self.recordComboBoxEvent)

        # titles
        rank = QLabel("rank".center(10))
        WCAid = QLabel("WCAid".center(10))
        name = QLabel("name".center(20))
        avg = QLabel("average".center(20))
        best = QLabel("best".center(20))
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(rank)
        hbox.addStretch(1)
        hbox.addWidget(WCAid)
        hbox.addStretch(1)
        hbox.addWidget(name)
        hbox.addStretch(1)
        hbox.addWidget(avg)
        hbox.addStretch(1)
        hbox.addWidget(best)
        hbox.addStretch(1)
        self.recordLayout.addRow(hbox)

        self.record = QFormLayout()
        self.recordLayout.addRow(self.record)

        self.recordButtons = QHBoxLayout()
        self.recordLayout.addRow(self.recordButtons)

        self.tabWidget2.setTabText(2, 'Records')
        self.tab3.setLayout(self.recordLayout)


    def getShowCompetitionEvents(self):
        if self.recordComboBoxCom.currentText() == "select...":
            # self.tabWidget2.removeTab(self.tab3)
            # self.recordUI()
            self.recordLayout.removeRow(self.record)
            self.recordLayout.removeRow(self.recordButtons)
            self.record = QFormLayout()
            self.recordComboBoxEvent.currentIndexChanged.disconnect(self.showCompetitionRecord)
            self.recordComboBoxEvent.clear()
            self.recordComboBoxEvent.addItem("select...")
            self.recordComboBoxEvent.setCurrentIndex(0)
            self.recordComboBoxEvent.currentIndexChanged.connect(self.showCompetitionRecord)
            return
        competition = self.recordComboBoxCom.currentText()
        self.recordComboBoxEvent.clear()
        # self.recordComboBoxEvent.addItem("select...")
        self.recordComboBoxEvent.addItems(dataAccess.getCompetitionEvents(competition))

    def showCompetitionRecord(self):
        competition = self.recordComboBoxCom.currentText()
        event = self.recordComboBoxEvent.currentText()

        self.records = dataAccess.getCompetitionRecord(event, competition)

        # clear self.record
        self.recordLayout.removeRow(self.record)
        self.recordLayout.removeRow(self.recordButtons)
        self.record = QFormLayout()

        self.ranksLabels = []

        i=1
        for record in self.records:
            row = []
            hbox = QHBoxLayout()
            rankLabel = QLabel(str(i).center(10))
            WCAidLabel = QLabel(str(record[0]).center(10))
            nameLabel = QLabel(record[1].center(20))
            avgLabel = QLabel(str(record[2]).center(20))
            bestLabel = QLabel(str(record[3]).center(20))

            row.append(rankLabel)
            row.append(WCAidLabel)
            row.append(nameLabel)
            row.append(avgLabel)
            row.append(bestLabel)
            self.ranksLabels.append(row)

            hbox.addStretch(1)
            hbox.addWidget(rankLabel)
            hbox.addStretch(1)
            hbox.addWidget(WCAidLabel)
            hbox.addStretch(1)
            hbox.addWidget(nameLabel)
            hbox.addStretch(1)
            hbox.addWidget(avgLabel)
            hbox.addStretch(1)
            hbox.addWidget(bestLabel)
            hbox.addStretch(1)

            self.record.addRow(hbox)
            i = i + 1
        self.recordLayout.addRow(self.record)

        # buttons
        self.recordButtons = QHBoxLayout()
        self.recordChangeButton = QPushButton("change")
        self.recordChangeButton.clicked.connect(self.changeCompetitionRecord)
        self.recordAddButton = QPushButton("add")
        self.recordAddButton.clicked.connect(self.addCompetitionRecord)
        self.recordDeleteButton = QPushButton("delete")
        self.recordDeleteButton.clicked.connect(self.deleteCompetitionRecord)
        self.recordButtons.addStretch(1)
        self.recordButtons.addWidget(self.recordChangeButton)
        self.recordButtons.addStretch(1)
        self.recordButtons.addWidget(self.recordAddButton)
        self.recordButtons.addStretch(1)
        self.recordButtons.addWidget(self.recordDeleteButton)
        self.recordButtons.addStretch(1)
        self.recordLayout.addRow(self.recordButtons)

    def addCompetitionRecord(self):
        dialog = QDialog()
        dialog.resize(200, 100)

        formLayout = QFormLayout()

        self.WCAidLineEdit = QLineEdit()
        self.avgLineEdit = QLineEdit()
        self.bestLineEdit = QLineEdit()
        formLayout.addRow("WCAid:", self.WCAidLineEdit)
        formLayout.addRow("avg:", self.avgLineEdit)
        formLayout.addRow("best:", self.bestLineEdit)
        self.recordSaveButton = QPushButton("save")
        self.recordSaveButton.clicked.connect(dialog.close)
        self.recordSaveButton.clicked.connect(self.recordAdd)
        formLayout.addRow(self.recordSaveButton)

        dialog.setWindowTitle("add")
        dialog.setLayout(formLayout)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()


    def recordAdd(self):
        WCAid = int(self.WCAidLineEdit.text())
        competition = self.recordComboBoxCom.currentText()
        event = self.recordComboBoxEvent.currentText()
        avg = self.avgLineEdit.text()
        best = self.bestLineEdit.text()

        print(WCAid, competition, event, avg, best)
        dataAccess.saveCompetitionRecord(WCAid, competition, event, avg, best)
        self.showCompetitionRecord()


    def changeCompetitionRecord(self):
        dialog = QDialog()
        dialog.resize(200, 100)

        formLayout = QFormLayout()
        self.recordChangeComboBox = QComboBox()
        for record in self.records:
            self.recordChangeComboBox.addItem(str(record[0]))
        self.recordChangeComboBox.currentIndexChanged.connect(self.recordChangeComboBoxchange)
        formLayout.addRow("WCAid:", self.recordChangeComboBox)

        self.avgLineEdit = QLineEdit()
        self.bestLineEdit = QLineEdit()
        WCAid = int(self.recordChangeComboBox.currentText())
        for record in self.records:
            if WCAid == record[0]:
                self.avgLineEdit.setText(str(record[2]))
                self.bestLineEdit.setText(str(record[3]))
                break
        formLayout.addRow("avg:", self.avgLineEdit)
        formLayout.addRow("best:", self.bestLineEdit)
        self.recordSaveButton = QPushButton("save")
        self.recordSaveButton.clicked.connect(dialog.close)
        self.recordSaveButton.clicked.connect(self.recordSave)
        formLayout.addRow(self.recordSaveButton)

        dialog.setWindowTitle("change")
        dialog.setLayout(formLayout)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def recordChangeComboBoxchange(self):
        WCAid = int(self.recordChangeComboBox.currentText())
        for record in self.records:
            if WCAid == record[0]:
                self.avgLineEdit.setText(str(record[2]))
                self.bestLineEdit.setText(str(record[3]))
                break

    def recordSave(self):
        WCAid = int(self.recordChangeComboBox.currentText())
        competition = self.recordComboBoxCom.currentText()
        event = self.recordComboBoxEvent.currentText()
        avg = self.avgLineEdit.text()
        best = self.bestLineEdit.text()

        dataAccess.changeCompetitionRecord(WCAid, competition, event, avg, best)
        self.showCompetitionRecord()

    def deleteCompetitionRecord(self):
        dialog = QDialog()
        dialog.resize(200, 100)

        formLayout = QFormLayout()
        self.recordDeleteComboBox = QComboBox()
        for record in self.records:
            self.recordDeleteComboBox.addItem(str(record[0]))

        self.deleteRecordButton = QPushButton("delete")
        self.deleteRecordButton.clicked.connect(dialog.close)
        self.deleteRecordButton.clicked.connect(self.deleteRecord)
        formLayout.addRow("WCAid:", self.recordDeleteComboBox)
        formLayout.addRow(self.deleteRecordButton)

        dialog.setWindowTitle("delete")
        dialog.setLayout(formLayout)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def deleteRecord(self):
        WCAid = int(self.recordDeleteComboBox.currentText())
        competition = self.recordComboBoxCom.currentText()
        event = self.recordComboBoxEvent.currentText()

        print(WCAid, competition, event)
        dataAccess.deleteCompetitionRecord(WCAid, competition, event)
        self.showCompetitionRecord()



def setup():
    app = QApplication(sys.argv)
    ex = Organizer()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    setup()
    pass
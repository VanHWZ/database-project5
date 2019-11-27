import sys
import dataAccess

from PyQt5.QtWidgets import QWidget, QApplication, QFormLayout, QTabWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, \
    QTextEdit, QGridLayout, QComboBox


class Competitor(QWidget):

    def __init__(self, WCAid):
        super().__init__()
        self.WCAid = WCAid

    def setWCAid(self, id):
        self.WCAid = id
        self.initUI()

    def initUI(self):
        self.setGeometry(550, 250, 800, 600)
        self.setWindowTitle('Competitor')

        layout = QFormLayout()

        self.tabWidget1 = QTabWidget()

        layout.addRow(self.tabWidget1)

        self.InfoUI()
        self.competitionUI()
        self.competitorUI()
        self.rankUI()

        self.setLayout(layout)
        # self.show()

    # tag 1 Info
    def InfoUI(self):
        self.tab1 = QWidget()
        self.tabWidget1.addTab(self.tab1, "Info")

        layout = QFormLayout()

        self.WCAidEdit = QLineEdit(self.WCAid)
        self.nameEdit = QLineEdit()
        self.regionEdit = QLineEdit()
        self.passwordEdit = QLineEdit()

        self.WCAidEdit.setDisabled(True)
        self.nameEdit.setDisabled(True)
        self.regionEdit.setDisabled(True)
        self.passwordEdit.setDisabled(True)

        self.changeInfoButton = QPushButton("change")
        self.changeInfoButton.clicked.connect(self.changeCompetitorInfo)

        layout.addRow("WCAid:", self.WCAidEdit)
        layout.addRow("name:", self.nameEdit)
        layout.addRow("region:", self.regionEdit)
        layout.addRow("password:", self.passwordEdit)
        layout.addRow(self.changeInfoButton)

        self.showCompetitorInfo()

        self.tabWidget1.setTabText(0, 'Info')
        self.tab1.setLayout(layout)

    def showCompetitorInfo(self):
        info = dataAccess.getCompetitorInfo(self.WCAid)
        self.WCAidEdit.setText(str(info[0]))
        self.nameEdit.setText(info[2])
        self.regionEdit.setText(info[1])
        self.passwordEdit.setText(info[3])

    def changeCompetitorInfo(self):
        if self.changeInfoButton.text() == "change":
            self.nameEdit.setDisabled(False)
            self.regionEdit.setDisabled(False)
            self.passwordEdit.setDisabled(False)
            self.changeInfoButton.setText("save")
        else:
            self.nameEdit.setDisabled(True)
            self.regionEdit.setDisabled(True)
            self.passwordEdit.setDisabled(True)
            region = self.regionEdit.text()
            name = self.nameEdit.text()
            password = self.passwordEdit.text()
            dataAccess.changeCompetitorInfo(self.WCAid, region, name, password)
            self.changeInfoButton.setText("change")

    # tag 2 Competition
    def competitionUI(self):
        self.tab2 = QWidget()
        self.tabWidget1.addTab(self.tab2, "Competition")

        self.competitionLayout = QFormLayout()
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

        self.competitionLayout.addRow(hbox)

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
            from_time.setFixedSize(80, 24)
            to_time.setFixedSize(80, 24)

            i = 0
            for each in row:
                each.setDisabled(True)
                gridlayout.addWidget(each, 0, i)
                i = i + 1

            self.competitionLayout.addRow(gridlayout)


        self.competitionRecordUI()

        self.record = QFormLayout()
        self.recordLayout.addRow(self.record)

        self.tabWidget1.setTabText(1, 'Competition')
        self.tab2.setLayout(self.competitionLayout)


    # tag 2.1 Competition Record
    def competitionRecordUI(self):
        self.recordWidget = QWidget()
        self.competitionLayout.addRow(self.recordWidget)
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

        self.recordWidget.setLayout(self.recordLayout)

    def showCompetitionRecord(self):
        competition = self.recordComboBoxCom.currentText()
        event = self.recordComboBoxEvent.currentText()
        self.records = dataAccess.getCompetitionRecord(event, competition)

        # clear self.record
        self.recordLayout.removeRow(self.record)
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

    def getShowCompetitionEvents(self):
        if self.recordComboBoxCom.currentText() == "select...":
            self.recordComboBoxEvent.currentIndexChanged.disconnect(self.showCompetitionRecord)
            self.recordComboBoxEvent.clear()
            self.recordComboBoxEvent.addItem("select...")
            self.recordComboBoxEvent.setCurrentIndex(0)
            self.recordComboBoxEvent.currentIndexChanged.connect(self.showCompetitionRecord)
            return

        # clear record content
        self.recordLayout.removeRow(self.record)
        self.record = QFormLayout()

        competition = self.recordComboBoxCom.currentText()
        self.recordComboBoxEvent.currentIndexChanged.disconnect(self.showCompetitionRecord)
        self.recordComboBoxEvent.clear()
        self.recordComboBoxEvent.addItem("select...")
        self.recordComboBoxEvent.addItems(dataAccess.getCompetitionEvents(competition))
        self.recordComboBoxEvent.currentIndexChanged.connect(self.showCompetitionRecord)


    def getCompetitionNames(self):
        competitions = dataAccess.getCompetition()
        names = []
        for c in competitions:
            names.append(c[2])
        return names


    # tag 3 Competitor
    def competitorUI(self):
        self.tab3 = QWidget()
        self.tabWidget1.addTab(self.tab3, "Competitor")

        self.competitorLayout = QFormLayout()

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Input WCAid:"))
        self.searchLineEdit = QLineEdit()
        hbox.addWidget(self.searchLineEdit)
        self.searchButton = QPushButton("search")
        self.searchButton.clicked.connect(self.showCompetitorRecord)
        hbox.addWidget(self.searchButton)
        self.competitorLayout.addItem(hbox)

        self.competitorRecordLayout = QFormLayout()
        self.competitorLayout.addRow(self.competitorRecordLayout)

        self.tabWidget1.setTabText(2, 'Competitor')
        self.tab3.setLayout(self.competitorLayout)


    def showCompetitorRecord(self):
        WCAid = self.searchLineEdit.text()
        try:
            int(WCAid)
        except:
            self.competitorLayout.removeRow(self.competitorRecordLayout)
            return
        records = dataAccess.searchCompetitor(WCAid)
        self.competitorLayout.removeRow(self.competitorRecordLayout)
        self.competitorRecordLayout = QFormLayout()
        # print(records)

        eventLabel = QLabel("Event".center(30))
        avgLabel = QLabel("average".center(20))
        avgRankLabel = QLabel("avg wr".center(20))
        bestLabel = QLabel("best".center(20))
        bestRankLabel = QLabel("best wr".center(20))

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(eventLabel)
        hbox.addStretch(1)
        hbox.addWidget(avgLabel)
        hbox.addStretch(1)
        hbox.addWidget(avgRankLabel)
        hbox.addStretch(1)
        hbox.addWidget(bestLabel)
        hbox.addStretch(1)
        hbox.addWidget(bestRankLabel)
        hbox.addStretch(1)

        self.competitorRecordLayout.addRow(hbox)

        for record in records:
            temphbox = QHBoxLayout()
            event = QLabel(record[0].center(30))
            avg = QLabel(str(record[1]).center(20))
            avgRank = QLabel(str(record[3]).center(20))
            best = QLabel(str(record[2]).center(20))
            bestRank = QLabel(str(record[4]).center(20))
            temphbox.addStretch(1)
            temphbox.addWidget(event)
            temphbox.addStretch(1)
            temphbox.addWidget(avg)
            temphbox.addStretch(1)
            temphbox.addWidget(avgRank)
            temphbox.addStretch(1)
            temphbox.addWidget(best)
            temphbox.addStretch(1)
            temphbox.addWidget(bestRank)
            temphbox.addStretch(1)

            self.competitorRecordLayout.addRow(temphbox)

        self.competitorLayout.addRow(self.competitorRecordLayout)


    # tag 4 Rank
    def rankUI(self):
        self.tab4 = QWidget()
        self.tabWidget1.addTab(self.tab4, "Rank")

        self.rankLayout = QFormLayout()

        self.rankComboBoxRegion = QComboBox()
        self.rankComboBoxRegion.addItem("select...")
        self.rankComboBoxRegion.addItem("World")
        self.rankComboBoxRegion.addItems(dataAccess.getRegions())
        self.rankComboBoxRegion.currentIndexChanged.connect(self.rankComboBoxRegionChange)
        self.rankLayout.addRow("select region:", self.rankComboBoxRegion)

        self.rankComboBoxEvent = QComboBox()
        self.rankComboBoxEvent.addItem("select...")
        self.rankComboBoxEvent.addItems(self.getEventNames())
        self.rankComboBoxEvent.currentIndexChanged.connect(self.rankComboBoxEventChange)
        self.rankLayout.addRow("select event:", self.rankComboBoxEvent)

        self.rank = QFormLayout()
        self.rankLayout.addRow(self.rank)

        self.tabWidget1.setTabText(3, 'Rank')
        self.tab4.setLayout(self.rankLayout)

    def getEventNames(self):
        events = dataAccess.getEvents()
        names = []
        for each in events:
            names.append(each[1])
        return names

    def rankComboBoxRegionChange(self):
        if self.rankComboBoxEvent.currentText() == "select..." or self.rankComboBoxRegion.currentText() == "select...":
            return
        self.showRank()

    def rankComboBoxEventChange(self):
        if self.rankComboBoxEvent.currentText() == "select..." or self.rankComboBoxRegion.currentText() == "select...":
            return
        self.showRank()

    def showRank(self):
        selected = self.rankComboBoxRegion.currentText()
        self.rankLayout.removeRow(self.rank)
        if selected == "World":
            self.showWorldRank()
        else:
            self.showRegionRank()

    def showWorldRank(self):
        event = self.rankComboBoxEvent.currentText()
        rank = dataAccess.getWorldRank(event)
        # avg
        rankLabel = QLabel("Rank".center(20))
        WCAidLabel = QLabel("WCAid".center(20))
        nameLabel = QLabel("Name".center(20))
        avgLabel = QLabel("Average".center(20))

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(rankLabel)
        hbox.addStretch(1)
        hbox.addWidget(WCAidLabel)
        hbox.addStretch(1)
        hbox.addWidget(nameLabel)
        hbox.addStretch(1)
        hbox.addWidget(avgLabel)
        hbox.addStretch(1)

        self.rank = QFormLayout()
        self.rank.addRow(hbox)

        i = 1
        for each in rank[0]:
            temphbox = QHBoxLayout()
            rankLabel = QLabel(str(i).center(20))
            WCAidLabel = QLabel(str(each[0]).center(20))
            nameLabel = QLabel(each[1].center(20))
            avgLabel = QLabel(str(each[2]).center(20))

            temphbox.addStretch(1)
            temphbox.addWidget(rankLabel)
            temphbox.addStretch(1)
            temphbox.addWidget(WCAidLabel)
            temphbox.addStretch(1)
            temphbox.addWidget(nameLabel)
            temphbox.addStretch(1)
            temphbox.addWidget(avgLabel)
            temphbox.addStretch(1)

            self.rank.addRow(temphbox)
            i = i + 1

        # best
        rankLabel = QLabel("Rank".center(20))
        WCAidLabel = QLabel("WCAid".center(20))
        nameLabel = QLabel("Name".center(20))
        avgLabel = QLabel("Best".center(20))

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(rankLabel)
        hbox.addStretch(1)
        hbox.addWidget(WCAidLabel)
        hbox.addStretch(1)
        hbox.addWidget(nameLabel)
        hbox.addStretch(1)
        hbox.addWidget(avgLabel)
        hbox.addStretch(1)

        self.rank.addRow(hbox)

        i = 1
        for each in rank[1]:
            temphbox = QHBoxLayout()
            rankLabel = QLabel(str(i).center(20))
            WCAidLabel = QLabel(str(each[0]).center(20))
            nameLabel = QLabel(each[1].center(20))
            avgLabel = QLabel(str(each[2]).center(20))

            temphbox.addStretch(1)
            temphbox.addWidget(rankLabel)
            temphbox.addStretch(1)
            temphbox.addWidget(WCAidLabel)
            temphbox.addStretch(1)
            temphbox.addWidget(nameLabel)
            temphbox.addStretch(1)
            temphbox.addWidget(avgLabel)
            temphbox.addStretch(1)

            self.rank.addRow(temphbox)
            i = i + 1

        self.rankLayout.addRow(self.rank)

    def showRegionRank(self):
        region = self.rankComboBoxRegion.currentText()
        event = self.rankComboBoxEvent.currentText()
        rank = dataAccess.getRegionRank(event, region)
        # avg
        rankLabel = QLabel("Rank".center(20))
        WCAidLabel = QLabel("WCAid".center(20))
        nameLabel = QLabel("Name".center(20))
        avgLabel = QLabel("Average".center(20))

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(rankLabel)
        hbox.addStretch(1)
        hbox.addWidget(WCAidLabel)
        hbox.addStretch(1)
        hbox.addWidget(nameLabel)
        hbox.addStretch(1)
        hbox.addWidget(avgLabel)
        hbox.addStretch(1)

        self.rank = QFormLayout()
        self.rank.addRow(hbox)

        i = 1
        for each in rank[0]:
            temphbox = QHBoxLayout()
            rankLabel = QLabel(str(i).center(20))
            WCAidLabel = QLabel(str(each[0]).center(20))
            nameLabel = QLabel(each[1].center(20))
            avgLabel = QLabel(str(each[2]).center(20))

            temphbox.addStretch(1)
            temphbox.addWidget(rankLabel)
            temphbox.addStretch(1)
            temphbox.addWidget(WCAidLabel)
            temphbox.addStretch(1)
            temphbox.addWidget(nameLabel)
            temphbox.addStretch(1)
            temphbox.addWidget(avgLabel)
            temphbox.addStretch(1)

            self.rank.addRow(temphbox)

        # best
        rankLabel = QLabel("Rank".center(20))
        WCAidLabel = QLabel("WCAid".center(20))
        nameLabel = QLabel("Name".center(20))
        avgLabel = QLabel("Best".center(20))

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(rankLabel)
        hbox.addStretch(1)
        hbox.addWidget(WCAidLabel)
        hbox.addStretch(1)
        hbox.addWidget(nameLabel)
        hbox.addStretch(1)
        hbox.addWidget(avgLabel)
        hbox.addStretch(1)

        self.rank.addRow(hbox)

        i = 1
        for each in rank[1]:
            temphbox = QHBoxLayout()
            rankLabel = QLabel(str(i).center(20))
            WCAidLabel = QLabel(str(each[0]).center(20))
            nameLabel = QLabel(each[1].center(20))
            avgLabel = QLabel(str(each[2]).center(20))

            temphbox.addStretch(1)
            temphbox.addWidget(rankLabel)
            temphbox.addStretch(1)
            temphbox.addWidget(WCAidLabel)
            temphbox.addStretch(1)
            temphbox.addWidget(nameLabel)
            temphbox.addStretch(1)
            temphbox.addWidget(avgLabel)
            temphbox.addStretch(1)

            self.rank.addRow(temphbox)
        self.rankLayout.addRow(self.rank)

def setup():
    app = QApplication(sys.argv)
    ex = Competitor("2")
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    setup()
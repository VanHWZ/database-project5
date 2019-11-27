import pypyodbc
import os

path = os.getcwd()
mdb = 'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+ path +'\\WCA_A5.accdb'
conn = pypyodbc.win_connect_mdb(mdb)
cur = conn.cursor()

def login_check(identity, id, password):
    print(identity, id, password)
    if id == "" or password == "":
        return False
    if identity == "Competitor":
        try:
            query = "select password from Competitor where WCAid = %d " % (int(id))
        except:
            return False
    elif identity == "Organizer":
        try:
            query = "select password from Organizer where oid = %d " % (int(id))
        except:
            return False
    else:
        return False

    cur.execute(query)
    if password == cur.fetchone()[0]:
        return True
    else:
        return False

def getCompetition():
    query = "select * from Competition"
    result = []

    for row in cur.execute(query):
        result.append(row)

    return result

def changeCompetition(cid, info, cname, from_time, to_time):
    update = "update Competition set info='%s', cname='%s', from_time='%s',to_time='%s' where cid=%d" % (info, cname, from_time, to_time, cid)
    cur.execute(update)
    cur.commit()

def addCompetition(info, cname, from_time, to_time):
    query = "select max(cid) from Competition"
    cur.execute(query)
    cid = cur.fetchone()[0] + 1
    insert = "insert into Competition(cid,info,cname,from_time,to_time) values(%d,'%s','%s','%s','%s')" % (cid, info, cname, from_time, to_time)
    cur.execute(insert)
    cur.commit()

def getEvents():
    query = "select * from Events"
    results = []
    for row in cur.execute(query):
        results.append(row)

    return results

def getCompetitionEvents(competition):
    query = "select E.ename " \
            "from Events E, Competition C, Competition_events CE " \
            "where C.cname='%s' and E.eid=CE.eid and C.cid=CE.cid" % (competition)
    results = []
    for row in cur.execute(query):
        results.append(row[0])
    return results

def addEvent(event, competition):
    query = "select eid from Events where ename='%s'" % (event)
    cur.execute(query)
    eid = cur.fetchone()[0]
    query = "select cid from Competition where cname='%s'" % (competition)
    cur.execute(query)
    cid = cur.fetchone()[0]
    insert = "insert into Competition_events values(%d,%d)" % (cid, eid)
    cur.execute(insert)
    cur.commit()

def deleteEvent(event, competition):
    query = "select eid from Events where ename='%s'" % (event)
    cur.execute(query)
    eid = cur.fetchone()[0]
    query = "select cid from Competition where cname='%s'" % (competition)
    cur.execute(query)
    cid = cur.fetchone()[0]
    delete = "delete from Competition_events where cid=%d and eid=%d" % (cid, eid)
    cur.execute(delete)
    cur.commit()


def getCompetitionRecord(event, competition):
    query = "select C.WCAid, C.name, CR.avg, CR.best " \
            "from Competitor C, Competition_record CR, Events E, Competition Com " \
            "where E.ename='%s' and Com.cname='%s' and E.eid=CR.eid and Com.cid=CR.cid " \
            "and C.WCAid=CR.WCAid " \
            "order by CR.avg" % (event, competition)
    results = []
    for row in cur.execute(query):
        results.append(row)
    return results

def changeCompetitionRecord(WCAid, competition, event, avg, best):
    query = "select eid from Events where ename='%s'" % (event)
    cur.execute(query)
    eid = cur.fetchone()[0]
    query = "select cid from Competition where cname='%s'" % (competition)
    cur.execute(query)
    cid = cur.fetchone()[0]
    update = "update Competition_record CR set CR.avg=%.2f, CR.best=%.2f " \
             "where CR.WCAid=%d and CR.eid=%d and CR.cid=%d" % (float(avg), float(best), WCAid, eid, cid)
    cur.execute(update)
    cur.commit()

def saveCompetitionRecord(WCAid, competition, event, avg, best):
    query = "select eid from Events where ename='%s'" % (event)
    cur.execute(query)
    eid = cur.fetchone()[0]
    query = "select cid from Competition where cname='%s'" % (competition)
    cur.execute(query)
    cid = cur.fetchone()[0]
    insert = "insert into Competition_record values(%d,%d,%d,%s,%s)" % (eid, cid, WCAid, avg, best)
    cur.execute(insert)
    cur.commit()

def deleteCompetitionRecord(WCAid, competition, event):
    query = "select eid from Events where ename='%s'" % (event)
    cur.execute(query)
    eid = cur.fetchone()[0]
    query = "select cid from Competition where cname='%s'" % (competition)
    cur.execute(query)
    cid = cur.fetchone()[0]
    delete= "delete from Competition_record where eid=%d and cid=%d and WCAid=%d" % (eid, cid, WCAid)
    cur.execute(delete)
    cur.commit()

def getCompetitorInfo(WCAid):
    query = "select * from Competitor where WCAid=%s" % WCAid
    cur.execute(query)
    result = cur.fetchone()
    return result

def changeCompetitorInfo(WCAid, region, name, password):
    update = "update Competitor set region='%s', name='%s', password='%s' " \
             "where WCAid=%s" % (region, name, password, WCAid)
    print(update)
    cur.execute(update)
    cur.commit()

def searchCompetitor(WCAid):
    query = "SELECT distinct E.ename, min(CR.avg), min(CR.best)" \
            "FROM Competition_record AS CR, Events AS E " \
            "WHERE CR.WCAid=%s and E.eid=CR.eid " \
            "GROUP BY E.ename" % WCAid
    results = []
    cur.execute(query)
    all = cur.fetchall()
    for row in all:
        l = list(row)
        event = row[0]
        avg = row[1]
        # get the avg world rank
        query = "select count(*)+1 " \
                "from " \
                "(select name, average from " \
                "(SELECT DISTINCT C.name, min(R.avg) as average FROM Competitor AS C, Events AS E, Competition_record AS R " \
                "WHERE C.WCAid=R.WCAid and E.eid=R.eid and E.ename='%s' " \
                "group by C.name )" \
                "order by average) T2 " \
                "where T2.average<%.2f" % (event, avg)
        cur.execute(query)
        l.append(cur.fetchone()[0])
        best = row[2]
        # get the best world rank
        query = "select count(*)+1 " \
                "from " \
                "(select * from " \
                "(SELECT DISTINCT C.name, min(R.best) as best FROM Competitor AS C, Events AS E, Competition_record AS R " \
                "WHERE C.WCAid=R.WCAid and E.eid=R.eid and E.ename='%s' " \
                "group by C.name ) " \
                "order by best) " \
                "where best<%.2f" % (event, best)
        cur.execute(query)
        l.append(cur.fetchone()[0])
        results.append(l)
        # results.append(row)
    return results

def getRegions():
    query = "select distinct region from Competitor"
    results = []
    for row in cur.execute(query):
        results.append(row[0])
    return results

def getWorldRank(event):
    results = []
    # get the avg world rank
    query = "select * from " \
            "(select C.WCAid, C.name, min(R.avg) as average " \
            "from Events E, Competition_record R, Competitor C " \
            "where E.ename='%s' and E.eid=R.eid and C.WCAid=R.WCAid " \
            "group by C.name, C.WCAid) " \
            "order by average" % event
    # print(query)
    avg = []
    for row in cur.execute(query):
        avg.append(row)
    results.append(avg)
    # get the best world rank
    query = "select * from " \
            "(select C.WCAid, C.name, min(R.best) as best " \
            "from Events E, Competition_record R, Competitor C " \
            "where E.ename='%s' and E.eid=R.eid and C.WCAid=R.WCAid " \
            "group by C.name, C.WCAid) " \
            "order by best" % event
    # print(query)
    best = []
    for row in cur.execute(query):
        best.append(row)
    results.append(best)
    return results

def getRegionRank(event, region):
    results = []
    # get the avg region rank
    query = "select * from " \
            "(select C.WCAid, C.name, min(R.avg) as average " \
            "from Events E, Competition_record R, Competitor C " \
            "where E.ename='%s' and E.eid=R.eid and C.WCAid=R.WCAid and C.region='%s' " \
            "group by C.name, C.WCAid) " \
            "order by average" % (event, region)
    # print(query)
    avg = []
    for row in cur.execute(query):
        avg.append(row)
    results.append(avg)
    # get the best region rank
    query = "select * from " \
            "(select C.WCAid, C.name, min(R.best) as best " \
            "from Events E, Competition_record R, Competitor C " \
            "where E.ename='%s' and E.eid=R.eid and C.WCAid=R.WCAid and C.region='%s'" \
            "group by C.name, C.WCAid) " \
            "order by best" % (event, region)
    # print(query)
    best = []
    for row in cur.execute(query):
        best.append(row)
    results.append(best)
    return results


if __name__ == "__main__":
    # addCompetition("1",'2','2019/11/20','2020/11/21')
    # changeCompetition(4,"1",'2','2019/11/20','2020/11/21')
    # print(getEvents())
    # print(getCompetition())
    # print(getCompetitionEvents('Nanjing Autumn 2019'))
    # deleteEvent("3x3x3one-handed", "Nanjing Autumn 2019")
    # print(getCompetitionRecord("3x3x3cube", "Nanjing Autumn 2019"))
    # changeCompetitionRecord(5, "Nanjing Autumn 2019", "3x3x3cube", "15.78", "13.25")
    # print(getCompetitorInfo("1"))
    changeCompetitorInfo("1","China", "Tommy Lyman", "1")
    # print(searchCompetitor("2"))
    # print(getRegions())
    # print(getWorldRank("3x3x3cube"))
    pass


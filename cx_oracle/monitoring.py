import os
import cx_Oracle
from datetime import datetime


#for settings (modify if necessary)
watch_group=8701
watch_url= 'http://api.noti.daumkakao.io/send/group/kakaotalk'
dbuser = 'infa_mon'
#prod, qa
stage = 'qa'
#if proc_date is null -> run with now date default
proc_date =''


############################################################################
######################add settings #########################################
#db conn (default qa)
dbcon = 'rg-nex-qa-ora2-vip.kpsec.io:37979/DBKJQ'
dbpw = 'dufma01!'
dbcon_prod = 'rg-nex-prod-ora2-vip.kpsec.io:37979/DBKJP'
dbpw_prod = 'ejdns01!'

######################functions ############################################

def make_query(proc_date):
    query = """ SELECT
    WFS.POW_WORKFLOWDEFINITIONNAM AS WRK_WORKFLOWNAME,
    to_date('19700101', 'YYYYMMDD') + ( 1 / 24 / 60 / 60 / 1000) * WFS.POW_STARTTIME + 9/24 AS WRK_STARTTIME,
    to_date('19700101', 'YYYYMMDD') + ( 1 / 24 / 60 / 60 / 1000) * WFS.POW_ENDTIME + 9/24 AS WRK_ENDTIME,
    RS.POR_OBJECTNAME AS MAP_MAPPINNAME ,
    CASE
    WHEN RS.POR_STATE = 0
    THEN CASE WHEN WFS.POW_STATE = 1 THEN 'COMPLETED' ELSE 'RUNNING' END
    WHEN RS.POR_STATE = 1
    THEN 'COMPLETED' 
    WHEN RS.POR_STATE = 2
    THEN 'FAILED' 
    WHEN RS.POR_STATE = 3
    THEN 'ABORTED' 
    WHEN RS.POR_STATE = 5
    THEN 'CANCELED' 
    ELSE 'TBD' 
    END AS MAP_STATE_DESC
    ,rs.POR_MESSAGE
    FROM PO_REQUESTSTAT RS
    LEFT JOIN PO_TASKSTAT TS
    ON ( TS.POT_STATID= RS.POR_PARENTSTATID )
    LEFT JOIN PO_WORKFLOWSTAT WFS
    ON (WFS.POW_STATID = TS.POT_PARENTSTATID)
    LEFT JOIN PO_WORKFLOWFEATURESTAT WFSE
    ON (WFSE.POW_STATID = WFS.POW_PARENTSTATID)
    LEFT JOIN PO_DSNAMEDELEMENT WDND
    ON (WFSE.POW_PARENTSTATID = WDND.POD_STATID
    OR RS.POR_PARENTSTATID = WDND.POD_STATID)
    WHERE 1=1
    AND RS.POR_USERNAME = 'Administrator' 
    AND to_char(to_date('19700101', 'YYYYMMDD') + ( 1 / 24 / 60 / 60 / 1000) * WFS.POW_STARTTIME + 9/24, 'YYYYMMDDHH24MISS') >= """

    query +="'"+proc_date+"'"

    query +=""" AND RS.POR_STATE != 1
    AND (RS.POR_STATE != 0 OR WFS.POW_STATE != 1)
    ORDER BY WRK_STARTTIME DESC """
    return query

#for using column name
def make_dict_factory(cursor):
    cloumns = [d[0] for d in cursor.description]

    def create_row(*args):
        return dict(zip(cloumns, args))
    return create_row

#get status from oracle
def get_status(dbuser, dbpw, dbcon, proc_date) :
    #make query with date string
    query = make_query(proc_date)
    
    #db connect
    connection = cx_Oracle.connect(dbuser, dbpw, dbcon)
    cursor = connection.cursor()
    cursor.execute(query)

    #fetch from db
    cursor.rowfactory = make_dict_factory(cursor)
    rows = cursor.fetchall()
    return rows


#send watch center
def sendNoti(url, to, msg):
    import json
    import requests
    params = {'to' : to, 'msg' : msg}
    response = requests.post(url=url, data=params)
    print(response.text)

######################functions ############################################
############################################################################



##################### main flow ############################################

if proc_date=='':
    proc_date = datetime.today().strftime('%Y%m%d')
print('chaeck workflow status of ' + proc_date)

if stage=='prod':
    dbcon = dbcon_prod
    dbpw = dbpw_prod

fail_rows = get_status(dbuser, dbpw, dbcon, proc_date)
for row in fail_rows:
    endtime = row['WRK_ENDTIME'].strftime('%Y%m%d %H:%M:%S')
    status = row['MAP_STATE_DESC']
    mapping = row['MAP_MAPPINNAME']
    workflow = row['WRK_WORKFLOWNAME']
    message = row['POR_MESSAGE']
    #make alert message
    msg = "[{0}] ETL ALERT \n[workflow] :{1} \n[mapping] :{2} \n[status] :{3} \n[end time] :{4} \n[message] {5}".format(stage.upper(), workflow, mapping, status, endtime, message)
    print(msg)
    #send watch center
    #sendNoti(watch_url, watch_group, msg)






   







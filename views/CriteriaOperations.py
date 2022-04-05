#from database.DBConnection import databaseOperation, databaseOperationSave
#from models.Configuration import Criteria
import json
import numpy as np
import requests
from scorecard_backend.database.DBConnection import databaseOperation, databaseOperationSave
from scorecard_backend.models.Configuration import Criteria


def getAllCriteriaFromDB():
    sql = "select * from m_criteria"
    result = databaseOperation(sql)
    sql_criteria = "select * from m_criteriascore"
    result_criteria = np.array(databaseOperation(sql_criteria)).tolist()
    print(result_criteria)
    crit = []
    sc = []
    for row in result_criteria :
        print("row: "+ str(row))
        crit.append(row['criteria'])
        sc.append(row['score'])

    print(crit,sc)
    response = []
    if result:
        for row in result:
            # id 0, product 3, category 2, datasource 4, sqlapi 5, keyvalue 6, feature 1)
            criteria = Criteria(row['id'], row['product'], row['category'], row['datasource'], row['sqlapi'], row['keyvalue'], row['feature'],crit, sc)
            response.append(json.dumps(criteria.__dict__))
    return response

def getByCriteriaId(id):
    sql = "select * from m_criteria where id = '%d'" % id
    result = databaseOperation(sql)
    sql_criteria = "select * from m_criteriascore where cscriteriatableid = '%d'" % id
    result_criteria = np.array(databaseOperation(sql_criteria)).tolist()
    print(result_criteria)
    crit = []
    sc = []
    for row in result_criteria :
        crit.append(row['criteria'])
        sc.append(row['score'])
        print("row: "+ str(row))
    if result:
        for row in result:
            # id, product, category, datasource, sqlapi, keyvalue, feature
            criteria = Criteria(row['id'], row['product'], row['category'], row['datasource'], row['sqlapi'], row['keyvalue'], row['feature'], crit, sc)
            print(criteria.criteria)
        return criteria
    else:
        return None

def saveCriteria(id,feature, category, product, datasource, keyvalue, sqlapi, scoreCriteria):
    if id:
        sql = "update m_criteria set feature='"+feature+"', category='"+category+"', product='"+product+"', datasource='"+datasource+"', keyvalue='"+keyvalue+"', sqlapi='"+sqlapi+"' where id=%d" %int(id)
    else:
        sql = "insert into m_criteria (product, category, datasource, sqlapi, keyvalue, feature) values ('" + product + "','" + category + "','" + datasource + "','" + sqlapi + "','" + keyvalue + "','" + feature + "')"
    print(sql)
    test_query = sqlapi
    try:
    	if(datasource == "SQL"):
    		databaseOperation(test_query)
    	elif(datasource == "JSON" or datasource == "XML"):
    		r = requests.get(test_query)
    		if(r.status_code != 200):
    			raise ValueError("wrong JSON/XML query")
    except Exception as e:
        raise ValueError("wrong sql query")
    result = databaseOperationSave(sql)
    print(result)
    print(scoreCriteria)
    # result = 14
    saveCriteriaScore(scoreCriteria, id, feature, result)
    if result:
        return {"status" : "SUCCESS"}
    else:
        return {"status": "FAILURE"}

def saveCriteriaScore(scoreCriteria, id, feature, result):
    id_sql = "SELECT id from m_criteria where feature = '" + str(feature) + "'" 
    res = databaseOperation(id_sql)
    ids = []
    if(res):
        for row in res:
            crit_id = row['id']
    print("CRIT ID", crit_id)
    get_ids = "SELECT id from mifostenant.m_criteriascore where cscriteriatableid = " + str(crit_id)
    result_query = databaseOperation(get_ids)
    print("RESULT QUERY", result_query)
    if(result_query):
        for row in result_query:
            print(row)
            ids.append(row['id'])
    print("IDS", ids)
    for idx, cr in enumerate(scoreCriteria):
        print(cr['criteria'])
        #print("@@@",cr[1])
        if(cr['id']):
            sql = "update m_criteriascore set criteria='"+cr['criteria']+"', score='"+cr['score']+"' where id=" + str(ids[idx]) + " and cscriteriatableid=" + str(cr['id'])
        else:
            sql = "insert into m_criteriascore (cscriteriatableid, criteria, score) values ("+str(crit_id)+",'"+cr['criteria']+"', '"+cr['score']+"')"
        print(sql)
        databaseOperationSave(sql)
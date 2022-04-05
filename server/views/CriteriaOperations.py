#from database.DBConnection import databaseOperation, databaseOperationSave
#from models.Configuration import Criteria
import json

from scorecard_backend.database.DBConnection import databaseOperation, databaseOperationSave
from scorecard_backend.models.Configuration import Criteria


def getAllCriteriaFromDB():
    sql = "select * from m_criteria"
    result = databaseOperation(sql)
    response = []
    if result:
        for row in result:
            # id 0, product 3, category 2, datasource 4, sqlapi 5, keyvalue 6, feature 1)
            criteria = Criteria(row[0], row[3], row[2], row[4], row[5], row[6], row[1])
            response.append(json.dumps(criteria.__dict__))
    return response

def getByCriteriaId():
    sql = "select * from m_criteria where id = '%d'" % id
    result = databaseOperation(sql)
    if result:
        for row in result:
            # id, product, category, datasource, sqlapi, keyvalue, feature
            criteria = Criteria(row[0], row[3], row[2], row[4], row[5], row[6], row[1])

        return criteria
    else:
        return None

def saveCriteria(id,feature, category, product, datasource, keyvalue, sqlapi, scoreCriteria):
    if id:
        sql = "update m_criteria set feature='"+feature+"', category='"+category+"', product='"+product+"', datasource='"+datasource+"', keyvalue='"+keyvalue+"', sqlapi='"+sqlapi+"' where id=%d" %int(id)
    else:
        sql = "insert into m_criteria (product, category, datasource, sqlapi, keyvalue, feature) values ('" + product + "','" + category + "','" + datasource + "','" + sqlapi + "','" + keyvalue + "','" + feature + "')"
    print(sql)
    result = databaseOperationSave(sql)
    # print(result)
    # print(scoreCriteria)
    # result = 14
    saveCriteriaScore(scoreCriteria, result)
    if result:
        return {"status" : "SUCCESS"}
    else:
        return {"status": "FAILURE"}

def saveCriteriaScore(scoreCriteria, id):
    for  cr in scoreCriteria:
        print(cr['criteria'])
        print(cr['score'])
        if(cr['id']):
            sql = "update m_criteriascore set criteria='"+cr['criteria']+"', score='"+cr['score']+"' where csid=%d and cscriteriatableid=%d" %int(cr[id]) %id
        else:
            sql = "insert into m_criteriascore (cscriteriatableid, criteria, score) values ("+str(id)+",'"+cr['criteria']+"', '"+cr['score']+"')"
        print(sql)
        databaseOperationSave(sql)
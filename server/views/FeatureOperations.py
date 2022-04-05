#from database.DBConnection import databaseOperation, databaseOperationSave
#from models.Configuration import Feature
import json

from scorecard_backend.database.DBConnection import databaseOperation, databaseOperationSave
from scorecard_backend.models.Configuration import Feature


def getByFeatureId(id):
    sql = "select * from m_feature where id = '%d'" % id
    result = databaseOperation(sql)
    if result:
        for row in result:
            feature = Feature(row[4], id, row[3], row[1], row[5], row[2])

        return feature
    else:
        return None


def getAllFeaturesFromDB():
    sql = "select * from m_feature"
    result = databaseOperation(sql)
    response = []
    if result:
        for row in result:
            feature = Feature(row[4], row[0], row[3], row[1], row[5], row[2])
            response.append(json.dumps(feature.__dict__))
    return response

def getFeatureNCategoryFromDB():
    sql = "select id,feature,category from m_feature"
    result = databaseOperation(sql)
    response = []
    if result:
        for row in result:
            feature = Feature(row[2], row[0], None, row[1], None, None)
            response.append(json.dumps(feature.__dict__))
    return response

def saveAFeature(id,feature, value, data, category, status):
    if id:
        sql = "update m_feature set feature='"+feature+"', value='"+value+"', data='"+data+"', category='"+category+"', status='"+str(status)+"' where id=%d" %int(id)
    else:
        sql = "insert into m_feature (feature, value, data, category, status) values ('"+feature+"','"+value+"','"+data+"','"+category+"','"+str(status)+"')"
    print(sql)
    result = databaseOperationSave(sql)
    if result:
        return {"status" : "SUCCESS"}
    else:
        return {"status": "FAILURE"}


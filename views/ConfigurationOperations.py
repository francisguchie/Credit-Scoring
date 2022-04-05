# from database.DBConnection import databaseOperation, databaseOperationSave
# from models.Configuration import Configuration
import json

from scorecard_backend.database.DBConnection import databaseOperation, databaseOperationSave
from scorecard_backend.models.Configuration import Configuration


def getByConfigId(id):
    sql = "select * from m_configuration where id = '%d'" % id
    result = databaseOperation(sql)
    print(result)
    if result:
        for row in result:
            configuration = Configuration( row['id'], row['product'], row['feature'], row['category'], row['weightage'],
                                           row['greenmin'], row['greenmax'], row['ambermin'], row['ambermax'], row['redmin'], row['redmax'])

        return configuration
    else:
        return None


def getAllConfigurationFromDB():
    sql = "select * from m_configuration"
    result = databaseOperation(sql)
    response = []
    if result:
        for row in result:

            configuration = Configuration( row['id'], row['product'], row['feature'], row['category'], row['weightage'],
                                           row['greenmin'], row['greenmax'], row['ambermin'], row['ambermax'], row['redmin'], row['redmax'])
            response.append(json.dumps(configuration.__dict__))
    return response

def saveAConfiguration(id,feature,category,product,weightage,greenmax,greenmin,ambermax,ambermin,redmax,redmin):
    if id:
        sql = "update m_configuration set feature='"+feature+"', product='"+product+"', weightage='"+weightage+"', category='"+category+"', greenmax='"+greenmax+"', greenmin='"+greenmin+"' , ambermax='"+ambermax+"', ambermin='"+ambermin+"', redmax='"+redmax+"', redmin='"+redmin+"'where id=%d" %int(id)
    else:
        sql = "insert into m_configuration (feature,category,product,weightage,greenmax,greenmin,ambermax,ambermin,redmax,redmin) values " \
              "('"+feature+"','"+category+"','"+product+"','"+weightage+"','"+greenmax+"','"+greenmin+"','"+ambermax+"','"+ambermin+"','"+redmax+"','"+redmin+"')"
    print(sql)
    result = databaseOperationSave(sql)
    if result:
        return {"status" : "SUCCESS"}
    else:
        return {"status": "FAILURE"}


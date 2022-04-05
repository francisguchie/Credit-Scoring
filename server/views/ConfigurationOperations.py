# from database.DBConnection import databaseOperation, databaseOperationSave
# from models.Configuration import Configuration
import json

from scorecard_backend.database.DBConnection import databaseOperation, databaseOperationSave
from scorecard_backend.models.Configuration import Configuration


def getByConfigId(id):
    sql = "select * from m_configuration where id = '%d'" % id
    result = databaseOperation(sql)
    if result:
        for row in result:
            configuration = Configuration( row[0], row[1], row[2], row[3], row[4],
                                           row[5], row[6], row[7], row[8], row[9], row[10])

        return configuration
    else:
        return None


def getAllConfigurationFromDB():
    sql = "select * from m_configuration"
    result = databaseOperation(sql)
    response = []
    if result:
        for row in result:

            configuration = Configuration( row[0], row[1], row[2], row[3], row[4],
                                           row[5], row[6], row[7], row[8], row[9], row[10])
            response.append(json.dumps(configuration.__dict__))
    return response

def saveAConfiguration(id,feature,category,product,weightage,greenmax,greenmin,ambermax,ambermin,redmax,redmin
):
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


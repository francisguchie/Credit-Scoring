from scorecard_backend.database.DBConnection import databaseOperation, databaseOperationSave
from scorecard_backend.models.Configuration import Configuration
import json

def getByAge(age):
    # sql = "SELECT cs.criteria, (CONVERT(cs.score, DECIMAL(10,2)) * CONVERT(a.weightage , DECIMAL(10,2))) as mul " \
    #       "FROM mifostenant.m_criteriascore as cs, mifostenant.m_configuration a " \
    #       "where cs.cscriteriatableid = a.id and  a.feature = 'Age' and cs.cscriteriatableid=1"
    sql ="SELECT cs.criteria, (CONVERT(cs.score, DECIMAL(10,2)) * CONVERT(a.weightage , DECIMAL(10,2))) as mul, case " \
         "when (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0))) >=a.ambermin and (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0)))<=a.ambermax then 'amber'" \
         "when (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0))) >=a.greenmin and (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0)))<=a.greenmax then 'green'" \
         "when(CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0))) >=a.redmin and (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0)))<=a.redmax then 'red'" \
         "end as color " \
         "FROM  mifostenant.m_criteriascore as cs, mifostenant.m_configuration a where cs.cscriteriatableid = a.id and  a.feature = 'Age' "
    result = databaseOperation(sql)
    scorecolor = {
        "score" : 0,
        "color": ''

    }
    score = 0
    if(result):
        for row in result:
            criteria = row[0]
            minage, maxage = criteria.split('-')
            if(age >= int(minage) and age <= int(maxage)):
                scorecolor["score"] = int(row[1])
                scorecolor["color"] = row[2]
                # score = int(row[1])
                break
    return scorecolor

def getByGender(gender):
    sql = "SELECT cs.criteria, (CONVERT(cs.score, DECIMAL(10,2)) * CONVERT(a.weightage , DECIMAL(10,2))) as mul, case " \
         "when (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0))) >=a.ambermin and (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0)))<=a.ambermax then 'amber'" \
         "when (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0))) >=a.greenmin and (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0)))<=a.greenmax then 'green'" \
         "when(CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0))) >=a.redmin and (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0)))<=a.redmax then 'red'" \
         "end as color " \
         "FROM  mifostenant.m_criteriascore as cs, mifostenant.m_configuration a  " \
          "where cs.cscriteriatableid = a.id and  Upper(a.feature)= 'GENDER' and cs.cscriteriatableid=2"
    result = databaseOperation(sql)
    score = 0
    scorecolor = {
        "score": 0,
        "color": ''

    }
    if(result):
        for row in result:
            criteria = row[0]
            if(criteria.upper() == gender):
                scorecolor["score"] = int(row[1])
                scorecolor["color"] = row[2]
                break
    return scorecolor



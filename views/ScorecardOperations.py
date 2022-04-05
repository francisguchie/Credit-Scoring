from scorecard_backend.database.DBConnection import databaseOperation, databaseOperationSave
from scorecard_backend.models.Configuration import Configuration
import json
import requests
import xmltodict

def getByAge(age):
    # sql = "SELECT cs.criteria, (CONVERT(cs.score, DECIMAL(10,2)) * CONVERT(a.weightage , DECIMAL(10,2))) as mul " \
    #       "FROM mifostenant.m_criteriascore as cs, mifostenant.m_configuration a " \
    #       "where cs.cscriteriatableid = a.id and  a.feature = 'Age' and cs.cscriteriatableid=1"
    sql ="SELECT cs.criteria, (CONVERT(cs.score, DECIMAL(10,2)) * CONVERT(a.weightage , DECIMAL(10,2))) as mul, case " \
         "when (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0))) >=a.ambermin and (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0)))<=a.ambermax then 'amber'" \
         "when (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0))) >=a.greenmin and (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0)))<=a.greenmax then 'green'" \
         "when(CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0))) >=a.redmin and (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0)))<=a.redmax then 'red'" \
         "end as color " \
         "FROM  mifostenant.m_criteriascore as cs, mifostenant.m_configuration a where a.feature = 'Age' and cs.cscriteriatableid = 3"
    result = databaseOperation(sql)
    scorecolor = {
        "score" : 0,
        "color": ''

    }
    score = 0
    if(result):
        for row in result:
            print("scorecard > " + str(row))
            criteria = row[0]
            minage, maxage = criteria.split('-')
            if(age >= int(minage) and age <= int(maxage)):
                scorecolor["score"] = float(row[1])
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
          "where cs.cscriteriatableid = 4 and  Upper(a.feature)= 'GENDER'"
    result = databaseOperation(sql)
    score = 0
    scorecolor = {
        "score": 0,
        "color": ''
    }
    if(result):
        for row in result:
            print("row>> "+ str(row))
            criteria = row[0]
            if(criteria.upper() == gender):
                scorecolor["score"] = float(row[1])
                scorecolor["color"] = row[2]
                break
    return scorecolor

def getBySQL(loan_id):
    sql = "SELECT id, feature, sqlapi, keyvalue, category from m_criteria where datasource = 'SQL'"
    result = databaseOperation(sql)
    urls = []
    features = []
    keys = []
    ids = []
    types = []
    categories = []
    if(result):
        for row in result:
           
            ids.append(row["id"])
            features.append(row["feature"])
            urls.append(row["sqlapi"])
            keys.append(row["keyvalue"])
            categories.append(row["category"])
        # print("FEAT", urls)
        for feature in features:
            feature_sql = "SELECT value from m_feature where feature = '" + str(feature) + "'"
            feature_res = databaseOperation(feature_sql)
            if(feature_res):
                for row in feature_res :
                    types.append(row["value"])

        score = 0
        scorecolor = {
            "category": [],
            "feature": [],
            "score": [],
            "color": []
        }

        for idx, feature in enumerate(features):
            sql_query = urls[idx]
            sql_query = sql_query +" where id = "+ str(loan_id)
            print("sql",sql_query)
            result = databaseOperation(sql_query)
            print(result)
            flag = 0
            if(result):
                for row in result:
                    if(len(row) > 1):
                        print("enumerate : " + str(row))
                        if(row["feature"] == 'Age' or row["feature"] == 'Gender'):
                            flag = 1 
                            continue
                    feat = row["id"]
                    print("feature", feat)
            # r = requests.get(url=urls[idx], params=None)
            # data = r.json()
            # feat = data[str(loan_id)][str(keys[idx])]
            # add json reading code
            if(flag == 1):
                continue

            calc_score_sql = "SELECT cs.criteria, (CONVERT(cs.score, DECIMAL(10,2)) * CONVERT(a.weightage , DECIMAL(10,2))) as mul, case " \
         "when (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0))) >=a.ambermin and (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0)))<=a.ambermax then 'amber'" \
         "when (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0))) >=a.greenmin and (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0)))<=a.greenmax then 'green'" \
         "when(CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0))) >=a.redmin and (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0)))<=a.redmax then 'red'" \
         "end as color " \
         "FROM  mifostenant.m_criteriascore as cs, mifostenant.m_configuration a  " \
          "where cs.cscriteriatableid = " + str(ids[idx]) + " and  Upper(a.feature)= '" + str(feature).upper() + "'"

            result_calc_score = databaseOperation(calc_score_sql)
            scorecolor['category'].append(categories[idx])
            scorecolor['feature'].append(feature)
            print("RES", result_calc_score)
            if(result_calc_score):
                for row in result_calc_score:
                    print("calc" + str(row))
                    criteria = row[0]
                    if(types[idx] == 'Nominal' or types[idx] == 'Binary'):
                      if(criteria.upper() == feat.upper()):
                        scorecolor["score"].append(float(row[1]))
                        scorecolor["color"].append(row[2])
                        break
                    else:
                        mini, maxi = criteria.split('-')
                        print("Mini, maxi", mini, maxi)
                        if(feat >= int(mini) and feat <= int(maxi)):
                            scorecolor["score"].append(float(row[1]))
                            scorecolor["color"].append(row[2])
                        # score = int(row[1])
                            break
    return scorecolor

def getByJSON(loan_id):
    sql = "SELECT id, feature, sqlapi, keyvalue, category from m_criteria where datasource = 'JSON'"
    result = databaseOperation(sql)
    urls = []
    features = []
    keys = []
    ids = []
    types = []
    categories = []

    if(result):
        for row in result:
            
            ids.append(row["id"])
            features.append(row["feature"])
            urls.append(row["sqlapi"])
            keys.append(row["keyvalue"])
            categories.append(row["category"])

        for feature in features:
            feature_sql = "SELECT value from m_feature where feature = '" + str(feature) + "'"
            feature_res = databaseOperation(feature_sql)
            if(feature_res):
                for row in feature_res :
                    types.append(row["value"])

        score = 0
        scorecolor = {
            "category": [],
            "feature": [],
            "score": [],
            "color": []
        }

        for idx, feature in enumerate(features):
            r = requests.get(url=urls[idx], params=None)
            data = r.json()
            feat = data[str(loan_id)][str(keys[idx])]
            # add json reading code

            calc_score_sql = "SELECT cs.criteria, (CONVERT(cs.score, DECIMAL(10,2)) * CONVERT(a.weightage , DECIMAL(10,2))) as mul, case " \
         "when (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0))) >=a.ambermin and (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0)))<=a.ambermax then 'amber'" \
         "when (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0))) >=a.greenmin and (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0)))<=a.greenmax then 'green'" \
         "when(CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0))) >=a.redmin and (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0)))<=a.redmax then 'red'" \
         "end as color " \
         "FROM  mifostenant.m_criteriascore as cs, mifostenant.m_configuration a  " \
          "where cs.cscriteriatableid = " + str(ids[idx]) + " and  Upper(a.feature)= '" + str(feature).upper() + "'"

            result_calc_score = databaseOperation(calc_score_sql)
            scorecolor['category'].append(categories[idx])
            scorecolor['feature'].append(feature)

            if(result_calc_score):
                for row in result_calc_score:
                    criteria = row["criteria"]
                    if(types[idx] == 'Nominal' or types[idx] == 'Binary'):
                      if(criteria.upper() == feat.upper()):
                        scorecolor["score"].append(float(row["mul"]))
                        scorecolor["color"].append(row["color"])
                        break
                    else:
                        mini, maxi = criteria.split('-')
                        if(feat >= int(mini) and feat <= int(maxi)):
                            scorecolor["score"].append(float(row["mul"]))
                            scorecolor["color"].append(row["color"])
                        # score = int(row[1])
                            break
    return scorecolor


def getByXML(loan_id):
    sql = "SELECT id, feature, sqlapi, keyvalue, category from m_criteria where datasource = 'XML'"
    result = databaseOperation(sql)
    urls = []
    features = []
    keys = []
    ids = []
    types = []
    categories = []

    if(result):
        for row in result:
            
            ids.append(row["id"])
            features.append(row["feature"])
            urls.append(row["sqlapi"])
            keys.append(row["keyvalue"])
            categories.append(row["category"])

        for feature in features:
            feature_sql = "SELECT value from m_feature where feature = '" + str(feature) + "'"
            feature_res = databaseOperation(feature_sql)
            if(feature_res):
                for row in feature_res :
                    types.append(row["value"])

        score = 0
        scorecolor = {
            "category": [],
            "feature": [],
            "score": [],
            "color": []
        }

        for idx, feature in enumerate(features):
            r = requests.get(url=urls[idx], params=None)
            r_parse = xmltodict.parse(r.text)
            res = json.dumps(r_parse)
            data = json.loads(res)

            for element in data['Company']['Loan']:
            	print(element['id'])
            	if(element['id'] == str(loan_id)):
            		feat = element[str(keys[idx])]
            		break
            #feat = data[str(loan_id)][str(keys[idx])]
            # add json reading code

            calc_score_sql = "SELECT cs.criteria, (CONVERT(cs.score, DECIMAL(10,2)) * CONVERT(a.weightage , DECIMAL(10,2))) as mul, case " \
         "when (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0))) >=a.ambermin and (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0)))<=a.ambermax then 'amber'" \
         "when (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0))) >=a.greenmin and (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0)))<=a.greenmax then 'green'" \
         "when(CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0))) >=a.redmin and (CONVERT(cs.score, DECIMAL(10,0)) * CONVERT(a.weightage , DECIMAL(10,0)))<=a.redmax then 'red'" \
         "end as color " \
         "FROM  mifostenant.m_criteriascore as cs, mifostenant.m_configuration a  " \
          "where cs.cscriteriatableid = " + str(ids[idx]) + " and  Upper(a.feature)= '" + str(feature).upper() + "'"

            result_calc_score = databaseOperation(calc_score_sql)
            scorecolor['category'].append(categories[idx])
            scorecolor['feature'].append(feature)

            if(result_calc_score):
                for row in result_calc_score:
                    print("scorecard-row" + str(row))
                    
                    criteria = row[0]
                    if(types[idx] == 'Nominal' or types[idx] == 'Binary'):
                      if(criteria.upper() == feat.upper()):
                        scorecolor["score"].append(float(row[1]))
                        scorecolor["color"].append(row[2])
                        break
                    else:
                        mini, maxi = criteria.split('-')
                        if(int(feat) >= int(mini) and int(feat) <= int(maxi)):
                            scorecolor["score"].append(float(row[1]))
                            scorecolor["color"].append(row[2])
                        # score = int(row[1])
                            break
    return scorecolor
                    # check for attribute type and then assign score



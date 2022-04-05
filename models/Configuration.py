
# from database.DBConnection import db
from json import JSONEncoder

import pymysql
from sqlalchemy import Column, Integer, String, ARRAY


# db = pymysql.connect("localhost", "root", "password", "mifostenant")

class Configuration():
    """Tasks for the To Do list."""
    id = Column(Integer, primary_key=True)
    product = Column(String(20))
    feature = Column(String(20))
    category = Column(String(60))
    weightage = Column(String(20))
    greenmin = Column(String(20))
    greenmax = Column(String(20))
    ambermin = Column(String(20))
    ambermax = Column(String(20))
    redmin = Column(String(20))
    redmax = Column(String(20))


    def __init__(self,id,product,feature,category,weightage,greenmin,greenmax,ambermin,ambermax,redmin,redmax):
        self.category=category
        self.id=id
        self.product=product
        self.feature=feature
        self.weightage=weightage
        self.greenmax=greenmax
        self.greenmin=greenmin
        self.redmax=redmax
        self.redmin=redmin
        self.ambermax= ambermax
        self.ambermin=ambermin


class Criteria():
    """Tasks for the To Do list."""
    id = Column(Integer, primary_key=True)
    product = Column(String(20))
    category = Column(String(20))
    datasource = Column(String(20))
    sqlapi = Column(String(20))
    keyvalue = Column(String(20))
    feature = Column(String(20))
    criteria = Column(ARRAY(String))
    score = Column(ARRAY(String))

    def __init__(self,id,product,category,datasource,sqlapi,keyvalue,feature,criteria,score):
        self.id = id
        self.product = product
        self.category=category
        self.datasource=datasource
        self.sqlapi=sqlapi
        self.keyvalue=keyvalue
        self.feature=feature
        self.criteria=criteria
        self.score=score


class Feature():
    """Tasks for the To Do list."""
    id = Column(Integer, primary_key=True)
    value = Column(String(20))
    category = Column(String(20))
    feature = Column(String(60))
    data = Column(String(20))
    status = Column(String(20))

    def __init__(self, category, id,data,feature,status,value):
        self.category = category
        self.id = id
        self.data = data
        self.feature = feature
        self.status = status
        self.value = value


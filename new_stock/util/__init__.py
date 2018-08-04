import datetime
import pymongo
from pymongo import MongoClient
from pymongo import errors
import pandas as pd

FirstQuarter = datetime.datetime.strptime('03-31', '%m-%d')
SecondQuarter = datetime.datetime.strptime('06-30', '%m-%d')
ThirdQuarter = datetime.datetime.strptime('09-30', '%m-%d')
FourthQuarter = datetime.datetime.strptime('12-31', '%m-%d')

def getYear(date: datetime.datetime):
    return date.year

def getQuarter(date: datetime.datetime):
    return date.month

def isSameQuarter(d1: datetime.datetime, d2: datetime.datetime):
    return d1.month == d2.month


def priorYear(date):
    return date.replace(year=date.year-1)

def nextYear(date):
    return date.replace(year=date.year+1)

def priorQuarter(date):
    if isSameQuarter(date, FourthQuarter):
        return getThirdQuarter(date)
    elif isSameQuarter(date, ThirdQuarter):
        return getSecondQuarter(date)
    elif isSameQuarter(date, SecondQuarter):
        return getFirstQuarter(date)
    elif isSameQuarter(date, FirstQuarter):
        newOne = priorYear(date)
        return getFourthQuarter(newOne)

    return None


def nextQuarter(date):
    if isSameQuarter(date, FirstQuarter):
        return getSecondQuarter(date)
    elif isSameQuarter(date, SecondQuarter):
        return getThirdQuarter(date)
    elif isSameQuarter(date, ThirdQuarter):
        return getFourthQuarter(date)
    elif isSameQuarter(date, FourthQuarter):
        newOne = nextYear(date)
        return getFirstQuarter(newOne)

    return None



def changeQuarter(date, des):
    return date.replace(month=des.month, day=des.day)

def getFirstQuarter(date):
    return changeQuarter(date, FirstQuarter)

def getSecondQuarter(date):
    return changeQuarter(date, SecondQuarter)

def getThirdQuarter(date):
    return changeQuarter(date, ThirdQuarter)

def getFourthQuarter(date):
    return changeQuarter(date, FourthQuarter)


def priorXQuarter(date, x):
    date = priorQuarter(date)
    for n in range(1, x):
        if date != None:
            date = priorQuarter(date)

    return date


def nextXQuarter(date, x):
    date = nextQuarter(date)
    for n in range(1, x):
        if date != None:
            date = nextQuarter(date)

    return date


def saveMongoDB(data: pd.DataFrame, keyFunc, dbName, collectionName, callback=None):
    client = MongoClient()
    db = client[dbName]
    collection = db[collectionName]

    for k, v in data.iterrows():
        result = v.to_dict()
        # print(dir(k))
        result.update(keyFunc(k))
        if callback:
            callback(result)
        update_result = collection.update_one({'_id': result['_id']},
                                              {'$set': result})
        if update_result.matched_count == 0:
            try:
                if collection.insert_one(result):
                    print('Saved to Mongo')
            except errors.DuplicateKeyError as e:
                pass


def genKeyDateFunc(k):
    def keyDateFunc(v):
        return {k: v.strftime('%Y-%m-%d')}
    return keyDateFunc

def genEmptyFunc():
    def emptyFunc(v):
        return {}
    return emptyFunc

###########################
def addSysPath(path):
    import sys
    for one in sys.path:
        if one == path:
            return
    sys.path.append(path)


if __name__ == '__main__':
    pass

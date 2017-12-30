import os
import psycopg2
#import urlparse
import urllib.parse
from django.contrib.auth.hashers import make_password, check_password
import time


class Profile(object):
    """ this class is for defining each user based on inputted information about
    the user. It takes in user information and stores them accordingly in the database
    """
    def __init__(self, profileInfo):
        self.profileInfo = str(profileInfo)
    def updateInfo(self):
        profile_list = self.profileInfo.split('&')
        profile_dict = {}
        attribute_excluded = ["b'csrfmiddlewaretoken", 'Pass-repeat']
        for element in profile_list:
            element_list = element.split('=')
            profile_key = element_list[0]
            profile_val = element_list[1]
            
            #password encryption
            if profile_key == 'Pass':
                plain_pass = profile_val
                encrypted_pass = make_password(plain_pass)
                profile_val = encrypted_pass
            
            if (profile_key not in (attribute_excluded)):
                profile_dict[profile_key] = profile_val
        #add date and time created 
        time_stamp = time.strftime('%Y/%m/%d %H:%M:%S', time.gmtime())
        profile_dict['date_created'] = time_stamp
        
        for attribute in profile_dict:
            setattr(self,attribute,profile_dict[attribute])
    def gatherAttr(self):
        identifiedAttr = []
        for attribute in self.__dict__:
            if attribute != 'profileInfo':
                identifiedAttr.append(attribute + ": " + self.__dict__[attribute])
        return " ".join(identifiedAttr)
    def __repr__(self):
        return '{0}- {1}'.format(self.__class__.__name__, self.gatherAttr()) 


class UserProfile(Profile):
    def enableDao(self):
        setattr(self,'dao',UserProfileDao())
    
class BaseDao(object):
    def initiateConn(self):
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse('postgres://ctomdacurckzmh:9296e40a59aacf97c93020e5f0b77e565f6e6f2cf9c0ec00a663b983216711d3@ec2-184-72-245-58.compute-1.amazonaws.com:5432/df0ehsr6unrr28')
        
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
            )
        cur = conn.cursor()
        setattr(self,'conn',conn)
        setattr(self,'cur',cur)
    
    def resultAsDict(self,cur):
        cols = [col[0] for col in cur.description]
        results = cur.fetchall()
        processedDict = {}
        for colName in cols:
            processedDict[colName] = []
            for count,row in enumerate(results):
                processedDict[colName].append(row[count])
        return processedDict
        
    def commit(self):
        self.conn.commit()
    def close(self):
        self.cur.close()
    def rollBack(self):
        self.cur.rollback()
        

class UserProfileDao(BaseDao):
    def storeInfo(self, userDict):
        #store all info for tblUser
        #userDict = sampleUser.__dict__
        queryCol= 'Insert INTO tbluser ("Admin","Developer",'
        queryVal = ['1', '1']
        attributeExcluded = ['profileInfo', 'dao']
        for attribute in userDict:
            if attribute not in attributeExcluded:
                queryCol += '"' + attribute + '",'
                if attribute.find('ID') > -1:
                    userDict[attribute] = userDict[attribute][:-1]
                queryVal.append(userDict[attribute])
        
        queryCol = queryCol[:-1] + ') values %s'
        self.cur.execute(queryCol,
                            (tuple(queryVal),))
        
    def pullIds(self):
        self.cur.execute('select * from tbluser')
        id_list = [userId[0] for userId in self.cur.fetchall()]
        return id_list
    
    def checkDuplicate(self, column, value):
        query = ('select count(' + '"' + column +'"' + ') from tbluser where '
                 'tbluser."' + column + '"=  %s')
        self.cur.execute(query,(value,))
        if (self.cur.fetchall()[0][0] > 0):
            return True
        else:
            return False
    def saveUser(self,userInfo):
        self.updateInfo()
        self.enableDao()
        self.dao.initiateConn()
        if (self.dao.checkDuplicate("ID",self.ID)):
            return ('Username already exists')
        if (self.dao.checkDuplicate("Email",self.Email)):
            return ('Email already exists')
        self.dao.storeInfo(self.__dict__)
        self.dao.commit()
        self.dao.close()
        return ('User successfully created')


class ChurchProfile(Profile):
    def enableDao(self):
        setattr(self,'dao',ChurchProfileDao())
    def saveChurch(self):
        self.updateInfo()
        self.enableDao()
        self.dao.initiateConn()
        self.dao.storeInfo(self.__dict__)
        self.dao.commit()
        self.dao.close()
    
class ChurchProfileDao(BaseDao):
    def storeInfo(self, userDict):
        #store all info for tblUser
        #userDict = sampleUser.__dict__
        queryCol= 'Insert INTO "tblchurch" ('
        queryVal = []
        attributeExcluded = ['profileInfo', 'dao']
        for attribute in userDict:
            if attribute not in attributeExcluded:
                queryCol += '"' + attribute + '",'
                if attribute.find('id') > -1:
                    userDict[attribute] = userDict[attribute][:-1]
                queryVal.append(userDict[attribute])
        
        queryCol = queryCol[:-1] + ') values %s'
        print (queryCol)
        print (queryVal)
        self.cur.execute(queryCol,
                            (tuple(queryVal),))    
    def pullChurchName(self):
        self.cur.execute('select church_pk, name from tblchurch')
        church_dict = {}
        for row in self.cur.fetchall():
            church_dict[row[0]]= row[1]
        return church_dict
    

        

    

    

def testMain():
    newChurch = 'name=Connecticut Church'
    newChurch = ChurchProfile(newChurch)
    newChurch.saveChurch()
        
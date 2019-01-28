import os
import psycopg2
from psycopg2 import sql
#import urlparse
import urllib.parse
from django.contrib.auth.hashers import make_password, check_password
import time
import geocoder

class Profile(object):
    """ this class is for defining each user based on inputted information about
    the user. It takes in user information and stores them accordingly in the database
    """
    def __init__(self, profileInfo):
        self.profileInfo = str(profileInfo)
    def updateInfo(self):
        profile_list = self.profileInfo.split('&')
        profile_dict = {}
        attribute_excluded = ["b'csrfmiddlewaretoken", 'pass-repeat', 'csrfmiddlewaretoken']
        for element in profile_list:
            element_list = element.split('=')
            profile_key = element_list[0]
            profile_val = element_list[1]
            
            #password encryption
            if profile_key == 'pass':
                plain_pass = profile_val
                encrypted_pass = make_password(plain_pass)
                profile_val = encrypted_pass
            
            if ((profile_key not in (attribute_excluded)) and (profile_val != '') and (profile_val != "'")):
                if profile_val[-1] == "'":
                    profile_val = profile_val[:-1]
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
        
    def saveUser(self):
        self.updateInfo()
        self.enableDao()
        self.dao.initiateConn()
        if (self.dao.checkDuplicate("id",self.id)):
            return ('Username already exists')
        if (self.dao.checkDuplicate("email",self.email)):
            return ('Email already exists')
        self.dao.storeInfo(self.__dict__)
        self.dao.commit()
        self.dao.close()
        return ('User successfully created')

class BaseDao(object):
    def initiateConn(self):
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse('removed db crendentials from this code because remnant tech is a public repo.')
        
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
    
    def resultAsDict(self):
        cols = [col[0] for col in self.cur.description]
        results = self.cur.fetchall()
        processedDict = {}
        for col_num,colName in enumerate(cols):
            processedDict[colName] = []
            for row in results:
                processedDict[colName].append(row[col_num])
        return processedDict
    
    def selectStatement(self, tblName, whereClause):
        if len(whereClause) == 0:
            query = sql.SQL("select * from {0}").format(
                sql.Identifier(tblName))
            self.cur.execute(query)
        else:
            whereCol = whereClause[0]
            whereVal = whereClause[1]
            selectWithTable = sql.SQL("select * from {0} where lower({1})= lower(%s)").format(
                sql.Identifier(tblName),sql.Identifier(whereCol))
            self.cur.execute(selectWithTable, (whereVal,))
    def urlToDict(self,url):
        parsedUrl = url.split('&')
        criteriaDict = {}
        excludedAttributes = ["b'csrfmiddlewaretoken", 'pass-repeat', 'csrfmiddlewaretoken']
        for element in parsedUrl:
            element_list = element.split('=')
            criterionKey = element_list[0]
            criterionVal = element_list[1]
            if criterionKey not in excludedAttributes:
                if criterionVal[-1] == "'":
                    criteriaDict[criterionKey] = criterionVal[:-1]
                else:
                    criteriaDict[criterionKey] = criterionVal
                
        return criteriaDict
            
        
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
        queryCol= 'Insert INTO tbluser ("admin","developer",'
        queryVal = ['1', '1']
        attributeExcluded = ['profileInfo', 'dao']
        for attribute in userDict:
            if attribute not in attributeExcluded:
                queryCol += '"' + attribute + '",'
                if userDict[attribute][-1] == "'":
                    userDict[attribute] = userDict[attribute][:-1]
                queryVal.append(userDict[attribute])
        
        queryCol = queryCol[:-1] + ') values %s'
        self.cur.execute(queryCol,
                            (tuple(queryVal),))
        
    def pullIds(self):
        self.cur.execute('select * from tbluser')
        id_list = [userId[0] for userId in self.cur.fetchall()]
        return id_list
    
    def authenticateUser(self, pass_input, identification):
        
        if identification.find('@') != -1:
            idCol = 'email'
        else:
            idCol = 'id'
        self.initiateConn()
        self.selectStatement('tbluser',[idCol,identification])
        retrievedUser = self.resultAsDict()
        if retrievedUser['id'] == []:
            return 'no user found'
        else:
            encryptedPass = retrievedUser['pass'][0]
            self.close()
            return check_password(pass_input,encryptedPass)
        
    
    def checkDuplicate(self, column, value):
        query = ('select count(' + '"' + column +'"' + ') from tbluser where '
                 'tbluser."' + column + '"=  %s')
        self.cur.execute(query,(value,))
        if (self.cur.fetchall()[0][0] > 0):
            return True
        else:
            return False


class ChurchProfile(Profile):
    def enableDao(self):
        setattr(self,'dao',ChurchProfileDao())
    def saveChurch(self):
        self.updateInfo()
        self.enableDao()
        self.dao.initiateConn()
        if (self.dao.checkDuplicate("name",self.name)):
            return ('church name already exists in the database')
        self.dao.storeInfo(self.__dict__)
        self.dao.commit()
        self.dao.close()
        return ('church registered successfully')



    
    
    
class ChurchProfileDao(BaseDao):
    def storeInfo(self, userDict):
        #store all info for tblUser
        #userDict = sampleUser.__dict__
        latLng = self.getGeocodes(userDict)
        if latLng != None:
            userDict['latitude'] = latLng[0]
            userDict['longitude'] = latLng[1]
        queryCol= 'Insert INTO "tblchurch" ('
        queryVal = []
        attributeExcluded = ['profileInfo', 'dao']
        for attribute in userDict:
            if attribute not in attributeExcluded:
                queryCol += '"' + attribute + '",'
                userDict[attribute] = str(userDict[attribute])
                if userDict[attribute][-1] == "'":
                    userDict[attribute] = userDict[attribute][:-1]
                queryVal.append(userDict[attribute])
        
        queryCol = queryCol[:-1] + ') values %s'
        self.cur.execute(queryCol,
                            (tuple(queryVal),))    
    def pullChurchName(self):
        self.cur.execute('select church_pk, name from tblchurch')
        church_dict = {}
        for row in self.cur.fetchall():
            church_dict[row[0]]= row[1]
        return church_dict
    def checkDuplicate(self, column, value):
        query = ('select count(' + '"' + column +'"' + ') from tblchurch where '
                 'tblchurch."' + column + '"=  %s')
        self.cur.execute(query,(value,))
        if (self.cur.fetchall()[0][0] > 0):
            return True
        else:
            return False
    def getGeocodes(self,userDict):
        address = ''
        if 'street_address' in userDict:
            address += userDict['street_address'] + ' '
            if 'city' in userDict:
                address += userDict['city'] + ' '
                if 'state' in userDict:
                    address += userDict['state'] + ' '
                    if 'country' in userDict:
                        address += userDict['country']
        googleAddress = geocoder.google(address)
        googleLatLng = googleAddress.latlng
        return googleLatLng
    

    def pullGeocodeByCriteria(self,criteria):
        self.initiateConn()
        self.selectStatement('tblchurch', [criteria[0], criteria[1]])
        resultDict= self.resultAsDict()
        if resultDict['church_pk'] == []:
            resultDict= "no results found"
        return resultDict


    

        

    

    

def testMain():
    parsedCriteria= urllib.parse.unquote_plus("csrfmiddlewaretoken=vC9WLHviiPksRxbS74nY0PlA5hI66ZGBHyissDvdUbUjh19eHVrT8hOwz5GCe6kX&name=Boston%20Imuel%20Church")
    newChurchDao = ChurchProfileDao()
    criteriaDict = newChurchDao.urlToDict(parsedCriteria)
    finalizedChurchList = []
    for criterion in criteriaDict:
        churchDict = newChurchDao.pullGeocodeByCriteria([criterion,criteriaDict[criterion]])
        finalizedChurchList.append(churchDict)
    newChurchDao.close()
    return (json.dumps(finalizedChurchList))

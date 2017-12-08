import os
import psycopg2
#import urlparse
import urllib.parse




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
            
            if (profile_key not in (attribute_excluded)):
                profile_dict[profile_key] = profile_val
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
    pass

class UserProfileDao(UserProfile):
    def storeInfo(self):
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
        #store all info for tblUser
        queryCol= '"Admin", "Developer",'
        queryVal = "1, 1, "
        
        for attribute in self.__dict__:
            if attribute != 'profileInfo':
                queryCol += '"' + attribute + '",'
                if attribute == 'ChurchID':
                    queryVal += self.__dict__[attribute] + ","
                else:
                    queryVal += ("'" + self.__dict__[attribute] + "',")

        userQuery = ('Insert INTO "tblUser" ({0}) values ({1})'.format(queryCol[:-1],
                     queryVal[:-2]))
        cur.execute(userQuery)
        conn.commit()
    
class ChurchProfile(Profile):
    def storeInfo(self): 
        #store all info for tblUser
        queryColumns = {'church' : ""}
        queryValues = {'church' : ""}
        
        for attribute in self.__dict__:
            if attribute != 'profileInfo':
                queryColumns['church'] += '"' + attribute + '", '
                queryValues['church'] += ("\'" + self.__dict__[attribute] + "\', ")

        churchQuery = ('Insert INTO "tblUser" ({0}) values ({1})'.format(queryColumns['church'],
                     queryValues['church']))
        return churchQuery
    def getChurchID(self):
        pass
    def updateChurchInfo(self):
        pass

class ProfileDao(object):
    pass
        
    

def testMain():
    sampleUser = 'FirstName=djangotest&LastName=123&ID=jaewonrt&Pass=remnant&Email=jaewonrt@gmail.com'
    sampleUser = UserProfile(sampleUser)
    sampleUser.updateInfo()
    UserProfileDao.storeInfo(sampleUser)
    return sampleUser

            
        
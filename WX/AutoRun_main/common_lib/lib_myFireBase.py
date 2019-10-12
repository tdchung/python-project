#!/usr/bin/python
# -*- coding: utf8 -*-

# date:    x
# author:  tdchung
# mail:    tdchung.9@gmail.com
#
#
# update
#
from __future__ import print_function
import json
import hashlib
import base64

# user lib
try:
    from lib_myPrint import MyPrint
except:
    print("Import my print ERROR")
    class MyPrint():
        def __init__(self, logLevel=""):
            pass
        def debug(self, string):
            print(string)
        def error(self, string):
            print(string)


myPrint = MyPrint(logLevel="debug")

IDontWantTestNow = False

class MyFireBase():
    def __init__(self, url=u'', isBase64=False):
        self.url = url
        self.isBase64 = isBase64
        myPrint.debug(self.url)

        if isBase64:
            try:
                self.url = base64.b64decode(url).decode('utf-8')
                myPrint.debug(self.url)
            except:
                myPrint.error("Url not correct format")

    # default in /users
    def validateUser(self, user="", password=""):
        """
        :param user:
        :param password:
        :return:  1: user and password is correct
                  0: password is incorrect
                 -1: user not existed
                 -2: other failed. Exception
        """

        if not self.isUserExisted(user):
            myPrint.error("User not exist")
            return -1
        try:
            # 
            from firebase import firebase
        except Exception as e:
            myPrint.info("Validate import exception: %s" % str(e))
            return -2
        try:
            user = hashlib.sha256(user.encode())
            user = user.hexdigest()

            password = hashlib.sha256(password.encode())
            password = password.hexdigest()
            my_firebase = firebase.FirebaseApplication(self.url, None)
            myPrint.debug("DEBUG: firebase: " + str(firebase))
            result = my_firebase.get("/users/", None)
            myPrint.debug("DEBUG: result: " + str(result))
            myPrint.debug("DEBUG: result type: " + str(type(result)))
            list_key = list(result.keys())
            myPrint.debug("DEBUG: list key: " + str(list_key))
            data = result
            myPrint.debug("DEBUG: data 0: " + str(data[list_key[0]]))
            myPrint.debug("DEBUG: data: " + str(data))
            for i in range(len(list_key)):
                myPrint.debug(
                    "DEBUG: validate user. num %d. type %s" % (i + 1, str(type(data[list_key[i]]))))
                myPrint.debug(
                    "DEBUG: validate user. num %d. type %s" % (i + 1, str(data[list_key[i]])))
                json_data = json.loads(data[list_key[i]])
                if (user == json_data["name"]) and (password == json_data["password"]):
                    return 1
            return 0
        except:
            # TODO:
            myPrint.debug("exception: internet???")
            return -2

    def isUserExisted(self, user=u''):
        """
        :param user:
        :return:
        """
        user_en = hashlib.sha256(user.encode()).hexdigest()
        try:
            from firebase import firebase
        except Exception as e:
            myPrint.debug("Validate import exception: %s" % str(e))
            return False
        try:
            fb = firebase.FirebaseApplication(self.url, None)

            result = fb.get("/users/", None)
            for i in range(len(list(result.keys()))):
                json_data = json.loads(result[list(result.keys())[i]])
                myPrint.debug(str(json_data))
                if user_en == json_data["name"]:
                    myPrint.debug("User already existed")
                    return True
        except Exception as e:
            # TODO:
            myPrint.debug(str(e))
            myPrint.debug("exception: internet???")
            return False
        return False

    # create new account, put to firebase
    def createNewAccount(self, user="", password="", email=""):
        """
        :param user:
        :param password:
        :param email:
        :return:
        """
        user_en = hashlib.sha256(user.encode()).hexdigest()
        pw_en = hashlib.sha256(password.encode()).hexdigest()
        myPrint.debug(user)
        myPrint.debug(password)
        myPrint.debug(email)
        myPrint.debug(user_en)
        myPrint.debug(pw_en)
        data = {"name": user_en, "password": pw_en, "user_str": user, "email": email}
        data = json.dumps(data)
        myPrint.debug(data)
        if IDontWantTestNow:
            myPrint.debug("not post")
            return False
        try:
            from firebase import firebase
        except Exception as e:
            myPrint.debug("Validate import exception: %s" % str(e))
            return False
        try:
            fb = firebase.FirebaseApplication(self.url, None)

            result = fb.get("/users/", None)
            for i in range(len(list(result.keys()))):
                json_data = json.loads(result[list(result.keys())[i]])
                myPrint.debug(str(json_data))
                if (user_en == json_data["name"]):
                    myPrint.error("User already existed")
                    return False
            fb.post("/users/", data)
        except Exception as e:
            # TODO:
            myPrint.debug(str(e))
            myPrint.debug("exception: internet???")
            return False
        return True

    def changePassword(self, user=u'', old_password=u'', new_password=u''):
        """
        :param user:
        :param old_password:
        :param new_password:
        :return:
        """
        if not self.validateUser(user, old_password):
            # TODO: return old password is not corrected
            return -1
        # TODO: get name id, then update Password
        return 1 # or 0 in case cannot put

    def removeUser(self, user=u''):
        """
        :param user:
        :return:
        """
        # TODO: remove user
        pass

    def __del__(self):
        pass


if __name__ == '__main__':
    # test
    MyFireBase = MyFireBase()
    MyFireBase.isUserExisted("")
    pass
    
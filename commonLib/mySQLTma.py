#
from __future__ import print_function
from lib_myPrint import MyPrint

import os
import sys
import time

import mysql.connector

# user lib
ROOT = "{}/..".format(os.path.abspath(__file__).replace(os.path.basename(__file__), ""))
sys.path.append("{}/commonLib".format(ROOT))


#
try:
    sys.path.append("{}/Config".format(ROOT))
    from config import *
    if MYSQL_HOST is None or MYSQL_USER is None or MYSQL_PASSWD is None or DB is None:
        raise Exception
except:
    # raise Exception
    # set here
    MYSQL_HOST = "MyHost"
    MYSQL_USER = "MyUserName"
    MYSQL_PASSWD = "MyPassword"
    DB = "MyDbName"


# define print
myPrint = MyPrint(
    saveLog=True, logFile="{}/Logs/test-mysql_lib.txt".format(ROOT))


class MySQLTma():
    def __init__(self,
                 host=MYSQL_HOST,
                 user=MYSQL_USER,
                 passwd=MYSQL_PASSWD,
                 database=DB
                 ):

        self.mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            auth_plugin='mysql_native_password',
            database=database
        )
        self.mycursor = self.mydb.cursor()
        self.database = database

        myPrint.debug(self.mydb)
        myPrint.debug(self.mycursor)
        myPrint.debug(self.database)

    def __db_execute_cmd_only(self, cmd):
        myPrint.debug("COMMAND_ONLY: ", cmd)
        try:
            self.mycursor.execute(cmd)
            self.mydb.commit()
            return True, None
        except Exception as e:
            myPrint.debug(e)
            return False, e

    def __db_execute_cmd(self, cmd):
        myPrint.debug("COMMAND: ", cmd)
        self.mycursor.execute(cmd)
        results = self.mycursor.fetchall()
        results_list = [item[0] for item in results]
        myPrint.debug("__db_execute_cmd", results_list)
        return results_list

    # NOTE: do not use
    def list_all_databases(self):
        sql_cmd = "SHOW databases"
        return self.__db_execute_cmd(sql_cmd)

    # NOTE: do not use
    def create_database(self, database_name):
        sql_cmd = "CREATE DATABASE {}".format(database_name)
        return self.__db_execute_cmd_only(sql_cmd)

    def list_all_tables(self):
        sql_cmd = "SHOW TABLES"
        return self.__db_execute_cmd(sql_cmd)

    def create_table(self, table_name, *argv):
        # argumets is tuple or array. (), []  ["column_name", lenght]
        # TODO: check input value
        sql_cmd = "CREATE TABLE {}".format(table_name)
        if 1 == len(argv):
            sql_cmd += " (`{}` VARCHAR({}))".format(argv[0][0], argv[0][1])
        else:
            for i in range(len(argv)):
                if 0 == i:
                    sql_cmd += " (`{}` VARCHAR({}), ".format(
                        argv[i][0], argv[i][1])
                elif len(argv)-1 == i:
                    sql_cmd += " `{}` VARCHAR({}))".format(
                        argv[i][0], argv[i][1])
                else:
                    sql_cmd += " `{}` VARCHAR({}), ".format(
                        argv[i][0], argv[i][1])
        # myPrint.debug(sql_cmd)
        return self.__db_execute_cmd_only(sql_cmd)

    def delete_table(self, table_name):
        sql_cmd = "DROP TABLE {}".format(table_name)
        return self.__db_execute_cmd_only(sql_cmd)

    def check_table_existed(self, table_name):
        tables = self.list_all_tables()
        if table_name in tables:
            myPrint.debug(table_name, ' was found!')
            return True
        else:
            myPrint.debug(table_name, ' was not found!')
            return False

    def insert_into_table(self, table_name, *argv):
        # argumets is tuple or array. (), []  ["column_name", "data"]
        # TODO: check input value
        # sql_cmd = "INSERT INTO {}".format( table_name)
        column = ""
        value = ""
        if 1 == len(argv):
            column += "(`{}`)".format(argv[0][0])
            value += "(\"{}\")".format(argv[0][1])
        else:
            for i in range(len(argv)):
                if 0 == i:
                    column += "(`{}`, ".format(argv[i][0])
                    value += "(\"{}\", ".format(argv[i][1])
                elif len(argv)-1 == i:
                    column += "`{}`)".format(argv[i][0])
                    value += "\"{}\")".format(argv[i][1])
                else:
                    column += "`{}`, ".format(argv[i][0])
                    value += "\"{}\",".format(argv[i][1])
        sql_cmd = "INSERT INTO {} {} VALUES {}".format(
            table_name, column, value)
        # myPrint.debug(sql_cmd)
        return self.__db_execute_cmd_only(sql_cmd)

    def get_columns(self, table_name):
        sql_cmd = sql = "SHOW COLUMNS FROM `{}`".format(table_name)
        return self.__db_execute_cmd(sql_cmd)

    def __del__(self):
        # TODO: cannot use open
        # https://stackoverflow.com/questions/23422188/why-am-i-getting-nameerror-global-name-open-is-not-defined-in-del
        # myPrint.debug("delete data pointer")
        # print(self.mydb.close())
        self.mydb.close()


if __name__ == "__main__":
    mysqldb = MySQLTma()
    # mysqldb.list_all_databases()
    # mysqldb.list_all_tables()

    if not mysqldb.check_table_existed("test_table"):
        mysqldb.create_table("test_table", ("test", 10),
                             ("dsadasdasd", 100),
                             ("dsadsssssasdasd", 10)
                             )
    mysqldb.insert_into_table("test_table", ("test", 124524),
                              ("dsadasdasd", "100"),
                              ("dsadsssssasdasd", "123")
                              )
    mysqldb.get_columns("test_table")
    mysqldb.delete_table("test_table")

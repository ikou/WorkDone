#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import json
import mysql.connector

try:
        cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='work_done')

        cursor = cnx.cursor()

        query = ("SELECT * FROM workdone_workinfo ")

        cursor.execute(query)

        for cc in cursor:
                for ccc in cc:
                        print ccc

except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
        else:
                print(err)
else:
        cnx.close()




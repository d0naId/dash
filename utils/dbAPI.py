import cx_Oracle
import pandas as pd
import sys

class Oracleclient:
    def __init__(self, user, passwd, host, port, service_name):
        self.dns = cx_Oracle.makedsn(host,port,service_name=service_name)
        self.user = user
        self.passwd = passwd
#         self.conn = cx_Oracle.connect(user,passwd,dsn)

    def request(self, request):
        with cx_Oracle.connect(self.user, self.passwd, self.dns, encoding='UTF-8') as conn:
            df = pd.read_sql(request, conn)
        return df

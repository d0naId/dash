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

class DataPrepare():
    def __init__(self, min_date, max_date, req):
        self.min_date = min_date
        self.max_date = max_date
        self.req = req
        self.df = pd.DataFrame()
        self.db = None

    def connection(self, user, passwd, host, port, service_name):
        self.db = Oracleclient(user, passwd, host, port, service_name)

    def take_data(self):
        self.df = self.db.request(self.req.format(self.max_date, self.min_date))

    def get_new_date(self, new_max):
        if new_max > self.max_date:
            self.df = self.df.append(self.db.request(self.req.format(new_max, self.max_date)))
            self.max_date = new_max

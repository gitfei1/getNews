# -*-coding:utf-8-*-
__author__ = 'howie'
import tornado.web
import hashlib
import json
from config.n_conf import admin
import methods.db as mSql


class Confirm(tornado.web.RequestHandler):
    # time=1 tooken=764bfd755bc07f6871eee104219b2b2c
    def tooken(self, time):
        tooken = "apiNews"
        tooken = hashlib.md5((tooken + str(time)).encode("utf-8")).hexdigest()
        return tooken


class Register(Confirm):
    def get(self, *args, **kwargs):
        name = self.get_argument('name')
        passwd = self.get_argument('passwd')
        phone = self.get_argument('phone')
        getTooken = self.get_argument('tooken')
        time = self.get_argument('time')
        tooken = self.tooken(time=time)
        if getTooken == tooken:
            passwd = hashlib.md5((admin["TOKEN"] + passwd).encode("utf-8")).hexdigest()
            numSql = " select count(*) from user"
            try:
                mSql.cur.execute(numSql)
                # 提交到数据库执行
                num = mSql.cur.fetchall()
                user_id = ("%06d"%(num[0][0]+1))
                insertSql = mSql.insert_table(table="user", field="(user_id,phone,name,passwd,time)",
                                      values="('" + str(user_id) + "','" + phone + "','" + name + "','" + passwd + "',now())")
                if insertSql:
                    data = {"user_id":user_id,"flag":1}
                    result = {"message": "success", "data": data}
                    result = json.dumps(result)
                    self.write(result)
            except:
                # 出现错误则回滚
                mSql.conn.rollback()

        else:
            data = {}
            result = {"message": "failed", "data": data,"flag":0}
            result = json.dumps(result)
            self.write(result)

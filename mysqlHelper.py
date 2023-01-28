import contextlib
import pymysql
from pymysql.cursors import DictCursor, Cursor

MYSQL_config = {
    'host': "localhost",
    'port': 3306,
    'user': 'root',
    'password': '12345678',
    'database': 'a_job',
}


class MySQLConnect():
    def __init__(self, cursorclass=DictCursor, config=MYSQL_config):
        self.connection = pymysql.connect(host=config['host'],
                                          port=config['port'],
                                          user=config['user'],
                                          password=config['password'],
                                          db=config['database'],
                                          cursorclass=cursorclass,
                                          charset='utf8mb4'
                                          )
        self.connection.autocommit(True)

    # 通过以下两个方法判断mysql是否连通，以及重连。
    def is_connected(self, num=28800, stime=3):  # 重试连接总次数为1天,这里根据实际情况自己设置,如果服务器宕机1天都没发现就......
        _number = 0
        _status = True
        while _status and _number <= num:
            """Check if the server is alive"""
            try:
                self.connection.ping(reconnect=True)  # ping 校验连接是否异常
                _status = False
            except:
                if self.re_connect() == True:  # 重新连接,成功退出
                    _status = False
                    break
                _number += 1
                time.sleep(stime)  # 连接不成功,休眠3秒钟,继续循环，知道成功或重试次数结束

    def re_connect(self):
        try:
            self.connection = pymysql.connect(host=self.MYSQL_config['host'],
                                              port=self.MYSQL_config['port'],
                                              user=self.MYSQL_config['user'],
                                              password=self.MYSQL_config['password'],
                                              db=self.MYSQL_config['db'],
                                              cursorclass=self.cursorclass,
                                              )
            self.connection.autocommit(True)
            return True
        except:
            return False

    @contextlib.contextmanager
    def cursor(self, cursor=None):
        """通过yield返回一个curosr对象
        """
        cursor = self.connection.cursor(cursor)
        try:
            yield cursor
        except Exception as err:
            self.connection.rollback()
            raise err
        finally:
            cursor.close()

    def close(self):
        self.connection.close()

    def fetchone(self, sql=None):
        self.is_connected()
        if sql:
            with self.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchone()

        if self.connection.cursorclass == Cursor:
            return ()
        else:
            return {}

    # 查询
    def fetchall(self, sql=None):
        self.is_connected()
        if sql:
            with self.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
        return []

    # 插入一条数据
    def execute(self, sql=None):
        self.is_connected()
        if sql:
            with self.cursor() as cursor:
                return cursor.execute(sql)

    # 插入多条数据
    def executemany(self, sql=None, data=None):
        self.is_connected()
        if sql and data:
            with self.cursor() as cursor:
                return cursor.executemany(sql, data)


def get_a_conn(cursorclass=DictCursor):
    return MySQLConnect(cursorclass)



if __name__ == '__main__':
    # 查询
    mysql = get_a_conn()
    # sql = 'select * from tb_movie_year'
    # result = mysql.fetchall(sql)
    # for item in result:
    #     print(item)

    # 插入一条
    # values = ('22', '无敌浩克', '科幻/惊悚', '5389', '28', '21', '美国', '2008-08-20', '2008')
    # sql = 'insert into tb_movie_year (id,movie_name,movie_type,movie_money,movie_price,movie_peo,movie_country,movie_date,movie_year) values("%s","%s","%s","%s","%s","%s","%s","%s","%s")' % values
    # mysql.execute(sql)

    # 插入多条
    # values1 = ('3', '无敌浩克', '科幻/惊悚', '5389', '28', '21', '美国', '2008-08-20', '2008')
    # values2 = ('4', '无敌浩克', '科幻/惊悚', '5389', '28', '21', '美国', '2008-08-20', '2008')
    # data = [values1, values2]
    # sql = 'insert into tb_movie_year (id,movie_name,movie_type,movie_money,movie_price,movie_peo,movie_country,movie_date,movie_year) values(%s,"%s","%s","%s","%s","%s","%s","%s","%s")'
    # mysql.executemany(sql, data)

    # 删除
    # sql = 'truncate table tb_movie_year'
    # mysql.fetchall(sql)

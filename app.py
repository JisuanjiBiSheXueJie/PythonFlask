from mysqlHelper import get_a_conn
from flask import Flask, request, jsonify
from data_zhilian import getZhilian
from getCloud import GetWordCloud
from zhongweishu import median

# 创建应用程序
app = Flask(__name__)
app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'


# https://blog.51cto.com/u_15624328/5281760

# 取消收藏
@app.route('/delCollect', methods=['POST'])
def delCollect():
    try:
        user_id = request.json.get('user_id')
        job_id = int(request.json.get('job_id'))
        mysql = get_a_conn()
        sql = "delete from tbl_user_job where user_id = '%s' and job_id = '%s'" % (user_id, job_id)
        mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': '取消成功'})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})

# 收藏
@app.route('/collect', methods=['POST'])
def collect():
    try:
        user_id = request.json.get('user_id')
        job_id = int(request.json.get('job_id'))
        mysql = get_a_conn()
        sql = "insert into tbl_user_job (user_id,job_id) values (%s,%s) " % (user_id, job_id)
        mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': '新增成功'})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})

# 公司性质
@app.route('/getComXz', methods=['POST'])
def getComXz():
    mysql = get_a_conn()
    sql = "SELECT companytype_text value,companytype_text label from tbl_job WHERE companytype_text is not null and companytype_text != '' GROUP BY companytype_text  "
    result = mysql.fetchall(sql)
    return jsonify({'code': '200', 'info': result})

# 公司规模
@app.route('/getComSize', methods=['POST'])
def getComSize():
    mysql = get_a_conn()
    sql = "SELECT company_size value,company_size label from tbl_job WHERE company_size is not null and company_size != '' GROUP BY company_size "
    result = mysql.fetchall(sql)
    return jsonify({'code': '200', 'info': result})

# 城市字典表
@app.route('/getCityDict', methods=['POST'])
def getCityDict():
    try:
        mysql = get_a_conn()
        sql = "select city_code value,city_name label from tbl_city"
        res = mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': res})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})

# 处理薪资信息
@app.route('/get_salary', methods=['POST'])
def get_salary():
    try:
        mysql = get_a_conn()
        sql = "select * from tbl_job"
        result = mysql.fetchall(sql)
    except Exception as e:
        return jsonify({'code': '500', 'info': e})


# 薪资预测
@app.route('/yuce', methods=['POST'])
def yuce():
    try:
        search = request.json.get('search', None)
        location = request.json.get('location', None)
        xueli = request.json.get('xueli', None)
        jingyan = request.json.get('jingyan', None)
        company = request.json.get('company', None)
        companytype_text = request.json.get('companytype_text', None)
        mysql = get_a_conn()
        sql = "SELECT ( t.a + t.b ) / 2 avg0 FROM ( " \
              "	SELECT q, " \
              "	case when a like '%千'  then a*1000  " \
              "		 when a like '%千' or a like '%千及以下'  then a*1000  " \
              "		 when a not like '%千' and a not like '%万' and b like '%万' then a*10000 " \
              "		 when a not like '%千' and a not like '%万' and b like '%千' then a*1000 " \
              "		 when a not like '%千' and a not like '%万' and (b like '%万·13薪' or b like '%万·14薪')then a*10000 " \
              "		 when a not like '%千' and a not like '%万' and b like '%万/年' then  round(a*10000/12,0) " \
              "		 else 0 end as a, " \
              "	case when b like '%千'  then b*1000  " \
              "		 when b like '%千' or a like '%千及以下'  then b*1000  " \
              "		 when b like '%万' then b*10000 " \
              "		 when b like '%万·13薪' or b like '%万·14薪' then b*10000 " \
              "		 when b like '%万/年' then  round(b*10000/12,0) " \
              "		 else 0 end as b, " \
              "	salary,search,xueli,location FROM ( " \
              "		SELECT substring_index( salary, '·13薪', 1 ) AS q,SUBSTRING_INDEX( salary, '-', 1 ) a,SUBSTRING_INDEX( salary, '-',- 1 ) b,salary,search,xueli,location  FROM tbl_job  WHERE 1 = 1  "
        if search != None and search != '' and search != 'undefined':
            sql += " and (job_name like '%"
            sql += search
            sql += " %' or search like '%"
            sql += search
            sql += "%')"
        if xueli != None and xueli != '' and xueli != 'undefined':
            sql += " and xueli = '%s'" % (xueli)
        if location != None and location != '' and location != 'undefined':
            sql += " and location like '%"
            sql += location
            sql += "%' "
        if jingyan != None and jingyan != '' and jingyan != 'undefined':
            sql += " and jingyan = '%s'" % (jingyan)
        if company != None and company != '' and company != 'undefined':
            sql += " and company_size = '%s'" % (company)
        if companytype_text != None and companytype_text != '' and companytype_text != 'undefined':
            sql += " and companytype_text = '%s'" % (companytype_text)
        sql += " ) x) t"

        print(sql)
        result = mysql.fetchall(sql)
        res = '0'
        if result:
            xinziList = ''
            for avg in result:
                xinziList += str(avg.get('avg0'))
                xinziList += ','
            res = median(list(eval(xinziList)))
        return jsonify({'code': '200', 'info': res})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})


# 公司信息分析
@app.route('/gsinfo', methods=['POST'])
def gsinfo():
    try:
        type = request.form.get('type', None)
        search = request.form.get('search', None)
        location = request.form.get('location', None)
        xueli = request.form.get('xueli', None)
        mysql = get_a_conn()
        if type == 'sx':  # 公司属性
            sql = "SELECT company_sx name,count(company_sx) value FROM tbl_job where 1=1 "
        if type == "xz":  # 公司性质
            sql = "SELECT companytype_text name,count(companytype_text) value FROM tbl_job where 1=1 "
        if type == 'size':  # 公司规模
            sql = "SELECT company_size name,count(company_size) value FROM tbl_job where 1=1 "

        if search != None and search != '':
            sql += " and search = '%s'" % (search)
        if location != None and location != '':
            sql += " and location = '%s'" % (location)
        if xueli != None and xueli != '':
            sql += " and xueli = '%s'" % (xueli)

        if type == 'sx':  # 公司属性
            sql += "GROUP BY company_sx ORDER BY count(company_sx) desc limit 15 "
        if type == "xz":  # 公司性质
            sql += "GROUP BY companytype_text ORDER BY count(companytype_text) desc "
        if type == 'size':  # 公司规模
            sql += "GROUP BY company_size ORDER BY count(company_size) desc "
        result = mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': result, 'type': type})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})


# 生成福利词云
@app.route('/fuli', methods=['POST'])
def fuli():
    search = request.json.get('search', None)
    location = request.json.get('location', None)
    xueli = request.json.get('xueli', None)
    jingyan = request.json.get('jingyan', None)
    short_evals = ""
    mysql = get_a_conn()
    sql = "SELECT fuli FROM tbl_job WHERE fuli != ''"
    if search != None and search != '' and search != 'undefined':
        sql += " and (job_name like '%"
        sql += search
        sql += " %' or search like '%"
        sql += search
        sql += "%')"
    if xueli != None and xueli != '' and xueli != 'undefined':
        sql += " and xueli = '%s'" % (xueli)
    if location != None and location != '' and location != 'undefined':
        sql += " and location like '%"
        sql += location
        sql += "%' "
    if jingyan != None and jingyan != '' and jingyan != 'undefined':
        sql += " and jingyan = '%s'" % (jingyan)
    evals = mysql.fetchall(sql)
    if (len(evals) > 0):
        for item in evals:
            short_evals += item.get('fuli')
    else:
        short_evals += '暂无数据'
    result = GetWordCloud(short_evals)
    if result == '1':
        return jsonify({'code': '200', 'info': '生成词云图成功'})
    else:
        return jsonify({'code': '500', 'info': '生成词云图失败'})


# 经验要求
@app.route('/jingyan', methods=['POST'])
def jingyan():
    mysql = get_a_conn()
    sql = "SELECT jingyan value,jingyan label FROM tbl_job GROUP BY jingyan"
    result = mysql.fetchall(sql)
    return jsonify({'code': '200', 'info': result})


# 学历要求
@app.route('/xueli', methods=['POST'])
def xueli():
    mysql = get_a_conn()
    sql = "SELECT xueli value,xueli label FROM tbl_job GROUP BY xueli"
    result = mysql.fetchall(sql)
    return jsonify({'code': '200', 'info': result})


# 招聘要求
@app.route('/yaoqiu', methods=['POST'])
def yaoqiu():
    search = request.form.get('search', None)
    location = request.form.get('location', None)
    mysql = get_a_conn()
    sql_jingyan = "SELECT jingyan name,count(jingyan) value FROM tbl_job where 1=1  "
    sql_xueli = "SELECT xueli name,count(xueli) value FROM tbl_job where 1=1  "
    if search != None and search != '':
        sql_jingyan += " and search = '%s'" % (search)
        sql_xueli += " and search = '%s'" % (search)
    if location != None and location != '':
        sql_jingyan += " and location = '%s'" % (location)
        sql_xueli += " and location = '%s'" % (location)
    sql_jingyan += "GROUP BY jingyan"
    sql_xueli += "GROUP BY xueli"
    result_jingyan = mysql.fetchall(sql_jingyan)
    result_xueli = mysql.fetchall(sql_xueli)
    return jsonify({'code': '200', 'info': result_jingyan, 'info2': result_xueli})


# 薪资比例
@app.route('/zpXinzi', methods=['POST'])
def zpXinzi():
    search = request.form.get('search', None)
    xueli = request.form.get('xueli', None)
    location = request.form.get('location', None)
    mysql = get_a_conn()
    sql = "SELECT z.xinzi name,count(z.xinzi) value from (  " \
          "	SELECT case when (y.a+y.b)/2 < 5000 then '小于5千元'" \
          "					when (y.a+y.b)/2 >= 5000 && (y.a+y.b)/2 < 10000 then '5千-1万元'" \
          "					when (y.a+y.b)/2 >= 10000 && (y.a+y.b)/2 < 15000 then '1万-1.5万元'  " \
          "					when (y.a+y.b)/2 >= 15000 && (y.a+y.b)/2 < 20000 then '1.5万-2万元'" \
          "					when (y.a+y.b)/2 >= 20000 && (y.a+y.b)/2 < 25000 then '2万-2.5万元'" \
          "					when (y.a+y.b)/2 >= 25000 && (y.a+y.b)/2 < 3000 then '2万-2.5万元'" \
          "					else '大于3万'" \
          "					end xinzi" \
          "	from (    " \
          "	SELECT q, " \
          "	case when a like '%千'  then a*1000  " \
          "		 when a like '%千' or a like '%千及以下'  then a*1000  " \
          "		 when a not like '%千' and a not like '%万' and b like '%万' then a*10000 " \
          "		 when a not like '%千' and a not like '%万' and b like '%千' then a*1000 " \
          "		 when a not like '%千' and a not like '%万' and (b like '%万·13薪' or b like '%万·14薪')then a*10000 " \
          "		 when a not like '%千' and a not like '%万' and b like '%万/年' then  round(a*10000/12,0) " \
          "		 else 0 end as a, " \
          "	case when b like '%千'  then b*1000  " \
          "		 when b like '%千' or a like '%千及以下'  then b*1000  " \
          "		 when b like '%万' then b*10000 " \
          "		 when b like '%万·13薪' or b like '%万·14薪' then b*10000 " \
          "		 when b like '%万/年' then  round(b*10000/12,0) " \
          "		 else 0 end as b, " \
          "	salary,search,xueli,location FROM ( " \
          "		SELECT substring_index( salary, '·13薪', 1 ) AS q,SUBSTRING_INDEX( salary, '-', 1 ) a,SUBSTRING_INDEX( salary, '-',- 1 ) b,salary,search,xueli,location  FROM tbl_job  " \
          "  where 1=1 "
    if search != None and search != '':
        sql += " and search = '%s'" % (search)
    if xueli != None and xueli != '':
        sql += " and xueli = '%s'" % (xueli)
    if location != None and location != '':
        sql += " and location = '%s'" % (location)
    sql += " ) x) y) z GROUP BY z.xinzi "
    result = mysql.fetchall(sql)
    return jsonify({'code': '200', 'info': result})


# 城市招聘分布
@app.route('/zpcity', methods=['POST'])
def zpcity():
    search = request.form.get('search', None)
    mysql = get_a_conn()
    sql = 'SELECT t.location name,count(t.location) value FROM tbl_job t  WHERE 1=1 '
    if search != None and search != '':
        sql += " and search = '%s'" % (search)
    sql += " group by t.location ORDER BY count(t.location) desc limit 30 "
    result = mysql.fetchall(sql)
    return jsonify({'code': '200', 'info': result})


# 用户数据
@app.route('/delData', methods=['POST'])
def delData():
    try:
        id = request.form.get('id')
        if (id == None or id == '' or id == 'undefined'):
            return jsonify({'code': '500', 'info': 'id不存在，删除失败'})
        mysql = get_a_conn()
        sql = "delete from tbl_job where id =  '%s'" % id
        mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': '删除成功'})
    except Exception as e:
        return jsonify({'code': '500', 'info': '删除失败' + e})


# 数据概览
@app.route('/getDatas', methods=['POST'])
def getDatas():
    pageno = int(request.json.get('pageNo', 1))
    pagesize = int(request.json.get('pageSize', 10))
    search = request.json.get('search', None)
    location = request.json.get('location', None)
    xueli = request.json.get('xueli', None)
    user_id = request.json.get('user_id')
    searchType = request.json.get('searchType')
    mysql = get_a_conn()
    sql = "SELECT *,(SELECT count(1) FROM tbl_user_job WHERE job_id = t.id and user_id = " + str(user_id) + ") is_collect FROM tbl_job t WHERE 1=1 "
    if search != None and search != '':
        sql += " and (job_name like '%"
        sql += search
        sql += " %' or search like '%"
        sql += search
        sql += "%') "
    if xueli != None and xueli != '':
        sql += " and xueli = '%s'" % (xueli)
    if location != None and location != '':
        sql += " and location like '%"
        sql += location
        sql += "%' "
    if searchType != None and searchType != '' and searchType == '0':
        sql += " and (SELECT count(1) FROM tbl_user_job WHERE job_id = t.id and user_id = " + str(user_id) + ")  > 0 "
    sql += " ORDER BY create_time desc limit %s,%s" % ((pageno - 1) * pagesize, pagesize)
    result = mysql.fetchall(sql)
    sql_count = 'select count(1) num from tbl_job  t WHERE 1=1 '
    if search != None and search != '':
        sql_count += " and (job_name like '%"
        sql_count += search
        sql_count += " %' or search like '%"
        sql_count += search
        sql_count += "%') "
    if xueli != None and xueli != '':
        sql_count += " and xueli = '%s'" % (xueli)
    if location != None and location != '':
        sql_count += " and location like '%"
        sql_count += location
        sql_count += "%' "
    if searchType != None and searchType != '' and searchType == '0':
        sql_count += " and (SELECT count(1) FROM tbl_user_job WHERE job_id = t.id and user_id = " + str(user_id) + ")  > 0 "
    count = mysql.fetchall(sql_count)
    total = count[0].get('num')
    return jsonify({'code': '200', 'info': result, 'pageno': pageno, 'pagesize': pagesize, 'total': total})


# 获取日志
@app.route('/getLogs', methods=['POST'])
def getLogs():
    pageno = int(request.json.get('pageNo', 1))
    pagesize = int(request.json.get('pageSize', 10))
    userRole = request.json.get('userRole')
    userName = request.json.get('userName')
    mysql = get_a_conn()
    sql = "SELECT * FROM tbl_data_log where 1=1 "
    if userRole != None and userRole != '' and userRole != '1':
        sql += "and user_name = '"  + str(userName) + "'"
    sql += "ORDER BY end_time desc limit %s,%s" % ((pageno - 1) * pagesize, pagesize)
    result = mysql.fetchall(sql)
    sql_count = 'select count(1) num from tbl_data_log where 1=1 '
    if userRole != None and userRole != '' and userRole != '1':
        sql_count += "and user_name = '"  + str(userName) + "'"
    count = mysql.fetchall(sql_count)
    total = count[0].get('num')
    return jsonify({'code': '200', 'info': result, 'pageno': pageno, 'pagesize': pagesize, 'total': total})


# 爬取数据
@app.route('/getJobData', methods=['POST'])
def getJobs():
    username = request.json.get('username')
    search = request.json.get('search', '+')
    pagesize = int(request.json.get('pageSize', 2))
    city_id = request.json.get('city_id', 358)
    if search == '':
        search = ''
    if city_id == '':
        city_id = 358
    result = getZhilian(username,city_id, search, pagesize)
    return jsonify({'code': '200', 'info': result})


# 用户新增
@app.route('/addUser', methods=['POST'])
def addUser():
    try:
        account = request.json.get('account')
        name = request.json.get('name')
        email = request.json.get('email', None)
        phone = request.json.get('phone', None)
        role = request.json.get('role', None)
        remarks = request.json.get('remarks', None)
        mysql = get_a_conn()
        sql = "insert tbl_user (name,account,pwd,email,phone,login_flag,remarks,role) values ('%s','%s','%s','%s','%s','%s','%s','%s') " % (
            name, account, '123456', email, phone, '1', remarks, role)
        mysql.fetchall(sql)

        return jsonify({'code': '200', 'info': '新增成功'})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})


# 用户编辑
@app.route('/editUser', methods=['POST'])
def editUser():
    try:
        id = request.json.get('id')
        name = request.json.get('name')
        email = request.json.get('email', None)
        phone = request.json.get('phone', None)
        role = request.json.get('role', None)
        remarks = request.json.get('remarks', None)
        mysql = get_a_conn()
        sql = "update tbl_user set name = '%s',email='%s',phone='%s',role='%s',remarks='%s' where id = '%s'" % (
            name, email, phone, role, remarks, id)
        mysql.fetchall(sql)

        return jsonify({'code': '200', 'info': '修改成功'})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})


# 用户停用
@app.route('/stopUser', methods=['POST'])
def stopUser():
    try:
        id = request.form.get('id')
        if (id == None or id == '' or id == 'undefined'):
            return jsonify({'code': '500', 'info': 'id不存在，启用失败'})
        mysql = get_a_conn()
        sql = "update tbl_user set login_flag = '0' where id = '%s'" % id
        mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': '停用成功'})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})


# 重置密码
@app.route('/chongzhi', methods=['POST'])
def chongzhi():
    try:
        id = request.form.get('id')
        if (id == None or id == '' or id == 'undefined'):
            return jsonify({'code': '500', 'info': 'id不存在，重置失败'})
        mysql = get_a_conn()
        sql = "update tbl_user set pwd = '123456' where id = '%s'" % id
        mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': '重置成功，密码为 123456'})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})


# 用户启用
@app.route('/startUser', methods=['POST'])
def startUser():
    try:
        id = request.form.get('id')
        if (id == None or id == '' or id == 'undefined'):
            return jsonify({'code': '500', 'info': 'id不存在，启用失败'})
        mysql = get_a_conn()
        sql = "update tbl_user set login_flag = '1' where id = '%s'" % id
        mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': '启用成功'})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})


# 用户删除
@app.route('/delUser', methods=['POST'])
def delUser():
    try:
        id = request.form.get('id')
        if (id == None or id == '' or id == 'undefined'):
            return jsonify({'code': '500', 'info': 'id不存在，删除失败'})
        mysql = get_a_conn()
        sql = "delete from tbl_user where id =  '%s'" % id
        mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': '删除成功'})
    except Exception as e:
        return jsonify({'code': '500', 'info': '删除失败' + e})


# 用户列表
@app.route('/getUsers', methods=['POST'])
def getUsers():
    pageno = int(request.form.get('pageNo', 1))
    pagesize = int(request.form.get('pageSize', 10))
    name = request.form.get("name")
    phone = request.form.get("phone")
    mysql = get_a_conn()
    sql = "SELECT * FROM tbl_user where 1=1 "
    if name != None and name != '':
        sql += " and name like '%"
        sql += name
        sql += "%'"
    if phone != None and phone != '':
        sql += " and phone = '%s'" % (phone)
    sql += " ORDER BY id asc limit %s,%s" % ((pageno - 1) * pagesize, pagesize)
    result = mysql.fetchall(sql)
    sql_count = 'select count(1) num from tbl_user'
    count = mysql.fetchall(sql_count)
    total = count[0].get('num')
    return jsonify({'code': '200', 'info': result, 'pageno': pageno, 'pagesize': pagesize, 'total': total})


# 修改密码
@app.route('/changePwd', methods=['POST'])
def changePwd():
    account = request.form.get('account', None)
    oldPwd = request.form.get('oldPwd', None)
    newPwd = request.form.get('newPwd', None)
    mysql = get_a_conn()
    sql = """ SELECT * FROM tbl_user t where t.account = '%s' and t.pwd = '%s' """ % (account, oldPwd)
    result = mysql.fetchall(sql)
    if (result):
        sql = "update tbl_user set pwd = '%s' WHERE account = '%s'" % (newPwd, account)
        result1 = mysql.fetchall(sql)
        print(result1)
        return jsonify({'code': '200', 'info': '修改成功'})
    else:
        return jsonify({'code': '500', 'info': '旧密码输入不正确'})


# 注册
@app.route('/reg', methods=['POST'])
def reg():
    try:
        account = request.form.get('account', None)
        pwd = request.form.get('pwd', None)
        name = request.form.get('name', None)

        # 账号是否存在校验
        mysql = get_a_conn()
        sql_username = 'select count(1) count from tbl_user t where t.account = "%s"' % (account)
        result = mysql.fetchall(sql_username)
        if (result[0].get('count') > 0):
            return jsonify({'code': '500', 'info': '该账号已注册'})
        else:
            sql = "INSERT into tbl_user (name,account,pwd,login_flag,role) values ('%s','%s','%s','%s','%s')" % (
                name, account, pwd, '1', '2')
            mysql = get_a_conn()
            mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': '注册成功，请登录'})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})


# 登录
@app.route('/login', methods=['POST'])
def login():
    account = request.form.get('account', None)
    pwd = request.form.get('pwd', None)
    mysql = get_a_conn()
    sql = """ SELECT * FROM tbl_user t where t.account = '%s' and t.pwd = '%s' """ % (account, pwd)
    result = mysql.fetchall(sql)
    if (result):
        return {'code': '200', 'info': '%s登录成功' % account, 'session': result}
    else:
        return {'code': '500', 'info': '%s登录失败' % account}


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)  # 启动Flask项目

import  pymysql

username=''
def open():
    db=pymysql.connect(host="localhost", user="root", password="Pirelli001", database="cisco")
    return db

def exec(sql,values):
    db = open()  # 连接数据库
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    try:
        cursor.execute(sql, values)  # 执行增删改的SQL语句
        db.commit()  # 提交数据
        return 1  # 执行成功
    except:
        db.rollback()  # 发生错误时回滚
        return 0  # 执行失败
    finally:
        cursor.close()  # 关闭游标
        db.close()  # 关闭数据库连接

def query(sql,*keys):
    db=open()
    cs=db.cursor()
    cs.execute(sql,keys)
    result = cs.fetchall()
    cs.close()
    db.close()
    return result




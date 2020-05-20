from DBUtils import cursor, connection
import json

def select_executor(sql):
    cursor.execute(sql)
    details = cursor.fetchall()
    connection.commit()
    return details

def get_columns_names(table_name):
    query = "SELECT column_name, data_type FROM information_schema.columns where table_name='" + table_name + "' and table_schema='noos'"
    cursor.execute(query)
    print(query)
    details = dict(cursor.fetchall())
    return json.dumps(details)

def get_all_settings():
    query = "select * from setting"
    return select_executor(query)

def store_settings(table_name, json_string):
    query = "insert into setting (name, view, value ) values ('"+table_name+"',0,'"+json_string+"')"
    cursor.execute(query)
    connection.commit()
    return

def delete(id):
    query = "delete from setting where id ="+id
    cursor.execute(query)
    connection.commit()
    return

def get_time_graph(table_name="verification"):
    query = "SELECT count(trackingcode), MONTHNAME(date) as Month FROM "+table_name+" GROUP BY MONTH(date), MONTHNAME(date) ORDER BY MONTH(date) ASC"
    datas = select_executor(query)
    labels = []
    values = []
    for data in datas:
        labels.append(data[1])
        values.append(data[0])
    return labels, values



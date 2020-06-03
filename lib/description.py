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
    # print(query)
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

def get_time_graph(table_name, start_date, end_date):
    query = "SELECT count(trackingcode), MONTHNAME(date) as Month FROM "+table_name+" where date between '"+start_date+"' and '"+end_date+"' GROUP BY MONTH(date), MONTHNAME(date) ORDER BY MONTH(date) ASC"
    print(query)
    datas = select_executor(query)
    labels = []
    values = []
    for data in datas:
        labels.append(data[1])
        values.append(data[0])
    return labels, values

def get_count(table_name, column_name, start_date, end_date):
    query = "select count(*), "+column_name+" from " + table_name + " where date between '"+start_date+"' and '"+end_date+"' group by "+ column_name
    print(query)
    datas = select_executor(query)
    labels = []
    values = []
    for data in datas:
        labels.append(data[1])
        values.append(data[0])
    return labels, values

def update(graph, description, id, date, end_date):
    query = "update setting " \
            "set setting.value = JSON_SET(value, '$.graph', '"+graph+"'), " \
            "setting.value = JSON_SET(value, '$.description', '"+description+"')," \
            "setting.value = JSON_SET(value, '$.date', '"+date+"'), " \
            "setting.value = JSON_SET(value, '$.end_date', '"+end_date+"') " \
            "where id = "+str(id)
    # print(query)
    cursor.execute(query)
    connection.commit()
    return

def get_reg_vs_verif_count(start_date, end_date):
    vquery = "select count(*) from verification where date between '" + start_date + "' and '" + end_date + "'"
    rquery = "select count(*) from registration where date between '" + start_date + "' and '" + end_date + "'"

    labels = ["verification", "registration"]
    vdatas = select_executor(vquery)
    rdatas = select_executor(rquery)

    # print(vquery, rquery)
    values = [vdatas[0][0], rdatas[0][0]]
    return labels, values

# print(get_reg_vs_verif_count("2019-10-11"))


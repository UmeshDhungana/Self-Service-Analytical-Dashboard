from mysql import connector
connection = cursor = None


try:
    connection = connector.connect(host='localhost',
                                   database='noos',
                                   user='root',
                                   password='root')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()


except connector.Error as e:
    print("Error while connecting to MySQL", e)


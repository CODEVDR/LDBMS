import mysql.connector as sqlctr

# variables
pw = input("Enter Password : ")


def connect_server():
    connection = None
    try:
        connection = sqlctr.connect(
            host="localhost",
            user="root",
            password=pw
        )
    except:
        print("Incorrrect Password")
    return connection, pw


def connect_database(pasword):
    connection = None
    try:
        connection = sqlctr.connect(
            host="localhost",
            user="root",
            password=pasword,
            database="GNPS"
        )
    except:
        pass
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()


def read_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result


q1 = f"create database if not exists gnps;"
cnecn = connect_server()
execute_query(cnecn[0], q1)

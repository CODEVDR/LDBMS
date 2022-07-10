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
        print("Error")
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

import oracledb

def get_connection():
    connection = oracledb.connect(
        user="system",
        password="yourpassword",
        dsn="localhost/XE"
    )
    return connection

import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user  # Corrigido aqui
        self.password = password
        self.database = database
        self.conn = None
        self.connect()

    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()

    def reconnect(self):
        if self.conn is None or not self.conn.is_connected():
            self.connect()
        else:
            self.cursor = self.conn.cursor()

    def execute_query(self, query, params, commit=True):
        try:
            self.reconnect()
            self.cursor.execute(query, params)
            if commit:
                self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Erro ao executar query: {err}")
            self.conn.rollback()
            raise

    def fetch_all(self, query, params=None):
        self.reconnect()
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def close(self):
        if self.conn:
            self.conn.close()

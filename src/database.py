import sqlite3
import os

class Database():
    _istance = None

    #Singleton pattern for creation of a single istance of database and singl connection
    def __new__(cls):
        if cls._istance is None:
            cls._istance = super(Database, cls).__new__(cls)
            cls._istance.conn = None 
        return cls._istance
    

    def create_connection(self, db_bath: str): 
        if self.conn is None:
            try:
                self.conn = sqlite3.connect(db_bath) #, detect_types=True
                print("Connessione riuscita")
                return self.conn
            except Exception as e:
                print(f"Connessione non riuscita causa Errore: {e}")
        else:
            print("Connessione già esistente")
        
    
    def create_table(self):
        if self.conn is None:
            print("Nessuna connessione attiva")
        else:
            create_table_query = '''CREATE TABLE IF NOT EXISTS storic_currencies_table
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    base_currency CHAR, 
                    date CHAR,
                    corresponding_currency CHAR,
                    corresponding_currency_value FLOAT)'''
            cur = self.conn.cursor()
            try:
                cur.execute(create_table_query)
                self.conn.commit()
                print("Tabella creata correttamente")
            except Exception as e:
                print(f"Errore nella creazione della tabella: {e}")
        
    
    def insert_values(self, records):
        if self.conn is None:
            print("Nessuna connessione attiva")
        else:
            try:
                insert_query = '''INSERT INTO storic_currencies_table 
                          (base_currency, date, corresponding_currency, corresponding_currency_value) 
                          VALUES (?, ?, ?, ?)'''
                cur = self.conn.cursor()
                cur.executemany(insert_query, records) 
                self.conn.commit()
                print("Valori inseriti correttamente")
            except Exception as e:
                print(f"Errore nell'inserimento: {e}")


    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Connessione DB chiusa correttamene")
            self.conn = None
        else:
            print("Connessione già chiusa")

    
    def test_insert(self):
        cur = self.conn.cursor()
        query = "SELECT * FROM storic_currencies_table"
        cur.execute(query)
        ris = cur.fetchall()
        print(ris)
        

    def test_table_creation(self):
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM sqlite_master")
        result = cur.fetchone()
        print(result)


# if __name__ == '__main__':
#     db = Database()
#     # db2 = Database()
#     db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'db_prova.db')
#     db.create_connection(db_path)
#     db.create_table()
#     db.test_table_creation()
#     # db.insert_values('1', 'Gigi', 'Sciarra')
#     db.test_insert()
#     db.close_connection()

        
    




import sqlite3
import os

class Database():
    _istance = None

    #Singleton pattern for creation of a single istance of database and single connection
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
        
    
    def create_table(self, table: str):
        if self.conn is None:
            print("Nessuna connessione attiva")
        else:
            create_table_query = f'''CREATE TABLE IF NOT EXISTS {table}
                    (
                    base_currency TEXT, 
                    date TEXT,
                    corresponding_currency TEXT,
                    corresponding_currency_value FLOAT,
                    PRIMARY KEY (date, corresponding_currency))'''
            cur = self.conn.cursor()
            try:
                cur.execute(create_table_query)
                self.conn.commit()
                print("Tabella creata correttamente")
            except Exception as e:
                print(f"Errore nella creazione della tabella: {e}")
        
    
    def insert_values(self, records: tuple, table: str):
        if self.conn is None:
            print("Nessuna connessione attiva")
        else:
            try:
                insert_query = f'''INSERT INTO {table} 
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

    
    #Funzioni di supporto

    def get_last_date(self, table:str) -> str:
        cur = self.conn.cursor()
        query = f"SELECT MAX(date) FROM {table}"
        cur.execute(query)
        max_date_aggiornamento = cur.fetchone()[0]
        print(f"La data più recente è {max_date_aggiornamento}")
        return max_date_aggiornamento
    

    def get_current_date(self, table: str):
        cur = self.conn.cursor()
        query = "SELECT date('now');"
        cur.execute(query)
        current_date = cur.fetchone()[0]
        print(f"La data odierna è {current_date}")
        return current_date




    def test_insert(self, table: str):
        cur = self.conn.cursor()
        query = f"SELECT * FROM {table}"
        cur.execute(query)
        ris = cur.fetchall()
        print(ris)
        

    def test_table_creation(self):
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM sqlite_master")
        result = cur.fetchone()
        print(result)


    
    def count_row(self, table:str):
        cur = self.conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {table};")
        result = cur.fetchall()
        print(f"Row number: {result}")




        
    




import sqlite3
from datetime import date, datetime, timedelta
from typing import Union

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
                print("Connection to database succeeded")
                return self.conn
            except Exception as e:
                print(f"Connection to database failed. Error: {e}")
        else:
            print("Existing connection")
        
    
    def create_table(self, table: str):
        if self.conn is None:
            print("No active connection")
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
                print("Table correctly created")
            except Exception as e:
                print(f"Error in table creation: {e}")
        
    
    def insert_values(self, records: tuple, table: str):
        if self.conn is None:
            print("No active connection")
        else:
            try:
                insert_query = f'''INSERT INTO {table} 
                          (base_currency, date, corresponding_currency, corresponding_currency_value) 
                          VALUES (?, ?, ?, ?)'''
                cur = self.conn.cursor()
                cur.executemany(insert_query, records) 
                self.conn.commit()
                print("Values entered successfully")
            except Exception as e:
                print(f"Erro during insert values: {e}")


    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Database connection correctly closed")
            self.conn = None
        else:
            print("Connection already closed")

    
    #Funzioni di supporto
    def test_insert(self, table: str):
        """ Support function to test insert data on table"""
        cur = self.conn.cursor()
        query = f"SELECT * FROM {table}"
        cur.execute(query)
        ris = cur.fetchall()
        print(ris)
        
    
    def count_row(self, table:str):
        """ Support function to print the total number of record on table"""
        cur = self.conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {table};")
        result = cur.fetchall()
        print(f"Row number: {result}")


    def get_last_date(self, table:str) -> str:
        """ The function return the last updated date on db on format %Y-%m-%d."""
        cur = self.conn.cursor()
        query = f"SELECT MAX(date) FROM {table}"
        cur.execute(query)
        max_date_aggiornamento = cur.fetchone()[0]
        #print(f"La data più recente è {max_date_aggiornamento}")
        return max_date_aggiornamento
    
    
    def get_current_date(self):
        """ The function return the current date on format %Y-%m-%d"""
        cur = self.conn.cursor()
        query = "SELECT date('now');"
        cur.execute(query)
        current_date = cur.fetchone()[0]
        #print(f"La data odierna è {current_date}")
        return current_date
    
    
    # def test_table_creation(self):
    #     """ Support function to test table creation"""
    #     cur = self.conn.cursor()
    #     cur.execute("SELECT name FROM sqlite_master")
    #     result = cur.fetchone()
    #     print(result)
    

    @staticmethod
    def add_one_day_to_last_db_update(last_db_update: Union[str, datetime]) -> str:
        """ The function add one day to the last updated date in db for making the right request"""
        # Fist conversion in date for adding one day
        date_format = "%Y-%m-%d"
        if isinstance(last_db_update, date):
            date_for_request_dateformat = last_db_update + timedelta(days = 1)
        elif isinstance(last_db_update, str):
            last_db_update_dateformat = datetime.strptime(last_db_update, date_format)
            date_for_request_dateformat = last_db_update_dateformat + timedelta(days = 1)
        else:
            raise TypeError("The parameter must be a string in the format YYYY-MM-DD or a datetime object")
        # Deconversion in str format 
        date_for_request_strformat = date_for_request_dateformat.strftime(date_format)
        return date_for_request_strformat
    
    @staticmethod
    def get_delta_time(current_date:str, last_date_db: str) -> int:
        """ This function return a boolean flag for coosing the requests types (daily, storic or nothing)"""
        date_format = "%Y-%m-%d"
        #str to date conversion
        current_date_dateformat = datetime.strptime(current_date, date_format)
        last_date_dateformat = datetime.strptime(last_date_db, date_format)
        # Compute difference
        difference = current_date_dateformat - last_date_dateformat
        day_difference = difference.days
        return day_difference
    
    @staticmethod
    def prepare_storic_data_for_db(json_response:dict) -> list[tuple]:
        """
        The goal of this function is to prepare data in the record format for the DB insert,
        in case of storic requests"""
        processing_storic_data = [] 
        base_currency = json_response['base']
        for daily_date, corresponding_curr in json_response['rates'].items():
            for corresponding_currency, corresponding_value in corresponding_curr.items():
                processing_storic_data.append((base_currency, daily_date, corresponding_currency, corresponding_value))
        return processing_storic_data


    @staticmethod
    def prepare_daily_dates_for_db(json_response:dict) -> list[tuple]:
        """ The goal of this function is to prepare data in the record format for the DB insert,
        in case of daily request"""
        processing_daily_data = []
        base_currency= json_response['base']
        daily_date = json_response['date']
        for corresponding_currency, corresponding_value in json_response['rates'].items():
            processing_daily_data.append((base_currency, daily_date, corresponding_currency, corresponding_value))
        return processing_daily_data






        
    




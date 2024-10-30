from src.APIClient import APIClient
from src.database import Database
import os

def prepare_data_for_db(json_response:dict) -> list[tuple]:
    """
    The goal of this function is to prepare data in the record format for the DB insert"""
    processing_data = [] 
    base_currency = json_response['base']
    for daily_date, corresponding_curr in storic_result['rates'].items():
        for corresponding_currency, corresponding_value in corresponding_curr.items():
            processing_data.append((base_currency, daily_date, corresponding_currency, corresponding_value))
    return processing_data



if __name__ == '__main__':
    
    #base_url = "https://api.frankfurter.app/"
    client = APIClient()
    storic_result = client.get_storic_rates('2024-01-01', '2024-05-05')
    data = prepare_data_for_db(storic_result)

    #database iteraction
    db = Database()
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'currencyDB.db') #, 'db_prova.db'
    print(f"db path {db_path}")
    db.create_connection(db_path)
    db.create_table()
    db.test_table_creation()
    db.insert_values(data)
    db.test_insert()
    db.close_connection()
    

    

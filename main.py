from src.APIClient import APIClient
from src.database import Database
import os

def prepare_data_for_db(json_response:dict) -> list[tuple]:
    """
    The goal of this function is to prepare data in the record format for the DB insert"""
    processing_data = [] 
    base_currency = json_response['base']
    for daily_date, corresponding_curr in json_response['rates'].items():
        for corresponding_currency, corresponding_value in corresponding_curr.items():
            processing_data.append((base_currency, daily_date, corresponding_currency, corresponding_value))
    return processing_data



if __name__ == '__main__':
    
    #base_url = "https://api.frankfurter.app/"
    # currency_list = [
    # 'AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'GBP', 'HKD',
    # 'HUF', 'IDR', 'ILS', 'INR', 'ISK', 'JPY', 'KRW', 'MXN', 'MYR', 'NOK',
    # 'NZD', 'PHP', 'PLN', 'RON', 'SEK', 'SGD', 'THB', 'TRY', 'USD', 'ZAR']

    client = APIClient()
    storic_result = client.get_storic_rates('2002-01-01', '2024-11-04')

    data = prepare_data_for_db(storic_result)
    table_name = 'storic_currencies_table_official'

    #database iteraction
    db = Database()
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'currency.db') #, 'db_prova.db'
    # #print(f"db path {db_path}")
    db.create_connection(db_path)
    db.create_table(table_name)
    db.test_table_creation()
    db.insert_values(data, table_name)
    #db.test_insert(table_name)
    db.count_row(table_name)
    db.close_connection()

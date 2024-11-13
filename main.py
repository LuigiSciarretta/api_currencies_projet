from src.APIClient import APIClient
from src.database import Database
import os

        
if __name__ == '__main__':
    
    #base_url = "https://api.frankfurter.app/"
    
    

    client = APIClient()
    # storic_result = client.get_storic_rates('2002-01-01', '2024-11-04')
    # daily_result = client.get_daily_rates()
    #daily_data = prepare_daily_dates_for_db(daily_result)

    # storic_data = prepare_storic_data_for_db(storic_result)
    # daily_data = prepare_daily_dates_for_db(daily_result)
    table_name = 'storic_currencies_table_official'

    #database iteraction
    db = Database()
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'currency.db') 
    # #print(f"db path {db_path}")
    db.create_connection(db_path)
    last_date_aggiornamento = db.get_last_date(table_name)
    last_date_for_request = db.add_one_day_to_last_db_update(last_date_aggiornamento)
    print("Ultima data di inserimento nel db: ", last_date_aggiornamento)
    print("Data per nuova richiesta: ", last_date_for_request)
    current_date = db.get_current_date()
    print("La data corrente è: ", current_date)
    day_difference = db.get_delta_time(current_date, last_date_aggiornamento)
    request_type = client.choose_request_type(day_difference)
    print("request_type:", request_type)
    if request_type == 'storic':
        storic_response = client.get_storic_rates(last_date_for_request, current_date)
        storic_data = db.prepare_storic_data_for_db(storic_response)
        db.insert_values(storic_data, table_name) #inserisco lo storico
    elif request_type == 'daily':
        daily_response = client.get_daily_rates()
        daily_data = db.prepare_daily_dates_for_db(daily_response)
        db.insert_values(daily_data, table_name)
    
    #delta_result = client.get_storic_rates(last_date_aggiornamento, current_date)
    # delta_data = prepare_storic_data_for_db()
    # db.insert_values(delta_result, table_name) #inserisco lo storico

    
    # db.create_table(table_name)
    # #db.test_table_creation()
    # db.insert_values(storic_data, table_name) #inserisco lo storico
    # db.insert_values(daily_data, table_name)
    #db.test_insert(table_name)
    #db.count_row(table_name)
    db.close_connection()

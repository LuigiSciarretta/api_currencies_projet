from src.APIClient import APIClient
from src.database import Database
from src.data_analysis import *
import os

        
if __name__ == '__main__':
    
    #### request and db part

    client = APIClient()

    table_name = 'storic_currencies_table_official'

    #database iteraction
    db = Database()
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'currency.db') 
    db.create_connection(db_path)

    # compute delta date for the request
    last_date_aggiornamento = db.get_last_date(table_name)
    last_date_for_request = db.add_one_day_to_last_db_update(last_date_aggiornamento)
    print("Last date on db: ", last_date_aggiornamento)
    print("New request date: ", last_date_for_request)
    current_date = db.get_current_date()
    day_difference = db.get_delta_time(current_date, last_date_aggiornamento)
    request_type = client.choose_request_type(day_difference)
    #print("request_type:", request_type)
    
    # compute request and insert values depending on delta date
    if request_type == 'storic':
        storic_response = client.get_storic_rates(last_date_for_request, current_date)
        storic_data = db.prepare_storic_data_for_db(storic_response)
        db.insert_values(storic_data, table_name) #inserisco lo storico
    elif request_type == 'daily':
        daily_response = client.get_daily_rates()
        daily_data = db.prepare_daily_dates_for_db(daily_response)
        db.insert_values(daily_data, table_name)
    else:
        print("The Database is already update and it doesn't need to make an api request and insert new data")
    #clode db connection
    db.close_connection()

    #Compute daily rates EUR/USD
    client.get_daily_time_specific_rates('USD')

    
    ## Data Analysis
    currency_list = [
    'AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'GBP', 'HKD',
    'HUF', 'IDR', 'ILS', 'INR', 'ISK', 'JPY', 'KRW', 'MXN', 'MYR', 'NOK',
    'NZD', 'PHP', 'PLN', 'RON', 'SEK', 'SGD', 'THB', 'TRY', 'USD', 'ZAR']

    df = create_dataframe_from_db('storic_currencies_table_official')
    date_index_df = df.copy()
    date_index_df['date'] = pd.to_datetime(date_index_df['date'])
    date_index_df.set_index('date', inplace=True)

    all_df = create_dataframe_by_corresponding_currency(date_index_df, currency_list)
    show_temporale_rates(all_df['USD'])



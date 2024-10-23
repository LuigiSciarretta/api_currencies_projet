import requests

def get_endpoint(url: str) -> dict:
    """
    La funzione in oggetto effettua una richiesta GET all'endpoint specificato
    e restituisce il contenuto della risposta in formato JSON"""
    response = requests.get(url)
    #status_code = response.status_code
    if response.ok:
        print("Richiesta eseguita correttameente")
        try:
            response_json = response.json()
        except Exception as e:
            print(f"Errore: {e}")
    else:
        print("La richiesta non è andata a buon fine")
    return response_json


def get_field(response_json: dict) -> str:
    """"
    La funzione restiutisce il tipo di dato di ogni campo della risposta"""
    try:
        for key, value in response_json.items():
            print(f"key: {key}, value type: {type(value)}")
    except Exception as e:
        print(f"Errore: {e}")


def convert_to_all_currencies(response:dict):
    """" 
    La funzione converte la moneta locale in tutte le possibili altre monete nella data della richiesta"""
    try:
        actual_currency = response['base']
        all_currency = [k for k,v in response['rates'].items()]
        data = response['date']
        for currency in all_currency:
            print(f"Il {data} la monetea {actual_currency} vale {response['rates'][currency]} {currency}")
    except Exception as e:
        print(f"Errore: {e}")


def convert_to_specific_currencies(response:dict, currency : str):
    """La funzione converta la valuta in una specifica valuta inserita come parametro"""
    try:
        actual_currency = response['base']
        currency_value = response['rates'][currency]
        data = response['date']
        print(f"Il {data} la moneta {actual_currency} vale {currency_value} {currency}")
    except Exception as e:
        print(f"Errore: {e}")


def get_storic_rates(url:str, start_date:str, end_date:str)-> dict:
    """"La funzione si occupa di scaricare il valore delle valute nel tempo"""

    dynamic_url = f"{url}{start_date}..{end_date}"
    response = requests.get(dynamic_url)
    if response.ok:
        print("Richiesta eseguita correttameente")
        try:
            response_json = response.json()
        except Exception as e:
            print(f"Errore: {e}")
    else:
        print("La richiesta non è andata a buon fine")
    return response_json



def get_specific_date(url:str, date:str) -> dict:
    """"La funzione si occupa di scaricare il valore delle valute nel tempo"""

    dynamic_url = f"{url}{date}"
    response = requests.get(dynamic_url)
    if response.ok:
        print("Richiesta eseguita correttameente")
        try:
            response_json = response.json()
        except Exception as e:
            print(f"Errore: {e}")
    else:
        print("La richiesta non è andata a buon fine")
    return response_json




if __name__== '__main__':
    url_latest = "https://api.frankfurter.app/latest"

    base_url = "https://api.frankfurter.app/"

    # result = get_endpoint(url_latest)
    # print(result)
    # convert_to_specific_currencies(result, 'USD')
    # convert_to_all_currencies(result)
    
    # storic_result = get_storic_rates(base_url, '2024-01-01', '2024-03-01')
    # print(storic_result)

    # date_result = get_specific_date(base_url, '2022-10-10')
    # print(date_result)


    


    
    

    
    
    


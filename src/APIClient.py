import requests

class APIClient:

    #variabile di classe
    base_url = "https://api.frankfurter.app/"

    
    #definisco il costruttore che ha un attributo pari all'endpoint
    def __init__(self, url = None): 
        #se l'url viene passato, prende quello dato in input, altirmeti prende il valore dell'attributo di classe
        if url:
            self.url = str(url)
        else:
            self.url = APIClient.base_url
    


    def get_storic_rates(self, start_date: str, end_date: str) -> dict:
        """
        Metodo di istanza che dati due intervalli temporali 
        restiuisce le conversioni giornaliere della moneta locale"""
        dynamic_url = f"{self.url}{start_date}..{end_date}"
        response = requests.get(dynamic_url)
        if response.ok:
            print("Richiesta eseguita correttamente")
            try:
                response_json = response.json()
            except Exception as e:
                print(f"Errore: {e}")
        else:
            print("La richiesta non è andata a buon fine")
        return response_json
    

    def get_daily_rates(self):
        daily_url = f"{APIClient.base_url}/latest"
        daily_response = requests.get(daily_url)
        if daily_response.ok:
            print("Richieta verso endpoint giornaliero effettuata correttamente")
            try:
                daily_response_json = daily_response.json()
            except Exception as e:
                print(f"Errore: {e}")
        else:
            print("La Richiesta all'endpoint giornaliero non è andata a buon fine")
        return daily_response_json
    


    def  get_daily_time_specific_rates(self, currency: str) -> str:
        """
        Il metodo di istanza, effettua una conversione ad una particolare 
        valuta corrispondete al giorno dell'esecuzione del programma"""
        daily_url = f"{APIClient.base_url}/latest"
        response = requests.get(daily_url)
        if response.ok:
            try:
                response_json = response.json()
                actual_date = response_json['date']
                actual_currency = response_json['base']
                currency_value = response_json['rates'][currency]
                print(f"Il {actual_date} la valuta {actual_currency} vale {currency_value} {currency}")
            except Exception as e:
                print(f"Errore: {e} ")


    @staticmethod
    def choose_request_type(time_difference:int) -> str:
        tipology = ''
        if time_difference > 1: #soglia storica
            tipology = 'storic'
        elif time_difference == 1: #soglia giornaliera
            tipology = 'daily'
        return tipology
            
    

# importo l'immagine di python 
FROM python:3.11-slim

#Imposto la directory del container
WORKDIR /api_app

#Copio a directory del progetto nel container
COPY . /api_app

#Installo le dipendenza tramite il requirements
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
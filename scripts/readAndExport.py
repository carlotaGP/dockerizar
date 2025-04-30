import pymongo
import pandas as pd

try:
    # Conectar a MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')  # Ajusta la URI si es necesario
    db = client['bicis_db']  # Nombre de tu base de datos
    collection = db['bicicorunha']  # Nombre de tu colección

    # Verificar la conexión
    client.admin.command('ping')  # Verifica si la conexión es exitosa
    print("Conexión a MongoDB exitosa.")

    # Obtener los datos de MongoDB
    data = list(collection.find())  # Recupera todos los documentos de la colección

    # Extraer los datos relevantes de cada estación
    stations_data = []
    for doc in data:
        # Asegúrate de que cada documento tiene una estación
        station = doc  # Cada documento es una estación

        # Extraer los datos de la estación
        extra_data = station.get('extra', {})
        
        # Crear el diccionario con los datos de la estación
        station_data = {
            'station_id': station.get('id'),
            'station_name': station.get('name'),
            'timestamp': station.get('timestamp'),
            'free_bikes': station.get('free_bikes'),
            'empty_slots': station.get('empty_slots'),
            'extra_uid': extra_data.get('uid'),
            'extra_last_updated': extra_data.get('last_updated'),
            'extra_slots': extra_data.get('slots'),
            'extra_normal_bikes': extra_data.get('normal_bikes'),
            'extra_ebikes': extra_data.get('ebikes'),
        }
        stations_data.append(station_data)

    # Crear el DataFrame
    df = pd.DataFrame(stations_data)

    # Exportar el DataFrame a un archivo CSV y Parquet
    df.to_csv('../datasets/bicicorunha_stations.csv', index=False)
    df.to_parquet('../datasets/bicicorunha_stations.parquet', index=False)

    print("Datos exportados correctamente.")

except pymongo.errors.ServerSelectionTimeoutError as e:
    print(f"Error al conectar a MongoDB: {e}")
except Exception as e:
    print(f"Se produjo un error: {e}")

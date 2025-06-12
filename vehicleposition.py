import requests
import time
from datetime import datetime
from gtfs_realtime_pb2 import FeedMessage, FeedHeader, FeedEntity, VehiclePosition, TripDescriptor

# URL do feed
url = "http://wsbus.systemsatx.com.br/WCFMoovit.svc/ListaUltimaPosicao?HashCode=fca82037402a"

# Fazendo a requisição
response = requests.get(url)
data = response.json()  # Converte os dados da resposta para JSON

# Cria o FeedMessage
feed = FeedMessage()

# Preenche o header
feed.header.gtfs_realtime_version = "2.0"
feed.header.incrementality = FeedHeader.FULL_DATASET
feed.header.timestamp = int(time.time())  # Timestamp atual

# Adiciona entidades ao feed
for idx, vehicle in enumerate(data):
    entity = feed.entity.add()
    entity.id = str(idx + 1)  # ID único para cada entidade

    # Preenche os dados do veículo
    vehicle_position = entity.vehicle

    # Adiciona informações da viagem
    vehicle_position.trip.trip_id = f"{vehicle['Linha']}_{vehicle['Rota']}"  # trip_id único
    vehicle_position.trip.route_id = vehicle["Linha"]
    vehicle_position.trip.schedule_relationship = TripDescriptor.ADDED

    # Adiciona informações da posição do veículo
    vehicle_position.timestamp = int(
        datetime.strptime(vehicle["DataHora"], "%m-%d-%Y %H:%M:%S").timestamp()
    )
    vehicle_position.vehicle.id = vehicle["Veiculo"]
    vehicle_position.position.latitude = float(vehicle["Latitude"])
    vehicle_position.position.longitude = float(vehicle["Longitude"])

# Salvar como arquivo .pb
with open("vehicle_positions.pb", "wb") as f:
    f.write(feed.SerializeToString())

print("Arquivo GTFS-RT gerado: vehicle_positions.pb")

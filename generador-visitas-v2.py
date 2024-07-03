import pandas as pd
from geopy.distance import geodesic
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

# Cargar datos de la planilla
file_path = './estaciones lat.xlsx'  # En el caso de que necesitemos el xlsx tenemos que cambiar en line 8 el read_csv por read_xlsx y argumento file_path2 por el file_path
file_path2 = './estaciones.csv'

# Leer el archivo CSV con el delimitador adecuado
data = pd.read_csv(file_path2, delimiter=';')

print(data.head())

# De coordenadas a una lista de tuplas...
locations = list(zip(data['lat'], data['lon']))

# Coordenadas de Buenos Aires (Capital Federal)
capital_federal = (-34.6037, -58.3816)
locations.insert(0, capital_federal)

# Calcular la matriz de distancias
def compute_distance_matrix(locations):
    distance_matrix = []
    for loc1 in locations:
        row = []
        for loc2 in locations:
            row.append(geodesic(loc1, loc2).km)
        distance_matrix.append(row)
    return distance_matrix

distance_matrix = compute_distance_matrix(locations)

# Crear el modelo de TSP
def create_data_model(distance_matrix):
    data = {}
    data['distance_matrix'] = distance_matrix
    data['num_locations'] = len(distance_matrix)
    data['depot'] = 0  # Capital Federal está en el índice 0
    return data

data_model = create_data_model(distance_matrix)

# Crear el solucionador de TSP
def solve_tsp(data_model):
    manager = pywrapcp.RoutingIndexManager(len(data_model['distance_matrix']), 1, data_model['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data_model['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        index = routing.Start(0)
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        return route
    else:
        return None

optimal_route = solve_tsp(data_model)

# Excluir el punto de partida del itinerario
optimal_route = optimal_route[1:]

# Organizar las visitas en grupos de 8 estaciones por semana y 2 por día
def organize_visits(optimal_route, locations_per_week=8, locations_per_day=2):
    # Ordenar por cercanía inicial desde Capital Federal
    optimal_route = sorted(optimal_route, key=lambda i: distance_matrix[0][i])
    weeks = [optimal_route[i:i + locations_per_week] for i in range(0, len(optimal_route), locations_per_week)]
    itinerary = []
    for week in weeks:
        days = [week[i:i + locations_per_day] for i in range(0, len(week), locations_per_day)]
        itinerary.append(days)
    return itinerary

itinerary = organize_visits(optimal_route)

# Ajustar las visitas para que la persona vuelva a Buenos Aires solo al final de cada semana
def adjust_itinerary(itinerary):
    adjusted_itinerary = []
    for week in itinerary:
        adjusted_week = []
        for day in week:
            adjusted_week.append(day)
        adjusted_week.insert(0, [0])  # Añadir Capital Federal al inicio de la semana
        adjusted_week.append([0])  # Añadir Capital Federal al final de la semana
        adjusted_itinerary.append(adjusted_week)
    return adjusted_itinerary

adjusted_itinerary = adjust_itinerary(itinerary)

# Imprimir el itinerario
for week_num, week in enumerate(adjusted_itinerary):
    print(f"Semana {week_num + 1}:")
    for day_num, day in enumerate(week):
        print(f"  Día {day_num + 1}: {day}")

# Opcional: Guardar el itinerario en un archivo
output_file = 'itinerario_ajustado.xlsx'
with pd.ExcelWriter(output_file) as writer:
    for week_num, week in enumerate(adjusted_itinerary):
        week_df = pd.DataFrame(week)
        week_df.to_excel(writer, sheet_name=f'Semana {week_num + 1}', index=False)
print(f'Itinerario guardado en {output_file}')

Generador de visitas V 1.1.1

- generador de visitas 2 > Genera vuelta a punto cero ( obelisco ) cada dia despues de las 2 visitas.
- generador de visitas 3 > Genera vuelta a punto cero ( obelisco ) al finalizar la semana con las 8 visitas cumplidas
solo al final de la semana. Si es a menos. aplica la vuelta diaria.

- generador de visitas 4 > Falla en distribución de dias

- NOTA IMPORTANTE:

    El modelo se ejecuta por un algoritmo de aproximación por lo que podria NO SER EXACTO. ( se tendria que validar )
    Nos enfrentamos al problema de TSP. (Traveling Salesman Problem)
    Este exige un número Exponencial de Soluciones: A medida que aumenta el número de puntos a visitar, el número de posibles rutas aumenta factorialmente. Por ejemplo, si hay 5 ciudades, hay 5! (factorial de 5) = 120 rutas posibles. Esto se vuelve rápidamente inmanejable para números grandes. EJ 139 DESTINOS EXPONENCIADOS.

- Para ejecutar:

    - Descargar el repositorio / code / https / copy https
    - Con gitbash : git clone {pegar url previamente copiada}
    - abrir con vs code u otro
    - ejecutar pipenv install
    - ejecutar python generador-visitas-2.py   / o generador-visitas-3.py




03/07/2024 - 



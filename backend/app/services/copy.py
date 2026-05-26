from collections import defaultdict
from pulp import *

def generate_schedule(people, days, max_shifts_per_person):
    """
    Gera uma escala otimizada com base na disponibilidade das pessoas e nas necessidades diárias.
    Parâmetros:
    - people: Lista de nomes das pessoas disponíveis para a escala.
    - days: Lista de dicionários, cada um representando um dia com suas necessidades.
            Exemplo: [{"day": "12", "period": ["Morning", "Afternoon"], "people_per_period": [4, 5]}, ...]
    - availability: Dicionário onde as chaves são nomes das pessoas e os valores são dicionários
                    indicando a disponibilidade para cada dia e período.
                    Exemplo: {"Alice Silva": {"day": 10, "Period": ["Morning","Afternoon"]}, ...}
    - max_shifts_per_person: Número máximo de turnos que cada pessoa pode trabalhar.
    Retorna:
    - assignments: Dicionário onde as chaves são nomes das pessoas e os valores são listas de turnos atribuídos.
                   Exemplo: {"Alice Silva": {"day": 10, "Period": "Morning"}, ...}
    """

    volunteers = [i["id"] for i in people]

    availability = {
                p["id"]: {f"{d['day']} {period}": (p["availability"]["day"] == d["day"] and period in p["availability"]["period"])
                                        for d in days for period in d["period"]}
                for p in people
        }

        shift = [d["day"] for d in days]
        people_per_shift = [d["people_per_period"] for d in days]

        consecutive_shifts = []  
        for d in days:
                if d["period"] and len(d["period"]) > 1:
                periods = list(d["period"])
                for i in range(len(periods) - 1):
                        consecutive_shifts.append((f"{d['day']} {periods[i]}", f"{d['day']} {periods[i+1]}"))
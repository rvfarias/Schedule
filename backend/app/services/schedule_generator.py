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
    # Preparar os dados de entrada para o modelo de otimização
    volunteers = [p["name", "last_name"] for p in people]
    availability = {
        p["name", "last_name"]: {f"{d['day']} {period}": (p["availability"]["day"] == d["day"] and period in p["availability"]["period"])
                                for d in days for period in d["period"]}
        for p in people
    }
    
    shift = [d["day"] for d in days]
    people_per_shift = [d["people_per_period"] for d in days]
    
    consecutive_shifts = []  # Lista de tuplas representando turnos consecutivos (ex: [("12 Morning", "12 Afternoon"), ...])
    for d in days:
        periods = list(d["period"])
        for i in range(len(periods) - 1):
            consecutive_shifts.append((f"{d['day']} {periods[i]}", f"{d['day']} {periods[i+1]}"))
    

    # 1. Cria o problema de otimização (Problema de Maximização)
    model = LpProblem("Schedule_Problem", LpMaximize)

    # 2. Variáveis de Decisão: X[v][t] = 1 se o Voluntário 'v' for escalado no Turno 't', 0 caso contrário.
    X = LpVariable.dicts("Assign", (volunteers, shift), 0, 1, LpBinary)

    # --- 3. Função Objetivo ---
    model += lpSum(X[v][s] for v in volunteers for s in shift), "Total_Assignments"

    # --- 4. Restrições do Problema ---
    # Restrição 1: Cobertura Mínima. Garantir que cada turno tenha o número necessário de pessoas.
    for s in shift:
        model += lpSum(X[v][s] for v in volunteers) >= people_per_shift[s], f"People_per_shift_{s}"

    # Restrição 2: Disponibilidade. Um voluntário só pode ser escalado se estiver disponível (A[i][t] = 1).
    # O modelo só pode atribuir se o dado de entrada for 1. Se for 0, o produto é 0.
    for v in volunteers:
        for s in shift:
            if availability[v][s] == 0:
                model += X[v][s] == 0, f"Availability_{v}_{s}"
    
    
    # Restrição 3: Limite de Turnos por Voluntário (Restrição de Justiça/Equidade)
    # for p in people:
    #     model =+ lpSum(X[p][t] for s in shift) <= max_shifts_per_person, f"Max_Turnos_{p}"

    # Restrição 4: Restrição de Turnos Consecutivos (Exemplo: Domingo Manhã e Noite)
    # Você precisaria de um parser que identifica os turnos do mesmo dia (ex: 'Dom 05/05 Manhã' e 'Dom 05/05 Noite')
    # Vamos simular um par de turnos consecutivos
    for (s1, s2) in consecutive_shifts:
        for v in volunteers:
            model += X[v][s1] + X[v][s2] <= 1, f"Consecutive_Shifts_{v}_{s1}_{s2}"
    
    # 5. Resolve o problema de otimização
    model.solve()

    # 6. Extrai as atribuições do modelo
    assignments = defaultdict(list)
    for v in volunteers:
        for s in shift:
            if X[v][s].varValue == 1:
                day, period = s.split()
                assignments[v].append({"day": int(day), "period": period})
    
    return assignments
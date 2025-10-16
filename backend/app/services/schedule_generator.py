from collections import defaultdict
from pulp import LpProblem, LpMaximize, LpVariable, LpBinary, lpSum, PULP_CBC_CMD

def generate_schedule(people, days, max_shifts_per_person):
    """
    Gera uma escala otimizada.
    Entrada:
      - people: lista de dicts com ao menos "id" e "availability"
          ex: {"id": 1, "availability": {"day": 5, "period": ["manhã", "tarde"]}}
      - days: lista de dicts com "day", "period" (lista) e "people_per_period" (lista de ints)
          ex: {"day": 5, "period": ["manhã","tarde"], "people_per_period": [2,3]}
      - max_shifts_per_person: int
    Retorna:
      - dict {person_id: [ {"day": int, "period": str}, ... ], ...}
    """

    # --- Preparação dos dados ---
    # lista de ids/voluntários
    volunteers = [p["id"] for p in people]

    # constroi lista de turnos no formato "dia periodo" e um mapeamento people_per_shift por turno
    shifts = []
    people_per_shift = {}
    for d in days:
        periods = list(d.get("period", []))
        counts = d.get("people_per_period", [])
        for i, period in enumerate(periods):
            shift_key = f"{d['day']} {period}"
            shifts.append(shift_key)
            people_per_shift[shift_key] = counts[i] if i < len(counts) else 1

    # disponibilidade por voluntário por turno (True/False)
    availability = {}
    for p in people:
        p_av = p.get("availability", {})
        # espera p_av ter "day" e "period" (lista)
        availability[p["id"]] = {}
        for d in days:
            for period in d.get("period", []):
                key = f"{d['day']} {period}"
                is_available = (p_av.get("day") == d["day"]) and (period in p_av.get("period", []))
                availability[p["id"]][key] = is_available

    # pares de turnos consecutivos no mesmo dia (adjacentes na lista periods)
    consecutive_shifts = []
    for d in days:
        periods = list(d.get("period", []))
        for i in range(len(periods) - 1):
            consecutive_shifts.append((f"{d['day']} {periods[i]}", f"{d['day']} {periods[i+1]}"))

    # --- Modelo de otimização ---
    model = LpProblem("Schedule_Problem", LpMaximize)

    # variáveis binárias Assign[volunteer][shift]
    X = LpVariable.dicts("Assign", (volunteers, shifts), 0, 1, LpBinary)

    # objetivo: maximizar total de atribuições (pode ser alterado para balanceamento)
    model += lpSum(X[v][s] for v in volunteers for s in shifts), "Total_Assignments"

    # restrição: cobertura mínima por turno
    for s in shifts:
        required = people_per_shift.get(s, 0)
        model += lpSum(X[v][s] for v in volunteers) >= required, f"People_per_shift_{s}"

    # restrição: disponibilidade (se não disponível, X == 0)
    for v in volunteers:
        for s in shifts:
            if not availability.get(v, {}).get(s, False):
                model += X[v][s] == 0, f"Availability_{v}_{s}"

    # restrição: máximo de turnos por voluntário
    for v in volunteers:
        model += lpSum(X[v][s] for s in shifts) <= max_shifts_per_person, f"Max_Shifts_{v}"

    # restrição: não permitir turnos consecutivos definidos
    for (s1, s2) in consecutive_shifts:
        # só adiciona a restrição se ambos os turnos existirem na lista de shifts
        if s1 in shifts and s2 in shifts:
            for v in volunteers:
                model += X[v][s1] + X[v][s2] <= 1, f"Consecutive_Shifts_{v}_{s1}_{s2}"

    # resolve o modelo usando CBC (silencioso)
    model.solve(PULP_CBC_CMD(msg=False))

    # extrai as atribuições com segurança (get varValue)
    assignments = defaultdict(list)
    for v in volunteers:
        for s in shifts:
            val = getattr(X[v][s], "varValue", 0)
            if val == 1:
                day_str, period = s.split(maxsplit=1)
                try:
                    day_int = int(day_str)
                except ValueError:
                    day_int = day_str
                assignments[v].append({"day": day_int, "period": period})

    return dict(assignments)
from app.schemas import schedule_schema
from pulp import LpProblem, LpMaximize, LpVariable, LpBinary, lpSum, PULP_CBC_CMD

def generate_schedule(schedule_data: schedule_schema.ScheduleBase):
    
    people = schedule_data.people
    days = schedule_data.days
    max_shifts_per_person = schedule_data.max_period_per_person

    # --- Preparação dos dados ---
    # lista de nomes de voluntários como chave única para variáveis
    volunteers = [f"{p.name} {p.last_name}" for p in people]
    # shifts: lista de turnos únicos (ex: "Segunda Manhã")
    shifts = []
    # mapa turno -> número de pessoas necessárias nesse turno
    people_per_shift = {}
    for d in days:
        # d.period é esperado ser lista/iterável de períodos naquele dia
        periods = list(d.period or [])
        # d.people_per_period é lista com contagens por período (opcional)
        counts = d.people_per_period or []
        for i, period in enumerate(periods):
            shift_key = f"{d.day} {period}"
            if shift_key not in shifts:  # garante que não duplica
                shifts.append(shift_key)
                # se counts não tiver índice i, assume 1 como padrão
                people_per_shift[shift_key] = counts[i] if i < len(counts) else 1

    # --- Disponibilidade por voluntário por turno ---
    # availability será dict: { "Nome Sobrenome": { "Dia Período": True/False, ... }, ... }
    availability = {}
    for p in people:
        p_av = getattr(p, "availability", {})  # pode ser lista ou dict/None
        availability[f"{p.name} {p.last_name}"] = {}
        for d in days:
            for period in (d.period or []):
                key = f"{d.day} {period}"
                # se availability for lista de objetos (cada um com day e period)
                if isinstance(p_av, list) and len(p_av) > 0:
                    # está disponível se algum elemento da lista tiver mesmo dia e conter o período
                    is_available = any(
                        (a.day == d.day and period in a.period)
                        for a in p_av
                    )
                else:
                    # se availability for dict único: compara campos day e period
                    is_available = (
                        p_av.get("day") == d.day and period in p_av.get("period", [])
                        if isinstance(p_av, dict)
                        else False
                    )
                availability[f"{p.name} {p.last_name}"][key] = is_available

    # --- Pares de turnos consecutivos no mesmo dia ---
    # Cria lista de pares (turno_i, turno_{i+1}) para cada dia para evitar alocação consecutiva
    consecutive_shifts = []
    for d in days:
        periods = list(d.period or [])
        for i in range(len(periods) - 1):
            consecutive_shifts.append((f"{d.day} {periods[i]}", f"{d.day} {periods[i+1]}"))

    # --- Modelo de otimização (PULP) ---
    # maximizar número total de atribuições (pode ser trocado para outro objetivo)
    model = LpProblem("Schedule_Problem", LpMaximize)
    # X[v][s] = 1 se voluntário v for atribuído ao turno s
    X = LpVariable.dicts("Assign", (volunteers, shifts), 0, 1, LpBinary)

    # Objetivo: somar todas as atribuições
    model += lpSum(X[v][s] for v in volunteers for s in shifts), "Total_Assignments"

    # Restrição: por turno, número de voluntários <= required (people_per_shift)
    for s in shifts:
        required = people_per_shift.get(s, 0)
        model += lpSum(X[v][s] for v in volunteers) <= required, f"People_per_shift_{s}"

    # Restrição: respeitar disponibilidade (se indisponível, variável = 0)
    for v in volunteers:
        for s in shifts:
            if not availability.get(v, {}).get(s, False):
                model += X[v][s] == 0, f"Availability_{v}_{s}"

    # Restrição: cada pessoa tem limite máximo de turnos no período
    for i, v in enumerate(volunteers):
        model += lpSum(X[v][s] for s in shifts) <= max_shifts_per_person, f"Max_Shifts_{i}_{v}"


    # Restrição: não alocar a mesma pessoa em turnos consecutivos do mesmo dia
    for ci, (s1, s2) in enumerate(consecutive_shifts):
        if s1 in shifts and s2 in shifts:
            for vi, v in enumerate(volunteers):
                model += X[v][s1] + X[v][s2] <= 1, f"Consecutive_Shifts_{ci}_{vi}_{v}_{s1}_{s2}"

    # Resolve o modelo com solver CBC (sem saída de log)
    model.solve(PULP_CBC_CMD(msg=False))

    # --- Pós-processamento: normaliza dias e monta resultado legível ---
    def _normalize_day(day_val):
        # tenta converter string numérica para int (ex: "1" -> 1), senão retorna original
        try:
            return int(day_val)
        except Exception:
            return day_val

    # Estrutura final: assignments[day][period] = [lista de "Nome Sobrenome"]
    assignments = {}
    for d in days:
        day_key = _normalize_day(d.day)
        assignments.setdefault(day_key, {})
        for period in (d.period or []):
            assignments[day_key].setdefault(period, [])

    # Percorre as variáveis X e coleta as que foram fixadas em 1 pelo solver
    for v in volunteers:
        for s in shifts:
            val = getattr(X[v][s], "varValue", 0)
            if val and val >= 0.5:
                # separa o shift "Dia Período" em componentes
                day_str, period = s.split(maxsplit=1)
                day_key = _normalize_day(day_str)
                assignments.setdefault(day_key, {})
                assignments[day_key].setdefault(period, [])
                assignments[day_key][period].append(v)

    return assignments

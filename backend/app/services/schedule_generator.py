from app.schemas import schedule_schema
from pulp import LpProblem, LpMaximize, LpVariable, LpBinary, lpSum, PULP_CBC_CMD

def generate_schedule(schedule_data: schedule_schema.ScheduleBase):
    
    people = schedule_data.people
    days = schedule_data.days
    max_shifts_per_person = schedule_data.max_period_per_person

    # --- Preparação dos dados ---
    volunteers = [f"{p.name} {p.last_name}" for p in people]

    shifts = []
    people_per_shift = {}
    for d in days:
        periods = list(d.period or [])
        counts = d.people_per_period or []
        for i, period in enumerate(periods):
            shift_key = f"{d.day} {period}"
            if shift_key not in shifts:  # garante que não duplica
                shifts.append(shift_key)
                people_per_shift[shift_key] = counts[i] if i < len(counts) else 1

    # disponibilidade por voluntário por turno (True/False)
    availability = {}
    for p in people:
        p_av = getattr(p, "availability", {})
        availability[f"{p.name} {p.last_name}"] = {}
        for d in days:
            for period in (d.period or []):
                key = f"{d.day} {period}"
                # se availability for lista, ajusta aqui
                if isinstance(p_av, list) and len(p_av) > 0:
                    is_available = any(
                        (a.day == d.day and period in a.period)
                        for a in p_av
                    )
                else:
                    is_available = (
                        p_av.get("day") == d.day and period in p_av.get("period", [])
                        if isinstance(p_av, dict)
                        else False
                    )
                availability[f"{p.name} {p.last_name}"][key] = is_available

    # pares de turnos consecutivos no mesmo dia
    consecutive_shifts = []
    for d in days:
        periods = list(d.period or [])
        for i in range(len(periods) - 1):
            consecutive_shifts.append((f"{d.day} {periods[i]}", f"{d.day} {periods[i+1]}"))

    # --- Modelo de otimização ---
    model = LpProblem("Schedule_Problem", LpMaximize)
    X = LpVariable.dicts("Assign", (volunteers, shifts), 0, 1, LpBinary)

    model += lpSum(X[v][s] for v in volunteers for s in shifts), "Total_Assignments"

    for s in shifts:
        required = people_per_shift.get(s, 0)
        model += lpSum(X[v][s] for v in volunteers) >= required, f"People_per_shift_{s}"

    for v in volunteers:
        for s in shifts:
            if not availability.get(v, {}).get(s, False):
                model += X[v][s] == 0, f"Availability_{v}_{s}"

    for i, v in enumerate(volunteers):
        model += lpSum(X[v][s] for s in shifts) <= max_shifts_per_person, f"Max_Shifts_{i}_{v}"


    for ci, (s1, s2) in enumerate(consecutive_shifts):
        if s1 in shifts and s2 in shifts:
            for vi, v in enumerate(volunteers):
                model += X[v][s1] + X[v][s2] <= 1, f"Consecutive_Shifts_{ci}_{vi}_{v}_{s1}_{s2}"

    model.solve(PULP_CBC_CMD(msg=False))

    def _normalize_day(day_val):
        try:
            return int(day_val)
        except Exception:
            return day_val

    assignments = {}
    for d in days:
        day_key = _normalize_day(d.day)
        assignments.setdefault(day_key, {})
        for period in (d.period or []):
            assignments[day_key].setdefault(period, [])

    for v in volunteers:
        for s in shifts:
            val = getattr(X[v][s], "varValue", 0)
            if val and val >= 0.5:
                day_str, period = s.split(maxsplit=1)
                day_key = _normalize_day(day_str)
                assignments.setdefault(day_key, {})
                assignments[day_key].setdefault(period, [])
                assignments[day_key][period].append(v)

    return assignments

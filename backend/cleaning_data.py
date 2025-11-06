import pandas as pd
import re
from datetime import datetime
from pathlib import Path
# 1) Läs som råtext, inte som väldefinierad CSV (filen är oregelbunden)
path = Path(__file__).parents[1] / "data" / "StrengthLog-2025-09-241.csv"
with open(path, "r", encoding="utf-8") as f:
    lines = [ln.strip() for ln in f.readlines()]

# 2) Ta bort tomma rader och nonsens
lines = [ln for ln in lines if ln and "Instance of 'Loc'" not in ln]

# 3) Hjälpfunktioner
def is_header_or_workouts_line(ln: str) -> bool:
    low = ln.lower()
    return low.startswith("name,language") or low == "workouts"

def looks_like_workout_row(ln: str) -> bool:
    # Format: WorkoutName,YYYY-MM-DD,bodyweight,shape,sleep,calories,stress
    # Försök upptäcka datum i fält 2
    parts = split_csv_loose(ln)
    if len(parts) < 2:
        return False
    try:
        datetime.strptime(parts[1], "%Y-%m-%d")
        return True
    except Exception:
        return False

def is_exercise_set_row(ln: str) -> bool:
    # "Exercise, Bench Press",Set,1,... eller Exercise, Bench Press,Set,1,...
    low = ln.lower()
    return low.startswith('"exercise,') or low.startswith('exercise,')

def split_csv_loose(ln: str):
    # Splitta med hänsyn till eventuella citattecken runt första fältet
    # Enkel robust delning: dela på kommatecken, men ta bort inledande/avslutande "
    parts = [p.strip().strip('"') for p in ln.split(",")]
    return parts

def hhmmss_to_seconds(s: str):
    try:
        h, m, sec = s.split(":")
        return int(h) * 3600 + int(m) * 60 + int(sec)
    except:
        return None

# 4) Iterera och bygg två listor
workouts = []
sets = []

current_workout = None

for ln in lines:
    if is_header_or_workouts_line(ln):
        continue

    if looks_like_workout_row(ln):
        p = split_csv_loose(ln)
        # Hantera ev. kommatecken i workout_name (t.ex. "Friday Evening: Back, Shoulders...")
        # Vi antar att datum ligger i första fältet som verkligen matchar YYYY-MM-DD.
        # Sök index för datum:
        date_idx = None
        for i, val in enumerate(p):
            try:
                datetime.strptime(val, "%Y-%m-%d")
                date_idx = i
                break
            except:
                continue
        if date_idx is None:
            continue

        workout_name = ",".join(p[:date_idx])  # slå ihop allt före datum tillbaka till namn
        workout_date = p[date_idx]
        rest = p[date_idx+1:]

        # rest borde vara: body_weight, shape, sleep, calories, stress (5 fält)
        def get_safe(lst, idx, default=None):
            return lst[idx] if idx < len(lst) else default

        body_weight = pd.to_numeric(get_safe(rest, 0), errors="coerce")
        shape = pd.to_numeric(get_safe(rest, 1), errors="coerce")
        sleep = pd.to_numeric(get_safe(rest, 2), errors="coerce")
        calories = pd.to_numeric(get_safe(rest, 3), errors="coerce")
        stress = pd.to_numeric(get_safe(rest, 4), errors="coerce")

        current_workout = {
            "workout_name": workout_name,
            "workout_date": workout_date,
            "body_weight": body_weight,
            "shape": shape,
            "sleep": sleep,
            "calories": calories,
            "stress": stress,
        }
        workouts.append(current_workout)
        continue

    if is_exercise_set_row(ln) and current_workout is not None:
        p = split_csv_loose(ln)

        # Första två fälten bör vara ["Exercise", "<name>"] eller ["Exercise <name>"] beroende på export
        # I materialet är mönstret typ: "Exercise, Bench Press", Set, 1, reps, 10, weight, 50
        # Efter split blir p ungefär: ["Exercise", "Bench Press", "Set", "1", "reps", "10", "weight", "50"]
        # Men i filen är första fältet ofta '"Exercise' och andra 'Bench Press"' efter strip('"') blev det rent.
        if p[0].lower() == "exercise":
            exercise_name = p[1]
            idx = 2
        else:
            # I vissa rader kan det första fältet vara "Exercise Bench Press" sammanslaget
            # fallback: ta bort prefix "Exercise" och kommatecken
            first = p[0]
            if first.lower().startswith("exercise"):
                exercise_name = first.split(" ", 1)[-1].strip()
                idx = 1
            else:
                exercise_name = first
                idx = 1

        # Hitta setnummer efter keyword 'Set'
        set_no = None
        for i in range(idx, len(p)):
            if p[i].lower() == "set" and i+1 < len(p):
                set_no = pd.to_numeric(p[i+1], errors="coerce")
                idx = i + 2
                break

        # Nyckel-värde par efter 'Set, <n>'
        kv = {}
        i = idx
        while i < len(p):
            key = p[i].lower()
            val = p[i+1] if i+1 < len(p) else None
            kv[key] = val
            i += 2

        reps = pd.to_numeric(kv.get("reps"), errors="coerce")
        weight = pd.to_numeric(kv.get("weight"), errors="coerce")
        bodyweight = pd.to_numeric(kv.get("bodyweight"), errors="coerce")
        extra_weight = pd.to_numeric(kv.get("extraweight"), errors="coerce")
        time_raw = kv.get("time")
        time_sec = hhmmss_to_seconds(time_raw) if time_raw else None

        sets.append({
            "workout_name": current_workout["workout_name"],
            "workout_date": current_workout["workout_date"],
            "exercise_name": exercise_name,
            "set_number": set_no,
            "reps": reps,
            "weight_kg": weight,
            "bodyweight_kg": bodyweight,
            "extra_weight_kg": extra_weight,
            "time_sec": time_sec,
        })

# 5) DataFrames
df_workouts = pd.DataFrame(workouts).drop_duplicates()
df_sets = pd.DataFrame(sets)

# 6) Generera ett stabilt workout_id för att kunna länka (hash på namn+datum)
df_workouts["workout_id"] = (
    df_workouts["workout_name"].astype(str) + "|" + df_workouts["workout_date"].astype(str)
).apply(lambda s: abs(hash(s)) % (10**12))

df_sets = df_sets.merge(
    df_workouts[["workout_name","workout_date","workout_id"]],
    on=["workout_name","workout_date"],
    how="left"
)

# 7) Sortera och kolumnordning
df_workouts = df_workouts[[
    "workout_id","workout_name","workout_date","body_weight","shape","sleep","calories","stress"
]].sort_values(["workout_date","workout_name"])

df_sets = df_sets[[
    "workout_id","workout_name","workout_date","exercise_name","set_number",
    "reps","weight_kg","bodyweight_kg","extra_weight_kg","time_sec"
]].sort_values(["workout_date","workout_name","exercise_name","set_number"])

print(df_workouts.head(), "\n")
print(df_sets.head(), "\n")

# 8) Spara till CSV/Parquet för staging-inload via dlt
df_workouts.to_csv("stg_strength_workouts.csv", index=False)
df_sets.to_csv("stg_strength_sets.csv", index=False)
# Alternativt Parquet (rekommenderas ofta):
df_workouts.to_parquet("stg_strength_workouts.parquet", index=False)
df_sets.to_parquet("stg_strength_sets.parquet", index=False)
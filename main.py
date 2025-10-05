import random
import math
import time
import json
from datetime import timedelta

#  Palīgfunkcija laiku pārvēšanām 
def to_minutes(t_str):
    h, m = map(int, t_str.split(":"))
    return h * 60 + m

def to_time_str(minutes):
    return str(timedelta(minutes=minutes))[:-3]

#  Izmantotās domēna definīcijas 
class Airplane:
    def __init__(self, arrival_str, size, id):
        self.arrival = to_minutes(arrival_str)
        self.size = size
        self.id = id

class Runway:
    def __init__(self, service_time, allowed_sizes, id):
        self.service_time = service_time
        self.allowed_sizes = allowed_sizes
        self.id = id

#  Novērtēšanas(Cost) funkcija 
def evaluate(solution, airplanes, runways):
    total_wait = 0
    # Sagalbā katra skrejceļa nākamo brīvo laiku minūtēs
    runway_times = {r.id: 0 for r in runways}
    for plane_id, runway_id in solution.items():
        # Atrod lidmašīnu un skrejceļu pēc to id
        plane = airplanes[plane_id]
        runway = next(r for r in runways if r.id == runway_id)
        # Aprēķina, kad lidmašīna var sākt nolaišanos un pieskaita kopējam gaidīšanas laikam
        start_time = max(plane.arrival, runway_times[runway.id])
        wait_time = start_time - plane.arrival
        total_wait += wait_time
        # Ja gaidīšana ir lielāka par 20 minūtēm, pievieno papildus izmakasas. 50 par katrām 20 minūtēm
        if wait_time > 20:
            total_wait+=wait_time % 20 * 50
        # Atjauno skrejceļa pieejamības laiku
        runway_times[runway.id] = start_time + runway.service_time
    return total_wait

#  Palīgfunkcija detalizētāka grafika izprintēšanai
def simulated_schedule(solution, airplanes, runways):
    runway_times = {r.id: 0 for r in runways}
    schedule = {}
    for plane_id, runway_id in solution.items():
        # Atrod lidmašīnu un skrejceļu pēc to id
        plane = airplanes[plane_id]
        runway = next(r for r in runways if r.id == runway_id)
        # Aprēķina lidmašīnas nolaišanās un beigu laiku
        start_time = max(plane.arrival, runway_times[runway.id])
        end_time = start_time + runway.service_time
        # Pievieno grafikam
        schedule[plane_id] = (runway_id, start_time, end_time)
        # Atjauno skrejceļa pieejamības laiku
        runway_times[runway.id] = end_time
    return schedule

#  Sākotnējā nejaušā grafika izveide
def random_solution(airplanes, runways):
    solution = {}
    # Katrai lidmašinai piešķir vienu skrejceliņu, kas atbilst tās lielumam, pēc nejaušības principa
    for plane in airplanes:
        possible = [r.id for r in runways if plane.size in r.allowed_sizes]
        solution[plane.id] = random.choice(possible)
    return solution

#  Gājiens 
def random_move(solution, airplanes, runways):
    new_solution = solution.copy()
    plane = random.choice(airplanes) # izvēlas vienu nejaušu lidmašīnu
    possible = [r.id for r in runways if plane.size in r.allowed_sizes and r.id != solution[plane.id]] # Atrod iespējamos skrejceliņus uz kuriem var pārcelt izvēlēto lidmašīnu
    if possible:
        new_solution[plane.id] = random.choice(possible)
    return new_solution


#  Simulated Annealing 
def simulated_annealing(airplanes, runways, T=1000, alpha=0.99):
    current = random_solution(airplanes, runways)
    current_score = evaluate(current, airplanes, runways)
    best = current
    best_score = current_score

    while T > 0.1:
        candidate = random_move(current, airplanes, runways)
        candidate_score = evaluate(candidate, airplanes, runways)

        delta = current_score - candidate_score

        if delta > 0 or random.random() < math.exp(delta / T):
            current = candidate
            current_score = candidate_score

            if current_score < best_score:
                best = current
                best_score = current_score
        T *= alpha

    return best, best_score


if __name__ == "__main__":
    # Ielasa testa gadījumus no JSON
    with open("test_cases.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for case_idx, case in enumerate(data["cases"], start=1):
        print(f"\n=== Testa gadījums {case_idx} ===")

        # Izveido Airplane un Runway objektus
        airplanes = [Airplane(a["arrival"], a["size"], a["id"]) for a in case["airplanes"]]
        runways = [Runway(r["service_time"], r["allowed_sizes"], r["id"]) for r in case["runways"]]

        # Palaiž algrotimu un nosaka izpildes ilgumu
        start = time.time()
        best_solution, best_score = simulated_annealing(airplanes, runways)
        end = time.time()

        # Izdrukā labāko atrasto risinājumu
        print("Labākais atrastais risinājums:")
        schedule = simulated_schedule(best_solution, airplanes, runways)
        for plane_id, (runway_id, start_time, end_time) in schedule.items():
            arrival_str = to_time_str(airplanes[plane_id].arrival)
            print(f"  Lidmašīna {plane_id} (ierašanās {arrival_str})"
                  f" -> Skrejceļš {runway_id}, apkalpošana {to_time_str(start_time)}–{to_time_str(end_time)}")

        print("Kopējās izmaksas:", best_score)
        print("Testa izpildes laiks (sek):", round(end - start, 4))

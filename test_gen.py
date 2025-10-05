import json
import random

def generate_airplanes(n):
    sizes = ["small", "medium", "large"]
    airplanes = []
    start_hour = random.randint(7, 11)
    current_time = start_hour * 60  # sākuma laiks minūtēs

    for i in range(n):
        # Lidmašīnas pienāk ar nejaušiem intervāliem no 0–10 min
        arrival = current_time + random.randint(0, 10)
        arrival_str = f"{arrival // 60:02d}:{arrival % 60:02d}"
        size = random.choice(sizes)
        airplanes.append({"id": i, "arrival": arrival_str, "size": size})
        current_time = arrival 

    return airplanes

def generate_runways(m):
    sizes = ["small", "medium", "large"]
    runways = []

    # vispirms nodrošinām, ka katrs izmērs tiek iekļauts vismaz vienā skrejceļā
    for i, size in enumerate(sizes):
        service_time = random.randint(5, 12)
        runways.append({
            "id": i,
            "service_time": service_time,
            "allowed_sizes": [size] if m <= len(sizes) else random.sample(sizes, random.randint(1, 3))
        })

    # ja skrejceļu skaits > izmēru skaits, ģenerē pārējos nejauši
    for i in range(len(sizes), m):
        service_time = random.randint(5, 12)
        allowed_count = random.randint(1, 3)
        allowed_sizes = random.sample(sizes, allowed_count)
        runways.append({
            "id": i,
            "service_time": service_time,
            "allowed_sizes": allowed_sizes
        })

    return runways

def generate_test_cases(num_cases=5, airplanes_per_case=100, runways_per_case=5):
    cases = []
    for _ in range(num_cases):
        airplanes = generate_airplanes(airplanes_per_case)
        runways = generate_runways(runways_per_case)
        cases.append({"airplanes": airplanes, "runways": runways})
    return {"cases": cases}

if __name__ == "__main__":
    # Ģenerē 5 testus ar 100 lidmašīnām un 5 skrejceļiem katrā
    test_data = generate_test_cases(num_cases=5, airplanes_per_case=100, runways_per_case=5)
    with open("test_cases.json", "w", encoding="utf-8") as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)

    print("Izveidots test_cases.json!")

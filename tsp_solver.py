import math
import time

class MobileEcoHybridTSP:
    def __init__(self, cities_dict):
        self.cities = cities_dict
        x_coords = [c[0] for c in self.cities.values()]
        y_coords = [c[1] for c in self.cities.values()]
        self.center = (sum(x_coords)/len(x_coords), sum(y_coords)/len(y_coords))

    def calculate_eco_cost(self, c1, c2):
        base_dist = math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)
        return base_dist * 1.15 # Eco & Traffic multiplier

    def solve(self):
        start_time = time.time()
        
        # Fast Polar Sorting
        polar_sorted = []
        for name, coords in self.cities.items():
            angle = math.atan2(coords[1] - self.center[1], coords[0] - self.center[0])
            polar_sorted.append((name, angle))
        polar_sorted.sort(key=lambda x: x[1])
        route = [item[0] for item in polar_sorted]
        
        # Cost calculation
        def get_total_cost(r):
            total = 0.0
            for i in range(len(r)):
                c1 = self.cities[r[i]]
                c2 = self.cities[r[(i + 1) % len(r)]]
                total += self.calculate_eco_cost(c1, c2)
            return total
            
        best_cost = get_total_cost(route)
        
        # 2-Opt Optimization
        improved = True
        while improved:
            improved = False
            for i in range(len(route) - 1):
                for j in range(i + 2, len(route) + (1 if i > 0 else 0)):
                    if j - i == 1:
                        continue
                    new_route = route.copy()
                    new_route[i+1:j] = reversed(new_route[i+1:j])
                    new_cost = get_total_cost(new_route)
                    if new_cost < best_cost:
                        route = new_route
                        best_cost = new_cost
                        improved = True
                        break
                if improved:
                    break
                    
        end_time = time.time()
        return route, best_cost, (end_time - start_time)

# Sample Egyptian Cities Data
egypt_cities = {
    "Mansoura": (31.0364, 31.3807),
    "Cairo": (30.0444, 31.2357),
    "Alexandria": (31.2001, 29.9187),
    "Tanta": (30.7885, 31.0019),
    "Damanhur": (31.0409, 30.4682),
    "Zagazig": (30.5877, 31.5020),
    "PortSaid": (31.2653, 32.3019),
    "Suez": (29.9668, 32.5498),
    "Ismailia": (30.5965, 32.2715),
    "Banha": (30.4661, 31.1837)
}

optimizer = MobileEcoHybridTSP(egypt_cities)
print("=== Eco-Dynamic TSP Mobile Optimization ===")
route, cost, exec_time = optimizer.solve()

print(f"Nodes Processed: {len(route)}")
print(f"Total Eco-Cost: {cost:.4f}")
print(f"Execution Time: {exec_time:.5f} sec")
print("Optimal Route:")
print(" -> ".join(route))

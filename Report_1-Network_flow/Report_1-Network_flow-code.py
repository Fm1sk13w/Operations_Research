import pulp

# 1. Initialize the maximization model
model = pulp.LpProblem("Maximum_Flow", pulp.LpMaximize)

# 2. Define the edges and their maximum capacities
capacities = {
    ('S', 'A'): 400, ('S', 'B'): 400,
    ('A', 'B'): 200, ('A', 'C'): 200,
    ('B', 'C'): 200, ('A', 'T'): 100,
    ('B', 'T'): 200, ('C', 'T'): 400
}

# 3. Create decision variables for flow (x_ij >= 0)
x = pulp.LpVariable.dicts("flow", capacities.keys(), lowBound=0)

# 4. Apply capacity constraints (x_ij <= capacity)
for edge, cap in capacities.items():
    x[edge].upBound = cap

# 5. Objective Function: Maximize flow leaving the source S
model += x[('S', 'A')] + x[('S', 'B')], "Total_Throughput"

# 6. Flow Conservation Constraints (Inflow == Outflow)
model += x[('S', 'A')] == x[('A', 'B')] + x[('A', 'C')] + x[('A', 'T')], "Node_A"
model += x[('S', 'B')] + x[('A', 'B')] == x[('B', 'C')] + x[('B', 'T')], "Node_B"
model += x[('A', 'C')] + x[('B', 'C')] == x[('C', 'T')], "Node_C"

# 7. Solve the model
model.solve()

# 8. Output the results
print(f"Status: {pulp.LpStatus[model.status]}")
print(f"Optimal Total Flow: {pulp.value(model.objective)} tons/day")
for edge in capacities.keys():
    print(f"Flow on {edge[0]} -> {edge[1]}: {x[edge].varValue}")
import pandas as pd
import heapq
import sys

# ======================
#  MIN-COST FLOW SOLVER
# ======================

class Edge:
    def __init__(self, v, cap, cost, rev):
        self.v = v
        self.cap = cap
        self.cost = cost
        self.rev = rev

def add_edge(graph, u, v, cap, cost):
    """Add a directed edge (u→v) with capacity and cost to the graph."""
    graph[u].append(Edge(v, cap, cost, len(graph[v])))
    graph[v].append(Edge(u, 0, -cost, len(graph[u]) - 1))

def min_cost_flow(supply_nodes, demand_nodes, supply, demand, costs):
    """Compute the minimum cost distribution plan from supply to demand nodes."""
    node_index = {}
    idx = 1
    for s in supply_nodes:
        node_index[s] = idx; idx += 1
    for d in demand_nodes:
        node_index[d] = idx; idx += 1
    SOURCE = 0
    SINK = idx
    N = SINK + 1

    # Build the graph
    graph = [[] for _ in range(N)]
    for s in supply_nodes:
        add_edge(graph, SOURCE, node_index[s], supply[s], 0)
    for s in supply_nodes:
        for d in demand_nodes:
            add_edge(graph, node_index[s], node_index[d], 10**9, costs[s][d])
    for d in demand_nodes:
        add_edge(graph, node_index[d], SINK, demand[d], 0)

    INF = 10**18
    total_flow = 0
    total_cost = 0
    potential = [0]*N
    parent_v = [0]*N
    parent_e = [0]*N
    required_flow = sum(demand.values())

    # Successive shortest path algorithm (with potentials)
    while total_flow < required_flow:
        dist = [INF]*N
        dist[SOURCE] = 0
        pq = [(0, SOURCE)]
        while pq:
            curd, u = heapq.heappop(pq)
            if curd != dist[u]: 
                continue
            for ei, e in enumerate(graph[u]):
                if e.cap > 0:
                    v = e.v
                    nd = curd + e.cost + potential[u] - potential[v]
                    if nd < dist[v]:
                        dist[v] = nd
                        parent_v[v] = u
                        parent_e[v] = ei
                        heapq.heappush(pq, (nd, v))
        if dist[SINK] == INF:
            raise RuntimeError(" Cannot deliver all goods – infeasible data.")

        for v in range(N):
            if dist[v] < INF:
                potential[v] += dist[v]

        addf = required_flow - total_flow
        v = SINK
        while v != SOURCE:
            u = parent_v[v]
            e = graph[u][parent_e[v]]
            addf = min(addf, e.cap)
            v = u

        v = SINK
        while v != SOURCE:
            u = parent_v[v]
            e = graph[u][parent_e[v]]
            e.cap -= addf
            graph[v][e.rev].cap += addf
            total_cost += addf * e.cost
            v = u
        total_flow += addf

    # Extract optimal allocation
    alloc = []
    for s in supply_nodes:
        u = node_index[s]
        for e in graph[u]:
            if e.v in [node_index[d] for d in demand_nodes]:
                flow_sent = graph[e.v][e.rev].cap
                if flow_sent > 0:
                    dname = [k for k, v in node_index.items() if v == e.v][0]
                    alloc.append({
                        'From': s,
                        'To': dname,
                        'Quantity': int(flow_sent),
                        'UnitCost': costs[s][dname],
                        'Cost': int(flow_sent)*costs[s][dname]
                    })
    df = pd.DataFrame(alloc)
    return df, total_cost


# ======================
#  INPUT FILE HANDLING
# ======================

def read_input(file_path):
    """Read supply, demand, and cost tables from an Excel file."""
    xls = pd.ExcelFile(file_path)

    supply_df = pd.read_excel(xls, "TramPhat")
    demand_df = pd.read_excel(xls, "TramThu")
    cost_df = pd.read_excel(xls, "ChiPhi")

    supply_nodes = supply_df["TenTram"].tolist()
    supply = dict(zip(supply_df["TenTram"], supply_df["Cung"]))

    demand_nodes = demand_df["TenTram"].tolist()
    demand = dict(zip(demand_df["TenTram"], demand_df["NhuCau"]))

    costs = {}
    for _, row in cost_df.iterrows():
        station = row["TramPhat"]
        costs[station] = {d: row[d] for d in demand_nodes}

    return supply_nodes, demand_nodes, supply, demand, costs


# ======================
#  MAIN EXECUTION
# ======================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python distribution_optimizer_from_file.py <input_file.xlsx>")
        sys.exit(1)

    file_path = sys.argv[1]
    print(f" Reading data from: {file_path} ...")

    supply_nodes, demand_nodes, supply, demand, costs = read_input(file_path)
    df, total_cost = min_cost_flow(supply_nodes, demand_nodes, supply, demand, costs)
    df = df[df['Quantity'] > 0].reset_index(drop=True)

    print("\n=== OPTIMAL DISTRIBUTION PLAN ===")
    print(df.to_string(index=False))
    print(f"\n Minimum total cost: {total_cost:,} VND")

    #  Save results as Excel file
    output_file = "allocation_optimal.xlsx"
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="OptimalPlan")

        # Add summary sheets
        summary_supply = df.groupby('From')['Quantity'].sum().rename('TotalSent').reset_index()
        summary_demand = df.groupby('To')['Quantity'].sum().rename('TotalReceived').reset_index()

        summary_supply.to_excel(writer, index=False, sheet_name="SupplySummary")
        summary_demand.to_excel(writer, index=False, sheet_name="DemandSummary")

        # Write overall total cost to a final summary sheet
        summary_info = pd.DataFrame({
            "Metric": ["Total Cost (VND)"],
            "Value": [total_cost]
        })
        summary_info.to_excel(writer, index=False, sheet_name="Summary")

    print(f"\n Results saved to: {output_file}")

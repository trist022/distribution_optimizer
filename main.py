import pandas as pd
import sys


def read_excel(file_path):
    supply_df = pd.read_excel(file_path, "TramPhat")
    demand_df = pd.read_excel(file_path, "TramThu")
    cost_df = pd.read_excel(file_path, "ChiPhi")

    supply = dict(zip(supply_df["TenTram"], supply_df["Cung"]))
    demand = dict(zip(demand_df["TenTram"], demand_df["NhuCau"]))

    costs = {}
    for _, row in cost_df.iterrows():
        costs[row["TramPhat"]] = {col: row[col] for col in demand.keys()}

    return supply, demand, costs


def find_optimal_plan(supply, demand, costs):
    result = []
    total_cost = 0

    remaining_supply = supply.copy()
    remaining_demand = demand.copy()

    while any(d > 0 for d in remaining_demand.values()):
        best_cost = float("inf")
        best_from = None
        best_to = None

        for from_station in remaining_supply:
            if remaining_supply[from_station] <= 0:
                continue
            for to_station in remaining_demand:
                if remaining_demand[to_station] <= 0:
                    continue
                if costs[from_station][to_station] < best_cost:
                    best_cost = costs[from_station][to_station]
                    best_from = from_station
                    best_to = to_station

        if best_from is None:
            break

        quantity = min(remaining_supply[best_from], remaining_demand[best_to])

        result.append(
            {
                "From": best_from,
                "To": best_to,
                "Quantity": quantity,
                "UnitCost": best_cost,
                "Cost": quantity * best_cost,
            }
        )

        remaining_supply[best_from] -= quantity
        remaining_demand[best_to] -= quantity
        total_cost += quantity * best_cost

    return pd.DataFrame(result), total_cost


def save_excel(df, total_cost, output_file="result.xlsx"):
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Plan")

        pd.DataFrame({"Metric": ["Total Cost"], "Value": [total_cost]}).to_excel(
            writer, index=False, sheet_name="Summary"
        )


def main():
    if len(sys.argv) < 2:
        print("Cách dùng: python main.py <file.xlsx>")
        sys.exit(1)

    file_path = sys.argv[1]

    supply, demand, costs = read_excel(file_path)
    df, total_cost = find_optimal_plan(supply, demand, costs)

    print("\n=== KẾ HOẠCH TỐI ƯU ===")
    print(df.to_string(index=False))
    print(f"\nTổng chi phí: {total_cost:,} VND")

    save_excel(df, total_cost)
    print("\nĐã lưu kết quả vào: result.xlsx")


if __name__ == "__main__":
    main()

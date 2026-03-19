import matplotlib.pyplot as plt
from simulator import run_simulation

fixed_params = {
    "steps": 100,
    "start_price": 100.0,
    "spread": 2.0,
    "base_fill_probability": 0.3,
    "fill_sensitivity": 0.1,
}

aware_params = {
    "steps": 100,
    "start_price": 100.0,
    "spread": 2.0,
    "base_fill_probability": 0.3,
    "fill_sensitivity": 0.1,
    "inventory_skew": 0.2,
}

seed = 42

fixed_result = run_simulation("fixed", fixed_params, rng_seed=seed)
aware_result = run_simulation("inventory_aware", aware_params, rng_seed=seed)

plt.plot(fixed_result["pnls"], label="Fixed Spread")
plt.plot(aware_result["pnls"], label="Inventory-Aware")
plt.title("PnL Comparison")
plt.xlabel("Time Step")
plt.ylabel("PnL")
plt.legend()
plt.show()

plt.plot(fixed_result["inventories"], label="Fixed Spread")
plt.plot(aware_result["inventories"], label="Inventory-Aware")
plt.title("Inventory Comparison")
plt.xlabel("Time Step")
plt.ylabel("Inventory")
plt.legend()
plt.show()

print("Fixed final pnl:", fixed_result["final_pnl"])
print("Aware final pnl:", aware_result["final_pnl"])
print("Fixed max abs inventory:", fixed_result["max_abs_inventory"])
print("Aware max abs inventory:", aware_result["max_abs_inventory"])
print("Fixed fills:", fixed_result["fills"])
print("Aware fills:", aware_result["fills"])




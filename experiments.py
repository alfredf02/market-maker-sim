import math
from simulator import run_simulation

DISPLAY_NAMES = {
    "fixed": "Fixed",
    "inventory_aware": "Inventory-Aware",
}

def mean(values):
    if not values:
        return 0.0
    return sum(values) / len(values)


def std(values):
    if not values:
        return 0.0

    avg = mean(values)
    variance = sum((value - avg) ** 2 for value in values) / len(values)
    return math.sqrt(variance)


def proportion_profitable(final_pnls):
    if not final_pnls:
        return 0.0

    profitable_runs = sum(1 for pnl in final_pnls if pnl > 0)
    return profitable_runs / len(final_pnls)


def summarize_results(results):
    final_pnls = [result["final_pnl"] for result in results]
    max_abs_inventories = [result["max_abs_inventory"] for result in results]
    fills = [result["fills"] for result in results]

    summary = {
        "num_runs": len(results),
        "mean_final_pnl": mean(final_pnls),
        "std_final_pnl": std(final_pnls),
        "mean_max_abs_inventory": mean(max_abs_inventories),
        "mean_fills": mean(fills),
        "best_final_pnl": max(final_pnls) if final_pnls else 0.0,
        "worst_final_pnl": min(final_pnls) if final_pnls else 0.0,
        "proportion_profitable": proportion_profitable(final_pnls),
    }

    return summary


def run_many_simulations(strategy_name, params, seeds):
    results = []

    for seed in seeds:
        result = run_simulation(strategy_name, params, rng_seed=seed)
        results.append(result)

    summary = summarize_results(results)

    return {
        "strategy_name": strategy_name,
        "params": params,
        "seeds": list(seeds),
        "results": results,
        "summary": summary,
    }


def compare_strategies(strategy_params_map, num_runs=200):
    seeds = range(num_runs)
    comparison = {}

    for strategy_name, params in strategy_params_map.items():
        experiment_result = run_many_simulations(strategy_name, params, seeds)
        comparison[strategy_name] = experiment_result["summary"]

    return comparison

def format_summary_table(summary_table):
    headers = [
        ("Strategy", 18),
        ("Mean PnL", 12),
        ("Std PnL", 12),
        ("Mean Max Inv", 16),
        ("Mean Fills", 14),
        ("Profitable %", 15),
        ("Best Run", 12),
        ("Worst Run", 12),
    ]

    header_line = "".join(title.ljust(width) for title, width in headers)
    separator_line = "-" * len(header_line)

    lines = [header_line, separator_line]

    for strategy_name, summary in summary_table.items():
        display_name = DISPLAY_NAMES.get(strategy_name, strategy_name)

        line = (
            f"{display_name:<18}"
            f"{summary['mean_final_pnl']:>12.2f}"
            f"{summary['std_final_pnl']:>12.2f}"
            f"{summary['mean_max_abs_inventory']:>16.2f}"
            f"{summary['mean_fills']:>14.2f}"
            f"{summary['proportion_profitable'] * 100:>14.2f}%"
            f"{summary['best_final_pnl']:>12.2f}"
            f"{summary['worst_final_pnl']:>12.2f}"
        )
        lines.append(line)

    return "\n".join(lines)

def print_summary_table(summary_table):
    if summary_table:
        first_summary = next(iter(summary_table.values()))
        num_runs = first_summary.get("num_runs", "N/A")
        print(f"Strategy comparison over {num_runs} runs")
        print()
        
    print(format_summary_table(summary_table))
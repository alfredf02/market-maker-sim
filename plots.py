import matplotlib.pyplot as plt
from config import DEFAULT_HIST_BINS

def plot_pnl_paths(strategy_results_map):
    plt.figure()

    for label, result in strategy_results_map.items():
        plt.plot(result["pnls"], label=label)

    plt.title("PnL Comparison")
    plt.xlabel("Time Step")
    plt.ylabel("PnL")
    plt.legend()
    plt.show()


def plot_inventory_paths(strategy_results_map):
    plt.figure()

    for label, result in strategy_results_map.items():
        plt.plot(result["inventories"], label=label)

    plt.title("Inventory Comparison")
    plt.xlabel("Time Step")
    plt.ylabel("Inventory")
    plt.legend()
    plt.show()


def plot_sample_path(fixed_result, aware_result):
    plot_pnl_paths(
        {
            "Fixed Spread": fixed_result,
            "Inventory-Aware": aware_result,
        }
    )

    plot_inventory_paths(
        {
            "Fixed Spread": fixed_result,
            "Inventory-Aware": aware_result,
        }
    )


def plot_final_pnl_histogram(strategy_experiments_map, bins=DEFAULT_HIST_BINS):
    plt.figure()

    for label, experiment_result in strategy_experiments_map.items():
        final_pnls = [result["final_pnl"] for result in experiment_result["results"]]
        plt.hist(final_pnls, bins=bins, alpha=0.6, label=label)

    plt.title("Histogram of Final PnL")
    plt.xlabel("Final PnL")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()
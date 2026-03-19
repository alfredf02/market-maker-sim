from config import DEFAULT_PARAMS, DEFAULT_NUM_RUNS, DEFAULT_SAMPLE_SEED
from experiments import compare_strategies, print_summary_table, run_many_simulations
from simulator import run_simulation
from plots import plot_sample_path, plot_final_pnl_histogram


def main():
    summary_table = compare_strategies(DEFAULT_PARAMS, num_runs=DEFAULT_NUM_RUNS)
    print_summary_table(summary_table)

    seed = DEFAULT_SAMPLE_SEED

    fixed_result = run_simulation("fixed", DEFAULT_PARAMS["fixed"], rng_seed=seed)
    aware_result = run_simulation("inventory_aware", DEFAULT_PARAMS["inventory_aware"], rng_seed=seed)
    plot_sample_path(fixed_result, aware_result)

    seeds = range(DEFAULT_NUM_RUNS)
    fixed_experiment = run_many_simulations("fixed", DEFAULT_PARAMS["fixed"], seeds)
    aware_experiment = run_many_simulations("inventory_aware", DEFAULT_PARAMS["inventory_aware"], seeds)

    plot_final_pnl_histogram(
        {
            "Fixed Spread": fixed_experiment,
            "Inventory-Aware": aware_experiment,
        }
    )


if __name__ == "__main__":
    main()


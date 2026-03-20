from config import (DEFAULT_PARAMS, 
                    DEFAULT_NUM_RUNS, 
                    DEFAULT_SAMPLE_SEED,
                    DEFAULT_SWEEP_PARAMETER,
                    DEFAULT_SWEEP_VALUES,
                    DEFAULT_SCENARIOS,
                    )

from experiments import (compare_strategies, 
                         print_summary_table, 
                         run_many_simulations,
                         run_parameter_sweep,
                         print_parameter_sweep_table,
                         run_scenario_comparison,
                         print_scenario_comparison_table,
                         )

from simulator import run_simulation
from plots import plot_sample_path, plot_final_pnl_histogram, plot_parameter_sweep_metric, plot_mid_price_paths, plot_adverse_drift_path


def main():
    summary_table = compare_strategies(DEFAULT_PARAMS, num_runs=DEFAULT_NUM_RUNS)
    print_summary_table(summary_table)
    print()

    sweep_result = run_parameter_sweep(
        DEFAULT_PARAMS,
        parameter_name=DEFAULT_SWEEP_PARAMETER,
        parameter_values=DEFAULT_SWEEP_VALUES,
        num_runs=DEFAULT_NUM_RUNS,
    )
    print_parameter_sweep_table(sweep_result)
    print()

    scenario_comparison_result = run_scenario_comparison(
        DEFAULT_PARAMS,
        DEFAULT_SCENARIOS,
        num_runs=DEFAULT_NUM_RUNS,
    )
    print_scenario_comparison_table(scenario_comparison_result)

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

    plot_parameter_sweep_metric(sweep_result, "mean_final_pnl")
    plot_parameter_sweep_metric(sweep_result, "mean_max_abs_inventory")


if __name__ == "__main__":
    main()


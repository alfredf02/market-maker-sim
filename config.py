BASE_PARAMS = {
    "steps": 100,
    "start_price": 100.0,
    "spread": 2.0,
    "volatility": 1.0,
    "base_fill_probability": 0.3,
    "fill_sensitivity": 0.1,
    "adverse_selection": False,
    "adverse_selection_strength": 0.2,
}

DEFAULT_PARAMS = {
    "fixed": {
        **BASE_PARAMS,
    },
    "inventory_aware": {
        **BASE_PARAMS,
        "inventory_skew": 0.2,
    },
}

DEFAULT_NUM_RUNS = 200
DEFAULT_SAMPLE_SEED = 42
DEFAULT_HIST_BINS = 20

DEFAULT_SWEEP_PARAMETER = "spread"
DEFAULT_SWEEP_VALUES = [1.0, 2.0, 3.0]

DEFAULT_SCENARIOS = {
    "No Adverse Selection": {
        "adverse_selection": False,
    },
    "Adverse Selection": {
        "adverse_selection": True,
        "adverse_selection_strength": 0.2,
    },
}
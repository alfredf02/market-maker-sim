# Market Making Simulator

A Python market making simulator that compares a **fixed spread strategy** against an **inventory-aware strategy** under the same simulated market conditions.

## Key Takeaway

This project compares a fixed spread market maker with an inventory-aware market maker under the same simulated random seeds. The main result is that inventory-aware quoting can reduce inventory risk and change execution behaviour by making quotes more or less aggressive depending on current position.

---

## What This Project Does

This simulator models a market maker quoting a bid and ask around a simulated mid price. At each time step, the simulator:

1. Updates the mid price using a random walk
2. Asks the chosen strategy for bid/ask quotes
3. Converts those quotes into probabilistic fill chances
4. Simulates fills
5. Updates cash, inventory, and mark-to-market PnL
6. Stores histories for analysis

---

## Strategies Compared

### 1. Fixed Spread

The fixed strategy always quotes symmetrically around the current mid price:

```
bid = mid - spread / 2
ask = mid + spread / 2
```

It does not react to inventory.

### 2. Inventory-Aware

The inventory-aware strategy shifts the quote center based on current inventory:

```
adjusted_mid = mid - inventory_skew × inventory
bid = adjusted_mid - spread / 2
ask = adjusted_mid + spread / 2
```

**Interpretation:**
- If inventory is too **positive**, the strategy lowers both quotes to encourage selling
- If inventory is too **negative**, the strategy raises both quotes to encourage buying

This makes the strategy more conservative with inventory accumulation.

---

## Model Assumptions

This simulator is intentionally simplified. Key assumptions:

- The mid price follows a **random walk**
- Quotes are updated **every time step**
- Fills are **probabilistic**, depending on quote attractiveness relative to mid
- Each fill has **size 1**
- There are **no fees, no latency, no queue position modeling**, and no real limit order book dynamics

PnL is marked to market as:

```
PnL = cash + inventory × mid
```

### Fill Model

Fill probability depends on quote aggressiveness relative to mid:

```
bid_fill_prob = base_fill_probability + fill_sensitivity × (bid - mid)
ask_fill_prob = base_fill_probability + fill_sensitivity × (mid - ask)
```

Both probabilities are clamped to `[0, 1]`.

**Interpretation:**
- A **higher bid** is more aggressive → more likely to be filled
- A **lower ask** is more aggressive → more likely to be filled

---

## Metrics Reported

For repeated experiments, the simulator reports:

| Metric | Description |
|---|---|
| Mean final PnL | Average PnL across all runs |
| Std of final PnL | Variability of outcomes |
| Mean max absolute inventory | Average peak inventory exposure |
| Mean number of fills | Average execution count |
| Profitable % | Proportion of runs with positive PnL |
| Best / Worst run | Extremes across the distribution |

These are computed over many random seeds so the comparison reflects a distribution of outcomes rather than a single lucky path.

---

## Project Structure

```
market_maker_sim/
├── main.py          # Entry point — runs the default experiment and prints results
├── config.py        # Default parameters and experiment settings
├── simulator.py     # Core simulation loop for one run
├── strategies.py    # Quote generation logic for each strategy
├── metrics.py       # One-run metrics: final PnL, max inventory, etc.
├── experiments.py   # Multi-run experiment logic and summary table formatting
├── plots.py         # Plotting helpers for sample paths and final PnL histograms
└── README.md
```

---

## How to Run

**1. Install dependencies**

```bash
pip install matplotlib
```

**2. Run the simulator**

```bash
python main.py
```

This will:
- Run the default multi-run experiment
- Print a summary table
- Optionally show plots if plotting is enabled in `main.py`

---

## Example Output

```
Strategy comparison over 200 runs

Strategy          Mean PnL    Std PnL    Mean Max Inv    Mean Fills    Profitable %    Best Run    Worst Run
------------------------------------------------------------------------------------------------------------
Fixed                 1.24       4.51            8.03         42.18           61.00%       12.77        -9.42
Inventory-Aware       2.87       3.76            5.41         39.64           71.50%       11.93        -4.08
```

> Exact numbers will vary with parameter settings.

---

## What I Found

In general, the inventory-aware strategy tends to:

- Reduce extreme inventory accumulation
- Produce lower average inventory risk
- Change fill behaviour by making one side of the quote more aggressive
- Improve the stability of outcomes compared with a purely fixed spread strategy

The exact trade-off depends on parameter choices:

- **Wider spreads** → fewer fills
- **Stronger inventory skew** → more aggressive inventory reduction
- **Higher fill sensitivity** → quote placement matters more

---

## Why This Project Is Useful

This project demonstrates:

- Decomposition of strategy logic from simulation logic
- Reproducible experiments using seeded randomness
- Comparison of trading strategies under shared market scenarios
- Basic quantitative evaluation across repeated runs
- Clean Python project structure rather than a monolithic script

It is intentionally simple, but provides a solid foundation for extending toward more realistic market making models.

---

## Possible Extensions

- Sweep over spread or `inventory_skew` and compare summary statistics
- Add transaction fees or rebates
- Add inventory limits
- Use a different mid-price process (e.g. mean-reverting, jump-diffusion)
- Compare additional strategies
- Export experiment results to CSV
- Add unit tests for strategy and metric helpers

---

## Notes

This is an educational simulator, not a real trading system. It ignores many important market microstructure effects, including queue priority, latency, adverse selection from informed flow, and full order book dynamics.
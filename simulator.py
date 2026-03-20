import random
from strategies import STRATEGIES
from metrics import final_pnl, max_abs_inventory, number_of_fills

def clamp(value, lower, upper) :
    return max(lower, min(upper, value))

def run_simulation(strategy_name, params, rng_seed):
    strategy_fn = STRATEGIES[strategy_name]
    rng = random.Random(rng_seed)

    steps = params.get("steps", 100)
    start_price = params.get("start_price", 100.0)
    spread = params.get("spread", 2.0)
    volatility = params.get("volatility", 1.0)
    base_fill_probability = params.get("base_fill_probability", 0.3)
    fill_sensitivity = params.get("fill_sensitivity", 0.1)
    adverse_selection = params.get("adverse_selection", False)
    adverse_selection_strength = params.get("adverse_selection_strength", 0.2)

    price = start_price
    inventory = 0
    cash = 0.0

    pnls = []
    inventories = []
    mids = []
    bids = []
    asks = []
    bid_fill_probs = []
    ask_fill_probs = []
    adverse_drifts = []
    price_moves = []

    buy_fills = 0
    sell_fills = 0

    last_fill_signal = 0

    for step in range(steps):
        adverse_drift = 0.0

        if adverse_selection:
            adverse_drift = adverse_selection_strength * last_fill_signal

        move = rng.uniform(-volatility, volatility) + adverse_drift
        price += move
        mid = price

        bid, ask = strategy_fn(mid, inventory, params)

        bid_fill_prob = base_fill_probability + fill_sensitivity * (bid - mid)
        ask_fill_prob = base_fill_probability + fill_sensitivity * (mid - ask)

        bid_fill_prob = clamp(bid_fill_prob, 0.0, 1.0)
        ask_fill_prob = clamp(ask_fill_prob, 0.0, 1.0)

        bid_filled = rng.random() < bid_fill_prob
        ask_filled = rng.random() < ask_fill_prob

        if bid_filled:
            inventory += 1
            cash -= bid
            buy_fills += 1

        if ask_filled:
            inventory -= 1
            cash += ask
            sell_fills += 1

        if bid_filled and not ask_filled:
            last_fill_signal = -1
        elif ask_filled and not bid_filled:
            last_fill_signal = 1
        else:
            last_fill_signal = 0

        pnl = cash + inventory * mid

        mids.append(mid)
        bids.append(bid)
        asks.append(ask)
        bid_fill_probs.append(bid_fill_prob)
        ask_fill_probs.append(ask_fill_prob)
        adverse_drifts.append(adverse_drift)
        price_moves.append(move)
        inventories.append(inventory)
        pnls.append(pnl)

    result = {
        "strategy_name": strategy_name,
        "params": params,
        "rng_seed": rng_seed,
        "pnls": pnls,
        "inventories": inventories,
        "mids": mids,
        "bids": bids,
        "asks": asks,
        "bid_fill_probs": bid_fill_probs,
        "ask_fill_probs": ask_fill_probs,
        "adverse_drifts": adverse_drifts,
        "price_moves": price_moves,
        "buy_fills": buy_fills,
        "sell_fills": sell_fills,
        "fills": number_of_fills(buy_fills, sell_fills),
        "final_pnl": final_pnl(pnls),
        "max_abs_inventory": max_abs_inventory(inventories),
    }

    return result
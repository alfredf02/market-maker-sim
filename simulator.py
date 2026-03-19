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
    base_fill_probability = params.get("base_fill_probability", 0.3)
    fill_sensitivity = params.get("fill_sensitivity", 0.1)

    price = start_price
    inventory = 0
    cash = 0.0

    inventories = []
    pnls = []
    mids = []
    bids = []
    asks = []
    bid_fill_probs = []
    ask_fill_probs = []

    buy_fills = 0
    sell_fills = 0

    for step in range(steps):
        move = rng.uniform(-1, 1)
        price += move
        mid = price

        bid, ask = strategy_fn(mid, inventory, params)

        random_number = rng.random()

        bid_fill_prob = base_fill_probability + fill_sensitivity * (bid - mid)
        ask_fill_prob = base_fill_probability + fill_sensitivity * (mid - ask)

        bid_fill_prob = clamp(bid_fill_prob, 0.0, 1.0)
        ask_fill_prob = clamp(ask_fill_prob, 0.0, 1.0)

        if rng.random() < bid_fill_prob:
            inventory += 1
            cash -= bid
            buy_fills += 1

        if rng.random() < ask_fill_prob:
            inventory -= 1
            cash += ask
            sell_fills += 1

        pnl = cash + inventory * mid

        mids.append(mid)
        bids.append(bid)
        asks.append(ask)
        bid_fill_probs.append(bid_fill_prob)
        ask_fill_probs.append(ask_fill_prob)
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
        "final_pnl": final_pnl(pnls),
        "max_abs_inventory": max_abs_inventory(inventories),
        "buy_fills": buy_fills,
        "sell_fills": sell_fills,
        "fills": number_of_fills(buy_fills, sell_fills),
    }

    return result
def final_pnl(pnls) :
    return pnls[-1] if pnls else 0.0

def max_abs_inventory(inventories) :
    return max((abs(inventory) for inventory in inventories), default=0)

def number_of_fills(buy_fills, sell_fills):
    return buy_fills + sell_fills
def get_fixed_quotes(mid, inventory, params) :
    spread = params["spread"]
    bid = mid - spread / 2
    ask = mid + spread / 2
    return bid, ask

def get_inventory_aware_quotes(mid, inventory, params) :
    spread = params["spread"]
    inventory_skew = params["inventory_skew"]

    adjusted_mid = mid - inventory_skew * inventory
    bid = adjusted_mid - spread / 2
    ask = adjusted_mid + spread / 2
    return bid, ask

STRATEGIES = {
    "fixed": get_fixed_quotes,
    "inventory_aware": get_inventory_aware_quotes,
}
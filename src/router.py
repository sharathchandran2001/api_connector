from config import ROUTE_MAP

def get_endpoints(rule: str) -> list:
    return ROUTE_MAP.get(rule, [])

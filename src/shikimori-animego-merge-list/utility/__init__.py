def groupBy(arr: list, key: str) -> dict[str, any]:
    result = {}
    for item in arr:
        result[item[key]] = item
    return result

def withLeading(left: object, right: object, field: str, left_main: bool = True):
    return left.get(field) or right.get(field) if left_main else right.get(field) or left.get(field)
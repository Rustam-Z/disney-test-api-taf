from jsonpath_ng import parse


def parser(selector: str, data: dict) -> list:
    jsonpath_expr = parse(selector)
    result = jsonpath_expr.find(data)
    result_list = [match.value for match in result]

    return result_list

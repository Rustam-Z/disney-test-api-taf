def check_model_common_values(request_model: dict, response_model: dict):
    if not isinstance(response_model, dict):
        response_model = dict(response_model)

    common_keys = set(request_model.keys()) & set(response_model.keys())  # Response may include entity `id`
    return all(request_model[key] == response_model[key] for key in common_keys)

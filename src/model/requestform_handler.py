def form_data_to_dict(form_data):
    data = dict()
    for key in form_data:
        data[key] = form_data.get(key)
    return data

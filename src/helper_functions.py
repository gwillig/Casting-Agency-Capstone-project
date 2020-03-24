def process_request(request):
    """
    Check if the parametre are in forms or in args
    :param request:
    :return:
    """
    if len(request.form) == 0:
        request_dict = request.args
    else:
        request_dict = request.form
    return request_dict
def get_user_ip_and_session_key(request):
    """To get user ip and set-get session key"""
    # print(request.META)
    ip_v4 = request.META['REMOTE_ADDR']
    request.session['ip_v4'] = ip_v4
    # print(ip_v4)
    return {'ip_v4': ip_v4}

def get_client_connection(request) -> tuple:
    ua = request.META.get("HTTP_USER_AGENT", "")
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0], ua
    return request.META.get("REMOTE_ADDR"), ua


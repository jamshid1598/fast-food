from string import digits
from secrets import choice as secret_choice


def get_client_ip(request) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def otp_generator(size: int = 6, char: str = digits) -> str:
    return "".join(secret_choice(char) for _ in range(size))

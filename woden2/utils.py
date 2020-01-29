from functools import wraps
from random import choice

def integer_setter(value):
    if not value:
        return 0
    else:
        return int(value)

def random_headers(user_agents):
    def selector():
        user_agent = choice(user_agents)
        return {
            "authority": "scholar.google.ca",
            "method": "GET",
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-CA,en;q=0.9,es-PE;q=0.8,es;q=0.7,en-GB;q=0.6,en-US;q=0.5",
            "cache-control": "max-age=0",
            "referer": "https://scholar.google.ca/scholar",
            "upgrade-insecure-requests": "1",
            'User-Agent': user_agent
        }
    return selector

def validate_options(options):
    if isinstance(options, dict):
        options = options.items()
    def inner(func):
        @wraps(func)
        def wrapper(selection, *args, **kwargs):
            for option in options:
                if selection in option:
                    break
            else:
                raise ValueError()
            return func(selection, *args, **kwargs)
        return wrapper
    return inner
        

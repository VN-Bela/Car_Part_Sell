try:
    from .production import *
except ImportError:
    try:
        from .dev import *
    except ImportError as e:
        raise Exception("Settings files are missing")

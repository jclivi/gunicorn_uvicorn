import sys
import traceback

from log import log

class TryExcept(object):
    """
        function try except check
        import TryExcept as try_except
    """
    def __init__(self, einfo=None, ifexit=False):
        self.einfo = einfo
        self.ifexit = ifexit

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = None
            try:
                result = func(*args, **kwargs)
            except Exception as error:
                message = "func: {}\n".format(func.__name__)
                if self.einfo:
                    message += "nerror_info: {} failed\n".format(self.einfo)

                message += "error: {}\n".format(error)
                tb = traceback.print_exc()
                if tb:
                    message += "traceback: {}\n".format(tb)

                log.error(message)
                if self.ifexit:
                    print("exit")
                    sys.exit(-1)
            finally:
                return result
        return wrapper

def number_of_workers(num=1, islimit=False):
    n = num
    cpu_count = 0
    if not islimit:
        import multiprocessing
        cpu_count = multiprocessing.cpu_count()
        n = (cpu_count * 2) + num

    return n

def read_yml(etc):
    f = open(etc, 'r', encoding='utf-8')
    r = f.read()
    if not r:
        return None

    import yaml
    result = yaml.safe_load(r)
    print("result", result)

    return result

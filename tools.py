import time

from uuid import uuid5
from uuid import NAMESPACE_DNS as npd

# import logging
import multiprocessing
import tqdm

def timefunc(f):
    """
    Time profiling
    """
    def f_timer(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f.__name__, 'took', end - start, 'time')
        return result
    return f_timer

def getUuid(file):
    return uuid5(npd, str(file))

def genericParallel(lst, methd, threads=2):
    """
    Launch a method in parallel
    """
    results = []
    # print "#####"
    # print lst
    if lst :
        # logger.warning('Running %s ...'%str(methd))
        pool = multiprocessing.Pool(threads)
        for x in tqdm.tqdm(pool.imap_unordered(methd, lst), total=len(lst)):
            results.append(x)
            pass
        pool.close()
        pool.join()
    # else :
        # logger.warning('Nothing to do %s'%methd)

    return [resnotNone for resnotNone in results if resnotNone is not None]
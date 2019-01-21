import time

from uuid import uuid5
from uuid import NAMESPACE_DNS as npd

# import logging
import multiprocessing
import tqdm

import logging 
from logging.handlers import RotatingFileHandler

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
    """
    Return uuid of a file
    """
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


def create_logger():
    """
    From Sam et Max 
    http://sametmax.com/ecrire-des-logs-en-python/
    and 
    http://domeu.blogspot.com/2016/08/python-logging-logger-ce-quil-ne-faut.html
    """
    # création de l'objet logger qui va nous servir à écrire dans les logs
    logger = logging.getLogger()
    # on met le niveau du logger à DEBUG, comme ça il écrit tout
    logger.setLevel(logging.DEBUG)
     
    # création d'un formateur qui va ajouter le temps, le niveau
    # de chaque message quand on écrira un message dans le log
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    # création d'un handler qui va rediriger une écriture du log vers
    # un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
    file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
    # on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
    # créé précédement et on ajoute ce handler au logger
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
     
    # création d'un second handler qui va rediriger chaque écriture de log
    # sur la console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
     
    # Après 3 heures, on peut enfin logguer
    # Il est temps de spammer votre code avec des logs partout :
    # logger.info('Hello')
    # logger.warning('Testing %s', 'foo')
    return
import os
import time
from path import Path as path
# from glob import glob
import gpxpy
from pandas import DataFrame

import pickle

from uuid import uuid5
from uuid import NAMESPACE_DNS as npd

import logging
import multiprocessing
import tqdm

import pygal
import itertools

#
FORMAT = 'DEBUG : %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('debug')
#

def timefunc(f):
    def f_timer(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print f.__name__, 'took', end - start, 'time'
        return result
    return f_timer

# @timefunc
def load_run_data(gpx_file, filter=""):
    gpx = gpxpy.parse(open(gpx_file, 'r'))
    uuid = uuid5(npd, str(gpx_file))
    # Loop through tracks
    for track_idx, track in enumerate(gpx.tracks):
        track_name = track.name
        track_time = track.get_time_bounds().start_time
        track_length = track.length_3d()
        track_duration = track.get_duration()
        track_speed = track.get_moving_data().max_speed

    return [uuid, os.path.basename(gpx_file), track_idx, track_name, 
                                 track_time, track_length, track_duration, track_speed]


@timefunc
def filter_data(data):
	df = DataFrame(data, columns=['UUID', 'File_Name', 'Index', 'Name',
	                              'Time', 'Length', 'Duration', 'Max_Speed'])
	cols = ['UUID', 'Time', 'Length', 'Duration', 'Max_Speed']
	tracks = df[cols].copy()
	tracks['Length'] /= 1e3
	tracks['Duration'] /= 3600
	tracks['Max_Speed'] *= 3.6
	tracks['Ave_Speed'] = tracks['Length'] / tracks['Duration']
	tracks.drop_duplicates(inplace=True)
	tracks['Year'] = tracks['Time'].apply(lambda x: x.year)
	tracks['Month'] = tracks['Time'].apply(lambda x: x.month)
	# tracks_grouped = tracks.groupby(['Year','Month'])
	return tracks

def rpickle(picke_file, state=None):
    results = []
    if picke_file.isfile():
        with open(picke_file, 'rb') as read_pickle:
            results += pickle.load(read_pickle)
    return results

def getUuid(file):
    return uuid5(npd, str(file))

def filter_files(file_unfiltered):
    if str(getUuid(file_unfiltered)) not in uuid_pickle:
        return file_unfiltered

def getfiles(results, strava_dir):
    files_unfiltered = strava_dir.files()
    global uuid_pickle
    uuid_pickle = ''
    for track in results :
        uuid_pickle+=str(track['uuid'])
    files = genericParallel(files_unfiltered, filter_files, 4)
    return files

def genericParallel(lst, methd, threads=2):
    results = []
    if lst :
        logger.warning('Running %s ...'%str(methd))
        pool = multiprocessing.Pool(threads)
        for x in tqdm.tqdm(pool.imap_unordered(methd, lst), total=len(lst)):
            results.append(x)
            pass
        pool.close()
        pool.join()
    else :
        logger.warning('Nothing to do %s'%methd)
    return results

@timefunc
def load_data_parallel():
	dirs = path('./data/GPX')
	pickle_file = dirs+path('data.pickle')

	data = rpickle(pickle_file)
	files = getfiles(data, dirs)
	data += genericParallel(files, load_run_data, 4)
	return data

def yearStats(data):
    km_y = data[data.Year == 2018]['Length'].sum()
    activities_y = len(data[data.Year == 2018])
    # data_grouped_year = data.groupby(['year'])
    # km_t = sum([datay['mvlenght'].sum() for year, datay in data_grouped_year])
    km_t = data['Length'].sum()
    return km_y, activities_y, km_t

def graphs(data):
    line_chart = pygal.Line(
        x_label_rotation=30, x_labels_major_count=12, interpolate='cubic')
    bar_chart = pygal.Bar(x_label_rotation=30, x_labels_major_count=12)
    box_chart = pygal.Box(x_label_rotation=30, x_labels_major_count=12)
    data_grouped_year = data.groupby(['year'])

    for year, datagr in data_grouped_year:
        datagr_m = datagr.groupby(['month'])

        bar_chart.title = 'Km by month by year'
        bar_chart.x_labels = [i for i, j in datagr_m]
        bar_chart.add('%s' % year, [{'value': i,
                                     'label': 'moy/act:%s' % str(j)}
                                    for i, j in
                                    itertools.izip(
                                    datagr_m['mvlenght'].sum(),
                                    datagr_m['mvlenght'].mean()
                                    )])

        box_chart.title = 'Km by month by year'
        box_chart.x_labels = [i for i, j in datagr_m]
        box_chart.add('%s' % year, [{'value': i,
                                     'label': 'moy/act:%s' % str(j)}
                                    for i, j in
                                    itertools.izip(
                                    datagr_m['mvlenght'].sum(),
                                    datagr_m['mvlenght'].mean()
                                    )])

        line_chart.title = 'Km by month by year'
        line_chart.x_labels = xrange(1, 13)
        line_chart.add('%s' % year, datagr_m['mvlenght'].sum().cumsum())
    bar_chart.render_to_file('./testbar.svg')
    box_chart.render_to_file('./testbox.svg')
    line_chart.render_to_file('./testline.svg')
    figs = [line_chart.render_data_uri(), 
            bar_chart.render_data_uri(), 
            box_chart.render_data_uri()]
    return figs

def globalRun(runtype='test', user='Thomas'):
    data = load_data_parallel()
    results = filter_data(data)
    # print results.head()
    # print results[results.Year == 2018]
    stats = yearStats(results)
    figs  = graphs(results)
    # print stats
    return stats, figs

# for year, datag in results: 
    # print year
    # print '#######'
    # print datag


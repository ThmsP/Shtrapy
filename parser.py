# import os
import sys
import time
import datetime
from calendar import month_name
from path import Path as path
# from glob import glob
import gpxpy
import pandas
import pickle

from uuid import uuid5
from uuid import NAMESPACE_DNS as npd

import logging
import multiprocessing
import tqdm

import matplotlib.pyplot as plt
import mplleaflet

import pygal
# import itertools

import termgraph.termgraph as tgraph


#
FORMAT = 'DEBUG : %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('debug')
#
global uuid_to_file
uuid_to_file = {}

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



# @timefunc
def load_run_data(gpx_file, filter=""):
    """
    Load a gps file and return a list of informations
    """
    gpx = gpxpy.parse(open(gpx_file, 'r'))
    uuid = uuid5(npd, str(gpx_file))
    global uuid_to_file
    uuid_to_file[str(uuid)]=gpx_file
    # Loop through tracks
    for track_idx, track in enumerate(gpx.tracks):
        track_name = track.name
        track_time = track.get_time_bounds().start_time
        track_length = track.length_3d()
        track_duration = track.get_duration()
        track_speed = track.get_moving_data().max_speed
        track_uphill, track_downhill = track.get_uphill_downhill()
        # print "uphill DownHill", track_uphill, track_downhill

    return [uuid, gpx_file, track_idx, track_name, 
            track_time, track_length, track_duration, 
            track_speed, track_uphill, track_downhill]

def leaflet(fname):
    """
    Load a gps file and show the track on map with mapleaflet
    """
    # global uuid_to_file
    # print uuid_to_file
    # gpx_file = uuid_to_file[uuid]
    gpx = gpxpy.parse(open(fname, 'r'))
    lat = []
    lon = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat.append(point.latitude)
                lon.append(point.longitude)
    # Plot the path as red dots connected by a blue line
    # plt.hold(True)
    # plt.plot(lon, lat, 'r.')
    plt.plot(lon, lat, 'b')
    #
    # Create the map. Save the file to basic_plot.html. _
    # map.html is the  default
    # root, ext = os.path.splitext(__file__)
    # mapfile = 'skeleton/'+root + '.html'
    mapfile = 'skeleton/parser.html'
    #
    # if 'path' is not specified
    #
    mplleaflet.save_html(fileobj=mapfile)
    print("Generating mplleaflet map")
    return 


@timefunc
def filter_data(data):
    """
    Take a list of informations and return a filtered DataFrame
    """
    df = pandas.DataFrame(data, columns=['UUID', 'File_Name', 'Index', 'Name',
	                              'Date', 'Length', 'Duration', 'Max_Speed',
                                  'UpHill', 'DownHill'])
    cols = ['UUID', 'File_Name', 'Date', 'Length', 'Duration', 'Max_Speed','UpHill', 'DownHill']
    tracks = df[cols].copy()

    tracks['Length'] /= 1e3
    tracks['Duration'] /= 3600 
    tracks['Time'] = tracks['Duration'].apply(lambda x: datetime.timedelta(seconds=x*3600))
    tracks['Max_Speed'] *= 3.6
    tracks['Ave_Speed'] = tracks['Length'] / tracks['Duration']
    tracks.drop_duplicates(inplace=True)
    tracks['Year'] = tracks['Date'].apply(lambda x: x.year)
    tracks['Month'] = tracks['Date'].apply(lambda x: x.month)
    
    # tracks['Date']=pandas.to_datetime(tracks.Date)
    tracks = tracks.sort_values(by='Date', ascending = False)
    tracks = tracks.round(1)
    # print(tracks.head(5))
    return tracks

def rpickle(picke_file, state=None):
    """
    Save the state of the gps file treated
    """
    logger.warning('Running rpickle ...')
    results = []
    if picke_file.isfile():
        with open(picke_file, 'rb') as read_pickle:
            results += pickle.load(read_pickle)
    # print results
    return results

def getUuid(file):
    return uuid5(npd, str(file))

def filter_files(file_unfiltered):
    """
    Compare uuid of a file with the one store in pickle
    """
    if str(getUuid(file_unfiltered)) not in uuid_pickle:
        return file_unfiltered

def getfiles(results, strava_dir):
    """
    From a list of file, generate a list of list of informations
    """
    files_unfiltered = strava_dir.files()
    global uuid_pickle
    uuid_pickle = ''
    for track in results :
        uuid_pickle+=str(track[0])
    files = genericParallel(files_unfiltered, filter_files, 4)
    return files

def genericParallel(lst, methd, threads=2):
    """
    Launch a method in parallel
    """
    results = []
    # print "#####"
    # print lst
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

    return [resnotNone for resnotNone in results if resnotNone is not None]

@timefunc
def load_data_parallel(user):
    """
    Load data from file
    Treatment is made in parallel
    """
    dirs = path('./data/GPX_%s'%user)
    pickle_file = dirs.parent+path('/data.pickle_%s'%user)
    data = rpickle(pickle_file)
    files = getfiles(data, dirs)
    data += genericParallel(files, load_run_data, 4)
    with open(pickle_file, 'wb') as saved_pickle:
        pickle.dump(data, saved_pickle)
    return data

def yearStats(data):
    """
    Return the basics stats of a year
    """
    km_y = data[data.Year == 2018]['Length'].sum()
    activities_y = len(data[data.Year == 2018])
    # data_grouped_year = data.groupby(['year'])
    # km_t = sum([datay['mvlenght'].sum() for year, datay in data_grouped_year])
    km_t = data['Length'].sum()
    data_y = data[data.Year == 2018]
    day_and_km = data_y[['Date', 'Length']].copy()
    return km_y, activities_y, km_t, day_and_km

def graphs(data):
    """
    Print the graph of all years using pygal
    Return a list of svg rendered graph
    """
    line_chart = pygal.Line(
        x_label_rotation=30, x_labels_major_count=12, interpolate='cubic')
    bar_chart = pygal.Bar(x_label_rotation=30, x_labels_major_count=12)
    box_chart = pygal.Box(x_label_rotation=30, x_labels_major_count=12)
    data_grouped_year = data.groupby(['Year'])

    for year, datagr in data_grouped_year:
        datagr_m = datagr.groupby(['Month'])

        bar_chart.title = 'Km by month by year'
        bar_chart.x_labels = [i for i, j in datagr_m]
        bar_chart.add('%s' % year, [{'value': i,
                                     'label': 'moy/act:%s' % str(j)}
                                    for i, j in
                                    zip(
                                    datagr_m['Length'].sum(),
                                    datagr_m['Length'].mean()
                                    )])

        box_chart.title = 'Km by month by year'
        box_chart.x_labels = [i for i, j in datagr_m]
        box_chart.add('%s' % year, [{'value': i,
                                     'label': 'moy/act:%s' % str(j)}
                                    for i, j in
                                    zip(
                                    datagr_m['Length'].sum(),
                                    datagr_m['Length'].mean()
                                    )])

        line_chart.title = 'Km by month by year'
        line_chart.x_labels = range(1, 13)
        line_chart.add('%s' % year, datagr_m['Length'].sum().cumsum())
    # bar_chart.render_to_file('./testbar.svg')
    # box_chart.render_to_file('./testbox.svg')
    # line_chart.render_to_file('./testline.svg')
    figs = [line_chart.render_data_uri(), 
            bar_chart.render_data_uri(),]
            # box_chart.render_data_uri()]
    return figs

def termgraphRun(dataF):
    """
    Graph in term
    """
    args = {'filename': './test_termgraph.txt', 
			'title': None, 
			'width': 50, 
			'format': '{:<5.2f}', 
			'suffix': '', 
			'no_labels': False, 
			'color': None, 
			'vertical': False, 
			'stacked': False, 
			'different_scale': False, 
			'calendar': True, 
			'start_dt': None, 
			'custom_tick': '', 
			'delim': '', 
			'verbose': False, 
			'version': False}

    data   = [[i] for i in dataF['Length'].tolist()]
    labels = (dataF['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))).tolist()
    args1 = args
    args1['start_dt'] = '2018-01-01'

    sys.stdout.write('\n')
    sys.stdout.write('########### GRAPHS\n')
    sys.stdout.write('\n')

    tgraph.calendar_heatmap(data, labels, args1)

    datay  = dataF[dataF.Year == 2018].groupby(['Month'])
    # print(datay.loc['Length'].sum())
    labels = []
    data   = []
    for key, item in datay:
    	# print(datay.get_group(key), "\n\n")
    	labels.append(month_name[key][:3])
    	data.append([datay.get_group(key)['Length'].sum()])

    sys.stdout.write('\n')
    sys.stdout.write('\n')

    tgraph.chart(None, data, args, labels)

    sys.stdout.write('\n')
    sys.stdout.write('########### TOTAL\n')
    sys.stdout.write('\n')

    ystats = yearStats(dataF)
    #(km_y, activities_y, km_t, day_and_km)
    print('Kilometrage    : %s'%ystats[0])
    print('Nombre sorties : %s'%ystats[1])
    sys.stdout.write('\n')
    return

def globalRun(runtype='test', user='Thomas'):
    data = load_data_parallel(user)
    results = filter_data(data)
    stats = yearStats(results)
    figs  = graphs(results)
    termgraphRun(results)
    return stats, figs, results

if __name__ == "__main__":
	globalRun()


 


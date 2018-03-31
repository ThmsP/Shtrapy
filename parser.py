import os
import time
from glob import glob
import gpxpy
from pandas import DataFrame

from uuid import uuid5
from uuid import NAMESPACE_DNS as npd

def timefunc(f):
    def f_timer(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print f.__name__, 'took', end - start, 'time'
        return result
    return f_timer

@timefunc
def load_run_data(gpx_path, filter=""):
    gpx_files = glob(os.path.join(gpx_path, filter + "*.gpx"))
    run_data = []
    for file_idx, gpx_file in enumerate(gpx_files): 
        gpx = gpxpy.parse(open(gpx_file, 'r'))
        uuid = uuid5(npd, str(gpx_file))
        # Loop through tracks
        for track_idx, track in enumerate(gpx.tracks):
            track_name = track.name
            track_time = track.get_time_bounds().start_time
            track_length = track.length_3d()
            track_duration = track.get_duration()
            track_speed = track.get_moving_data().max_speed
            
            for seg_idx, segment in enumerate(track.segments):
                segment_length = segment.length_3d()
                for point_idx, point in enumerate(segment.points):
                    run_data.append([uuid, os.path.basename(gpx_file), track_idx, track_name, 
                                     track_time, track_length, track_duration, track_speed, 
                                     seg_idx, segment_length, point.time, point.latitude, 
                                     point.longitude, point.elevation, segment.get_speed(point_idx)])
    return run_data


@timefunc
def filter_data(data):
	df = DataFrame(data, columns=['UUID', 'File_Name', 'Index', 'Name',
	                              'Time', 'Length', 'Duration', 'Max_Speed',
	                              'Segment_Index', 'Segment_Length', 'Point_Time', 'Point_Latitude',
	                              'Point_Longitude', 'Point_Elevation', 'Point_Speed'])

	# print df.head(10)
	# HTML(df.head().to_html(max_cols=4))
	cols = ['UUID', 'Time', 'Length', 'Duration', 'Max_Speed']
	tracks = df[cols].copy()
	tracks['Length'] /= 1e3
	tracks['Duration'] /= 3600
	tracks['Max_Speed'] *= 3.6
	tracks['Ave_Speed'] = tracks['Length'] / tracks['Duration']
	tracks.drop_duplicates(inplace=True)
	# print tracks.head()

	tracks['Year'] = tracks['Time'].apply(lambda x: x.year)
	tracks['Month'] = tracks['Time'].apply(lambda x: x.month)
	tracks_grouped = tracks.groupby(['Year','Month'])
	# print tracks_grouped.head()
	return tracks_grouped

data = load_run_data(gpx_path='./data/GPX/', filter="")
print filter_data(data).head


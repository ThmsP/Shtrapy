import datetime

import path
import gpxpy
import pandas
import pickle

# from path import Path as path

import tools
import config


class DataHandler():


    _gps_path    = config.get_gps_path() #TODO : not ok for multiple user
    _pickle_file = config.get_pickle()  #TODO : same 
    _data        = [] # will be a list
    _data_df     = None # will be a dataframe
    _uuid_stored = ''
    _fi_to_load  = []


    def __init__(self, gps_path=None, pickle_file=None):
        if gps_path :
            self._gps_path = path.Path(gps_path)
        if pickle_file : 
            self._pickle_file = path.Path(pickle_file)
        return 

    def process(self):
        self.rw_pickle('r')
        self.get_files()
        self._data += tools.genericParallel(self._fi_to_load, 
                                            self.load_data, 
                                            config.num_thread)
        self.rw_pickle('w')
        #After that _data will be remplaced by data_df
        self.convert_data()
        return


    def load_data(self, gpx_file, filter=""):
        """
        Load a gps file and return a list of informations
        """
        # gpx = None
        with open(gpx_file, 'r') as gpxf :
            gpx = gpxpy.parse(gpxf)
        uuid = tools.getUuid(gpx_file)
        # global uuid_to_file              #UNUSED
        # uuid_to_file[str(uuid)]=gpx_file #UNUSED

        # tracks_result = []

        # Loop through tracks
        # Check number of tracks by files
        # Most of them have only one
        if len(gpx.tracks) > 1:
            print('WARNING : more than one track in this file %s \n'%gpx_file)
            print('Only last track taken account\n')

        # TODO : to be improved
        for track_idx, track in enumerate(gpx.tracks):
            track_infos = []
            # print(trac)
            track_infos.append(uuid)
            track_infos.append(gpx_file)
            # track_infos.append(track_idx)
            track_infos.append(track.name)
            track_infos.append(track.get_time_bounds().start_time)
            track_infos.append(track.length_3d())
            track_infos.append(track.get_duration())
            track_infos.append(track.get_moving_data().max_speed)
            [track_infos.append(i) for i in track.get_uphill_downhill()]

            # tracks_result.append(track_infos)

        # print(tracks_result)
        return track_infos

    def convert_data(self):
        """
        Convert a list of data into a dataframe
        """
        self._data_df = pandas.DataFrame(self._data, 
                              columns=['UUID', 'File_Name', 'Name',
                                       'Date', 'Length', 'Duration', 'Max_Speed',
                                       'UpHill', 'DownHill'])

        # We no longer need _data : 
        self._data = None

        self._data_df['Length'] /= 1e3
        self._data_df['Duration'] /= 3600 
        self._data_df['Time'] = self._data_df['Duration'].apply(lambda x: datetime.timedelta(seconds=x*3600))
        self._data_df['Max_Speed'] *= 3.6
        self._data_df['Ave_Speed'] = self._data_df['Length'] / self._data_df['Duration']
        self._data_df.drop_duplicates(inplace=True)
        self._data_df['Year'] = self._data_df['Date'].apply(lambda x: x.year)
        self._data_df['Month'] = self._data_df['Date'].apply(lambda x: x.month)

        self._data_df = self._data_df.sort_values(by='Date', ascending = False)
        self._data_df = self._data_df.round(1)

        # print(tracks.head(5))

        return


    def get_data_df(self, cols=None):
        """
        Return the dataframe of the data filtered or not
        """
        if cols : 
            filtered_track = self._data_df[cols].copy()
        else : 
            filtered_track = self._data_df
   
        return filtered_track
    
    def rw_pickle(self, state, pickle_file=None):
        """
        Save the state of the gps file treated
        We write _data as a list not a dataframe
        """
        # logger.warning('Running rpickle ...')
        if not pickle_file : 
            pickle_file = self._pickle_file

        if state == 'r' : 
            # results = []
            if pickle_file.isfile() :
                with open(pickle_file, 'rb') as read_pickle:
                    self._data = pickle.load(read_pickle)
            # print results
            else : 
                print('No pickle file to load\n ')
        elif state == 'w' :
            with open(pickle_file, 'wb') as saved_pickle:
                pickle.dump(self._data, saved_pickle)
        else : 
            raise AttributeError('rw_pickle() : No state specified')
        return

    def get_files(self):
        """
        From a list of file, generate a list of list of informations
        """
        all_files = self._gps_path.files()
        # print(all_files)
        # global uuid_pickle
        # uuid_pickle = ''
        try :
            for track in self._data :
                self._uuid_stored+=str(track[0])
        except :
            print('No pickle file')
            pass
        self._fi_to_load = tools.genericParallel(all_files, 
                                                 self.filter_files, 
                                                 config.num_thread)
        return
    
    def filter_files(self, fi_to_test):
        """
        Compare uuid of a file with the one store in pickle
        """
        if str(tools.getUuid(fi_to_test)) not in self._uuid_stored:
            return fi_to_test
    
    

    def yearStats(self, year):
        """
        Return the basics stats of a year
        """
        km_y = self._data_df[self._data_df.Year == year]['Length'].sum()
        activities_y = len(self._data_df[self._data_df.Year == 2018])
        # data_grouped_year = data.groupby(['year'])
        # km_t = sum([datay['mvlenght'].sum() for year, datay in data_grouped_year])
        km_t = self._data_df['Length'].sum()
        data_y = self._data_df[self._data_df.Year == 2018]
        day_and_km = data_y[['Date', 'Length']].copy()
        return km_y, activities_y, km_t, day_and_km

if __name__ == "__main__":
    test = DataHandler()
    print(test.yearStats(2018))
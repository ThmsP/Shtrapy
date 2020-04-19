import path

user = 'Thomas'
gps_path = './data/GPX_%s'%user
# gpsfile_path = path('./data/GPX_%s'%user)
pickle_file  = '/data.pickle_%s'%user
num_thread   = 4

def get_gps_path():
	return path.Path(gps_path)

def get_pickle():
	return get_gps_path().parent+path.Path(pickle_file)

def get_nthread():
	return num_thread
import os
import pytest

import handler
import config


# Lancement des tests avec pytest : py.test .
# http://sametmax.com/un-gros-guide-bien-gras-sur-les-tests-unitaires-en-python-partie-3/

test_pickle_file = './tests/pickle_test'
test_data_path   = './tests/data'


# Cette méthode pourra être appelée avant chaque test.
@pytest.fixture()
def create_DataHandler():
    return handler.DataHandler(test_data_path, test_pickle_file)

def clean_pickle():
    if os.path.exists(test_pickle_file):
        os.remove(test_pickle_file)
    else:
        print("No pickle file to delete\n") 

# Chaque méthode dont le nom commence par 'test_'
# est un test.
def test_isDataHandler(create_DataHandler):
    assert isinstance(create_DataHandler,handler.DataHandler) 

def test_pickle_noargs(create_DataHandler):
    with pytest.raises(AttributeError):
        create_DataHandler.rw_pickle('a') 

def test_read_nopickle(create_DataHandler):
    clean_pickle()
    assert not create_DataHandler._data

def test_get_files(create_DataHandler):
    clean_pickle()
    create_DataHandler.get_files()
    #No pickle file, len(_fi_to_load) should be 4
    assert len(create_DataHandler._fi_to_load) == 4

def test_load_data(create_DataHandler):
    clean_pickle()
    create_DataHandler.get_files()
    data = []
    for fi in create_DataHandler._fi_to_load:
        data += create_DataHandler.load_data(fi)
    # print(data)
    assert len(set(data)) == len(data)




# def test_pickle_no_args(self):
    # self._data.rw_pickle()

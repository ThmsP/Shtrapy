import unittest
 
# Le code à tester doit être importable. On
# verra dans une autre partie comment organiser
# son projet pour cela.
# from ..handler import get
import handler

# Cette classe est un groupe de tests. Son nom DOIT commencer
# par 'Test' et la classe DOIT hériter de unittest.TestCase.
class TestDataHandler(unittest.TestCase):

    # Cette méthode sera appelée avant chaque test.
    def setUp(self):
        self._data = handler.DataHandler('./tests/data', './tests/pickle_test')
 
    # Cette méthode sera appelée après chaque test.
    def tearDown(self):
        print('Nettoyage !')

 
    # Chaque méthode dont le nom commence par 'test_'
    # est un test.
    def test_isDataHandler(self):        
        self.assertIsInstance(self._data, handler.DataHandler)

    # def test_pickle_no_args(self):
        # self._data.rw_pickle()


if __name__ == '__main__':
    unittest.main()
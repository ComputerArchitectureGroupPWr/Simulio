from unittest import TestCase
from src.main.fpgavisio import SimulationData

__author__ = 'pawel'


class TestSimulationData(TestCase):

    def setUp(self):
        self.simdata = SimulationData()
        self.simdata.load_dataset('../data/data.csv')

    def test_load_dataset(self):
        pass

    def test_get_thermometer(self):
        self.assertEqual(self.simdata.dataset['term13'], self.simdata.get_thermometer(11))

    def test_get_time_array(self):
        pass
        #self.assertEqual(self.simdata.dataset['time'], self.test_get_time_array())

    def test_get_thermometers_from_times_stamp(self):
        readings = self.simdata.get_thermometers_from_times_stamp(1, 1, 10)
        self.assertEqual(9, len(readings))
        print readings


    def test_convert_time_to_integer_vector(self):
        self.simdata.convert_time_to_integer_vector()
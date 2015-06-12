from unittest import TestCase
from src.main.parser import Parser

__author__ = 'pawel'


class TestParser(TestCase):

    def setUp(self):
        self.parser = Parser("../data/program.xml")

    def test_handleSimulationshow(self):
        pass

    def test_handleAllHeaters(self):
        pass

    def test_getHeaterName(self):
        self.assertEquals(self.parser.getHeaterName(0), "heater1")

    def test_handleConfigurations(self):
        pass

    def test_getHeater(self):
        pass

    def test_getHeaters(self):
        pass

    def test_handleConfHeaters(self):
        pass

    def test_fields_configuration(self):
        self.assertEquals(self.parser.stoptime, 21)
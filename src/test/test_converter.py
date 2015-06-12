__author__ = 'pawel'

from unittest import TestCase
from src.main.converter import *

class TestConverter(TestCase):

    def test_oscToTempConverter(self):
        oscToTempConverter('../data/data.csv', '../data/calibration.csv', '../data/final2.csv')

    def test_getCalibrationCoefficients(self):
        coefficents = []

        with open('../data/calibration.csv') as calibration_data:
            coefficents = getCalibrationCoefficients(calibration_data)

        self.assertEqual(float('-2.5643e-06'), coefficents[0][0])
        self.assertEqual(float('0.20699'), coefficents[0][1])
        self.assertEqual(float('-4028.4'), coefficents[0][2])

        for line in coefficents:
            print line
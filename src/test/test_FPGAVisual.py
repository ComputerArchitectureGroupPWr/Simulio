from unittest import TestCase
from src.main.fpgavisio import FPGAVisual

__author__ = 'pawel'


class TestFPGAVisual(TestCase):
    def test_make_simulation_movie(self):
        visualisation = FPGAVisual('../data/final.csv')
        visualisation.make_simulation_movie('../data/content.gif')

    def test_make_simulation_movie_frame(self):
        visualisation = FPGAVisual('../data/final2.csv')
        visualisation.make_simulation_movie_frame(1,'../data/lol_content.gif',(35,45))
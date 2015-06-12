import csv
from pylab import *
import os
import shutil
import subprocess

__author__ = 'pawel'


class FPGAVisual(object):
    """
    The FPGAVisual instance provides functionality needed to visualize the results
    collected by Simulio from FPGA.
    """
    # Dataset file or path
    datafile = ''
    # Thermometers grid description
    termgrid = (11, 11)

    def __init__(self, datafile, **kwargs):
        """
        :param datafile: data file name string
        :param kwargs: optional arguments describes dataset, the defaul values are:

            * termgrid * : (11,11)
                (row, column) tuple describes the shape of thermometers net
        """
        # Dataset object
        self.dataset = SimulationData()

        self.datafile = datafile
        self.dataset.load_dataset(datafile)

        if 'termgrid' in kwargs:
            self.termgrid = kwargs.pop('termgrid')

    def make_simulation_movie(self, filepath, **kwargs):
        """
        Method producing the movie from simulation

        :param filepath: path where file should be created
        :param kwargs: optional arguments describes movie properties, the default
         values are:

            * sampling * : 60
                sampling (int) describes the time intervals for following frame (value in seconds)

            * range * : (simulationstart, simulationend)
                range (tuple) describes the moment when movie starts and ends (values in second)

            * oscillations * : False
                boolean describes if the map is in number of oscillations or Celsius degrees
        """
        tempdir = filepath[:filepath.rfind('/')]+"/temp"
        os.mkdir(tempdir)

        sampling = kwargs['sampling'] if kwargs['sampling'] else sampling = 60
        oscillations = True if kwargs['oscillations'] else oscillations = False

        if 'range' not in kwargs:
            simtime = self.dataset.get_simulation_time()

            for i, timestamp in enumerate(range(0, simtime, sampling)):
                self.make_simulation_movie_frame(timestamp, filepath, (35, 90), i)

        cmd = ['ffmpeg', '-f', 'image2', '-r', '4', '-i', tempdir+'/frame%04d.png', '-vcodec',
               'mpeg4', '-y', filepath[:filepath.rfind('/')]+'/animation.mp4']

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        process.wait()
        for line in process.stdout:
            print line

        shutil.rmtree(tempdir)

    def make_simulation_movie_frame(self, timestamp, filepath, legendrange, i):
        """
        Method producing the frames for simulation movie

        :param timestamp: time stamp for which the frame is creating
        :param filepath describes the path for final file
        :param legendrange: tuple with the range of temperatures
        :return a frame in png format inside temp folder
        """

        for row in range(1, self.termgrid[1]+1):
            if row == 1:
                datarow = self.dataset.get_thermometers_from_times_stamp(timestamp, row*self.termgrid[0],
                                                                          row*self.termgrid[0]+self.termgrid[0])
                framearray = array([datarow])
            else:
                datarow = array(self.dataset.get_thermometers_from_times_stamp(timestamp, (row-1)*self.termgrid[0],
                                                                                (row-1)*self.termgrid[0]+self.termgrid[0]))
                framearray = concatenate((framearray, [datarow]), axis=0)

        framearray = framearray.T

        fig, ax = plt.subplots()
        norm = mpl.colors.normalize(vmin=legendrange[0], vmax=legendrange[1])
        p = ax.pcolor(framearray, norm=norm)
        cb = fig.colorbar(p, ax=ax)
        fig.gca().invert_yaxis()
        fig.gca().set_xlim([0, 11])
        fig.gca().set_ylim([0, 11])
        fig.gca().set_title("Time: %d sec." % timestamp)
        index = ''
        if i/1000. >= 0.1:
            index = '0'
        elif i/1000. >= 0.01:
            index = '00'
        else:
            index = '000'
        fig.savefig("".join([filepath[:filepath.rfind('/')], "/temp/", "frame{}{}".format(index, i)]))


class SimulationData(object):

    """
    The SimulationData instance 
    """
    # Dictionary with whole dataset
    dataset = {}
    # Information about thermometers number


    def __init__(self, datafile=None):
        """
        :param datafile: data file path (str)
        """
        if datafile is not None:
            self.load_dataset(datafile)

    def load_dataset(self, datafile):
        """
        Load simulio dataset file and save the data
        """
        headers = []

        with open(datafile,'r') as filedataset:
            csvdataset = csv.reader(filedataset, skipinitialspace=True)

            headers = csvdataset.next()

            for head in headers:
                self.dataset[head] = []

            for row in csvdataset:
                for data in zip(headers, row):
                    self.dataset[data[0]].append(data[1])

    def get_thermometer(self, number):
        """
        Returns thermometer readings values array

        :param number: positional number of desired thermometer
        :return: readings value
        """
        return self.dataset['term%d' % (number+2)]

    def get_time_array(self):
        """
        Returns simulation time vector

        :return: list with time stamps
        """
        return self.dataset['time']

    def get_thermometers_from_times_stamp(self, timestamp, startterm, stopterm):
        """
        Returns list with readings from particular time stamp

        :param timestamp: integer in seconds
        :return: list with readings from all thermometers for particular
        time stamp
        """
        if "time int" not in self.dataset:
            self.convert_time_to_integer_vector()
        timestampindex = self.dataset['time int'].index(timestamp)

        thermometersrow = []

        for term in range(startterm, stopterm):
            thermometersrow.append(self.dataset['term%d' % (term+3)][timestampindex])

        return thermometersrow

    def convert_time_to_integer_vector(self):
        """
        Convert time float stamps list to integer time stamps list for
        easier searching.

        :return: list of integer time stamps
        """
        self.dataset['time int'] = []
        for time_stamp in self.dataset['time']:
            self.dataset['time int'].append(int(float(time_stamp)))

    def get_simulation_time(self):
        if "time int" not in self.dataset:
            self.convert_time_to_integer_vector()
        return self.dataset['time int'][-1]

    def calculate_oscillations_delta(self):
        """
        Convert the thermometers oscillation vectors in absolute values into
        delta of oscillations

        :return: Updates dataset entries with oscillations
        """
        pass


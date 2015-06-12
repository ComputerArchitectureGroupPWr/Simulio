import xml.dom.minidom
import re

colors = {'n': ';38m', 'g': ';32m', 'r': ';31m', 'b': ';34m', 'y': ';33m', 'c': ';0m'}
style = {'normal': '\033[0', 'bold': '\033[1'}
formats = dict(colors.items() + style.items())

class Parser:
    def __init__(self, filename):
        self.f = xml.dom.minidom.parse(filename)
        self.output = self.f.getElementsByTagName("output")[0].getAttribute("name")
        if self.f.getElementsByTagName("program")[0].getAttribute("version") == '0.2':
            self.stoptime = self.f.getElementsByTagName("settings")[0].getAttribute("duration")
            if re.search('s', self.stoptime):
                self.stoptime = int(re.findall('\d+', self.stoptime)[0])
            elif re.search('min', self.stoptime):
                self.stoptime = int(re.findall('\d+', self.stoptime)[0])*60
            elif re.search('h', self.stoptime):
                self.stoptime = int(re.findall('\d+', self.stoptime)[0])*3600
            elif re.search('ms', self.stoptime):
                self.stoptime = int(re.findall('\d+', self.stoptime)[0])/1000.0
        else:
            self.stoptime = 1e+10

        self.gz = []
        self.handleSimulationshow()

    def handleSimulationshow(self):
        heaters = self.f.getElementsByTagName("heater")
        self.handleAllHeaters(heaters)

    def handleAllHeaters(self, heaters):
        print "{bold}{y}User emulation program:{normal}{n}".format(**formats)
        self.name_list = []
        for heater in heaters:
            name = heater.getAttribute("name")
            print ("\n{bold}{r}Heater name{normal}{n}: %s\n"%name).format(**formats)
            self.name_list.append(name)

            configurations = heater.getElementsByTagName("conf");
            self.handleConfigurations(configurations)

    def getHeaterName(self,number):
        return self.name_list[number]

    def handleConfigurations(self, confs):
        list = []
        for conf in confs:
            #Parsowanie mocy
            power = conf.getAttribute("power")

            #Parsowanie czasow
            time = conf.getAttribute("time")
            if re.search('min', time):
                list.append([round(float(re.findall('\d+', power)[0]) * 2.55, 0),
                             int(re.findall('\d+', time)[0]) * 60])
            elif re.search('h', time):
                list.append([round(float(re.findall('\d+', power)[0]) * 2.55, 0),
                             int(re.findall('\d+', time)[0]) * 3600])
            elif re.search('s', time):
                list.append([round(float(re.findall('\d+', power)[0]) * 2.55, 0),
                             int(re.findall('\d+', time)[0])])
            print ("{bold}{y}Power{normal}{n}: %s {bold}{y}Time{normal}{n}: %s"%(power, time)).format(**formats)
        self.gz.append(list)

    def getHeater(self, id):
        grzalki = []
        grzalki.extend(self.gz[id])
        out = []

        for x in grzalki:
            out.append([chr(int(x[0])), x[1]])

        return out

    def getHeaters(self):
        temp = []
        for i in range(len(self.gz)):
            g = self.getHeater(i)
            temp.extend([[chr(i + 1), a, b] for a, b in g])
        return sorted(temp, key=lambda temp: temp[2])


    def handleConfHeaters(self, conf):
        print "Power %s " % conf.getAttribute("power")

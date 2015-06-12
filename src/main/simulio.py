import serial
import time
from multiprocessing import Process, Queue
import argparse

from parser import Parser
#from graphs import defaultPlot


colors = {'n': ';38m', 'g': ';32m', 'r': ';31m', 'b': ';34m', 'y': ';33m', 'c': ';0m'}
style = {'normal': '\033[0', 'bold': '\033[1'}
formats = dict(colors.items() + style.items())

def rs232(t, h, portcom, parser):
    try:
        ser = serial.Serial(portcom)
    except serial.SerialException as e:
        print ("\n{bold}{r}Error!!! Something goes wrong ;-({normal}{n}: %s"%e).format(**formats)
        controlQ.put("True")
        return 0
    zero = time.time()
    ser.baudrate = 115200
    ser.timeout = 5
    print "\n{bold}{y}Current operations:{normal}{n}\n".format(**formats)
    while True:
        moment = time.time() - zero
        if not h.empty():
            command = h.get()
            print ("{bold}{g}%8.2f{normal}{n}: {bold}{r}Heater{normal}{n}: %s, {bold}{y}Power{normal}{n}:%3d%%"%\
                  (moment,parser.getHeaterName(ord(command[1])-1),float(ord(command[2]))/2.55)).format(**formats)
            for c in command:
                ser.write(c)
        try:
            t.put(ord(ser.read()))
        except:
            print "\n{bold}{r}Error!!! Something goes wrong ;-({normal}{n}: " \
                  "SuimulationCore not responding".format(**formats)
            controlQ.put("True")
            return 0

def createFile(filename):
    f = open(filename, 'w+')
    text = "time, "
    for i in range(1,127):
        if i == 1:
            text += "SM temperature, "
        elif i == 2:
            text += "SM core voltage, "
        else:
            text += "term%d, " % i
    f.write(text[:-1] + '\n')
    f.close()

def savetofile(filename, data, zero):
    f = open(filename, 'a')
    text = "%.2f," % (time.time() - zero,)
    for i in range(len(data) / 3):
        reading = data[3 * i + 1] * 2 ** 8 + data[3 * i + 2]
        if i == 0:
            text += " %.2f," % (((float(reading)*503.975)/1024)-273.15)
        elif i == 1:
            text += " %.2f," % ((float(reading)/1024.)*3.)
        else:
            text += " %d," % reading
    f.write(text[:-1] + '\n')
    #print text
    f.close()

def thermRead(t, filename):
    zero = time.time()
    dataIn = []
    i = 0
    n = 1
    while True:
        while i >= len(dataIn):
            dataIn.append(t.get())
        if dataIn[i] != n:
            del dataIn[0]
            i = 0
            n = 1
            continue
        if n == 126:
            dataIn.append(t.get())
            dataIn.append(t.get())
            savetofile(filename, dataIn, zero)
            del dataIn[:]
            i = 0
            n = 1
            continue
        n += 1
        i += 3

def heatControl(h, program):
    #prog = ['\x00','\x0d','\x1a','\x26','\x33','\x40','\x4d','\x59','\x66','\x73','\x80','\x00']
    zero = time.time()
    #print program
    i= 0
    for p in program:
        t = time.time() - zero
        if t < p[2]:
            time.sleep(p[2] - t)
        h.put((chr(0x55), p[0], p[1]))
        i+=1
    exit(0)

if __name__ == '__main__':
    time.clock()
    parser = argparse.ArgumentParser(
        description="{bold}{y}Simulio - tool controling the thermal emulation on FPGA and"
                    "collecting data from MeasurementCore{normal}{n}".format(**formats),
        prog='simulio',
        epilog='{bold}{g}PROJECT THERMAL 2013 - all rights reserved{normal}{n}'.format(**formats))

    parser.add_argument('-p', '--port', dest='portcom', action='store',
                        type=str, nargs=1, help="Select the serial port", required=True)
    parser.add_argument('-c', '--control_file', dest='control_xml', action='store',
                        type=str, nargs=1, help="Select the emulation program xml file",
                        required=True)
    parser.add_argument('--version', action='version', version='%(prog)s 1.0-stable')

    args = parser.parse_args()

    thermQ = Queue()
    heatQ = Queue()
    controlQ = Queue()
    parser = Parser(args.control_xml[0])
    createFile(parser.output)

    rs = Process(target=rs232, args=(thermQ, heatQ, args.portcom[0],parser))
    t = Process(target=thermRead, args=(thermQ, parser.output))
    h = Process(target=heatControl, args=(heatQ, parser.getHeaters()))

    rs.start()
    t.start()
    h.start()

    zero = time.time()

    while True:
        if parser.stoptime < time.time()-zero:
            print "Emulation duration time elapsed! Stop..."
            rs.terminate()
            t.terminate()
            h.terminate()
            break
        if not controlQ.empty():
            rs.terminate()
            t.terminate()
            h.terminate()
            break


    #defaultPlot(parser.output)

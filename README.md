# Simulio
Tool which establish connection with FPGA and supervise the emulation process.

REQUIREMENTS
------------

Simulio is tool written in python2 and it also requires additional 
[pySerial](http://pyserial.sourceforge.net/) library.

INSTALLATION
------------

To install Simulio just type:

  $ sudo python setup.py install
  
After installation is done reload your shell e.g.:

  $ bash
  
An try if Simulio works:

  $ simulio --version
  
USAGE
-----
  
usage: simulio [-h] -p PORTCOM -c CONTROL_XML [--version]

#### Optional arguments:
  * *-h*, *--help* - show this help message and exit
  * *-p* *PORTCOM*, *--port* *PORTCOM* - Select the serial port
  * *-c* *CONTROL_XML*, *--control_file* *CONTROL_XML* - Select 
  the emulation program xml file
  * *--version* - show program's version number and exit

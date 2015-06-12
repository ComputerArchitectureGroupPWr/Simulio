from distutils.core import setup, Extension

def installation():
	setup(
		name = "Simulio",
		version = "1.0",
		author = "Maciej Zagrabski & Pawel Weber",
		author_email = "maciej.zagrabski@ymail.com or pawelweber@yahoo.pl",
		description = "tool controling the thermal emulation on FPGA and' \
					  ' collecting data from MeasurementCore",
		platforms = ["Linux"],
		packages=['Simulio'],
		package_dir = {'Simulio': 'src/main'},
		scripts=['scripts/simulio'],
	)
	print "Everything done"

if __name__ == "__main__":
	installation()


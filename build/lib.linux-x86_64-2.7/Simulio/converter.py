__author__ = 'pawel'

import re
import csv

def oscToTempConverter(raw_results, calibrations, final_results):

    with open(raw_results, 'r') as raw_results_data, open(calibrations) as calibration_data,\
        open(final_results, 'w+') as final_results_data:

        coeffs = getCalibrationCoefficients(calibration_data)

        raw_reader = csv.reader(raw_results_data)

        final_writer = csv.writer(final_results_data, delimiter=',')

        base_temp = 1

        for i, line in enumerate(raw_reader):
            if i == 0:
                final_writer.writerow(line)
            else:
                if i == 1:
                    base_temp = line[1]
                row = []
                row.extend(line[:3])
                for term in range(3, len(coeffs)+3):
                    x = int(line[term])
                    temp_coeffs = coeffs[term-3]

                    if i == 1:
                        uncalibrated_temp = float(x * x * temp_coeffs[0] + x * temp_coeffs[1] + temp_coeffs[2])
                        temp_correction = uncalibrated_temp - float(base_temp)
                        temp_coeffs[2] -= temp_correction

                    row.append(' {:.2f}'.format(x * x * temp_coeffs[0] + x * temp_coeffs[1] + temp_coeffs[2]))
                final_writer.writerow(row)

def getCalibrationCoefficients(data):
    coefficients = []
    pattern = re.compile(r'([-]\d).(\d*)e-(\d*),0.(\d*),([-]\d*)?\W?(\d*)')

    for term in data:
        raw_coeff = pattern.match(term).groups()
        a_coeff = (float(raw_coeff[0])-float(raw_coeff[1])*pow(10, -len(raw_coeff[1])))*pow(10, -int(raw_coeff[2]))
        b_coeff = float(raw_coeff[3])*pow(10,-len(raw_coeff[3]))
        try:
            c_coeff = float(raw_coeff[4])-float(raw_coeff[5])*pow(10, -len(raw_coeff[5]))
        except ValueError:
            c_coeff = float(raw_coeff[4])

        coefficients.append([a_coeff, b_coeff, c_coeff])

    return coefficients


from os import listdir
from os.path import isfile, isdir, join
import sys
import numpy as np
import matplotlib.pyplot as plt

headless = False


def convert_text2csv(text):
    return [list(map(float, l.split(","))) for l in text]


def convert_csv2text(csv):
    return '\n'.join([','.join([str(n) for n in line]) for line in csv])


def read_csv(f):
    with open(f, 'r') as f:
        return convert_text2csv(f.read().strip().split("\n"))


def print_csv(csv, blank_lines=1):
    print(convert_csv2text(csv) + "\n" * blank_lines)


def average(path):
    """
    Scans for all csv files in a folder and creates an average csv file for these.
    To get the same number of lines, all files are cropped from the end to the same number of lines
    """

    csv_files = [f for f in listdir(path) if f.endswith('.csv') and isfile(join(path, f))]
    csvs = []
    for csv in csv_files:
        csvs.append(read_csv(join(path, csv)))

    min_lines = min(map(len, csvs))
    csvs = [csv[-min_lines:] for csv in csvs]  # crop from end so all files are same number of lines
    avg_csv = []
    for line in range(min_lines):
        lines_at_line = [csv[line] for csv in csvs]
        time = np.mean([line[0] for line in lines_at_line])
        x = np.mean([line[1] for line in lines_at_line])
        y = np.mean([line[2] for line in lines_at_line])
        avg_csv.append([time, x, y])

    print_csv(avg_csv)


def down_scale(num, avg):
    """
    This function tries to scale down the numeric big csv to match the average one so that they can be compared line by line.
    Returns a list of numpy arrays
    """
    newnum = []
    for line in avg:
        time = line[0]
        first_closest = num[0]
        second_closest = num[1]
        for nline in num:
            second_closest = nline
            if nline[0] > time:
                break
            first_closest = nline

        tdiff = abs(first_closest[0] - second_closest[0])
        if tdiff == 0:
            print('tdiff == 0!!')
            print(f'target: {time}, fc: {first_closest}, sc: {second_closest}')
            print()
        progress = (time - first_closest[0]) / tdiff  # first ratio
        first_closest = np.array(first_closest)
        second_closest = np.array(second_closest)
        arrdiff = second_closest - first_closest
        combined = first_closest + arrdiff * progress
        newnum.append(combined)
    return newnum


def compare(num, avg):
    """
    Compares two csv files, one big numeric one and one small average one.
    """
    num = read_csv(num)
    avg = read_csv(avg)
    avg = [np.array(line) for line in avg]

    num = down_scale(num, avg)

    diff = []
    for l1, l2 in zip(num, avg):
        diff.append(l1 - l2)

    print_csv(diff)

    if not headless:
        time = [line[0] for line in avg]
        x_pos_num = [line[1] for line in num]
        x_pos_avg = [line[1] for line in avg]
        x_pos_diff = [line[1] for line in diff]

        fig('Differanse i horisontal posisjon mellom numerisk og målt resultat', 'x', 'm', 't', 's')

        # list of colors:
        # https://matplotlib.org/3.1.0/gallery/color/named_colors.html

        plt.plot(time, x_pos_num, color="blue", label="Numerisk posisjon")
        plt.plot(time, x_pos_avg, color="green", label="Gjennomsnitt målt position")
        plt.plot(time, x_pos_diff, color="orangered", label="Differanse")
        plt.legend()
        plt.fill_between(time, x_pos_diff, [0] * len(time), color="lightcoral")
        plt.show()

        fig('Kun differanse i horisontal posisjon mellom numerisk og målt resultat', 'x', 'm', 't', 's')
        plt.plot(time, x_pos_diff, color="orangered", label="Differanse")
        plt.legend()
        plt.fill_between(time, x_pos_diff, [0] * len(time), color="lightcoral")
        plt.show()


def fig(title, y, y_unit, x='x', x_unit='m'):
    plt.figure(title, figsize=(12, 6))
    plt.title(title)
    plt.xlabel(f"${x}$ [{x_unit}]", fontsize=20)
    plt.ylabel(f"${y}$ [{y_unit}]", fontsize=20)
    plt.grid()


if len(sys.argv) < 2 or len(sys.argv) > 4:
    print('usage:')
    print("\t", sys.argv[0], "<folder/with/csv/files> - create and average csv file")
    print("\t", sys.argv[0], "<numeric-big> <avg-small> - compare two csv files")

elif len(sys.argv) == 2:
    folder = sys.argv[1]
    if isdir(folder):
        average(folder)
    else:
        print(f"'{folder} is not a folder or does not exist.")
        exit(1)

else:
    num = sys.argv[1]
    avg = sys.argv[2]
    if not isfile(num):
        print(f"'{num} is not a file or does not exist.")
        exit(2)
    if not isfile(avg):
        print(f"'{avg} is not a file or does not exist.")
        exit(3)
    compare(num, avg)

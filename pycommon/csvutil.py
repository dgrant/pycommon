import csv
import os

def write_csv_file(filename, rows, header=None):
    """
    Write a list of rows to a CSV file.

    :param filename: pathname of CSV file to write to
    :param rows: a list of rows, each row contains a list of values, each value going in to one column
    :param header: an optional list of column names to go in the header of the CSV file
    :return: nothing
    """

    with open(filename, 'wt') as handle:
        writer = csv.writer(handle, delimiter=',', lineterminator=os.linesep)
        print(type(writer))
        if header is not None:
            writer.writerow(header)
        for row in rows:
            writer.writerow(row)

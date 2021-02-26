"""
    great
"""
from datetime import timedelta
from datetime import datetime


def data_processing(data):
    tugs_data = list()
    print(data)
    print(len(data))
    for line in data:
        # calculate coming dates
        # fumigation once every three months
        # disinfection once every one month
        date_fumigation = datetime.strptime(line[2], "%d/%m/%Y").date() + timedelta(weeks=4 * 3)
        date_disinfection = datetime.strptime(line[3], "%d/%m/%Y").date() + timedelta(weeks=4)

        # create tugs data
        tugs_data.append(tuple(line[0:3] + [date_fumigation, 'Fumigation']))
        tugs_data.append(tuple(line[0:2] + [line[3]] + [date_disinfection, 'Disinfection']))

        # sorted by index[3] of tugs_data, index[3] = (date_fumigation and date_disinfection)
        tugs_data_sorted = sorted(tugs_data, key=lambda item: item[3])

    return tugs_data_sorted

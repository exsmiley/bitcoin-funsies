import csv
import tqdm
import os
dir = os.path.dirname(__file__)

def remove_irrelevant_rows():
    with open(os.path.join(dir, '../btcusd.csv')) as f:
        reader = csv.DictReader(f, delimiter=',')
        with open(os.path.join(dir, '../btcusd2.csv'), 'w') as f2:
            fieldnames = ['Low', 'High', 'Open', 'Close', 'Volume_(BTC)']
            writer = csv.DictWriter(f2, fieldnames=fieldnames)
            writer.writeheader()
            fieldnames = set(fieldnames)
            for row in tqdm.tqdm(reader):
                row = {k: v for k, v in row.iteritems() if k in fieldnames}
                writer.writerow(row)

def only2017():
    epoch = 1483228800
    with open(os.path.join(dir, '../btcusd.csv')) as f:
        reader = csv.DictReader(f, delimiter=',')
        with open(os.path.join(dir, '../only2017.csv'), 'w') as f2:
            fieldnames = ['Close']
            writer = csv.DictWriter(f2, fieldnames=fieldnames)
            # writer.writeheader()
            fieldnames = set(fieldnames)
            for row in tqdm.tqdm(reader):
                if int(row['Timestamp']) > epoch:
                    row2 = {k: v for k, v in row.iteritems() if k in fieldnames}
                    writer.writerow(row2)

def normalize():
    price_max = 6000
    vol_max = 2000
    with open(os.path.join(dir, '../btcusd2.csv')) as f:
        reader = csv.DictReader(f, delimiter=',')
        with open(os.path.join(dir, '../norm.csv'), 'w') as f2:
            fieldnames = ['Low', 'High', 'Open', 'Close', 'Volume']
            writer = csv.DictWriter(f2, fieldnames=fieldnames)
            writer.writeheader()

            for row in tqdm.tqdm(reader):
                new_row = {}
                for field in fieldnames[:-1]:
                    val = float(row[field])
                    new_row[field] = (val-price_max/2.)/(price_max/2.)
                vol = float(row['Volume_(BTC)'])
                new_row['Volume'] = (vol-vol_max/2.)/(vol_max/2.)
                writer.writerow(new_row)


def load_data():
    '''Can fit into RAM since just like 125MB'''
    data = []
    print 'Loading Historical Data...'
    with open(os.path.join(dir, '../norm.csv')) as f:
        reader = csv.reader(f)
        reader.next()  # read out the headers...

        for row in tqdm.tqdm(reader):
            data.append(map(float, row))

    print 'Finished Loading Data!'
    return data

def only_close():
    '''Can fit into RAM since just like 125MB'''
    data = []
    print 'Loading Historical Data...'
    with open(os.path.join(dir, '../norm.csv')) as f:
        reader = csv.reader(f)
        reader.next()  # read out the headers...

        for row in tqdm.tqdm(reader):
            data.append(float(row[3]))

    print 'Finished Loading Data!'
    return data

def load_2017():
    '''Can fit into RAM since much less than like 125MB'''
    data = []
    print 'Loading Historical Data...'
    with open(os.path.join(dir, '../only2017.csv')) as f:
        reader = csv.reader(f)

        for row in tqdm.tqdm(reader):
            data.append(float(row[0]))

    print 'Finished Loading Data!'
    return data

def daily():
    with open(os.path.join(dir, '../dailydata.csv')) as f:
        reader = csv.DictReader(f, delimiter=',')
        with open(os.path.join(dir, '../daily2.csv'), 'w') as f2:
            fieldnames = ['Price', 'Open', 'High', 'Low']
            writer = csv.DictWriter(f2, fieldnames=fieldnames)
            writer.writeheader()
            data = []
            fieldnames = set(fieldnames)
            for row in tqdm.tqdm(reader):
                try:
                    row2 = {k: float(v.replace(',', '')) for k, v in row.iteritems() if k in fieldnames}
                    data.append(row2)
                except:
                    pass
            for row in data[::-1]:
                writer.writerow(row)
                # if int(row['Timestamp']) > epoch:
                #     row2 = {k: v for k, v in row.iteritems() if k in fieldnames}
                #     writer.writerow(row2)

def load_daily():
    '''Can fit into RAM since much less than like 125MB'''
    data = []
    print 'Loading Historical Data...'
    with open(os.path.join(dir, '../daily2.csv')) as f:
        reader = csv.reader(f)
        reader.next()

        for row in tqdm.tqdm(reader):
            row = map(float, row)
            data.append(row)

    print 'Finished Loading Data!'
    return data

if __name__ == '__main__':
    # print len(load_2017())
    daily()

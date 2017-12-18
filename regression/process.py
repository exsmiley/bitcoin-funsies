import csv
import tqdm

def remove_irrelevant_rows():
    with open('../btcusd.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        with open('../btcusd2.csv', 'w') as f2:
            fieldnames = ['Low', 'High', 'Open', 'Close', 'Volume_(BTC)']
            writer = csv.DictWriter(f2, fieldnames=fieldnames)
            writer.writeheader()
            fieldnames = set(fieldnames)
            for row in tqdm.tqdm(reader):
                row = {k: v for k, v in row.iteritems() if k in fieldnames}
                writer.writerow(row)

def normalize():
    price_max = 6000
    vol_max = 2000
    with open('../btcusd2.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        with open('../norm.csv', 'w') as f2:
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
    with open('../norm.csv') as f:
        reader = csv.reader(f)
        reader.next()  # read out the headers...

        for row in tqdm.tqdm(reader):
            data.append(map(float, row))

    print 'Finished Loading Data!'

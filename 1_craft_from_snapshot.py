from config import *
from pprint import pprint as pp

chunk = {}

for (title, fname, score) in CONFIG_COL:

    # get file path
    src_path = '{}/{}'.format(DIR_SNAPSHOT, fname)

    # read file line by line
    for line in open(src_path, 'r'):
        (addr, qty) = line.strip().split(',')

        # add score to wallet
        wallet = chunk.get(addr)
        if wallet is None:
            chunk[addr] = {}
        chunk[addr][title] = score

pp(chunk)

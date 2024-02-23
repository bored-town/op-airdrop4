from config import *
from common import *
from pprint import pprint as pp
import os, time, math
from web3.utils.address import to_checksum_address

chunk = {}

# 1) load snapshot data
for (title, fname, score) in CONFIG_COL:
    # read file line by line
    src_path = '{}/{}'.format(DIR_SNAPSHOT, fname)
    for line in open(src_path, 'r'):
        (addr, qty) = line.strip().split(',')
        addr = addr.lower() # [!] use address in lowercase format
                            # [!] prevent sensitive address issue
        # add score to wallet
        info = chunk.get(addr)
        if info is None:
            chunk[addr] = {}
        chunk[addr][title] = score

# 2) recheck duplicate address
dup_addrs = find_duplicates_ignore_case(chunk.keys())
if len(dup_addrs) > 0:
    print(dup_addrs)
    print('found {} duplicated addresses'.format(len(dup_addrs)))
    exit()

# 3) remove ban list
for addr in BAN_WALLETS:
    del chunk[addr.lower()]

# 4) sum points
total_points = 0
for (addr, info) in chunk.items():
    info['points'] = sum(info.values())
    total_points += info['points']

# 5) before reshape
for (addr, info) in chunk.items():
    # add checksum address
    info['addr'] = to_checksum_address(addr)
    # calc OP
    info['op'] = REWARD_OP * (info['points'] / total_points)

# 6) reshape chunk to list of dict
chunk = chunk.values()

# 7) sort by points, address
chunk = sorted(chunk, key=lambda x: (-x['points'], x['addr']))

# 8) add no
cur_no = None
cur_points = None
for (idx, info) in enumerate(chunk):
    if info['points'] != cur_points:
        cur_no = idx + 1
        cur_points = info['points']
    info['no'] = cur_no

# 9) print output (header)
fields = ','.join([ title for (title, _, _) in CONFIG_COL ])
print("no,address,OP,points,{}".format(fields))

# 10) print output (body)
for c in chunk:
    op     = math.floor(c['op'] * 1_000) / 1_000 # floor 3 digits
    fields = ','.join([ str(c.get(title) or 0) for (title, _, _) in CONFIG_COL ])
    print('{},{},{},{},{}'.format(
        c['no'],        # no
        c['addr'],      # addr
        op,             # OP reward
        c['points'],    # points
        fields,         # collection points
    ))

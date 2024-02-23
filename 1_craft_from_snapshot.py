from config import *
from common import *
from pprint import pprint as pp
from web3.utils.address import to_checksum_address

chunk = {}

# load snapshot data
for (title, fname, score) in CONFIG_COL:
    # read file line by line
    src_path = '{}/{}'.format(DIR_SNAPSHOT, fname)
    for line in open(src_path, 'r'):
        (addr, qty) = line.strip().split(',')
        addr = addr.lower() # [!] store address in lowercase format
                            # [!] prevent duplicate sensitive address
        # add score to wallet
        info = chunk.get(addr)
        if info is None:
            chunk[addr] = {}
        chunk[addr][title] = score

# recheck duplicate address
dup_addrs = find_duplicates_ignore_case(chunk.keys())
if len(dup_addrs) > 0:
    print(dup_addrs)
    print('found {} duplicated addresses'.format(len(dup_addrs)))
    exit()

# remove ban list
for addr in BAN_WALLETS:
    del chunk[addr.lower()]

# sum points
total_points = 0
for (addr, info) in chunk.items():
    info['sum'] = sum(info.values())
    total_points += info['sum']

# calc OP
for (addr, info) in chunk.items():
    info['op'] = REWARD_OP * (info['sum'] / total_points)

# reshape output
output = []
for (addr, info) in chunk.items():
    body = [ to_checksum_address(addr) ]
    body.append(info['op'])
    body.append(info['sum'])
    for (title, _, _) in CONFIG_COL:
        body.append(info.get(title) or 0)
    output.append(body)

# sort by points
output = sorted(output, key=lambda x: -x[2])

# print output (header)
fields = ','.join([ title for (title, _, _) in CONFIG_COL ])
print("address,OP,sum,{}".format(fields))

# print output (body)
for row in output:
    print(','.join([ str(r) for r in row ]))

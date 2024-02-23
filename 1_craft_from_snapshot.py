from config import *
from pprint import pprint as pp

chunk = {}

for (title, fname, score) in CONFIG_COL:

    # read file line by line
    src_path = '{}/{}'.format(DIR_SNAPSHOT, fname)
    for line in open(src_path, 'r'):
        (addr, qty) = line.strip().split(',')

        # add score to wallet
        info = chunk.get(addr)
        if info is None:
            chunk[addr] = {}
        chunk[addr][title] = score

# remove ban list
for addr in BAN_WALLETS:
    del chunk[addr]

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
    body = [ addr ]
    body.append(info['op'])
    body.append(info['sum'])
    for (title, _, _) in CONFIG_COL:
        body.append(info.get(title) or 0)
    output.append(body)

# sort by points
output = sorted(output, key=lambda x: -x[-1])

# print output (header)
fields = ','.join([ title for (title, _, _) in CONFIG_COL ])
print("address,OP,sum,{}".format(fields))

# print output (body)
for row in output:
    print(','.join([ str(r) for r in row ]))

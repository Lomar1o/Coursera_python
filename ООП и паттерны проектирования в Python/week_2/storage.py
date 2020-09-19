import argparse
import json
import tempfile
import os

parser = argparse.ArgumentParser()
parser.add_argument('--key', help='enter key')
parser.add_argument('--val', help='enter value')
args = parser.parse_args()

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
value = list()
data = {args.key: value}

if args.val:
    if os.path.exists(storage_path):
        with open(storage_path, 'r') as f:
            data = json.load(f)
    with open(storage_path, 'w') as f:
        if args.key in data:
            data[args.key].append(args.val)
        else:
            val = list()
            val.append(args.val)
            data[args.key] = val
        json.dump(data, f)
elif args.key:
    if os.path.exists(storage_path):
        with open(storage_path, 'r') as f:
            data = json.load(f)
            if args.key in data:
                print(', '.join(data[args.key]))
    else:
        print('')

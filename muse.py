import argparse

import pylsl


parser = argparse.ArgumentParser()
parser.add_argument('-n', '--Muse-FE6F', type=str, required=True,
                    default='PetalStream_eeg', help='the name of the LSL stream')
args = parser.parse_args()

# first resolve an EEG stream
print(f'looking for a stream with name {args.stream_name}...')
streams = pylsl.resolve_stream('name', args.stream_name)

# create a new inlet to read from the stream
if len(streams) == 0:
    raise RuntimeError(f'Found no LSL streams with name {args.stream_name}')
inlet = pylsl.StreamInlet(streams[0])

while True:
    sample, timestamp = inlet.pull_sample()
    print(timestamp, sample)
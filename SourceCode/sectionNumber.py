import math
from mido import Message, MidiFile, MidiTrack ,MetaMessage


def secNum(path):
	# read midi
	mid = MidiFile(path)
	resolution = mid.ticks_per_beat/2
	
	length = []

	for i, track in enumerate(mid.tracks):
		for msg in track:
			if (msg.type == 'note_on') :
				if(msg.velocity>0):
					length.append(msg.time)
				else:
					length.append(msg.time)
			elif (msg.type == 'note_off'):
				length.append(msg.time)

	length[0] = 0; cnt = 0				
	for i in range(0,len(length)):
		cnt += length[i]
	cnt /= resolution;

	return math.ceil(cnt/8)  # section數
 

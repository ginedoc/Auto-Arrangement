import math
from mido import Message, MidiFile, MidiTrack ,MetaMessage


def cleanMIDI(path):
	# read midi
	mid = MidiFile(path)
	resolution = mid.ticks_per_beat/2
	
	# new midi
	cleanMID = MidiFile()
	cleanMID.ticks_per_beat = mid.ticks_per_beat
	new_track = MidiTrack();  cleanMID.tracks.append(new_track)

	melody = [];  vel = []; length = []

	for i, track in enumerate(mid.tracks):
		for msg in track:
			if (msg.type == 'key_signature' or msg.type == 'time_signature' or msg.type == 'set_tempo'):
				new_track.append(msg)
			
			if (msg.type == 'note_on') :
				if(msg.velocity>0):
					#print(msg)
					melody.append(msg.note)
					vel.append(msg.velocity)
					length.append(msg.time)
				else:
					#print(msg)
					length.append(msg.time)
			elif (msg.type == 'note_off'):
				#print(msg)
				length.append(msg.time)

	length[0] = 0; cnt = 0				
	for i in range(0,len(melody)):
		tmp = round((length[2*i]+length[2*i+1])/resolution); cnt += tmp;
		msg_on = Message('note_on', note=melody[i], velocity=vel[i], time=0)
		msg_off = Message('note_on', note=melody[i], velocity=0, time=int(tmp*resolution))
		new_track.append(msg_on);	
		new_track.append(msg_off);

	cleanMID.save("Recordings/clean/cleanMidi.mid")
	return math.ceil(cnt/8)  # section數
 

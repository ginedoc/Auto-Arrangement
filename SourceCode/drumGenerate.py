# 這檔案用來輸出midi檔
import math
from mido import Message, MidiFile, MidiTrack ,MetaMessage


def OutputMidi(path, durm_list,secNum):	

	hi_note = 42
	s_drum_note = 38
	b_drum_note = 36
	cnt = 0 ;

	mid = MidiFile(path)
	resolution = int(mid.ticks_per_beat/4)
	print(secNum)

	# drum
	new_track = MidiTrack()
	for i in range(0,secNum):  # repeat leng times
		for i in range(0,len(durm_list[0])):	# one section tempo
			if(durm_list[0][i] or durm_list[1][i] or durm_list[2][i]):	
				msg_on_h = Message('note_on', note=hi_note, velocity=durm_list[0][i]*48, time=cnt*resolution, channel = 9)
				msg_on_s = Message('note_on', note=s_drum_note, velocity=durm_list[1][i]*35, time=0, channel = 9)
				msg_on_b = Message('note_on', note=b_drum_note, velocity=durm_list[2][i]*48, time=0, channel = 9)
				new_track.append(msg_on_h); new_track.append(msg_on_s); new_track.append(msg_on_b)
				
				msg_off_h = Message('note_on', note=hi_note, velocity=0, time=resolution, channel = 9)
				msg_off_s = Message('note_on', note=s_drum_note, velocity=0, time=0, channel = 9)
				msg_off_b = Message('note_on', note=b_drum_note, velocity=0, time=0, channel = 9)
				new_track.append(msg_off_h); new_track.append(msg_off_s); new_track.append(msg_off_b)
				cnt = 0
			else:
				cnt+=1
	
	mid.tracks.append(new_track)
	
	mid.save('new_song.mid')

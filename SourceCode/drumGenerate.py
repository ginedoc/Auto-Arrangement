# 這檔案用來輸出midi檔
import math
from mido import Message, MidiFile, MidiTrack ,MetaMessage


def OutputMidi(outpath, path, durm_list,secNum,type):	

	hi_note = 42
	s_drum_note = 38
	b_drum_note = 36
	
	mid = MidiFile(path)
	ignore_pos = [3,7,8,12]
	print(durm_list)
	print(secNum)

	# drum
	new_track = MidiTrack()
	if type == 0:
		resolution = int(mid.ticks_per_beat/4);  cnt = 0;
		for i in range(0,secNum):  # repeat leng times
			for i in range(0,16):	# one section tempo
				if(durm_list[0][i] or durm_list[1][i] or durm_list[2][i]):	
					msg_on_h = Message('note_on', note=hi_note, velocity=durm_list[0][i]*48, time=cnt*resolution, channel = 9)
					msg_on_s = Message('note_on', note=s_drum_note, velocity=durm_list[1][i]*35, time=0, channel = 9)
					msg_on_b = Message('note_on', note=b_drum_note, velocity=durm_list[2][i]*100, time=0, channel = 9)
					new_track.append(msg_on_h); new_track.append(msg_on_s); new_track.append(msg_on_b)
					
					msg_off_h = Message('note_on', note=hi_note, velocity=0, time=resolution, channel = 9)
					msg_off_s = Message('note_on', note=s_drum_note, velocity=0, time=0, channel = 9)
					msg_off_b = Message('note_on', note=b_drum_note, velocity=0, time=0, channel = 9)
					new_track.append(msg_off_h); new_track.append(msg_off_s); new_track.append(msg_off_b)
					cnt = 0
				else:
					cnt+=1
	elif type == 1:
		resolution = int(mid.ticks_per_beat/3);  cnt = 0;
		for i in range(0,secNum):  # repeat leng times
			for i in range(0,16):	# one section tempo
				if (i in ignore_pos):
					continue;
				if(durm_list[0][i] or durm_list[1][i] or durm_list[2][i]):	
					msg_on_h = Message('note_on', note=hi_note, velocity=durm_list[0][i]*48, time=cnt*resolution, channel = 9)
					msg_on_s = Message('note_on', note=s_drum_note, velocity=durm_list[1][i]*35, time=0, channel = 9)
					msg_on_b = Message('note_on', note=b_drum_note, velocity=durm_list[2][i]*100, time=0, channel = 9)
					new_track.append(msg_on_h); new_track.append(msg_on_s); new_track.append(msg_on_b)
					
					msg_off_h = Message('note_on', note=hi_note, velocity=0, time=resolution, channel = 9)
					msg_off_s = Message('note_on', note=s_drum_note, velocity=0, time=0, channel = 9)
					msg_off_b = Message('note_on', note=b_drum_note, velocity=0, time=0, channel = 9)
					new_track.append(msg_off_h); new_track.append(msg_off_s); new_track.append(msg_off_b)
					cnt = 0
				else:
					cnt+=1
	'''
	if type == 1:
		resolution = int(mid.ticks_per_beat/3); remain_resolution = mid.ticks_per_beat-2*resolution
		print(resolution,remain_resolution)
		stop = 0; tmp = 0; 
		for i in range(0,secNum):  # repeat leng times
			for i in range(0,16):	# one section tempo
				if (i in ignore_pos):
					continue;	
			
				tmp += 1
				if(durm_list[0][i] or durm_list[1][i] or durm_list[2][i]):	
					if tmp ==3 :
					
						msg_on_h = Message('note_on', note=hi_note, velocity=durm_list[0][i]*48, time=stop, channel = 9)
						msg_on_s = Message('note_on', note=s_drum_note, velocity=durm_list[1][i]*35, time=0, channel = 9)
						msg_on_b = Message('note_on', note=b_drum_note, velocity=durm_list[2][i]*48, time=0, channel = 9)
						new_track.append(msg_on_h); new_track.append(msg_on_s); new_track.append(msg_on_b)
						
						msg_off_h = Message('note_on', note=hi_note, velocity=0, time=remain_resolution, channel = 9)
						msg_off_s = Message('note_on', note=s_drum_note, velocity=0, time=0, channel = 9)
						msg_off_b = Message('note_on', note=b_drum_note, velocity=0, time=0, channel = 9)
						new_track.append(msg_off_h); new_track.append(msg_off_s); new_track.append(msg_off_b)
						stop = 0
						
					else:
						msg_on_h = Message('note_on', note=hi_note, velocity=durm_list[0][i]*48, time=stop, channel = 9)
						msg_on_s = Message('note_on', note=s_drum_note, velocity=durm_list[1][i]*35, time=0, channel = 9)
						msg_on_b = Message('note_on', note=b_drum_note, velocity=durm_list[2][i]*48, time=0, channel = 9)
						new_track.append(msg_on_h); new_track.append(msg_on_s); new_track.append(msg_on_b)
						
						msg_off_h = Message('note_on', note=hi_note, velocity=0, time=resolution, channel = 9)
						msg_off_s = Message('note_on', note=s_drum_note, velocity=0, time=0, channel = 9)
						msg_off_b = Message('note_on', note=b_drum_note, velocity=0, time=0, channel = 9)
						new_track.append(msg_off_h); new_track.append(msg_off_s); new_track.append(msg_off_b)
						stop = 0
					
				else:
					if tmp == 3:
						stop += remain_resolution
						tmp = 0
					else :
						stop += resolution
			
	'''
	mid.tracks.append(new_track)
	mid.save(outpath)
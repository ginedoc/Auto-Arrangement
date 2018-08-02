from mido import Message, MidiFile, MidiTrack ,MetaMessage

hi_note = 42
s_drum_note = 38
b_drum_note = 36

def generate(track, drum_arr, resolution,leng): 

	global hi_note; global s_drum_note;	global b_drum_note
	cnt = 0

	print(drum_arr)
	
	# midi chord根音從48 開始	
	for i in range(0,leng):  # repeat n times
		for i in range(0,len(drum_arr[0])):	# one section tempo
			if(drum_arr[0][i] or drum_arr[1][i] or drum_arr[2][i]):	
				msg_on_h = Message('note_on', note=hi_note, velocity=drum_arr[0][i]*96, time=cnt*resolution, channel = 9)
				msg_on_s = Message('note_on', note=s_drum_note, velocity=drum_arr[1][i]*70, time=0, channel = 9)
				msg_on_b = Message('note_on', note=b_drum_note, velocity=drum_arr[2][i]*96, time=0, channel = 9)
				track.append(msg_on_h); track.append(msg_on_s); track.append(msg_on_b)
				
				msg_off_h = Message('note_on', note=hi_note, velocity=0, time=resolution, channel = 9)
				msg_off_s = Message('note_on', note=s_drum_note, velocity=0, time=0, channel = 9)
				msg_off_b = Message('note_on', note=b_drum_note, velocity=0, time=0, channel = 9)
				track.append(msg_off_h); track.append(msg_off_s); track.append(msg_off_b)
				cnt = 0
			else:
				cnt+=1
	
	return track
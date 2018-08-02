from mido import Message, MidiFile, MidiTrack ,MetaMessage

type = 0
resolution = 0
vel = 0

def dataSet(DEtype, Resolution, velocity):
	global type; 	global resolution;	global vel
	type = DEtype;	resolution = Resolution;	vel = velocity


def generate(track, chord_arr, len): 

	global type; global resolution;	global vel
	# midi chord根音從48 開始	
	if len == 1 :	# 一小節兩和弦
		msg_on = Message('note_on', note=48+chord_arr[0], velocity=vel, time=0)
		msg_off = Message('note_on', note=48+chord_arr[0], velocity=0, time=resolution)
		track.append(msg_on);	track.append(msg_off)
		msg_on1 = Message('note_on', note=48+chord_arr[1], velocity=vel, time=0)
		msg_on2 = Message('note_on', note=48+chord_arr[2], velocity=vel, time=0)
		msg_on3 = Message('note_on', note=48+chord_arr[3], velocity=vel, time=0)
		msg_off1 = Message('note_on', note=48+chord_arr[1], velocity=0, time=resolution)
		msg_off2 = Message('note_on', note=48+chord_arr[2], velocity=0, time=0)
		msg_off3 = Message('note_on', note=48+chord_arr[3], velocity=0, time=0)
		track.append(msg_on1);	track.append(msg_on2);	track.append(msg_on3)
		track.append(msg_off1);	track.append(msg_off2);	track.append(msg_off3)
			
	else :	# 一小節同一和弦
		if type	== 0 :  	# 琶音
			for shift in chord_arr:
				msg_on = Message('note_on', note=48+shift, velocity=vel, time=0)
				msg_off = Message('note_on', note=48+shift, velocity=0, time=resolution)
				track.append(msg_on)
				track.append(msg_off)

		elif type == 1 :	# 連音
			msg_on = Message('note_on', note=48+chord_arr[0], velocity=vel, time=0)
			msg_off = Message('note_on', note=48+chord_arr[0], velocity=0, time=resolution)
			track.append(msg_on)
			track.append(msg_off)
			for x in range(3):
				msg_on1 = Message('note_on', note=48+chord_arr[1], velocity=vel, time=0)
				msg_on2 = Message('note_on', note=48+chord_arr[2], velocity=vel, time=0)
				msg_on3 = Message('note_on', note=48+chord_arr[3], velocity=vel, time=0)
				msg_off1 = Message('note_on', note=48+chord_arr[1], velocity=0, time=resolution)
				msg_off2 = Message('note_on', note=48+chord_arr[2], velocity=0, time=0)
				msg_off3 = Message('note_on', note=48+chord_arr[3], velocity=0, time=0)
				track.append(msg_on1);	track.append(msg_on2);	track.append(msg_on3)
				track.append(msg_off1);	track.append(msg_off2);	track.append(msg_off3)
	
	return track
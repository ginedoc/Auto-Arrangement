# 這份code是用來將 midi File 拆解成Array的形式

import cmath
import numpy as np
import SourceCode.globalVar as gl
import SourceCode.noteShift as sf
from mido import Message, MidiFile, MidiTrack ,MetaMessage

note_list = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
note_on_off = [0,0,0,0,0,0,0,0,0,0,0,0]  		# 1*12 Array

def fill_note_array(cnt,arr,index):
	for i in range(0,cnt): 	# cnt loop 
		tmp_cnt = 1			# 0 is pause note
		for boo_value in note_on_off : # write the note situation in this time
			if (boo_value == 1) :
				arr[tmp_cnt,index] = boo_value 		# array[which note,time]
			tmp_cnt += 1 	# add array cnt
		index += 1
	return arr,index

def Generate_input_data() :

	file_pos = gl.get_pathName()
	resolution = gl.get_resolution()			# 放入training 的資料維度 (8[半小節]  16[全小節])
	ticks_per_beat = gl.get_ticks_per_beat()	# 一個4分音符的tick數
	ticks_per_16 = ticks_per_beat/4
	mainKey = gl.get_mainKey()
	mainKey_shift = sf.mainKey_shift_number(mainKey)
	print("main key",mainKey,", mainKey_shift",mainKey_shift)
	midi_length = gl.get_midi_length()

	mid = MidiFile(file_pos)
	for i, track in enumerate(mid.tracks):
		#print('Track {}: {}'.format(i, track.name))
		tick_cnt = 0
		array_index = 0
		
		length = (int(midi_length/ticks_per_16)+1) 
		note_array = np.zeros((13,length),dtype=np.int)
		print("length : ",length)
		
		for msg in track:
			tick_cnt += msg.time 	
			if (tick_cnt >= ticks_per_16 ) : 			# if the tick count is bigger then resolution(1/16音符)
				loop_cnt = int(tick_cnt/ticks_per_16) 	# repeat how many times
				#print(loop_cnt,tick_cnt)
				note_array,array_index = fill_note_array(loop_cnt,note_array,array_index)
				tick_cnt %= ticks_per_16 				# clear the tick cnt
				
			if( msg.type == 'note_on') :
				note_num = sf.chord_shift(msg.note%12 ,mainKey_shift)				# get which note number
				#print("note before shift : ",msg.note%12, note_list[msg.note%12])
				#print("note after shift : ",note_num, note_list[note_num] )
				if(msg.velocity > 0) : 						
					note_on_off[note_num] = 1				# play note is set to 1
				else :
					note_array[note_num+1,array_index] = 1
					note_on_off[note_num] = 0
				
			elif( msg.type == 'note_off') :
				note_num = sf.chord_shift(msg.note%12 ,mainKey_shift)	# get which note number
				#print("note before shift : ",msg.note%12, note_list[msg.note%12])
				#print("note after shift : ",note_num, note_list[note_num] )
				note_array[note_num+1,array_index] = 1
				note_on_off[note_num] = 0
					
		with open('TEST.csv', 'w') as file:	
			for row in note_array :
				for item in row :
					file.write("%s,"%item)
				file.write("\n")
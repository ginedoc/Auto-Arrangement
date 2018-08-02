# 這檔案用來輸出midi檔
# 輸出track為
# track 1 : 曲調、格式
# track 2 : 原先的midi檔(melody)
# track 3 : 伴奏(利用自定義的和弦拆解)

import SourceCode.globalVar as gl
import SourceCode.chordTable as ct
import SourceCode.noteShift as sf
import SourceCode.accompanyGenerate as ag
import SourceCode.drumGenerate as dg
from mido import Message, MidiFile, MidiTrack ,MetaMessage


def OutputMidi(chord_list, durm_list):
	type = gl.get_disassembleType()
	file = gl.get_pathName()
	mainKey = gl.get_mainKey() 
	mainKey_shift = sf.mainKey_shift_number(mainKey)
	#print(mainKey,mainKey_shift,"\n")
	resolution = gl.get_ticks_per_beat()	# 4分音符tick數
	
	#chord_list = ['C','C','G','C','C','C','G','C']	# 計算出來的結果
	#chord_list = ['C','G','C','C','G','G','C','C','C','C','C','C','G','G','C','C']
	

	mid = MidiFile()			# open a new midi file
	
	# melody
	mid_r = MidiFile(file)		
	mid.ticks_per_beat = resolution
	for i, track in enumerate(mid_r.tracks):
		new_track = MidiTrack()
		mid.tracks.append(new_track)
		for msg in track:
			new_track.append(msg)
			print(msg)
	'''
	# accompany
	ag.dataSet(type, resolution, 50)
	track = MidiTrack()			# create new track
	for i in range(0, len(chord_list), 2):
		if chord_list[i]==chord_list[i+1]:	# 一小節同一和弦
			chord_num = sf.mainKey_shift_number(chord_list[i])
			chord_num = sf.chord_shift_RETURN(chord_num,mainKey_shift)	# 轉回原先的調號
			chord_arr = ct.chord_list(chord_num,0)	
			track = ag.generate(track, chord_arr, 2)
			
		else :								# 一小節兩和弦
			chord_num = sf.mainKey_shift_number(chord_list[i])
			chord_num = sf.chord_shift_RETURN(chord_num,mainKey_shift)	# 轉回原先的調號
			chord_arr = ct.chord_list(chord_num,0)	
			track = ag.generate(track, chord_arr, 1)
	
			chord_num = sf.mainKey_shift_number(chord_list[i+1])
			chord_num = sf.chord_shift_RETURN(chord_num,mainKey_shift)	# 轉回原先的調號
			chord_arr = ct.chord_list(chord_num,0)	
			track = ag.generate(track, chord_arr, 1)
	mid.tracks.append(track)	# add track to midi file
	'''
	
	print("resolution : ",resolution)
	# drum
	new_track = MidiTrack()
	new_track = dg.generate(new_track,durm_list,int(resolution/4),int(len(chord_list)/2))
	mid.tracks.append(new_track)
	
	mid.save('new_song.mid')
	
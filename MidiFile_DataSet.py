# 負責檢視MIDI FILE 並將一些結果輸出到 GLOBAL VAR

from mido import Message, MidiFile, MidiTrack ,MetaMessage
import SourceCode.globalVar as gl

def initMIDIdata():
	mid = MidiFile(gl.get_pathName())
	#print(gl.get_pathName())
	gl.set_ticks_per_beat(mid.ticks_per_beat)
	#print("ticks_per_beat : ",gl.get_ticks_per_beat()) # resolution

	for i, track in enumerate(mid.tracks):

		total_time = 0
		for msg in track :
			total_time += msg.time
			if (msg.type == 'key_signature'):
				gl.set_mainKey(msg.key)
				#print("main Key : ", gl.get_mainKey())
		#print("total_time : ", total_time)		
		gl.set_midi_length(total_time) if (gl.get_midi_length()<total_time) else gl.set_midi_length(gl.get_midi_length())
		
	#print("midi length : ", gl.get_midi_length())
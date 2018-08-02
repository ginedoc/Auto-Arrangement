# 此檔用來存放一些共用的變數

#from note_shift_function import note_shift_function

pathName = ""#"D://CSIE_project/final_project2(global_var)/SourceFile/mary2.mid"			# 檔案路徑
resolution = 8			# 放入training 的資料維度 (8[半小節]  16[全小節])
ticks_per_beat = 0#480	# MIDI檔讀出的 一個四分音符的TICK數
disassembleType = 0		# 要選擇的和絃拆解方式
mainKey = "C"#"C"			# 該midi檔的調性

midi_length = 15360		# 總共resolution數

hi_het = [1,0,1,0,1,0,1,0, 1,0,1,0,1,0,1,0]
s_drum = [0,0,0,0,1,0,0,0, 0,1,0,0,1,0,0,0]
b_drum = [0,0,0,0,1,0,0,0, 0,0,0,0,1,0,0,0]



def set_pathName(path): 	
	global pathName
	pathName = path
def get_pathName() :
	global pathName
	return pathName
	
	
def set_resolution(resolu) :
	global resolution
	resolution = resolu
def get_resolution() :
	global resolution
	return resolution
	
	
def set_ticks_per_beat(resolu_tick) :
	global ticks_per_beat
	ticks_per_beat = resolu_tick
def get_ticks_per_beat() :
	global ticks_per_beat	
	return ticks_per_beat
	
	
def set_disassembleType(disassType) :
	global disassembleType
	disassembleType = disassType
def get_disassembleType() :
	global disassembleType
	return disassembleType
	

def set_mainKey(Key): 	
	global mainKey
	mainKey = Key
def get_mainKey() :
	global mainKey
	return mainKey

	global mainKeyShift
	return mainKeyShift

	
def set_midi_length(leg):
	global midi_length
	midi_length = leg
def get_midi_length():
	global midi_length
	return midi_length
	
	
def get_hiHet(index):
	return hi_het[index]
def get_sDrum(index):
	return s_drum[index]
def get_bDrum(index):
	return b_drum[index]
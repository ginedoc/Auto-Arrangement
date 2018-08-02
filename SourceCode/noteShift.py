# 這份code是用來轉調，調性判斷
# 會回傳一個int表示要轉成c chord 需要的位移量

# 使用方法 : 傳入一個string
# 回傳值   : 一個數字(代表偏移量) 

def mainKey_shift_number(mainkey):

	if mainkey == 'C':
		shift = 0
	elif mainkey == 'C#' or mainkey == 'Db':
		shift = 1
	elif mainkey == 'D':
		shift = 2
	elif mainkey == 'D#' or mainkey == 'Eb':
		shift = 3
	elif mainkey == 'E':
		shift = 4
	elif mainkey == 'F':
		shift = 5
	elif mainkey == 'F#' or mainkey == 'Gb':
		shift = 6
	elif mainkey == 'G':
		shift = 7
	elif mainkey == 'G#' or mainkey == 'Ab':
		shift = 8
	elif mainkey == 'A':
		shift = 9
	elif mainkey == 'A#' or mainkey == 'Bb':
		shift = 10
	elif mainkey == 'B':
		shift = 11
	else :
		shift = 0
		print ('error')	
	return shift
	


def note_shift(note,shift):
	tmp = (note-shift)
	if note == 0: 			# pause note (don't do anything)
		new_note = note
	elif tmp>0: 			# doesn't get over the pause note
		new_note = tmp
	else : 					# get over the pause note
		new_note = tmp-1
	return new_note
	

def chord_shift(chord,shift):
	return chord - shift
	
def chord_shift_RETURN(chord,shift):
	return chord + shift
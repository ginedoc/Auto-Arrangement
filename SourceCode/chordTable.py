# 此檔案用於輸出和弦的list
# (用來和弦拆解)

# 使用方法 : 傳入爾個int (什麼key,什麼類型)
# 回傳值   : 一個list(代表該和弦的和弦音) 

import numpy as np

major_triad = [0,4,7,12]
minor_triad = [0,3,7,12]
dominant_seventh = [0,4,7,10]
major_seventh = [0,4,7,11]
minor_seventh = [0,3,7,10]

chord_type = [major_triad, minor_triad, dominant_seventh, major_seventh, minor_seventh]
chord_table = []

root = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


for n, r in enumerate(root):
    n_list = []
    for t, arr in enumerate(chord_type):
        if n>= root.index('F'):
            arr = [a-(12-n) for a in arr]
        else:
            arr = [a+n for a in arr]
        sorted(arr)
        n_list.append(arr)
    chord_table.append(n_list)
#print(chord_table)
#print("")
#print(chord_table[1][0])

def chord_list(key,type):
	return chord_table[key][type]
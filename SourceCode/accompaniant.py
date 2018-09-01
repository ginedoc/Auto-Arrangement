#adding accompaniant
"""
instr:
    bass 33~40
"""
import mido

def acc(chord, instr, type, resolution=960):
    if instr>=33 and instr<=40:
        msg=_add_bass(chord, instr, type, int(resolution/4))
    elif instr>=1 and instr<=8:
        print(chord)
        msg=_add_piano(chord, instr, type, int(resolution/4))

    return msg

def _add_bass(chord, instr, type, tick_s):
    #channel 1
    #midi note range: 40(E2)~60(C4)
    #48~59
    last=-1
    note=[mido.Message('program_change', program=instr, channel=1, time=0)]
    for i, c in enumerate(chord):
            note.append(mido.Message('note_on', note=chord[i]%12+48, channel=1, time=0))
            if i+1<len(chord) and chord[i+1]-c==2:
                note.append(mido.Message('note_off', note=chord[i]%12+48, channel=1, time=6*tick_s))
                note.append(mido.Message('note_on', note=chord[i]%12+48-1, channel=1, time=0))
                note.append(mido.Message('note_off', note=chord[i]%12+48-1, channel=1, time=2*tick_s))
            elif i+1<len(chord) and chord[i+1]-c==-2:
                note.append(mido.Message('note_off', note=chord[i]%12+48, channel=1, time=6*tick_s))
                note.append(mido.Message('note_on', note=chord[i]%12+48+1, channel=1, time=0))
                note.append(mido.Message('note_off', note=chord[i]%12+48+1, channel=1, time=2*tick_s))
            else:
                note.append(mido.Message('note_off', note=chord[i]%12+48, channel=1, time=6*tick_s))
                note.append(mido.Message('note_on', note=chord[i]%12+48, channel=1, time=0))
                note.append(mido.Message('note_off', note=chord[i]%12+48, channel=1, time=2*tick_s))
    return note

def _add_piano(chord, instr, type, tick_s):
    #channel 2
    #
    print('tick_s:%d'%tick_s)
    
    note=[mido.Message('program_change', program=instr, channel=2, time=0)]
    inv, root = _set_root(chord)

    print(root)
    for i,r in enumerate(root):
        for _ in range(2):
            if chord[i] < 12:
                note = _add_Major(note, tick_s, inv[i], r)
            elif chord[i] >= 12:
                note = _add_minor(note, tick_s, inv[i], r)
        
    return note

def _set_root(chord):
    root = [chord[0]%12+60]
    inv = [0] # 原位
    for i, c in enumerate(chord[1:]):
        inverse, r = _maxRoot_M3(root[-1], c)
        inv.append(inverse)
        root.append(r)
    return inv, root
def _maxRoot_M3(lastR, newC):
    root = newC%12
    if newC < 12:
        chord = [root, root+4, root+7]
    else:
        chord = [root, root+3, root+7]
    rootR = [x for x in range(lastR-3, lastR+3)]
    ##
    for i, c in enumerate(chord):
        if c >= 12:
            chord[i] = c - 12
        elif c < 0:
            chord[i] = c + 12
    ##
    inv = 0
    newRoot = lastR
    in3M = 0
    
    for iR in range(0, 3):
        for i, c in enumerate(chord):
            # up
            if c == (lastR+iR)%12 and (lastR+iR)<72:
                inv = i
                newRoot = lastR+iR
                in3M = 1
                break  
            # down
            if c == (lastR+iR-3)%12 and (lastR+iR) > 48:
                inv = i
                newRoot = lastR+iR-3
                in3M = 1
                break
        if in3M ==1:
            break

    if in3M == 0:
        for i in range(0, 6):
            if chord[0] == (lastR+i-6)%12:
                newRoot = lastR+i-6
                break
            if chord[0] == (lastR+5-i)%12:
                newRoot = lastR+5-i
                break
    return inv, newRoot


def _add_Major(note, tick_s, inv, root):
    note.append(mido.Message('note_on', note=root, channel=2, time=0))
    if inv==0:
        note.append(mido.Message('note_on', note=root+4, channel=2, time=0))
        note.append(mido.Message('note_on', note=root+7, channel=2, time=0))
        note.append(mido.Message('note_off', note=root+4, channel=2, time=4*tick_s))
        note.append(mido.Message('note_off', note=root+7, channel=2, time=0))
    elif inv==1:
        note.append(mido.Message('note_on', note=root+3, channel=2, time=0))
        note.append(mido.Message('note_on', note=root+8, channel=2, time=0))
        note.append(mido.Message('note_off', note=root+3, channel=2, time=4*tick_s))
        note.append(mido.Message('note_off', note=root+8, channel=2, time=0))
    elif inv==2:
        note.append(mido.Message('note_on', note=root+5, channel=2, time=0))
        note.append(mido.Message('note_on', note=root+9, channel=2, time=0))
        note.append(mido.Message('note_off', note=root+5, channel=2, time=4*tick_s))
        note.append(mido.Message('note_off', note=root+9, channel=2, time=0))

    note.append(mido.Message('note_off', note=root, channel=2, time=0))
    return note

def _add_minor(note, tick_s, inv, root):
    note.append(mido.Message('note_on', note=root, channel=2, time=0))
    if inv==0:
        note.append(mido.Message('note_on', note=root+3, channel=2, time=0))
        note.append(mido.Message('note_on', note=root+7, channel=2, time=0))
        note.append(mido.Message('note_off', note=root+3, channel=2, time=4*tick_s))
        note.append(mido.Message('note_off', note=root+7, channel=2, time=0))
    elif inv==1:
        note.append(mido.Message('note_on', note=root+4, channel=2, time=0))
        note.append(mido.Message('note_on', note=root+9, channel=2, time=0))
        note.append(mido.Message('note_off', note=root+4, channel=2, time=4*tick_s))
        note.append(mido.Message('note_off', note=root+9, channel=2, time=0))
    elif inv==2:
        note.append(mido.Message('note_on', note=root+5, channel=2, time=0))
        note.append(mido.Message('note_on', note=root+8, channel=2, time=0))
        note.append(mido.Message('note_off', note=root+5, channel=2, time=4*tick_s))
        note.append(mido.Message('note_off', note=root+8, channel=2, time=0))

    note.append(mido.Message('note_off', note=root, channel=2, time=0))
    return note

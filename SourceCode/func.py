import numpy as np
import os
import pretty_midi
import mido
import pyace
from pydub import AudioSegment
import locale
from locale import atof
from midi2audio import FluidSynth

def midi2mp3(path):
    fname=os.path.basename(path)
    fname=os.path.splitext(fname)[0]
    fs = FluidSynth()
    fs.midi_to_audio(path, '../mp3/'+fname+'.wav')
    AudioSegment.from_wav('../mp3/'+fname+'.wav').export('../mp3/'+fname+'.mp3', format="mp3")
    os.remove('../mp3/'+fname+'.wav')
    return fname

def midi2pianoroll(mid):
    midd=mido.MidiFile(mid)
    midp=pretty_midi.PrettyMIDI(mid)
    # basic information
    tempo=get_tempo(midd)
    bpm=mido.tempo2bpm(tempo)
    sixteen_t=(1/(bpm/60))/4
    midi_length=int(np.ceil(midd.length/sixteen_t))

    # 
    notes=np.zeros((midi_length, 13))
    for instrument in midp.instruments:
        print(instrument)
        if instrument.is_drum==False:
            pr = instrument.get_piano_roll(1/sixteen_t)
            cnt = 0
            for i, ppr in enumerate(pr):
                # i: notes
                # j: time stamp
                for j, nt in enumerate(ppr):
                    if nt>0:
                        notes[j][i%12+1] += 1
    for i, note in enumerate(notes):
        if np.count_nonzero(note) == 0:
            notes[i][0] = 1               
    return notes, sixteen_t

def ace_info(src):
    des='./result.txt'
    pyace.simpleace(src, des)
    f=open(des, 'r')
    info=(f.read()).split()
    info=np.array(info).reshape((int(len(info)/3),3))
    os.remove(des)
    return info

def ratio_train_data(notes, chords, seg_t):
    note_ratio=[]
    chord_data=[]
    for chord in chords:
        tptr = atof(chord[0])
        while tptr+8*seg_t < atof(chord[1]):
            t=int(tptr/seg_t)
            note_ratio.append(roll2ration(notes[t:t+8]))
            chord_data.append(chord[2])
            tptr += seg_t
    return (note_ratio, chord_data)
def roll2ration(notes):
    scale = np.zeros(13)
    for seg in notes:
        for i, note in enumerate(seg):
            scale[i] += note
    total=scale.sum()
    scale=scale/total
    return scale

def load_data(notes, chords):
    fn = open(notes, 'r')
    fc = open(chords, 'r')
    notes = (fn.read()).split('\n')
    notes = np.array(notes)
    N=np.zeros((len(notes), 13))
    for i, note in enumerate(notes):
        note = note.split()
        for j, n in enumerate(note):
            N[i][j]=atof(n)
            if np.isnan(N[i][j])==True:
                N[i][j]=0
    notes = N

    chords=np.array((fc.read()).split())
    chords=chord2index(chords)    

    return notes, chords

def get_tempo(mid):
    for m in mid:
        if m.is_meta and m.type=='set_tempo':
            tempo = m.tempo
            break
    if tempo is None:
        tempo=500000
    return tempo
###

def chord2index(chordlist):
    chordlabel2num = {
        'C':0,'B#':0, 'N':0,
	'C#':1,'Db':1,
	'D':2,
	'D#':3,'Eb':3,
        'E':4,'Fb':4,
        'F':5,'E#':5,
	'F#':6,'Gb':6,
	'G':7,
	'G#':8,'Ab':8,
	'A':9,
	'A#':10,'Bb':10,
        'B':11,'Cb':11,
        'C:min':12,'B#:min':12,
        'C#:min':13,'Db:min':13,
        'D:min':14,
        'D#:min':15,'Eb:min':15,
        'E:min':16,'Fb:min':16,
        'F:min':17,'E#:min':17,
        'F#:min':18,'Gb:min':18,
        'G:min':19,
        'G#:min':20,'Ab:min':20,
        'A:min':21,
        'A#:min':22,'Bb:min':22,
        'B:min':23,'Cb:min':23,
        'N':24
	}
    for i, chord in enumerate(chordlist):
        chordlist[i]=chordlabel2num[chord]
    return chordlist

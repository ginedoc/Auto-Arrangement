import numpy as np
import mido
from midi2audio import FluidSynth
from pydub import AudioSegment
import os
import locale
from locale import atof
import SourceCode.accompaniant as acc
from SourceCode.func import midi2pianoroll, roll2ration
from keras.models import load_model
AudioSegment.converter = "/usr/bin/ffmpeg"
chordlabel2num = {
        'C':0,'B#':0,
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
    'B:min':23,'Cb:min':23
	}

class song():
    resolution = 960
    bpm = 96
    tempo = 0
    track = ' '
    track_name = ' '
    mp3path = './resources/mymp3.mp3'
    wavpath = './resources/mywav.wav'
    def __init__(self, path):
        self.track_name = path
        self._update_trackinfo(path)
    def _update_trackinfo(self, path):
        mid = mido.MidiFile(path)
        self.track = mid
        self.resolution = mid.ticks_per_beat
        self.tempo = self._get_tempo()
        self.bpm = self._get_bpm()

    def note_ticks(self,type):
        if type==1:
            res=self.resolution*4
        elif type==2:
            res=self.resolution*2
        elif type==4:
            res=self.resolution
        elif type==8:
            res=self.resolution/2
        elif type==16:
            res=self.resolution/4
        return int(res)
    def chord_estimation(self, model=None):
        # estimation using out model
        notes, seg_t = midi2pianoroll(self.track_name)
        note_ratio = []
        chord = []
        for i in range(0, len(notes), 8):
            note_ratio.append(roll2ration(notes[i:i+8]))
        note_ratio = np.array(note_ratio)
        model = load_model(model)
        predict = model.predict(note_ratio)
        for half_measure in predict:
            chord.append(np.argmax(half_measure))
        print(chord)   
        return chord         
        
        """Estimation using pyace
        self._mid2mp3()
        info_timechord = pyace.simpleace(self.mp3path, 'resources/time_domain.txt')
        #info_timechord = pyace.deepace(self.mp3path, 'resources/time_domain.txt', 'fcnn' ,'./pyace/model/fcnn512/CJKURB.cg.model')

        print(info_timechord)
        sixteenth_t = (1/(self.bpm/60))/4
        #tickchord - 16th
        tptr=0
        cptr=0
        info_16 = []

        while tptr<=self.track.length:
            if tptr>atof(info_timechord[cptr][1]) and tptr<=atof(info_timechord[-1][1]):
                cptr += 1
            info_16.append(info_timechord[cptr][2])            

            tptr += sixteenth_t
         
        info_16=self._chord2index(info_16)       
        return info_16
        """
    ##########################################
    def add_accompaniant(self, chord_arr, instrument, type=0):
        accTrack=mido.MidiTrack()
        myMidi=self._get_track(self.track)
        myMidi.tracks.append(accTrack)
        msgs=acc.acc(chord_arr, instrument, type, self.resolution)

        for msg in msgs:
            accTrack.append(msg)

        myMidi.save('mymidi.mid')
        self.track=mido.MidiFile('mymidi.mid')
        self._update_trackinfo('mymidi.mid')
        #os.remove('resources/mymidi.mid')
        print('adding '+str(instrument)+' in type '+str(type)+' success')

    ##########################################
    def _get_track(self, mid):
        mid0=mido.MidiFile()
        for track in mid.tracks:
            new_track = mido.MidiTrack()
            mid0.tracks.append(new_track)
            for msg in track:
                new_track.append(msg)
        return mid0

    def _mid2mp3(self):
        #mid2wav
        fs=FluidSynth()
        fs.midi_to_audio(self.track_name, self.wavpath)
        #wav2mp3
        mp3=AudioSegment.from_wav(self.wavpath).export(self.mp3path, format="mp3")
        os.remove(self.wavpath)

    #### bpm
    def _get_bpm(self):
        bpm = mido.tempo2bpm(self.tempo)
        return bpm

    #tempo(midi): microseconds per beats
    def _get_tempo(self):
        for m in self.track:
            if m.is_meta and m.type=='set_tempo':
                return m.tempo
        return 500000
    def _chord2index(self, chord):
        for i, c in enumerate(chord):
            chord[i]=chordlabel2num[c]
        return chord

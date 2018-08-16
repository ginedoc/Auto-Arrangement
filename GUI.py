import re
import sys
import os.path
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QRadioButton, QCheckBox, QLineEdit, QFileDialog, QLabel, QMessageBox, QComboBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QSize

import time
import rtmidi
import threading
from mido import Message

import SourceCode.drumSample as drumSample
import SourceCode.drumGenerate as drumGenerate
import SourceCode.cleanMidi as cleanMidi


class App(QWidget):
	
	filePath = ''
	
	hi_het = [0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0]; s_drum = [0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0]; b_drum = [0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0]
	hi_het_list_btn = []; s_drum_list_btn = []; b_drum_list_btn = []
	

	def __init__(self):
		super().__init__()
		self.initUI()

	def fileOpen_GUI(self,layout):
		grid = QGridLayout();	grid.setSpacing(10)
		grid.addWidget(QLabel("請選擇一個MIDI檔案：",self),0,0,1,8)
		
		# file path textbox
		self.filePath_textbox = QLineEdit(self)
		grid.addWidget(self.filePath_textbox, 1, 0, 1, 8)
		# open button
		open_button = QPushButton('Open File', self)
		grid.addWidget(open_button, 1, 9, 1, 1)
		open_button.clicked.connect(self.open_click)
		
		# listen button
		listen_button = QPushButton('試聽', self)
		grid.addWidget(listen_button, 1, 10, 1, 1)
		listen_button.clicked.connect(self.listen_click)
		# record button
		record_button = QPushButton('錄製', self)
		grid.addWidget(record_button, 1, 11, 1, 1)
		record_button.clicked.connect(self.record_click)
		
		layout.addLayout(grid)
		
	
	def excute_GUI(self,layout):
		grid = QGridLayout()
		# listen button
		listen_button = QPushButton('鼓組試聽', self)
		grid.addWidget(listen_button,0,5,1,1)
		listen_button.clicked.connect(self.drumLis_click)
		
		# reset button 
		reset_button = QPushButton('Reset', self)
		grid.addWidget(reset_button,1,0,1,2)
		reset_button.clicked.connect(self.reset_click)
		# run button
		run_button = QPushButton('Run', self)
		grid.addWidget(run_button,1,2,1,2)
		run_button.clicked.connect(self.run_click)
		# exit button
		exit_button = QPushButton('Exit', self)
		grid.addWidget(exit_button,1,4,1,2)
		exit_button.clicked.connect(self.exit_click)	
		
		layout.addLayout(grid)
	
	
	def drumBtn_GUI(self,layout):
	
		a = 25; cnt = 0
		grid = QGridLayout(); grid.setVerticalSpacing(11)
		grid.addWidget(QLabel("請選擇鼓組(以16分音符為一單位)："),0,0,1,50)
		
		self.select_button = QComboBox(self)
		grid.addWidget(self.select_button, 1, 0, 1 ,50)
		self.select_button.addItem("Empty")
		self.select_button.addItem("Basic 1")
		self.select_button.addItem("Basic 2")
		self.select_button.currentIndexChanged.connect(lambda:self.select_click(self.select_button))
		
		
		pic = QPixmap("SourceFile/drum.jpg").scaled(QSize(450,100))
		bgPic = QLabel("123",self);  bgPic.setPixmap(pic)	
		grid.addWidget(bgPic,2,0,10,50)
		for i in range(0,16):
			if i%4==0:
				cnt+=1
			self.hi_het_list_btn.append(QCheckBox("",self));  grid.addWidget(self.hi_het_list_btn[i],2,a+i+cnt,1,1)
			self.s_drum_list_btn.append(QCheckBox("",self));  grid.addWidget(self.s_drum_list_btn[i],4,a+i+cnt,1,1)
			self.b_drum_list_btn.append(QCheckBox("",self));  grid.addWidget(self.b_drum_list_btn[i],6,a+i+cnt,1,1)
			self.hi_het_list_btn[i].setTristate(True);	self.s_drum_list_btn[i].setTristate(True);	self.b_drum_list_btn[i].setTristate(True); 
		
		self.connectCheckBox()
		
		
		layout.addLayout(grid)
	
	def initUI(self):
		self.setWindowTitle('自動伴奏產生器')

		grid = QVBoxLayout(); #grid.setSpacing(10)
		self.fileOpen_GUI(grid)		
		self.drumBtn_GUI(grid)
		self.excute_GUI(grid)
		self.setLayout(grid)
		
		self.show()
		
		
	def MidiFile_DataSet_show(self):
		print("main Key : ", self.filePath)
		print("ticks_per_beat : ",self.ticks_per_beat) # resolution
		print("mainkey : ",self.mainKey)
		
	@pyqtSlot()
	
	def reset_click(self):
		for i in range(0,16):
			self.hi_het_list_btn[i].setCheckState(0)
			self.s_drum_list_btn[i].setCheckState(0)
			self.b_drum_list_btn[i].setCheckState(0)
		self.select_button.setCurrentIndex(0)
		self.filePath = '';  self.filePath_textbox.setText(self.filePath)
		
	
	def open_click(self):
		self.openFileNameDialog()
		self.filePath_textbox.setText(self.filePath)
	def openFileNameDialog(self): 
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			self.filePath = fileName # print(fileName)	

	def listen_click(self):
		print("listen click")
	def record_click(self):		
		print("record click")
	
	def select_click(self,box):
		#print(box.currentIndex())
		tmp = drumSample.get_drumList(box.currentIndex())
		for i in range(0,16):
			self.hi_het_list_btn[i].setCheckState(tmp[0][i]) 
			self.b_drum_list_btn[i].setCheckState(tmp[1][i]) 
			self.s_drum_list_btn[i].setCheckState(tmp[2][i]) 
			
	def typeSet_btn(self,b):	
		if b.checkState() == 2:
			b.setCheckState(0)
		
	def DrumOutputSample(self):
		hi_note = 42;	s_drum_note = 38;	b_drum_note = 36
		time_delta = 0.15; cnt = 0;
		
		midiout = rtmidi.MidiOut()
		available_ports = midiout.get_ports()
		
		for i in range(0,16):
			self.hi_het[i] = self.hi_het_list_btn[i].checkState()
			self.b_drum[i] = self.b_drum_list_btn[i].checkState()
			self.s_drum[i] = self.s_drum_list_btn[i].checkState()			
		durm_list = []; durm_list.append(self.hi_het); durm_list.append(self.s_drum);  durm_list.append(self.b_drum);

		if available_ports:
			midiout.open_port(0)
		else:
			midiout.open_virtual_port("My virtual output")

		for i in range(0,2):  # repeat leng times
			for i in range(0,len(durm_list[0])):	# one section tempo
				if(durm_list[0][i] or durm_list[1][i] or durm_list[2][i]):	
					time.sleep(cnt*time_delta)
					midiout.send_message( Message('note_on', note=hi_note, velocity=durm_list[0][i]*96, channel = 9).bytes() )
					midiout.send_message( Message('note_on', note=s_drum_note, velocity=durm_list[1][i]*70, channel = 9).bytes() )
					midiout.send_message( Message('note_on', note=b_drum_note, velocity=durm_list[2][i]*96, channel = 9).bytes() )
					time.sleep(time_delta)
					midiout.send_message( Message('note_on', note=hi_note, velocity=0, channel = 9).bytes() )
					midiout.send_message( Message('note_on', note=s_drum_note, velocity=0, channel = 9).bytes() )
					midiout.send_message( Message('note_on', note=b_drum_note, velocity=0, channel = 9).bytes() )
					cnt = 0
				else:
					cnt+=1
		time.sleep(time_delta)
		del midiout

		
	def drumLis_click(self):
		print("drum listen")
		t = threading.Thread(target = self.DrumOutputSample)
		t.start()
			
	def run_click(self):
		if self.filePath == "":
			self.filePath =  self.filePath_textbox.text() 
		else:
			self.filePath_textbox.setText(self.filePath)
		print(self.filePath)
		
		regular = r'([A-z]*)(.mid)' ;	p = re.compile(regular)
		if p.search(self.filePath) != None:
			if os.path.isfile( self.filePath ):
				
				for i in range(0,16):
					self.hi_het[i] = self.hi_het_list_btn[i].checkState()
					self.b_drum[i] = self.b_drum_list_btn[i].checkState()
					self.s_drum[i] = self.s_drum_list_btn[i].checkState()
					
				drumlist = []; 
				drumlist.append(self.hi_het); drumlist.append(self.s_drum);  drumlist.append(self.b_drum);
				# 整理midi樂譜
				sectionNum = cleanMidi.cleanMIDI(self.filePath)
				# 其他伴奏加入
				
				# 輸出鼓組
				drumGenerate.OutputMidi("clenaMidi.mid", drumlist, sectionNum)
				
				self.completeMsgBox()
				self.reset_click()
			else:
				self.errMsgBox("No such Midi File !!!")
		else:
			self.errMsgBox("Please select a Midi File !!!")

	def exit_click(self):
		self.close()
	
	def completeMsgBox(self):
		msgBox = QMessageBox()
		msgBox.setIcon(QMessageBox.Information)
		msgBox.setText("Your Output MidiFile is done ~")
		msgBox.setStandardButtons(QMessageBox.Ok)
		msgBox.exec_()

	def errMsgBox(self,msg):
		msgBox = QMessageBox();	msgBox.move(150,150)
		msgBox.setIcon(QMessageBox.Critical); msgBox.setStandardButtons(QMessageBox.Ok)
		msgBox.setText(msg); msgBox.exec_(); self.filePath = ''
		self.filePath_textbox.setText(self.filePath)

	def connectCheckBox(self):
		self.hi_het_list_btn[0].clicked.connect(lambda:self.typeSet_btn(self.hi_het_list_btn[0]))
		self.hi_het_list_btn[1].clicked.connect(lambda:self.typeSet_btn(self.hi_het_list_btn[1]))
		self.hi_het_list_btn[2].clicked.connect(lambda:self.typeSet_btn(self.hi_het_list_btn[2]))
		self.hi_het_list_btn[3].clicked.connect(lambda:self.typeSet_btn(self.hi_het_list_btn[3]))
		self.hi_het_list_btn[4].clicked.connect(lambda:self.typeSet_btn(self.hi_het_list_btn[4]))
		self.hi_het_list_btn[5].clicked.connect(lambda:self.typeSet_btn(self.hi_het_list_btn[5]))
		self.hi_het_list_btn[6].clicked.connect(lambda:self.typeSet_btn(self.hi_het_list_btn[6]))
		self.hi_het_list_btn[7].clicked.connect(lambda:self.typeSet_btn(self.hi_het_list_btn[7]))
		self.hi_het_list_btn[8].clicked.connect(lambda:self.typeSet_btn(self.hi_het_list_btn[8]))
		self.hi_het_list_btn[9].clicked.connect(lambda:self.typeSet_btn(self.hi_het_list_btn[9]))
		self.hi_het_list_btn[10].clicked.connect(lambda:self.typeSet_btn(self.hi_het_list_btn[10]))
		self.hi_het_list_btn[11].clicked.connect(lambda:self.typeSet_btn(self.hi_het_list_btn[11]))
		self.hi_het_list_btn[12].clicked.connect(lambda:self.typeSet_btn(self.hi_het_list_btn[12]))
		self.hi_het_list_btn[13].clicked.connect(lambda:self.typeSet_btn(self.hi_het_list_btn[13]))
		self.hi_het_list_btn[14].clicked.connect(lambda:self.typeSet_btn(self.hi_het_list_btn[14]))
		self.hi_het_list_btn[15].clicked.connect(lambda:self.typeSet_btn(self.hi_het_list_btn[15]))
		
		self.s_drum_list_btn[0].clicked.connect(lambda:self.typeSet_btn(self.s_drum_list_btn[0]))
		self.s_drum_list_btn[1].clicked.connect(lambda:self.typeSet_btn(self.s_drum_list_btn[1]))
		self.s_drum_list_btn[2].clicked.connect(lambda:self.typeSet_btn(self.s_drum_list_btn[2]))
		self.s_drum_list_btn[3].clicked.connect(lambda:self.typeSet_btn(self.s_drum_list_btn[3]))
		self.s_drum_list_btn[4].clicked.connect(lambda:self.typeSet_btn(self.s_drum_list_btn[4]))
		self.s_drum_list_btn[5].clicked.connect(lambda:self.typeSet_btn(self.s_drum_list_btn[5]))
		self.s_drum_list_btn[6].clicked.connect(lambda:self.typeSet_btn(self.s_drum_list_btn[6]))
		self.s_drum_list_btn[7].clicked.connect(lambda:self.typeSet_btn(self.s_drum_list_btn[7]))
		self.s_drum_list_btn[8].clicked.connect(lambda:self.typeSet_btn(self.s_drum_list_btn[8]))
		self.s_drum_list_btn[9].clicked.connect(lambda:self.typeSet_btn(self.s_drum_list_btn[9]))
		self.s_drum_list_btn[10].clicked.connect(lambda:self.typeSet_btn(self.s_drum_list_btn[10]))
		self.s_drum_list_btn[11].clicked.connect(lambda:self.typeSet_btn(self.s_drum_list_btn[11]))
		self.s_drum_list_btn[12].clicked.connect(lambda:self.typeSet_btn(self.s_drum_list_btn[12]))
		self.s_drum_list_btn[13].clicked.connect(lambda:self.typeSet_btn(self.s_drum_list_btn[13]))
		self.s_drum_list_btn[14].clicked.connect(lambda:self.typeSet_btn(self.s_drum_list_btn[14]))
		self.s_drum_list_btn[15].clicked.connect(lambda:self.typeSet_btn(self.s_drum_list_btn[15]))
		
		self.b_drum_list_btn[0].clicked.connect(lambda:self.typeSet_btn(self.b_drum_list_btn[0]))
		self.b_drum_list_btn[1].clicked.connect(lambda:self.typeSet_btn(self.b_drum_list_btn[1]))
		self.b_drum_list_btn[2].clicked.connect(lambda:self.typeSet_btn(self.b_drum_list_btn[2]))
		self.b_drum_list_btn[3].clicked.connect(lambda:self.typeSet_btn(self.b_drum_list_btn[3]))
		self.b_drum_list_btn[4].clicked.connect(lambda:self.typeSet_btn(self.b_drum_list_btn[4]))
		self.b_drum_list_btn[5].clicked.connect(lambda:self.typeSet_btn(self.b_drum_list_btn[5]))
		self.b_drum_list_btn[6].clicked.connect(lambda:self.typeSet_btn(self.b_drum_list_btn[6]))
		self.b_drum_list_btn[7].clicked.connect(lambda:self.typeSet_btn(self.b_drum_list_btn[7]))
		self.b_drum_list_btn[8].clicked.connect(lambda:self.typeSet_btn(self.b_drum_list_btn[8]))
		self.b_drum_list_btn[9].clicked.connect(lambda:self.typeSet_btn(self.b_drum_list_btn[9]))
		self.b_drum_list_btn[10].clicked.connect(lambda:self.typeSet_btn(self.b_drum_list_btn[10]))
		self.b_drum_list_btn[11].clicked.connect(lambda:self.typeSet_btn(self.b_drum_list_btn[11]))
		self.b_drum_list_btn[12].clicked.connect(lambda:self.typeSet_btn(self.b_drum_list_btn[12]))
		self.b_drum_list_btn[13].clicked.connect(lambda:self.typeSet_btn(self.b_drum_list_btn[13]))
		self.b_drum_list_btn[14].clicked.connect(lambda:self.typeSet_btn(self.b_drum_list_btn[14]))
		self.b_drum_list_btn[15].clicked.connect(lambda:self.typeSet_btn(self.b_drum_list_btn[15]))
		
	
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())
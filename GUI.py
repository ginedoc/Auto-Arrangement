from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QRadioButton, QCheckBox, QLineEdit, QFileDialog, QLabel, QMessageBox, QComboBox, QPlainTextEdit, QInputDialog
from PyQt5.QtGui import QIcon, QPixmap, QTextCursor
from PyQt5.QtCore import pyqtSlot, QSize, Qt, QThread
from PyQt5.QtMultimedia import QSound

import re
import sys
import os
import inspect
import time
import rtmidi
import threading
from midi2audio import FluidSynth
from mido import Message

from SourceCode.setup import Setup
from SourceCode.rec_classes import CK_rec

import SourceCode.drumSample as drumSample
import SourceCode.drumGenerate as drumGenerate
import SourceCode.midiscore as midiscore
import SourceCode.sectionNumber as sectionNumber


class App(QWidget):
	
	filePath = ''; guiObject = [];
	hi_het = [0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0]; 
	s_drum = [0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0]; 
	b_drum = [0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0];
	hi_het_list_btn = []; 
	s_drum_list_btn = []; 
	b_drum_list_btn = [];
	recording = 0

	modelName = ["model/model_pop.h5","model/model_Jazz.h5","model/model_classical.h5"]    #到時model的正確位置要打好
	drumType = 0; ignore_pos = [3,7,8,12]

	def __init__(self):
		super().__init__()
		self.initUI()
	
	def lockGUI(self):
		for item in self.guiObject:
			item.setDisabled(True)
		for i in range(0,len(self.s_drum_list_btn)):
			self.hi_het_list_btn[i].setDisabled(True)
			self.s_drum_list_btn[i].setDisabled(True)
			self.b_drum_list_btn[i].setDisabled(True)
		self.record_button.setText("停止錄音")
		
			
	def unlockGUI(self):
		for item in self.guiObject:
			item.setDisabled(False)
		for i in range(0,len(self.s_drum_list_btn)):
			self.hi_het_list_btn[i].setDisabled(False)
			self.s_drum_list_btn[i].setDisabled(False)
			self.b_drum_list_btn[i].setDisabled(False)
		self.record_button.setText("錄製")
		
	
	def hideDurmBtn(self):
		for i in self.ignore_pos:
			self.hi_het_list_btn[i].setVisible(False)
			self.s_drum_list_btn[i].setVisible(False)
			self.b_drum_list_btn[i].setVisible(False)
	
	def showDurmBtn(self):
		for i in self.ignore_pos:
			self.hi_het_list_btn[i].setVisible(True)
			self.s_drum_list_btn[i].setVisible(True)
			self.b_drum_list_btn[i].setVisible(True)
	
	def finishRecording(self):
		self.recording = 0;	
		name, ok = QInputDialog.getText(self, '', 'Save midi recording as?')
		if ok:
			print("FILE NAME : ", name)
			if name != "":
				self.midiRec.saveTrack(name)
				self.filePath_textbox.setText("Recordings/rec/" + name + '.mid')
			else :
				self.midiRec.saveTrack("default")
				self.filePath_textbox.setText("Recordings/rec/default.mid")	
			self.filePath = self.filePath_textbox.text()
			self.codeK.end()
			self.NoticeMsgBox("錄音完成，請按下OK後繼續操作"); 
		self.unlockGUI()
	
	
	def keyPressEvent(self, qKeyEvent):
		if self.recording == 1:
			if qKeyEvent.key() == Qt.Key_Return:
				print(qKeyEvent.key(),"Enter pressed - STOP RECORDING")
				self.finishRecording()
			else:
				print(qKeyEvent.key())
	
	
	def fileOpen_GUI(self,layout):
		grid = QGridLayout();	grid.setSpacing(10)
		
		# FILE OPEN
		self.label_selectFile = QLabel("請選擇一個MIDI檔案：",self)
		grid.addWidget(self.label_selectFile,0,0,1,8)
		# file path textbox
		self.filePath_textbox = QLineEdit(self)
		grid.addWidget(self.filePath_textbox, 1, 0, 1, 8)
		# open button
		self.open_button = QPushButton('開啟', self)
		grid.addWidget(self.open_button, 1, 9, 1, 1)
		self.open_button.clicked.connect(self.open_click)
		# listen button
		self.listen_button = QPushButton('試聽', self)
		grid.addWidget(self.listen_button, 1, 10, 1, 1)
		self.listen_button.clicked.connect(self.listen_click)
		
		self.guiObject.append(self.label_selectFile)
		self.guiObject.append(self.filePath_textbox);
		self.guiObject.append(self.open_button);
		self.guiObject.append(self.listen_button);
		
		
		# RECORDING
		self.label_deviceChoose = QLabel("MIDI device you are choosing : ",self)
		grid.addWidget(self.label_deviceChoose,2,0,1,2)
		# port select QLineEdit
		self.portSel = QLineEdit(self)
		self.portSel.setText('null')
		self.portSel.setDisabled(True)
		grid.addWidget(self.portSel, 2, 2, 1, 6)
		# port select button
		self.portSel_button = QPushButton('選擇', self)
		grid.addWidget(self.portSel_button, 2, 9, 1, 1)
		self.portSel_button.clicked.connect(self.sel_click)
		# record button
		self.record_button = QPushButton('錄製', self)
		grid.addWidget(self.record_button, 2, 10, 1, 1)
		self.record_button.clicked.connect(self.record_click)

		self.guiObject.append(self.label_deviceChoose)
		#self.guiObject.append(self.portSel);
		self.guiObject.append(self.portSel_button);
		#self.guiObject.append(self.record_button);
		
		layout.addLayout(grid)		
	
	def excute_GUI(self,layout):
		grid = QGridLayout()
		
		# drum listen button
		self.listen_button = QPushButton('鼓組試聽', self)
		grid.addWidget(self.listen_button,0,5,1,1)
		self.listen_button.clicked.connect(self.drumLis_click)
	
		# reset button 
		self.reset_button = QPushButton('Reset', self)
		grid.addWidget(self.reset_button,1,0,1,2)
		self.reset_button.clicked.connect(self.reset_click)
		# run button
		self.run_button = QPushButton('Run', self)
		grid.addWidget(self.run_button,1,2,1,2)
		self.run_button.clicked.connect(self.run_click)
		# exit button
		self.exit_button = QPushButton('Exit', self)
		grid.addWidget(self.exit_button,1,4,1,2)
		self.exit_button.clicked.connect(self.exit_click)	
		
		
		self.guiObject.append(self.listen_button)
		self.guiObject.append(self.reset_button)
		self.guiObject.append(self.run_button)
		self.guiObject.append(self.exit_button)
		
		layout.addLayout(grid)
	
	def drumBtn_GUI(self,layout):
	
		a = 16; cnt = 0
		grid = QGridLayout(); grid.setVerticalSpacing(11)
		self.label_selectDrum = QLabel("請選擇鼓組(以16分音符為一單位)：")
		grid.addWidget(self.label_selectDrum,0,0,1,50)
		
		
		# add new drum sample in there
		self.select_comboBox = QComboBox(self)
		grid.addWidget(self.select_comboBox, 1, 0, 1 ,50)
		self.select_comboBox.addItem("Empty")
		self.select_comboBox.addItem("POP Sample 1")
		self.select_comboBox.addItem("POP Sample 2")
		self.select_comboBox.addItem("JAZZ Sample 1")
		self.select_comboBox.addItem("JAZZ Sample 2")
		self.select_comboBox.currentIndexChanged.connect(lambda:self.select_click(self.select_comboBox))	
		
		
		pic = QPixmap("Pic/drum.jpg").scaled(QSize(600,120))
		self.bgPic = QLabel("123",self);  self.bgPic.setPixmap(pic)	
		grid.addWidget(self.bgPic,2,0,10,50)
		for i in range(0,16):
			if i%4==0:
				cnt+=3
			self.hi_het_list_btn.append(QCheckBox("",self));  grid.addWidget(self.hi_het_list_btn[i],2,a+i+cnt,1,1)
			self.s_drum_list_btn.append(QCheckBox("",self));  grid.addWidget(self.s_drum_list_btn[i],4,a+i+cnt,1,1)
			self.b_drum_list_btn.append(QCheckBox("",self));  grid.addWidget(self.b_drum_list_btn[i],6,a+i+cnt,1,1)
			self.hi_het_list_btn[i].setTristate(True);	self.s_drum_list_btn[i].setTristate(True);	self.b_drum_list_btn[i].setTristate(True); 
			
		self.guiObject.append(self.label_selectDrum)
		self.guiObject.append(self.select_comboBox)
		self.guiObject.append(self.bgPic)
		self.connectCheckBox()
		
		layout.addLayout(grid)
	
	def modelSelect_GUI(self,layout):
		grid = QGridLayout(); grid.setVerticalSpacing(11)
		self.label_selectStyle = QLabel("請選訓練模板：")
		grid.addWidget(self.label_selectStyle,0,0,1,50)
	
		self.select_Style = QComboBox(self)
		grid.addWidget(self.select_Style, 1, 0, 1 ,50)
		self.select_Style.addItem("POP")
		self.select_Style.addItem("JAZZ")
		self.select_Style.addItem("CLASSICAL")
		
		layout.addLayout(grid)
	
	def record_setup(self):
		currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
		parentdir = os.path.dirname(currentdir)
		sys.path.insert(0,parentdir)
		self.codeK = Setup()
		
	def initUI(self):
		self.setWindowTitle('自動伴奏產生器')

		grid = QVBoxLayout(); 
		self.fileOpen_GUI(grid)	
		self.modelSelect_GUI(grid)
		self.drumBtn_GUI(grid)
		self.excute_GUI(grid)
		self.setLayout(grid)
		self.show(); self.setFixedSize(self.size())
		
		self.record_setup()
		
	@pyqtSlot()
	
	def reset_click(self):
		self.filePath = '';  self.filePath_textbox.setText(self.filePath)
		self.portSel.setText('null'); 
		self.select_comboBox.setCurrentIndex(0)
		for i in range(0,16):
			self.hi_het_list_btn[i].setCheckState(0)
			self.s_drum_list_btn[i].setCheckState(0)
			self.b_drum_list_btn[i].setCheckState(0)
		self.select_Style.setCurrentIndex(0); 
		
		
	def open_click(self):
		self.openFileNameDialog()
		self.filePath_textbox.setText(self.filePath)
	def openFileNameDialog(self): 
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", ".","All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			self.filePath = fileName # print(fileName)	

			
	# MIDI檔案試聽
	def listen_click(self):
		print("listen click")
		#self.filePath
		t = threading.Thread(target = self.test_listen); t.start() 
	def test_listen(self):
            os.system('fluidsynth --audio-driver=alsa -i /usr/share/soundfonts/FluidR3_GM.sf2 '+ self.filePath)
        
	#選擇輸入的port
	def sel_click(self):
		self.codeK = Setup()
		self.items = self.codeK.get_ports()
		self.items.append('null') 
		#self.items.append('0')  #到時需刪除
		print(self.items)
	
		item, ok = QInputDialog.getItem(self, "", "List of ports", self.items, 0, False)
		if ok and item:
			self.portSel.setText(item)
			self.myPort = self.items.index(item)
		del self.items[:]
		
	#需再測試		
	def record_click(self):		
		print("record click");
		if self.recording == 0:		
			if self.portSel.text() == 'null':
				print("error midi device")
				self.errMsgBox("Error midi device")
			else:
				print("record set"); 
				
				#myPort = int(self.portSel.text()); print(myPort)
				print("myPort : ",self.myPort," ",self.portSel.text())
				self.codeK = Setup()
				self.codeK.open_port(self.myPort)	
				
				
				if self.NoticeMsgBox("OK後，請隨意按下一個keyboard上的鍵盤") == QMessageBox.Ok: 
					on_id = self.codeK.get_device_id();  print("on_id : ", on_id) 
					if self.NoticeMsgBox("準備開始錄音....\n－按下OK即可開始錄製\n－按下ENTER即可停止錄音") == QMessageBox.Ok:
						self.midiRec = CK_rec(self.myPort, on_id, debug=True)
						self.codeK.set_callback(self.midiRec)
						self.lockGUI()		
						self.recording = 1;	
						t = threading.Thread(target = self.record_start); t.start()
		elif self.recording == 1:
			self.finishRecording()
	def record_start(self):
		print("record_start")		
		while self.recording == 1:
			time.sleep(0.001)
		print("End Recording")  		
		
	
	def select_click(self,box):   # ComboBox select clicked
		#print(box.currentIndex())
		if box.currentIndex()<3:
			self.drumType = 0;
			self.showDurmBtn()
		else:
			self.drumType = 1;
			self.hideDurmBtn()
		print(self.drumType)
		
		tmp = drumSample.get_drumList(box.currentIndex())
		print(tmp)
		if self.drumType == 0:
			for i in range(0,16):
				self.hi_het_list_btn[i].setCheckState(tmp[0][i])
				self.s_drum_list_btn[i].setCheckState(tmp[1][i])
				self.b_drum_list_btn[i].setCheckState(tmp[2][i]) 
		elif self.drumType == 1:
			cnt = 0
			for i in range(0,16):
				if i in self.ignore_pos:
					self.hi_het_list_btn[i].setCheckState(0) 
					self.s_drum_list_btn[i].setCheckState(0) 
					self.b_drum_list_btn[i].setCheckState(0) 
				else:
					self.hi_het_list_btn[i].setCheckState(tmp[0][cnt]) 
					self.s_drum_list_btn[i].setCheckState(tmp[1][cnt])
					self.b_drum_list_btn[i].setCheckState(tmp[2][cnt])
					cnt+=1;
			
	def typeSet_btn(self,b):	
		if b.checkState() == 2:
			b.setCheckState(0)
		
	def drumLis_click(self):
		print("drum listen")
		self.listen_button.setDisabled(True)
		t = threading.Thread(target = self.DrumOutputSample);	t.start()
	def DrumOutputSample(self):
		hi_note = 42;	s_drum_note = 38;	b_drum_note = 36

		midiout = rtmidi.MidiOut()
		available_ports = midiout.get_ports()
		print(available_ports,midiout)

		if available_ports:
			midiout.open_port(0)
			print('open 0')
		else:
			midiout.open_virtual_port("My virtual output")
			print('My virtual')

		for i in range(0,16):
			self.hi_het[i] = self.hi_het_list_btn[i].checkState()
			self.b_drum[i] = self.b_drum_list_btn[i].checkState()
			self.s_drum[i] = self.s_drum_list_btn[i].checkState()			
		durm_list = []; durm_list.append(self.hi_het); durm_list.append(self.s_drum);  durm_list.append(self.b_drum);
			
		if self.drumType == 0:
			time_delta = 0.15; cnt = 0;
			for i in range(0,2):  # repeat leng times
				for i in range(0,16):	# one section tempo
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
			
		elif self.drumType == 1:
			time_delta = 0.2; cnt = 0;			
			for i in range(0,2):  # repeat leng times
				for i in range(0,16):	# one section tempo
					if (i in self.ignore_pos):
						continue;				
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
		
		self.listen_button.setDisabled(False)
		del midiout
		
		
	
	def run_click(self):
		#print(model)
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
				os.system('mscore ' + self.filePath + ' -o ' + 'Recordings/cleanMidi.mid')
				sectionNum = sectionNumber.secNum('Recordings/cleanMidi.mid')
				
				outpath = self.save_output()
				outpath = outpath 
				# 其他伴奏加入
				popoSong = midiscore.song('Recordings/cleanMidi.mid')              		
				popoChord = popoSong.chord_estimation(self.modelName[self.select_Style.currentIndex()])     #此處可能要修改
				popoSong.add_accompaniant(popoChord, 35)    # bass
				popoSong.add_accompaniant(popoChord, 5)     # piano
				

				# 輸出鼓組
				drumGenerate.OutputMidi(outpath, "mymidi.mid", drumlist, sectionNum,self.drumType)
				os.remove("mymidi.mid")
				
				self.NoticeMsgBox("Your File has been saved to **output/" + os.path.basename(outpath)+ "**")
				self.reset_click()
				os.system('mscore ' + outpath)
			else:
				self.errMsgBox("No such Midi File !!!")
		else:
			self.errMsgBox("Please select a Midi File !!!")

	def save_output(self): 
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self, "save output", "output/", "midi (*.mid)")
		if fileName:  return fileName        
	def exit_click(self):
		self.close()
	
	def NoticeMsgBox(self,msg):
		msgBox = QMessageBox();	#msgBox.move(150,150)
		msgBox.setIcon(QMessageBox.Information); msgBox.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
		msgBox.setText(msg);
		return msgBox.exec_()

	def errMsgBox(self,msg):
		self.filePath = '';	self.filePath_textbox.setText(self.filePath)
		msgBox = QMessageBox();	#msgBox.move(150,150)
		msgBox.setIcon(QMessageBox.Critical); msgBox.setStandardButtons(QMessageBox.Ok)
		msgBox.setText(msg); 
		return msgBox.exec_(); 

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

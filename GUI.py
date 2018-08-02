import os.path
import re
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QRadioButton, QCheckBox, QLineEdit, QFileDialog, QLabel, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QSize

import SourceCode.globalVar as gl
import MidiFile_DataSet 
import MidiFile_ExpendtoPianoRoll 
import MidiFile_ExporttheResult


class App(QWidget):
	
	hi_het = [1,0,1,0,1,0,1,0, 1,0,1,0,1,0,1,0]
	s_drum = [0,0,0,0,1,0,0,0, 0,1,0,0,1,0,0,0]
	b_drum = [0,0,0,0,1,0,0,0, 0,0,0,0,1,0,0,0]
	
	hi_het_list_btn = []; s_drum_list_btn = []; b_drum_list_btn = []
	

	def __init__(self):
		super().__init__()
		self.initUI()

	def fileOpen_GUI(self,layout):
		grid = QGridLayout()
		grid.setSpacing(10)
		# file path textbox
		self.filePath_textbox = QLineEdit(self)
		grid.addWidget(self.filePath_textbox, 0, 0, 1, 8)
		# open button
		open_button = QPushButton('Open File', self)
		grid.addWidget(open_button, 0, 8, 1, 2)
		open_button.clicked.connect(self.open_click)
		
		layout.addLayout(grid)
		
	def excute_GUI(self,layout):
		grid = QGridLayout()
		# listen button
		listen_button = QPushButton('鼓組試聽', self)
		grid.addWidget(listen_button,0,5,1,1)
			#reset_button.clicked.connect(self.reset_click)
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
	
	def accompanyType_GUI(self,layout):
		grid = QGridLayout()
		grid.setSpacing(10)
		# accompany type ration button 
		self.acc_0 = QRadioButton("1",self);		grid.addWidget(self.acc_0,2,0,1,1)
		self.acc_0.toggled.connect(lambda:self.typeSet(self.acc_0))
		self.acc_1 = QRadioButton("2",self);		grid.addWidget(self.acc_1,4,0,1,1)
		self.acc_1.toggled.connect(lambda:self.typeSet(self.acc_1))
		self.acc_0.setChecked(True)
		gl.set_disassembleType(0)
		# accompany type pic 
		accompany_0 = QPushButton('', self);	accompany_0.setEnabled(False)
		accompany_0.setFixedSize(400,100);		grid.addWidget(accompany_0,1,1,2,3)
		accompany_0.setIcon(QIcon("SourceFile/1.jpg"));	accompany_0.setIconSize(QSize(400,100))
		accompany_1 = QPushButton('', self);	accompany_1.setEnabled(False)
		accompany_1.setFixedSize(400,100);		grid.addWidget(accompany_1,3,1,2,3)
		accompany_1.setIcon(QIcon("SourceFile/2.jpg"));	accompany_1.setIconSize(QSize(400,100))
		
		
		layout.addLayout(grid)
		
	
	
	def drumBtn_GUI(self,layout):
		a = 25; cnt = 0
		grid = QGridLayout(); grid.setVerticalSpacing(11)
		pic = QPixmap("SourceFile/drum.jpg").scaled(QSize(450,100))
		bgPic = QLabel("123",self);  bgPic.setPixmap(pic)
		grid.addWidget(bgPic,0,0,10,50)
		
		for i in range(0,16):
			if i%4==0:
				cnt+=1
			self.hi_het_list_btn.append(QCheckBox("",self));  grid.addWidget(self.hi_het_list_btn[i],0,a+i+cnt,1,1)
			self.s_drum_list_btn.append(QCheckBox("",self));  grid.addWidget(self.s_drum_list_btn[i],2,a+i+cnt,1,1)
			self.b_drum_list_btn.append(QCheckBox("",self));  grid.addWidget(self.b_drum_list_btn[i],4,a+i+cnt,1,1)
			self.hi_het_list_btn[i].setTristate(True); self.hi_het_list_btn[i].setCheckState(gl.get_hiHet(i))
			self.s_drum_list_btn[i].setTristate(True); self.s_drum_list_btn[i].setCheckState(gl.get_sDrum(i))
			self.b_drum_list_btn[i].setTristate(True); self.b_drum_list_btn[i].setCheckState(gl.get_bDrum(i))
			
			# self.b_drum_list_btn[i].clicked.connect(lambda:self.typeSet(self.b_drum_list_btn[i]))
			
		layout.addLayout(grid)
	
	def initUI(self):
		self.setWindowTitle('自動伴奏產生器')

		grid = QVBoxLayout(); #grid.setSpacing(10)
		grid.addWidget(QLabel("請選擇一個MIDI檔案：",self))
		self.fileOpen_GUI(grid)
		grid.addWidget(QLabel("請選擇和弦拆解方式：",self))
		self.accompanyType_GUI(grid)
		grid.addWidget(QLabel("請輸入鼓組(以16分音符為一單位)：",self))
		self.drumBtn_GUI(grid)
		self.excute_GUI(grid)

		
		
		self.setLayout(grid)
		self.show()
		
		
	def MidiFile_DataSet_show(self):
				
		print("main Key : ", gl.get_mainKey())
		print("ticks_per_beat : ",gl.get_ticks_per_beat()) # resolution
		print("midi length : ", gl.get_midi_length())
		print("Type : ",gl.get_disassembleType())
				
	
		
	@pyqtSlot()
	
	def reset_click(self):
		for i in range(0,16):
			self.hi_het_list_btn[i].setCheckState(gl.get_hiHet(i))
			self.s_drum_list_btn[i].setCheckState(gl.get_sDrum(i))
			self.b_drum_list_btn[i].setCheckState(gl.get_bDrum(i))
		self.acc_0.setChecked(True)
		gl.set_pathName(""); self.filePath_textbox.setText(gl.get_pathName())
	
	def open_click(self):
		self.openFileNameDialog()
		self.filePath_textbox.setText(gl.get_pathName())
	def openFileNameDialog(self): 
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			gl.set_pathName(fileName)
			# print(gl.get_pathName())	

	def run_click(self):
		if gl.get_pathName() == "":
			gl.set_pathName( self.filePath_textbox.text() )
		else:
			self.filePath_textbox.setText(gl.get_pathName())
		print(gl.get_pathName())
		
		regular = r'([A-z]*)(.mid)' ;	p = re.compile(regular)
		if p.search(gl.get_pathName()) != None:
			if os.path.isfile( gl.get_pathName() ):
				print("reslolution is 8")
				gl.set_resolution(8)		
				
				print("\nIn MidiFile_DataSet : ");	
				MidiFile_DataSet.initMIDIdata()		
				self.MidiFile_DataSet_show()
				
				for i in range(0,16):
					self.hi_het[i] = self.hi_het_list_btn[i].checkState()
					self.b_drum[i] = self.b_drum_list_btn[i].checkState()
					self.s_drum[i] = self.s_drum_list_btn[i].checkState()
				for i in range(0,16):
					print(self.hi_het[i],self.b_drum[i],self.s_drum[i])
					
				
				print("\nIn MidiFile_ExpendtoPianoRoll : ")
				MidiFile_ExpendtoPianoRoll.Generate_input_data()
				
				print("\nIn MidiFile_ExporttheResult : ")
				chordlist = ['C','G','C','C','G','G','C','C','C','C','C','C','G','G','C','C']
				drumlist = []
				drumlist.append(self.hi_het); drumlist.append(self.s_drum);  drumlist.append(self.b_drum);
				MidiFile_ExporttheResult.OutputMidi(chordlist,drumlist)
				
				self.completeMsgBox()
				self.reset_click()
			else:
				self.errMsgBox("No such Midi File !!!")
		else:
			self.errMsgBox("Please select a Midi File !!!")
		
		#os.system('musescore ' + self.file_name)
	def exit_click(self):
		self.close()

	def typeSet(self,btn):
		if btn.text()=='1':
			gl.set_disassembleType(0)
		else:
			gl.set_disassembleType(1)
	
	def typeSet_btn(self,b):	
		print("change",b.checkState())
		if b.checkState() == 2:
			print("change2")
			b.setCheckState(0)
	
	
	def completeMsgBox(self):
		msgBox = QMessageBox()
		msgBox.setIcon(QMessageBox.Information)
		msgBox.setText("Your Output MidiFile is done ~")
		msgBox.setStandardButtons(QMessageBox.Ok)
		msgBox.exec_()

	def errMsgBox(self,msg):
		msgBox = QMessageBox();	msgBox.move(150,150)
		msgBox.setIcon(QMessageBox.Critical); msgBox.setStandardButtons(QMessageBox.Ok)
		msgBox.setText(msg); msgBox.exec_(); gl.set_pathName("")
		self.filePath_textbox.setText(gl.get_pathName())

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())
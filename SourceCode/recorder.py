import time
import rtmidi
import sys
import os
import inspect
from CK_rec.setup import Setup
from CK_rec.rec_classes import CK_rec


def record(textBox):
	
	currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	parentdir = os.path.dirname(currentdir)
	sys.path.insert(0,parentdir)
	
	# Start the Device
	codeK = Setup(textBox)
	myPort = codeK.perform_setup()
	codeK.open_port(myPort)

	
	on_id = codeK.get_device_id()
	print('your note on id is: ', on_id)
	
	# record
	midiRec = CK_rec(myPort, on_id, debug=False)
	codeK.set_callback(midiRec)


	# Loop to program to keep listening for midi input
	try:
		while True:
			time.sleep(0.001)
	except KeyboardInterrupt:
		print('')
	finally:
		name = input('\nsave midi recording as? (leaving the name blank discards the recording): ')
		if name != "":
			midiRec.saveTrack(name)
		codeK.end()
		return "Recordings/" + name + '.mid'
	

import time
import rtmidi
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QTextCursor

class Setup(object):


    def __init__(self, textbox):
        self.__midiin = rtmidi.MidiIn()
        self.__midiout = rtmidi.MidiOut()
        self.__ports = self.__midiin.get_ports()
        self.__ports_out = self.__midiout.get_ports()
        self.textBox = textbox
		self.selected_midiport = -1

    def print_welcome(self):
        print('');
        for i in range(1, 6):
            string = "####"
            space = " ";
            if i == 1:
                print(string[:4] + space + string[:1] + space*2 + string[:1] + space*4 + string[:4] + space + string[:4] + space + string[:4])
            elif i == 2:
                print(string[:1] + space*4 + string[:1] + space + string[:1] + space*5 + string[:1] + space*2 + string[:1] + space + string[:1] + space*4 + string[:1])
            elif i == 3:
                print(string[:1] + space*4 + string[:2]+ space*6 + string[:4] + space + string[:4] + space + string[:1])
            elif i == 4:
                print(string[:1] + space*4 + string[:1] + space + string[:1] + space*5 + string[:1] + space + string[:1] + space*2 + string[:1] + space*4 + string[:1])
            elif i == 5:
                print(string[:4] + space + string[:1] + space*2 + string[:1] + space*4 + string[:1] + space*2 + string[:1] + space + string[:4] + space + string[:4])

        print("\nWelcome to the Codeklavier MIDI Recorder!\n")
        self.textBox.setPlainText("Welcome to the Codeklavier MIDI Recorder!\n")

    def show_ports(self):
        print("These are your detected MIDI devices:\n")
        text = self.textBox.toPlainText()
        self.textBox.setPlainText(text+"These are your detected MIDI devices:\n")
        
        for port in self.__ports:
            text = self.textBox.toPlainText()
            print(self.__ports.index(port), " -> ", port)
            self.textBox.setPlainText(text + "    " + str(self.__ports.index(port)) + " -> " + port + "\n")			
        self.textBox.moveCursor(QTextCursor.End)
	
	def get_port_from_user(self):
		#self.selected_midiport = -1
        while self.selected_midiport < 0:
            try:
                #choice = input("Please choose the MIDI device (number) you want to use and hit Enter:")
                #self.selected_midiport = int(choice)
                if self.selected_midiport < 0 or self.selected_midiport >= len(self.__ports):
                    print("Invalid number, please try again:")
                    self.selected_midiport = -1
                else:
                    return self.selected_midiport
            except KeyboardInterrupt:
                print('\n', "You want to quit? ¯\('…')/¯  ok, Bye bye.")
                exit()
            except ValueError:
                print("Sorry, type a valid port numer!")
	
	'''
    def get_port_from_user(self):
	
        selected_midiport = -1
        while selected_midiport < 0:
            try:
                choice = input("Please choose the MIDI device (number) you want to use and hit Enter:")
                selected_midiport = int(choice)
                if selected_midiport < 0 or selected_midiport >= len(self.__ports):
                    print("Invalid number, please try again:")
                    selected_midiport = -1
                else:
                    return selected_midiport
            except KeyboardInterrupt:
                print('\n', "You want to quit? ¯\('…')/¯  ok, Bye bye.")
                exit()
            except ValueError:
                print("Sorry, type a valid port numer!")
	'''
	
    def open_port(self, pnum):
        print("You have chosen: ", self.__ports[pnum])

        if self.__ports:
            #TODO: do we need to check on the existence of ports?
            self.__midiin.open_port(pnum)
            # ignore sysex, timing and active sense messages
            self.__midiin.ignore_types(True, True, False)
        else:
            raise Exception("No midi ports! Maybe open a virtual device?")

    def open_port_out(self, num):
        print("opened midi out port")

        if self.__ports_out:
            self.__midiout.open_port(num)

    def close_port(self):
        self.__midiin.close_port()
        #TODO: add close out port too

    def get_message(self):
        return self.__midiin.get_message()

    def send_message(self, message):
        return self.__midiout.send_message(message)

    def set_callback(self,cb):
        self.__midiin.set_callback(cb)

    def get_device_id(self):
        print("Hit any note to get the device_id.")
        while True:
            msg = self.get_message()
            if msg:
                message, deltatime = msg
                if message[0] != 254: #active sense ignore
                    device_id = message[0]
                    if device_id:
                        return device_id

    def perform_setup(self):
        self.print_welcome()
        self.show_ports()
        myPort = self.get_port_from_user()
        return myPort

    def end(self):
        print("Bye bye from CodeKlavier Recorder! see you next time 🎹\n")
        self.close_port()
        del self.__midiin

def start_record():
    codeK = Setup()
    my_midiport = codeK.perform_setup()
    codeK.open_port(my_midiport)

    if my_midiport >= 0:
        print("CodeKlavier is ON. Showing incoming MIDI messages. Press Control-C to exit.")
        try:
            timer = time.time()
            while True:
                msg = codeK.get_message()

                if msg:
                    message, deltatime = msg
                    print('deltatime: ', deltatime, 'msg: ', message)

                time.sleep(0.01)

        except KeyboardInterrupt:
            print('')
        finally:
            codeK.end()


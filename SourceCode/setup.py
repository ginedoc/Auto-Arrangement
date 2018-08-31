import rtmidi

class Setup(object):
    def __init__(self):
        self.__midiin = rtmidi.MidiIn()
        self.__midiout = rtmidi.MidiOut()
        self.__ports = self.__midiin.get_ports()
        self.__ports_out = self.__midiout.get_ports()

    def get_ports(self):
        return self.__ports
	
    def open_port(self, pnum):
        print("You have chosen: ", self.__ports[pnum])
        if self.__ports:
            self.__midiin.open_port(pnum)
            self.__midiin.ignore_types(True, True, False)
        else:
            raise Exception("No midi ports! Maybe open a virtual device?")

    def get_device_id(self):
        print("Hit any note to get the device_id.")
        while True:
            msg = self.get_message()
            if msg:
                message, deltatime = msg;     print("message")
                if message[0] != 254:  #active sense ignore
                    device_id = message[0]
                    if device_id:
                        return device_id	
    def get_message(self):
        return self.__midiin.get_message()

    def set_callback(self,cb):
        self.__midiin.set_callback(cb)

    def end(self):
        print("Bye bye ,see you next time ~~\n")
        self.close_port()
        #del self.__midiin

    def close_port(self):
        self.__midiin.close_port()
        #TODO: add close out port too		
		
	
    #NO USED
    def open_port_out(self, num):
        print("opened midi out port")
        if self.__ports_out:
            self.__midiout.open_port(num)

    def send_message(self, message):
        return self.__midiout.send_message(message)
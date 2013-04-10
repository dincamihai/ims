#!/usr/bin/env python
import dbus
import dbus.service
import sys
import gobject
import json
from dbus.mainloop.glib import DBusGMainLoop

counter = {}

class Emitter(dbus.service.Object):

    def __init__(self, object_path):
        dbus.service.Object.__init__(self, dbus.SessionBus(), '/org/ikook/ims')

    @dbus.service.signal(dbus_interface='org.ikook.ims', rel_path_keyword='value')
    def test(self, value):
        pass

def notifications(account, sender, message, conversation, flags):
    global counter
    if counter.get(conversation, None) is not None:
        counter[conversation]+= 1
    else:
        counter[conversation]=1
    global e
    e.test('yellow')

def reseter(conv, type):
    global counter
    counter[conv] = 0;
    result = reduce(lambda x, y: x+y, counter.values())
    if result == 0:
        e.test('green')

def test(*args):
    print json.dumps(args, indent=4)

DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()

e = Emitter('/abc')

obj = bus.get_object('im.pidgin.purple.PurpleService', '/im/pidgin/purple/PurpleObject')
purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")

bus.add_signal_receiver(notifications,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="ReceivedImMsg")
bus.add_signal_receiver(reseter,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="ConversationUpdated")


mainloop = gobject.MainLoop()
mainloop.run()

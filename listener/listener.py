#!/usr/bin/env python
import dbus
import dbus.service
import sys
import gobject
import json
import time
from dbus.mainloop.glib import DBusGMainLoop

counter = {}
conversations = {}
received_timestamps = {}
timestamp = 0;

class Emitter(dbus.service.Object):

    def __init__(self, object_path):
        dbus.service.Object.__init__(self, dbus.SessionBus(), '/org/ikook/ims')

    @dbus.service.signal(dbus_interface='org.ikook.ims', rel_path_keyword='value')
    def test(self, value, conv):
        received_timestamps[conv] = time.time()

def notifications(account, sender, message, conversation, flags):
    global counter
    if counter.get(conversation, None) is not None:
        counter[conversation]+= 1
    else:
        counter[conversation]=1
    global e
    result = reduce(lambda x, y: x+y, counter.values(), 0)
    print 'increase: ', conversation, 'result: ', result
    e.test(True, conversation)

def reseter(conv, type=None):
    global counter
    timestamp = received_timestamps.get(conv, time.time())
    delta = time.time() - timestamp
    if delta > 0.5:
        counter[conv] = 0;
    result = reduce(lambda x, y: x+y, counter.values(), 0)
    if result == 0:
        print 'reset: ', conv, 'result: ', result
        e.test(False, conv)

def reset_on_writing(*args):
    print 'reset on WritingImMsg'
    reseter(args[3]);

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
bus.add_signal_receiver(reseter,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="ConversationSwitched")
bus.add_signal_receiver(reset_on_writing,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="WritingImMsg")


mainloop = gobject.MainLoop()
mainloop.run()

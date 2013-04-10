ims
===

python script that sends dbus signals with the number of Pidgin IMs received (dbus listener)

add this to ~/.config/awesome/rc.lua

imwidget = widget({ type = "textbox", name="ims" })
dbus.request_name("session", "org.ikook.ims")
dbus.add_match("session", "interface='org.ikook.ims',member='test'")
dbus.add_signal("org.ikook.ims", function (signal, value)
    local file = io.open("/home/mihai/out.txt", "w")
    local json = require("dkjson")
    local str = json.encode(arg)
    local format = "<span background='red' foreground='black'>IM:%s</span>"
    imwidget.text = string.format(format, value)
end)

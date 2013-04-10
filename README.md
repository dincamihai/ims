ims
===

python script that sends dbus signals with the number of Pidgin IMs received (dbus listener)

add this to ~/.config/awesome/rc.lua

-- Create im widget
imwidget = widget({ type = "textbox", name="ims" })
imwidget:add_signal("button::press", function()
    local file = io.open("/home/mihai/out.txt", "w")
    file:write('shit')
    local format = "<span background='red' foreground='black'>IM:%s</span>"
    imwidget.text = string.format(format, 0)
end)
dbus.request_name("session", "org.ikook.ims")
dbus.add_match("session", "interface='org.ikook.ims',member='test'")
dbus.add_signal("org.ikook.ims", function (signal, value, color)
    local format = "<span background='%s' foreground='black'>IM</span>"
    imwidget.text = string.format(format, value)
end)

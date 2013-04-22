ims
===

python script that sends dbus signals with the number of Pidgin IMs received (dbus listener)

add this to ~/.config/awesome/rc.lua

``` lua
--Blinkers
blinkers = {}
function blinking(tb,iv)
    if (tb==nil) then 
        return
    end
    local fiv = iv or 1
    if blinkers[tb] then
        if blinkers[tb].timer.started then
            blinkers[tb].timer:stop()
        else
            blinkers[tb].timer:start()
        end
    else
        if (tb.text == nil) then
            return
        end
        blinkers[tb]= {}
        blinkers[tb].timer = timer({timeout=fiv})
        blinkers[tb].text = tb.text
        blinkers[tb].empty = 0

        blinkers[tb].timer:add_signal("timeout", function ()
            if (blinkers[tb].empty==1) then
                tb.text = blinkers[tb].text
                blinkers[tb].empty=0
            else
                blinkers[tb].empty=1
                tb.text = ""
            end
        end)

        blinkers[tb].timer:start()

    end
end

-- Pidgin widget
--bashets.set_script_path("/dev/shm/bashets/")
--bashets.set_temporary_path("/dev/shm/tmp/")
is_blinking = false
imwidget = widget({ type = "textbox", name="ims" })
imwidget:buttons(awful.util.table.join(
   awful.button({ }, 1, function ()
        imwidget.text = nil
        is_blinking = false
        blinking(imwidget, .5)
   end)
 ))
dbus.request_name("session", "org.ikook.ims")
dbus.add_match("session", "interface='org.ikook.ims',member='test'")
dbus.add_signal("org.ikook.ims", function (signal, value)
    if value~=false then
        local format = "<span foreground='green' font='20'>✉</span>"
        imwidget.text = string.format(format, value)
        is_blinking = true
        blinking(imwidget, .5)
    else
        if is_blinking then
            imwidget.text = nil
            is_blinking = false
            blinking(imwidget, .5)
        end
    end
end)
```

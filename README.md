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
                    tb.text = "<span foreground='black' font='14'>●</span>"
                end
            end)

            blinkers[tb].timer:start()

        end
    end

    -- Pidgin widget
    imwidget = widget({ type = "textbox", name="ims" })
    imwidget:buttons(awful.util.table.join(
       awful.button({ }, 1, function ()
            imwidget.text = nil
            blinkers[imwidget].timer:stop()
       end)
     ))
    is_blinking = false;
    dbus.request_name("session", "org.ikook.ims")
    dbus.add_match("session", "interface='org.ikook.ims',member='test'")
    dbus.add_signal("org.ikook.ims", function (signal, value)
        if value > 0 then
            if blinkers[imwidget] then
                if is_blinking then
                    local format = "<span foreground='yellow' font='14'>●</span>"
                    imwidget.text = string.format(format, value)
                    is_blinking = true
                    blinkers[imwidget].timer:stop()
                else
                    blinkers[imwidget].timer:start()
                end
            else
                local format = "<span foreground='yellow' font='14'>●</span>"
                imwidget.text = string.format(format, value)
                blinking(imwidget, .5)
                is_blinking = true
            end
        else
            imwidget.text = ""
            is_blinking = false
            if blinkers[imwidget] then
                blinkers[imwidget].timer:stop()
            end
        end
    end)
```

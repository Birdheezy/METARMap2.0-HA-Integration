# METARMap2.0-HA-Integration
A Home Assistant Integration for my METARMap 2.0 Project

This is a custom integration and will not update automatically. It will create a button to fetch weather on your METARMap and a Swtich to turn the LED's on and off. 

# Step 1
Open a file editor in Home Assistant

# Step 2
Navigate to the "custom_compoents" folder and create a new folder called "metarmap"

# Step 3
Copy over the files __init__.py, button.py, sensor.py, config_flow.py, const.py, manifest.json, metarmap.py and swtich.py

# Step 4
Restart Home Assistant. 
Go to "settings". In the top right, click on the 3 dots and then "Restart Home Assistant". Then click "Restart Home Assistant". Then click "restart". 

# Step 5
After Home Assistant restarts, go to settings, Devices & Services then click the big blue "+ Add Integration" button. Search for METAR and "METAR Map Controller" should show up. 

Setup the IP address (either HTTP or HTTPS, depending on how you setup your map) then give it a name. Multiple maps can be setup, just use a different name for each one. 

You should then have a button that you can press to update the weather, a switch to turn the LED's off and on and a sensor that reports the last time the weather was updated. You can use the built in lights on/off time or  setup an automation that turns the lights on in the morning, and off in the evening. Again, you can use the built in wx updater in the settings website or build another automation that, every 5 minutes, looks to see if the LED switch is on, if it is, it presses the update weather button. That way the map isn't needlessly updating weather when the lights are off

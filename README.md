# METARMap2.0-HA-Integration
A Home Assistant Integration for my METARMap2.0 Project

This integration is available through HACS after adding a custom repo. 

# Installation 

## Using HACS and custom integration

### Setp One
Open HACS. In the top right corner, click on the 3 dots and select "custom repository".

### Step Two
In the repository field enter "https://github.com/Birdheezy/METARMap2.0-HA-Integration" (without quotes).
For type, select "integration".

### Step Three
Search for "metar" and download/install "METAR Map Controller"

### Step Four
Navigate to settings, then in the upper right, click the 3 dots, then restart home assistant (not quick reload).

### Step Five
Go to devices and services, click add integration and search for metar. Install.

### Step Six
Enter your controller's local IP address. If you enabled HTTPS, be sure to use HTTPS here. Give your map a name and click "submit".

### Step Seven
3 entities are now available:
A button to force update weather. 
A switch to turn the LEDs on/off. 
A sensor that outputs the last time the weather has been updated. 

You can use the built in lights on/off control and weather update function in the settings website,
or you can toggle the LEDs and weather update using an automation and the switch and button in this integration.

For example, turn the lights on at 0700 and off at 2200. Then, if the switch is on, every 5 minutes, press the wx update button.

## Custom Install

### Step 1
Open a file editor in Home Assistant

### Step 2
Navigate to the "custom_compoents" folder and create a new folder called "metarmap"

### Step 3
Copy over the files from the custom_components/metarmap folder into your newly created metarmap folder.

### Step 4
Restart Home Assistant. 
Go to "settings". In the top right, click on the 3 dots and then "Restart Home Assistant". Then click "Restart Home Assistant". Then click "restart". 

### Step 5
After Home Assistant restarts, go to settings, Devices & Services then click the big blue "+ Add Integration" button. Search for METAR and "METAR Map Controller" should show up. 

Setup the IP address (either HTTP or HTTPS, depending on how you setup your map) then give it a name. Multiple maps can be setup, just use a different name for each one. 

You should then have a button that you can press to update the weather, a switch to turn the LED's off and on and a sensor that reports the last time the weather was updated.
You can use the built in lights on/off time or  setup an automation that turns the lights on in the morning, and off in the evening. Again, you can use the built in wx updater in the settings website or build another automation that, every 5 minutes, looks to see if the LED switch is on, if it is, it presses the update weather button.
That way the map isn't needlessly updating weather when the lights are off

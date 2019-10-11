
# MySmappee - OS X Menubar plugin

Displays home energy consumption (electricity, gas & water) and solar production information in the Mac OS X menubar. 
Requires Bitbar and a Smappee appliance. Compatible with Smappee Energy, Smappee Solar and Smappee Gas & Water monitor.  

Current power consumption:

![Imgur](https://i.imgur.com/gxrmefr.png)

Browse appliances:

![Imgur](https://i.imgur.com/rXKlH4j.png)

**Update 2018.01.20:** Added Streaming support (requires Bitbar v2 beta10 or higher. Continuously updates and shows power consumption in menu bar.

**Update 2017.11.12:** Show your past 24h consumption, labelled and unlabelled appliances and sensors

**Update 2017.11.10:** [mylocalsmappee.30s.py](mylocalsmappee.30s.py) connects directly to the Smappee appliance on your local network

**Update 2017.11.10:** [mysmappee.5m.py](mysmappee.5m.py) works over the internet, through the Smappee API. 

Stores and retrieves your Smappee username and password from the Mac OS X keychain.

Not tested with Smappee Plus and Smappee Pro

## Installation instructions: 

1. Execute in terminal.app before running : sudo easy_install keyring==8.7 smappy
2. Ensure you have [bitbar](https://github.com/matryer/bitbar/releases/latest) installed.
3. Ensure your bitbar plugins directory does not have a space in the path (A known bitbar bug)
4. Copy [mysmappee.5m.py](mysmappee.5m.py) or [mylocalsmappee.30s.py](mylocalsmappee.30s.py) to your bitbar plugins folder and chmod +x the file from your terminal in that folder
5. Run bitbar

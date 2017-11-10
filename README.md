
# MySmappee - bitbar plugin

A simple plugin that displays Power Consumption and Solar Production for your Smappee-enabled home in the Mac OS X menubar.

Stores and retrieves your Smappee username and password from the Mac OS X keychain.

Tested with Smappee Energy and Smappee Solar


## Installation instructions: 

1. Execute in terminal.app before running : sudo easy_install keyring smappy
2. Ensure you have [bitbar](https://github.com/matryer/bitbar/releases/latest) installed.
3. Ensure your bitbar plugins directory does not have a space in the path (A known bitbar bug)
4. Copy [mysmappee.1m.py](mysmappee.1m.py) to your bitbar plugins folder and chmod +x the file from your terminal in that folder
5. Run bitbar

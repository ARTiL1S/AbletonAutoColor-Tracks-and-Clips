<div style="text-align:center; border: 2px solid black; padding: 5px;"> <img src="AbletonColorPalette_Crop2.jpg" style="width:35%;" /> </div>

# AbletonAutoColor (Forked)

Inspired by the original project by Cory Boris
Original repo: CoryWBoris/AbletonAutoColor
https://github.com/CoryWBoris/AbletonAutoColor/tree/main?tab=readme-ov-file#ableton-color-palette

## Overview

AbletonAutoColor automatically assigns colors to MIDI and audio tracks in Ableton Live 11 and above, based on the track name. This fork adds extra functionality, such as coloring the clips along with the tracks. Everything else is mostly identical to the original script

Works on both macOS and Windows.

## Installation (Simple 6-Step Setup)

This assumes you’re using Ableton’s default User Library folder.
If you’ve relocated your User Library, just make sure to create a Remote Scripts folder inside your current User Library and follow the same steps from there.

1. Mac users:  
   Go to `/Users/{your_username}/Music/Ableton/User Library`  
   Windows users:  
   Go to `\Users\[username]\Documents\Ableton\User Library`
2. Create a folder 'Remote Scripts' if it's not already created.
3. Create a folder titled 'ColorChanger' inside the 'Remote Scripts' folder.
4. Download **both** .py files, "Colorchanger.py" and "\_\_init\_\_.py", and place them in the 'Remote Scripts/ColorChanger' folder.
5. Restart or Open Ableton Live
6. In Ableton, select ColorChanger in the "Link|Tempo|Midi" tab, and make sure the input and output are set to 'None'.

### Important Notes

If you copy the two Python files while Ableton is open, you’ll still need to restart Ableton afterward for the script to activate.
Live loads and compiles Python control surface scripts only at startup, so any code changes won’t apply until you relaunch.

Once active, the script will automatically apply color assignments based on your defined track names.

## Ableton Color Reference
<div style="text-align:center; border: 2px solid black; padding: 5px;"> <img src="AbletonColorPalette_Indexed.jpg" style="width:29%;" /> </div>

The image above shows Ableton’s built-in color palette.
Color indices run from 0 (top-left) to 69 (bottom-right).
You can assign any of these numbers to track name keywords in your Python dictionary — and you can add as many pairs as you want within that range.

## Compatibility

Tested and confirmed working on Ableton Live 11+.
It may also function on earlier versions if adapted for Python 2 compatibility.

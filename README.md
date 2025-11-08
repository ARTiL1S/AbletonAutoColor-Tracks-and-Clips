<div style="text-align:center; border: 2px solid black; padding: 5px;"> <img src="AbletonColorPalette_Crop2.jpg" style="width:35%;" /> </div>

# AbletonAutoColor (Forked Edition)

Inspired by the original project by Cory Boris
Original repo: CoryWBoris/AbletonAutoColor
https://github.com/CoryWBoris/AbletonAutoColor/tree/main?tab=readme-ov-file#ableton-color-palette

## Overview

AbletonAutoColor automatically assigns colors to MIDI and audio tracks in Ableton Live 11 and above, based on the track name. This fork adds extra functionality, such as coloring the clips along with the tracks. Everything else is mostly identical to the original script

Works on both macOS and Windows.

## Installation (Simple 6-Step Setup)

This assumes you’re using Ableton’s default User Library folder.
If you’ve relocated your User Library, just make sure to create a Remote Scripts folder inside your current User Library and follow the same steps from there.

1. Find your Ableton User Library

Mac: /Users/{your_username}/Music/Ableton/User Library

Windows: \Users\[your_username]\Documents\Ableton\User Library

2. If there isn’t one already, create a folder named Remote Scripts inside your User Library.

3. Inside that folder, make another folder called ColorChanger.

4. Download the following two files and place them inside Remote Scripts/ColorChanger:

"ColorChanger.py"

"__init__.py"

5. Launch or restart Ableton Live.

6. In Live, go to Preferences → Link/Tempo/MIDI, then choose ColorChanger from the Control Surface list. Set both Input and Output to None.

### Important Notes

If you copy the two Python files while Ableton is open, you’ll still need to restart Ableton afterward for the script to activate.
Live loads and compiles Python control surface scripts only at startup, so any code changes won’t apply until you relaunch.

Once active, the script will automatically apply color assignments based on your defined track names.

For more advanced behavior (such as live updating color layouts without restarting Live), see the TrueAutoColor version — a standalone release that extends this idea.

## Ableton Color Reference
<div style="text-align:center; border: 2px solid black; padding: 5px;"> <img src="AbletonColorPalette_Indexed.jpg" style="width:29%;" /> </div>

The image above shows Ableton’s built-in color palette.
Color indices run from 0 (top-left) to 69 (bottom-right).
You can assign any of these numbers to track name keywords in your Python dictionary — and you can add as many pairs as you want within that range.

## Compatibility

Tested and confirmed working on Ableton Live 11+.
It may also function on earlier versions if adapted for Python 2 compatibility.

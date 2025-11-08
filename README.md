<div style="text-align:center; border: 2px solid black; padding: 5px;">
  <img src="AbletonColorPalette_Crop2.jpg" style="width:35%;" />
</div>



# AbletonAutoColor
![Stability Badge](https://img.shields.io/badge/-stable-blue)  
Originally By: Cory Boris  
https://github.com/CoryWBoris/AbletonAutoColor/tree/main?tab=readme-ov-file#ableton-color-palette

## Automatic Color Assignment Based On Midi or Audio Track Name In Ableton Live 11+ WITHOUT PLUGINS ;)

\*\*for Mac or Windows\*\*

### 6 Steps to setup. -note-, this assumes you are using the default user library folder. If you have moved this folder externally or otherwise, make a Remote Scripts folder inside of whatever user library folder you have pointed Ableton to, and start from step 2:
1. Mac users:  
   Go to `/Users/{your_username}/Music/Ableton/User Library`  
   Windows users:  
   Go to `\Users\[username]\Documents\Ableton\User Library`
2. Create a folder 'Remote Scripts' if it's not already created.
3. Create a folder titled 'ColorChanger' inside the 'Remote Scripts' folder.
4. Download **both** .py files, "Colorchanger.py" and "\_\_init\_\_.py", and place them in the 'Remote Scripts/ColorChanger' folder.
5. Restart or Open Ableton Live
6. In Ableton, select ColorChanger in the "Link|Tempo|Midi" tab, and make sure the input and output are set to 'None'.

**Note**: You can add the 2 mentioned files from here to their respective folders as shown by my tutorial while Ableton is open or quit, but if Ableton is open, then you *will* have to restart Ableton for the selected control surface to go into effect. The reason being is that Ableton compiles python and loads python code into memory when Ableton starts, but not after it loads up. This means for you using the software that in order to change a color layout and have the changes go into effect, you will have the restart Ableton. While I can't change the nature of how Ableton loads control surfaces, I circumvented this inconvenience with the full version of this program called 'TrueAutoColor'. The release details are at the bottom but with the full version you can change the layout without restarting Ableton.

### Ableton Color Palette
<div style="text-align:center; border: 2px solid black; padding: 5px;">
  <img src="AbletonColorPalette_Indexed.jpg" style="width:29%;" />
</div>

If you look at the picture above, the colors start at '0' and go to '69' from top left to right. You can add as many names and colors as you want, as long as you only use numbers 0 - 69.

Tested and working on Ableton 11+, but this could work for older versions if the python script were written to be backwards compatible for python 2.

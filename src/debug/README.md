# Debug System

This folder contains debug tools for PythonDungeon development and testing.

## Files:
- `debug_menu.py` - Main debug menu system with player stat manipulation

## Usage:
1. Start the game: `python main.py`
2. At the inn menu, type `debug` 
3. Access debug tools for testing

## Debug Menu Features:
- ⬆️ Add/Remove Levels
- ✨ Add/Remove XP
- ❤️ Set Health
- 💪 Set Strength  
- 🐛 Toggle Debug Mode (fast scrolling)

## Removal for Production:
To remove debug functionality:
1. Delete this entire `src/debug/` folder
2. Remove the debug handler from `src/locations/inn.py`

## Developer Notes:
- All debug functionality is isolated in this folder
- No production code depends on debug features
- Safe to remove without affecting core gameplay
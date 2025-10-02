# PythonDungeon 🐉

A professional text-based RPG adventure game built with Python and GitHub Copilot for learning purposes.

## Overview

PythonDungeon is a comprehensive text-based role-playing game featuring deep character progression, dynamic combat systems, equipment management, location exploration, and persistent data storage. This project demonstrates modern Python development practices, modular architecture, and serves as a learning platform for game development concepts.

## Core Features

### 🧙‍♂️ **Advanced Character System**
- **Experience & Leveling**: Progressive XP system with exponential level requirements
- **Dynamic Stats**: Strength, health, and defense with level-based scaling
- **Character Persistence**: Full save/load system with SQLite database integration
- **Multiple Characters**: Support for multiple player saves with unique progression

### ⚔️ **Dynamic Combat System**
- **Turn-Based Combat**: Strategic turn-based battles with damage calculations
- **Smart Monster Scaling**: AI-driven monster levels based on player progression (±2 levels)
- **Combat Statistics**: Detailed damage tracking and battle outcomes
- **Victory Rewards**: XP and potential equipment drops from defeated enemies

### 🎒 **Complete Equipment System**
- **10 Equipment Slots**: Main hand, off hand, head, body, legs, hands, feet, necklace, and two ring slots
- **Equipment Types**: Weapons (swords, daggers, bows), armor (leather, chain, plate), and accessories (rings, amulets)
- **Stat Bonuses**: Strength, health, defense, and damage modifiers from equipment
- **Inventory Management**: Robust inventory system with capacity limits and item sorting
- **Equipment Tiers**: Common to Legendary rarity with appropriate stat scaling

### 🌲 **Adventure Locations**
- **The Forest (Level 1-10 Area)**: Primary exploration zone with scaled encounters
- **The Cozy Dragon Inn**: Safe haven for rest, equipment management, and services
- **Dynamic Encounters**: Mix of combat, peaceful events, and exploration opportunities
- **Location-Specific Loot**: Area-appropriate equipment and rewards

### 💾 **Robust Data Management**
- **SQLite Integration**: Professional database system for all persistent data
- **Automatic Migrations**: Database schema updates handled automatically
- **Save System**: Multiple save slots with character statistics and progression tracking
- **Settings Persistence**: User preferences and game configuration storage

### 🎨 **Advanced UI System**
- **Scrolling Text Display**: Immersive text presentation with customizable speeds
- **Debug Mode**: Developer tools for testing (--debug flag or in-game toggle)
- **Rich Menus**: Formatted menus with clear navigation and status displays
- **Equipment Screens**: Detailed character and equipment information displays

## Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Setup
```bash
# Clone the repository
git clone https://github.com/suspectedspam/PythonDungeon.git
cd PythonDungeon

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=src
```

## Project Structure

```
PythonDungeon/
├── src/                          # Source code packages
│   ├── core/                     # Core game systems
│   │   ├── player.py            # Player management, XP, and progression
│   │   ├── combat.py            # Turn-based combat mechanics
│   │   └── gamedata.py          # SQLite database operations and migrations
│   ├── equipment/               # Equipment and inventory systems
│   │   ├── __init__.py         # Equipment package exports
│   │   ├── equipment.py        # Base equipment classes (Weapon, Armor, Accessory)
│   │   ├── equipped_items.py   # Equipped items management (10 slots)
│   │   └── inventory.py        # Inventory management and item storage
│   ├── locations/               # Game locations and adventures
│   │   ├── adventure.py         # Abstract base adventure system
│   │   ├── forest.py           # Forest exploration (Level 1-10 area)
│   │   └── inn.py              # Inn location, rest, and services
│   ├── entities/               # Game entities and NPCs
│   │   └── monster.py          # Monster definitions, AI, and level scaling
│   ├── ui/                     # User interface systems
│   │   └── display.py          # Advanced console display with scrolling
│   ├── debug/                  # Developer tools (removable for production)
│   │   ├── __init__.py         # Debug package exports
│   │   ├── debug_menu.py       # Debug menu with stat manipulation
│   │   └── README.md           # Debug system documentation
│   └── config/                 # Configuration management
│       └── gamesettings.py     # Game settings and preferences
├── data/                       # Game data files
│   └── pythondungeon.db       # SQLite database (auto-generated)
├── tests/                      # Comprehensive test suite
│   ├── test_delay.py          # Display delay testing
│   └── test_scroll.py         # Text scrolling tests
├── main.py                     # Game entry point with debug support
├── pyproject.toml             # Project configuration and metadata
└── requirements.txt           # Python dependencies
```

## Testing

The project includes a comprehensive test suite with 58 tests achieving 36.3% code coverage:

```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Generate coverage report
python -m pytest --cov=src --cov-report=html
```

## Usage

### Starting the Game
```bash
# Normal gameplay
python main.py

# Debug mode (fast text scrolling for testing)
python main.py --debug
```

### Game Controls
- **Menu Navigation**: Use numeric choices (1-6) for menu selection
- **Text Input**: Follow prompts for character names and commands
- **Debug Access**: Type `debug` in the inn menu for developer tools
- **Equipment**: Access inventory and equipment screens from inn services

### Character Progression
- **Experience Points**: Gain XP by defeating monsters in combat
- **Leveling Up**: Automatic stat increases when XP thresholds are reached
- **Equipment**: Find and equip weapons, armor, and accessories to enhance abilities
- **Save Progress**: Manual saves available at the inn, with automatic saves after major events

### Equipment System
- **10 Equipment Slots**: Fully customize your character's loadout
  - Weapons: Main hand and off hand for dual-wielding
  - Armor: Head, body, legs, hands, and feet protection
  - Accessories: Necklace and two ring slots for magical bonuses
- **Stat Bonuses**: Equipment provides damage, strength, health, and defense bonuses
- **Inventory Management**: Store unequipped items with capacity limits
- **Equipment Tiers**: Find increasingly powerful gear as you progress

### Adventure Areas
- **The Forest**: Level 1-10 exploration area with scaling monster encounters
  - 80% encounter rate with dynamic monster levels
  - Peaceful events and exploration opportunities
  - Equipment drops and XP rewards
- **The Cozy Dragon Inn**: Safe hub for character management
  - Rest to restore full health
  - Save your character progress
  - Access debug tools (type `debug`)

### Debug Features (Developer Tools)
- **Debug Mode Toggle**: Enable ultra-fast text scrolling (0.05s delays)
- **Character Manipulation**: Add/remove levels, XP, health, and strength
- **Testing Tools**: Quickly test game mechanics and progression systems
- **Access Methods**: 
  - Command line: `python main.py --debug`
  - In-game: Type `debug` at inn menu

## Architecture

### Design Principles
- **Modular Architecture**: Clean separation of concerns across specialized packages
- **Single Responsibility**: Each module handles one aspect of the game system
- **Composition over Inheritance**: Player "has" equipment rather than "is" equipment
- **Scalable Design**: Easy to extend with new equipment types, locations, and features

### Core Systems
- **Database Layer**: SQLite with automatic migrations and schema management
- **Equipment System**: Comprehensive gear management with 10 equipment slots
- **Combat Engine**: Turn-based combat with dynamic monster level scaling
- **UI Framework**: Advanced console display with scrolling text and formatted menus
- **Debug Infrastructure**: Isolated debug tools for development and testing

### Key Technologies
- **Python 3.11+**: Modern Python features and performance optimizations
- **SQLite**: Embedded database for persistent data storage
- **Enum Classes**: Type-safe equipment slots and game states
- **Abstract Base Classes**: Extensible adventure and equipment systems
- **Comprehensive Testing**: pytest with mocking and coverage reporting

## Development

### Modern Python Practices
- **Package Structure**: Professional src/ layout with logical module organization
- **Type Safety**: Comprehensive type hints and enum usage for better IDE support
- **Documentation**: Detailed docstrings following Python conventions
- **Code Quality**: Modular design with clear separation of concerns

### Development Tools
- **Testing Framework**: pytest with comprehensive test coverage
- **Debug System**: Built-in debug menu for rapid testing and development
- **Database Migrations**: Automatic schema updates and data persistence
- **Configuration Management**: Centralized settings with pyproject.toml

### Extensibility Features
- **Equipment System**: Easy to add new weapon types, armor pieces, and accessories
- **Adventure Framework**: Abstract base classes for creating new exploration areas
- **Monster System**: Dynamic level scaling and database-driven creature management
- **UI Components**: Reusable display components for consistent user experience

### Performance Considerations
- **Efficient Database Queries**: Optimized SQLite operations with proper indexing
- **Memory Management**: Careful object lifecycle management for long gaming sessions
- **Display Optimization**: Configurable text delays for optimal user experience
- **Scalable Architecture**: Designed to handle character progression and large inventories

## Game Mechanics

### Experience and Leveling
- **XP Requirements**: Exponential curve starting at 100 XP for level 2
- **Stat Growth**: +10 HP and +2 Strength per level
- **Level Scaling**: Monster levels dynamically adjust based on player level
- **Progression Rewards**: Equipment drops and stat bonuses scale with character advancement

### Combat System
- **Turn Order**: Player always acts first in combat encounters
- **Damage Calculation**: Base strength + weapon damage + equipment bonuses
- **Monster AI**: Intelligent level matching with ±2 level variance
- **Victory Conditions**: Defeat monsters to gain XP and potential equipment drops

### Equipment Mechanics
- **Slot System**: 10 distinct equipment slots for complete character customization
- **Stat Bonuses**: Cumulative bonuses from all equipped items
- **Equipment Tiers**: Common, Uncommon, Rare, Epic, and Legendary rarities
- **Dual Wielding**: Support for main hand and off hand weapon combinations
- **Inventory Limits**: Capacity management encourages strategic item decisions

### Monster Scaling (Forest Area)
- **Base Level Range**: Monsters spawn at levels 1-10 (forest area cap)
- **Probability Distribution**:
  - 50% chance: Same level as player
  - 40% chance: ±1 level from player (20% each direction)
  - 10% chance: ±2 levels from player (5% each direction)
- **Level Cap**: No monster exceeds level 10 regardless of player level
- **Minimum Level**: All monsters are at least level 1

## Contributing

This is a learning project built with GitHub Copilot. Contributions are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure all tests pass
5. Submit a pull request

## License

This project is for educational purposes and learning Python game development.

## Acknowledgments

Built with GitHub Copilot as a learning exercise in Python game development and modern software engineering practices.
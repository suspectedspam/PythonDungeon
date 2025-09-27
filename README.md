# PythonDungeon 🐉

A professional text-based RPG adventure game built with Python and GitHub Copilot for learning purposes.

## Overview

PythonDungeon is a comprehensive text-based role-playing game featuring player progression, combat systems, location exploration, and persistent data storage. This project demonstrates modern Python development practices and serves as a learning platform for game development concepts.

## Features

- **Character System**: Player creation, leveling, health management, and persistent saves
- **Combat System**: Turn-based combat with monsters and damage calculations
- **Adventure Locations**: Explorable areas including forests and inns with unique encounters
- **Monster Database**: SQLite-powered monster system with level-appropriate spawning
- **Save System**: Persistent player data, statistics tracking, and game settings
- **Display Engine**: Rich console UI with scrolling text and formatted menus
- **Settings Management**: Customizable game preferences and auto-save options

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
│   │   ├── player.py            # Player management and progression
│   │   ├── combat.py            # Combat mechanics
│   │   └── gamedata.py          # Database operations
│   ├── locations/               # Game locations and adventures
│   │   ├── adventure.py         # Base adventure system
│   │   ├── forest.py           # Forest exploration
│   │   └── inn.py              # Inn location and services
│   ├── entities/               # Game entities
│   │   └── monster.py          # Monster definitions and AI
│   ├── ui/                     # User interface
│   │   └── display.py          # Console display system
│   └── config/                 # Configuration
│       └── gamesettings.py     # Game settings management
├── data/                       # Game data files
│   └── pythondungeon.db       # SQLite database
├── tests/                      # Test suite
├── main.py                     # Game entry point
├── pyproject.toml             # Project configuration
└── requirements.txt           # Dependencies
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
python main.py
```

### Game Controls
- Follow on-screen prompts for navigation
- Use numeric choices for menu selection
- Type commands as prompted during gameplay

### Save System
- Games auto-save after combat and rest
- Multiple character saves supported
- Statistics and progress tracked automatically

## Architecture

- **Modular Design**: Organized into logical packages for maintainability
- **Database Integration**: SQLite for persistent data storage
- **Test Coverage**: Comprehensive pytest suite with mocking
- **Type Safety**: Modern Python practices with proper imports
- **Configuration Management**: Centralized settings system

## Development

This project uses modern Python development practices:

- **Package Structure**: Professional src/ layout
- **Testing**: pytest with coverage reporting
- **Configuration**: pyproject.toml for project metadata
- **Database**: SQLite with migration support
- **Documentation**: Comprehensive docstrings and type hints

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
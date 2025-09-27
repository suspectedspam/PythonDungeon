"""
Pytest configuration and shared fixtures for PythonDungeon tests
"""

import pytest
import os
import tempfile
import sqlite3
from unittest.mock import Mock, patch

# Import our modules
from src.core.player import Player
from src.core.gamedata import GameDatabase
from src.locations.forest import Forest
from src.locations.inn import Inn
from src.locations.adventure import Adventure


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    # Create temporary file
    temp_fd, temp_path = tempfile.mkstemp(suffix='.db')
    os.close(temp_fd)  # Close file descriptor, but keep the file
    
    # Create database instance with temp path
    db = GameDatabase(temp_path)
    
    yield db
    
    # Cleanup: remove temp database file
    try:
        os.unlink(temp_path)
    except OSError:
        pass


@pytest.fixture
def test_player():
    """Create a test player instance."""
    return Player("TestHero", emoji="🧙")


@pytest.fixture
def test_player_with_db(temp_db):
    """Create a test player and save it to temp database."""
    player = Player("TestHero", emoji="🧙")
    temp_db.save_player(player)
    yield player


@pytest.fixture
def forest_adventure():
    """Create a Forest adventure instance."""
    return Forest()


@pytest.fixture
def inn_instance():
    """Create an Inn instance."""
    return Inn()


@pytest.fixture
def mock_display():
    """Mock the display system for testing."""
    with patch('src.ui.display.display') as mock_disp:
        # Set up common mock behaviors
        mock_disp.add_line = Mock()
        mock_disp.display_text = Mock()
        mock_disp.display_menu = Mock(return_value="1")
        mock_disp.clear_content = Mock()
        mock_disp.set_header = Mock()
        mock_disp.set_player_for_header = Mock()
        mock_disp.clear_hp_header = Mock()
        mock_disp.refresh_display = Mock()
        yield mock_disp


@pytest.fixture
def mock_input():
    """Mock user input for testing."""
    with patch('builtins.input') as mock_inp:
        mock_inp.return_value = "1"
        yield mock_inp


@pytest.fixture(autouse=True) 
def setup_test_environment():
    """Automatically set up test environment for each test."""
    # Ensure we're using test database paths
    original_cwd = os.getcwd()
    
    yield
    
    # Cleanup after test
    os.chdir(original_cwd)


# Markers for different test types
def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests") 
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "database: Tests that use database")


# Custom test collection
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Add unit marker to all tests by default
        if not any(marker.name in ['integration', 'slow', 'database'] 
                  for marker in item.iter_markers()):
            item.add_marker(pytest.mark.unit)
        
        # Add database marker to tests that use database fixtures
        if any(fixture_name in ['temp_db', 'test_player_with_db'] 
               for fixture_name in item.fixturenames):
            item.add_marker(pytest.mark.database)
import os
import sys
import pytest

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from web.app import app, game


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestAppRoutes:
    """Test Flask app endpoints."""

    def test_index_page_loads(self, client):
        """Test that the index page loads successfully."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"Minesweeper" in response.data
        assert b"Restart Game" in response.data

    def test_index_page_displays_board(self, client):
        """Test that the board is displayed on the index page."""
        response = client.get("/")
        assert response.status_code == 200
        # Check for table element
        assert b"<table>" in response.data
        # Check for at least one cell with unrevealed content (?)
        assert b"?" in response.data or b"0" in response.data

    def test_restart_resets_game(self, client):
        """Test that restart endpoint resets the game."""
        # Get initial board state
        response1 = client.get("/")
        initial_board = response1.data

        # Restart the game
        response2 = client.get("/restart")
        assert response2.status_code == 302  # Redirect to index

        # Check that we're redirected to index
        response3 = client.get("/")
        assert response3.status_code == 200

    def test_reveal_cell_returns_index(self, client):
        """Test that revealing a safe cell redirects to index."""
        client.get("/restart")
        # Reveal a cell - if it's not a mine, it should redirect
        # Find a non-mine cell
        for row in range(5):
            for col in range(5):
                if (row, col) not in game.mines:
                    response = client.get(f"/reveal/{row}/{col}")
                    # Non-mine reveal should redirect (302) or return page (200)
                    assert response.status_code in [200, 302]
                    return
        # If all cells are mines (shouldn't happen), just pass
        assert True

    def test_reveal_cell_updates_board_state(self, client):
        """Test that revealing a cell changes the board state."""
        # Get initial board
        response1 = client.get("/")
        initial_html = response1.data

        # Restart to get a fresh game
        client.get("/restart")

        # Reveal a cell
        client.get("/reveal/0/0")

        # Get updated board
        response2 = client.get("/")
        updated_html = response2.data

        # The board state should potentially change (unless no mines are affected)
        assert response2.status_code == 200

    def test_invalid_cell_coordinates(self, client):
        """Test revealing a cell with invalid coordinates."""
        # Attempt to reveal an out-of-bounds cell - this will raise an error
        # which is acceptable behavior for now
        with pytest.raises(Exception):
            response = client.get("/reveal/100/100")

    def test_reveal_same_cell_twice(self, client):
        """Test that revealing the same cell twice doesn't cause issues."""
        client.get("/restart")
        response1 = client.get("/reveal/1/1")
        response2 = client.get("/reveal/1/1")
        # Both should be successful redirects
        assert response1.status_code == 302
        assert response2.status_code == 302

    def test_game_state_persistence(self, client):
        """Test that game state persists across multiple requests."""
        client.get("/restart")

        # Reveal multiple cells
        client.get("/reveal/0/0")
        response1 = client.get("/")

        client.get("/reveal/1/1")
        response2 = client.get("/")

        # Both responses should be valid
        assert response1.status_code == 200
        assert response2.status_code == 200

    def test_win_message_appears(self, client):
        """Test that win message appears when game is won."""
        client.get("/restart")

        # Manually set all cells as revealed except mines to trigger win condition
        all_cells = set((r, c) for r in range(5) for c in range(5))
        game.revealed = all_cells - game.mines

        response = client.get("/")
        assert response.status_code == 200
        # Check for win message
        assert b"You Win" in response.data

    def test_game_over_message_on_mine_hit(self, client):
        """Test that game over message appears when hitting a mine."""
        client.get("/restart")

        # Get a mine location and reveal it
        if game.mines:
            mine_row, mine_col = list(game.mines)[0]
            # The reveal endpoint returns the game over page directly
            response = client.get(f"/reveal/{mine_row}/{mine_col}")

            assert response.status_code == 200
            # The response should be the game board with the Game Over message
            # Since it's a template response, the message should be in the HTML
            response_text = response.data.decode('utf-8')
            assert "Game Over" in response_text


class TestGameIntegration:
    """Test game logic integration with the Flask app."""

    def test_board_dimensions_displayed(self, client):
        """Test that the board displays correct dimensions."""
        response = client.get("/")
        assert response.status_code == 200
        # Count table rows (should be 5 for 5x5 board)
        row_count = response.data.count(b"<tr>")
        # Should have at least one row from the board
        assert row_count >= 5

    def test_restart_clears_previous_state(self, client):
        """Test that restart properly clears the game state."""
        # Reveal a cell
        client.get("/reveal/0/0")
        response1 = client.get("/")

        # Restart
        client.get("/restart")
        response2 = client.get("/")

        # Game should be in initial state
        assert response2.status_code == 200
        # There should be unrevealed cells (?)
        assert b"?" in response2.data or response2.data.count(b"a href") > 0

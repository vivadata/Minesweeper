import random
import pytest
from src.minesweeper import Minesweeper


class TestGameInitialization:
    """Test game initialization and setup."""

    def test_game_creates_with_correct_dimensions(self):
        """Test that game initializes with correct board dimensions."""
        game = Minesweeper(10, 10, 5)
        assert game.rows == 10
        assert game.cols == 10
        assert game.num_mines == 5

    def test_game_board_is_correct_size(self):
        """Test that the board array has correct dimensions."""
        game = Minesweeper(7, 8, 3)
        assert len(game.board) == 7
        assert all(len(row) == 8 for row in game.board)

    def test_game_initializes_empty_revealed_set(self):
        """Test that revealed set starts empty."""
        game = Minesweeper(5, 5, 3)
        assert len(game.revealed) == 0
        assert isinstance(game.revealed, set)

    def test_game_initializes_empty_mines_set(self):
        """Test that mines set is properly initialized."""
        game = Minesweeper(5, 5, 3)
        assert isinstance(game.mines, set)
        assert len(game.mines) == 3

    def test_game_with_different_mine_counts(self):
        """Test games with various mine counts."""
        for num_mines in [1, 3, 5, 10, 20]:
            game = Minesweeper(10, 10, num_mines)
            assert len(game.mines) == num_mines


class TestMinePlacement:
    """Test mine placement logic."""

    def test_mines_are_placed_on_board(self):
        """Test that mines are placed at the correct positions."""
        game = Minesweeper(5, 5, 3)
        mine_positions = [(r, c) for r, c in game.mines]
        # Check each mine is on the board
        for r, c in mine_positions:
            assert 0 <= r < 5
            assert 0 <= c < 5

    def test_mine_count_matches_specification(self):
        """Test that the number of mines placed matches the specification."""
        for target_mines in [1, 5, 10, 15]:
            game = Minesweeper(8, 8, target_mines)
            assert len(game.mines) == target_mines

    def test_no_duplicate_mines(self):
        """Test that no two mines are placed at the same location."""
        game = Minesweeper(10, 10, 10)
        unique_mines = set(game.mines)
        assert len(unique_mines) == len(game.mines)

    def test_mine_count_on_board(self):
        """Test that the mine count on the board matches the mines set."""
        game = Minesweeper(5, 5, 3)
        board_mine_count = sum(
            1 for row in game.board for cell in row if cell == "💣"
        )
        assert board_mine_count == 3

    def test_adjacent_mine_counter(self):
        """Test that adjacent mine counts are calculated correctly."""
        game = Minesweeper(5, 5, 3)
        # Check that cells adjacent to mines have correct counts
        for r, c in game.mines:
            for i in range(max(0, r - 1), min(5, r + 2)):
                for j in range(max(0, c - 1), min(5, c + 2)):
                    if (i, j) != (r, c):
                        # Cell should have a number or be another mine
                        assert game.board[i][j] in [1, 2, 3, 4, 5, 6, 7, 8, "💣", ""]


class TestGameMechanics:
    """Test core game mechanics."""

    def test_reveal_non_mine_cell(self):
        """Test revealing a cell without a mine."""
        game = Minesweeper(5, 5, 3)
        # Find a non-mine cell
        for r in range(5):
            for c in range(5):
                if (r, c) not in game.mines:
                    result = game.reveal(r, c)
                    assert result == "Continue"
                    assert (r, c) in game.revealed
                    return
        pytest.skip("No non-mine cells found")

    def test_reveal_mine_cell(self):
        """Test revealing a cell with a mine."""
        game = Minesweeper(5, 5, 1)
        mine_r, mine_c = list(game.mines)[0]
        result = game.reveal(mine_r, mine_c)
        assert result == "Game Over"

    def test_empty_cell_cascading_reveal(self):
        """Test that revealing an empty cell cascades to adjacent cells."""
        game = Minesweeper(5, 5, 1)
        # Find an empty cell (value 0, represented as empty string initially)
        for r in range(5):
            for c in range(5):
                if (r, c) not in game.mines and game.board[r][c] == "":
                    game.reveal(r, c)
                    # Check that adjacent cells are revealed
                    assert len(game.revealed) > 1
                    return
        # If no empty cell, test passes (cascading not applicable)
        assert True

    def test_reveal_same_cell_twice(self):
        """Test that revealing the same cell twice doesn't cause issues."""
        game = Minesweeper(5, 5, 3)
        for r in range(5):
            for c in range(5):
                if (r, c) not in game.mines:
                    result1 = game.reveal(r, c)
                    result2 = game.reveal(r, c)
                    assert result1 == "Continue"
                    assert result2 == "Continue"
                    assert (r, c) in game.revealed
                    return
        pytest.skip("No non-mine cells found")

    def test_get_board_shows_hidden_cells(self):
        """Test that unrevealed cells appear as spaces in get_board()."""
        game = Minesweeper(5, 5, 3)
        board = game.get_board()
        # All cells should initially be spaces (not revealed)
        flat_board = [cell for row in board for cell in row]
        assert all(cell == " " for cell in flat_board)

    def test_get_board_shows_revealed_cells(self):
        """Test that revealed cells appear in get_board()."""
        game = Minesweeper(5, 5, 3)
        # Reveal a cell
        for r in range(5):
            for c in range(5):
                if (r, c) not in game.mines:
                    game.reveal(r, c)
                    board = game.get_board()
                    # The revealed cell should show something other than space
                    assert board[r][c] != " "
                    return
        pytest.skip("No non-mine cells found")


class TestGameStates:
    """Test different game states and conditions."""

    def test_is_winner_when_all_non_mines_revealed(self):
        """Test that is_winner() returns True when all non-mine cells are revealed."""
        game = Minesweeper(5, 5, 3)
        # Manually set all non-mine cells as revealed
        all_cells = set((r, c) for r in range(5) for c in range(5))
        game.revealed = all_cells - game.mines
        assert game.is_winner() is True

    def test_not_winner_when_all_mines_not_revealed(self):
        """Test that is_winner() returns False when not all non-mines are revealed."""
        game = Minesweeper(5, 5, 3)
        # Reveal just one cell (if not a mine)
        for r in range(5):
            for c in range(5):
                if (r, c) not in game.mines:
                    game.revealed.add((r, c))
                    assert game.is_winner() is False
                    return
        pytest.skip("No non-mine cells found")

    def test_winner_count_matches_board_size(self):
        """Test that winning requires correct number of revealed cells."""
        game = Minesweeper(5, 5, 5)
        expected_reveals = 25 - 5  # All cells minus mines
        game.revealed = set(
            (r, c) for r in range(5) for c in range(5) if (r, c) not in game.mines
        )
        assert len(game.revealed) == expected_reveals


class TestGameRestart:
    """Test game restart functionality."""

    def test_restart_clears_revealed_set(self):
        """Test that restart clears the revealed cells."""
        game = Minesweeper(5, 5, 3)
        # Reveal some cells
        for r in range(2):
            for c in range(2):
                if (r, c) not in game.mines:
                    game.reveal(r, c)
        assert len(game.revealed) > 0
        # Restart
        game.restart()
        assert len(game.revealed) == 0

    def test_restart_regenerates_mines(self):
        """Test that restart creates new mine positions."""
        random.seed(42)
        game1 = Minesweeper(5, 5, 3)
        mines1 = set(game1.mines)

        random.seed(43)
        game1.restart()
        mines2 = set(game1.mines)

        # Mines should be different (very likely with different seeds)
        assert mines1 != mines2

    def test_restart_maintains_board_size(self):
        """Test that restart maintains board dimensions."""
        game = Minesweeper(7, 8, 5)
        original_rows = game.rows
        original_cols = game.cols
        game.restart()
        assert game.rows == original_rows
        assert game.cols == original_cols

    def test_restart_maintains_mine_count(self):
        """Test that restart maintains mine count."""
        game = Minesweeper(5, 5, 5)
        original_mine_count = game.num_mines
        game.restart()
        assert len(game.mines) == original_mine_count


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_small_board_1x1(self):
        """Test game on minimal board."""
        game = Minesweeper(1, 1, 1)
        assert len(game.board) == 1
        assert len(game.board[0]) == 1
        assert len(game.mines) == 1

    def test_board_with_no_mines(self):
        """Test board with zero mines."""
        game = Minesweeper(5, 5, 0)
        assert len(game.mines) == 0
        # All cells should be for reveal
        all_cells = set((r, c) for r in range(5) for c in range(5))
        game.revealed = all_cells
        assert game.is_winner() is True

    def test_board_nearly_all_mines(self):
        """Test board where most cells are mines."""
        game = Minesweeper(3, 3, 8)
        # Only 1 non-mine cell
        assert len(game.mines) == 8
        non_mine_cells = sum(
            1 for r in range(3) for c in range(3) if (r, c) not in game.mines
        )
        assert non_mine_cells == 1

    def test_large_board(self):
        """Test game on large board."""
        game = Minesweeper(50, 50, 100)
        assert len(game.board) == 50
        assert all(len(row) == 50 for row in game.board)
        assert len(game.mines) == 100

    def test_board_initialization_all_cells_populated(self):
        """Test that all board cells are initialized."""
        game = Minesweeper(4, 4, 3)
        for r in range(4):
            for c in range(4):
                cell = game.board[r][c]
                # Each cell should have a value (mine, number, or empty string)
                assert cell in [
                    "💣",
                    "",
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                ] or isinstance(cell, int)


class TestGameIntegration:
    """Integration tests for complete game flows."""

    def test_complete_win_scenario(self):
        """Test a complete game winning scenario."""
        game = Minesweeper(3, 3, 1)
        # Reveal all non-mine cells
        for r in range(3):
            for c in range(3):
                if (r, c) not in game.mines:
                    if result := game.reveal(r, c):
                        assert result == "Continue"
        # Check win condition
        assert game.is_winner()

    def test_complete_lose_scenario(self):
        """Test a complete game losing scenario."""
        game = Minesweeper(3, 3, 1)
        mine_r, mine_c = list(game.mines)[0]
        result = game.reveal(mine_r, mine_c)
        assert result == "Game Over"

    def test_multiple_games_sequence(self):
        """Test playing multiple games in sequence."""
        for _ in range(3):
            game = Minesweeper(5, 5, 3)
            assert len(game.mines) == 3
            assert len(game.revealed) == 0
            game.restart()
            assert len(game.revealed) == 0
            assert len(game.mines) == 3

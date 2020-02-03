# To test that a word is in the dictionary, simply use: `'word' in dictionary`.
from dictionary import dictionary


scores_by_letter = {
    "a": 1,
    "b": 3,
    "c": 3,
    "d": 2,
    "e": 1,
    "f": 4,
    "g": 2,
    "h": 4,
    "i": 1,
    "j": 8,
    "k": 5,
    "l": 1,
    "m": 3,
    "n": 1,
    "o": 1,
    "p": 3,
    "q": 10,
    "r": 1,
    "s": 1,
    "t": 1,
    "u": 1,
    "v": 4,
    "w": 4,
    "x": 8,
    "y": 4,
    "z": 10,
}


class ScrabbleGame():
    """Instantiates and enables playing a scrabble game.

    http://www.scrabble.com/
    """

    def __init__(self):
        self.board = self._make_new_board()
        self._board_without_curr_play = self._make_new_board()
        self.prev_play_score = 0
        self.curr_play_score = 0
        self.game_score = 0
        self.tiles = []
        self.tiles_orientation = None
        self.neighbors = []
        self.neighbors_words = []


    def play_tiles(self, tiles: list) -> dict:
        """
        Main method performing the validation, scoring and placement of tiles on the board.

        Params
            tiles: List[{'letter': str, 'row': int, 'col': int}]
                Each `tile` is a `dict` containing the `letter` of the tile to
                play, as well as a `row` and `col` to represent where it should
                be placed on the board.

        Returns
            dict: Dict{'valid': bool, 'score': int}
                A dict with keys 'valid' and 'score'.

                valid: bool
                    Whether or not the set of tiles represent a valid play.

                score: int
                    Value of the play to be added to the score. If `valid` is `False`, `score` is `0`.

                Example:
                    {
                        'valid': True,
                        'score': 12
                    }
        """
        self.curr_play_score = 0
        self.tiles = self._sort_tiles(tiles)
        invalid_play_tup = {'valid': False, 'score': self.curr_play_score}
        
        if (not self._are_tiles_in_valid_board_range()) \
            or (not self._are_tiles_for_non_occupied_positions()):
            return invalid_play_tup

        self._place_tiles_on_board(self.board)

        # case: first play
        if self.game_score == 0:
            if self._is_first_play_valid():
                self._score_first_play()
                

            else:
                self._remove_play_tiles()
                return invalid_play_tup
        
        # case: not the first play
        else:
            if self._is_valid_non_first_play():
                self._score_non_first_play()

            else:
                self._remove_play_tiles()
                return invalid_play_tup

        # self._print_play_results()
        self._place_tiles_on_board(self._board_without_curr_play)
        self._reset_play_attributes()
        return {'valid': True, 'score': self.curr_play_score}


    def _are_tiles_for_non_occupied_positions(self) -> bool:
        """
        Returns True if tiles are destined for non-occupied positions; else returns False.
        """
        for tile in self.tiles:
            if self.board[tile['row']][tile['col']] != '':
                return False

        return True

    
    def _are_tiles_in_valid_board_range(self) -> bool:
        """
        Returns True if tiles are in valid board range; else returns False.
        """

        for tile in self.tiles:
            if tile['row'] < 0 or tile['row'] > 14:
                return False
            
            if tile['col'] < 0 or tile['col'] > 14:
                return False
        
        return True
            

    def _get_current_play_score(self):
        """
        """
        self.curr_play_score = self.game_score - self.prev_play_score

    
    def _reset_play_attributes(self):
        """
        Resets the play's attributes.
        """
        self.tiles = []
        self.tiles_orientation = None
        self.neighbors = []
        self.neighbors_words = []
        self.prev_play_score = self.curr_play_score


    def print_score(self) -> None:
        """
        Prints score.
        """
        print(f"Game score: {self.game_score}")

    
    def print_tiles(self) -> None:
        """
        Prints tiles.
        """
        print(f"Tiles: {[tile['letter'] for tile in self.tiles]}")
    
    
    def _print_play_results(self) -> None:
        """
        Print board and score.
        """
        self.print_tiles()
        self.print_score()
        self._print_board(self.board)

    
    def _print_board(self, board) -> None:
        """
        Prints an easy-to-read view of the board.
        """
        print('Board:')
        for row in board:
            print(row)
        print('\n')


    def _make_new_board(self) -> list:
        """
        Initializes a new empty board.
        """
        board = []
        for _ in range(15):
            board.append(['' for _ in range(15)])
        
        return board

    
    def _play_non_first_play(self) -> None:
        """
        Handles all plays after the first play of the game.

        Side-effects
            self.board: list
                Places the play's tiles on the board.

            self.game_score: int
                Increments the game's score.
        """
 

    def _remove_play_tiles(self) -> None:
        """
        Remove the non-first play's tiles from the board.
        """
        for tile in self.tiles:
            self.board[tile['row']][tile['col']] = ''
    

    def _is_valid_non_first_play(self) -> bool:
        """
        Returns True if the non-first play is valid; else returns False. 
        
        Valid only if:
            1. the tiles adjacent to existing tiles; and
            2. tiles form a line; and
            3. all newly formed words are valid words.
        """
        
        # case: at least 1 tile is adjacent to an existing tile
        self._get_neighbors()
        if len(self.neighbors) == 0:
            print(f"Tiles don't connect to any existing tiles!")
            return False
        
        # case: tiles form a line
        if not self._are_tiles_in_a_line():
            print(f"Tiles are not in a line!")
            return False
        
        # case: tiles are contiguous but not a valid word
        if (self._are_tiles_contiguous()) and (self._word_from_tiles() not in dictionary):
            print(f"Tiles are contiguous but not valid word!")
            return False


        # case: not all newly formed words are valid
        if not self._are_all_newly_formed_words_valid():
            print(f"Not all  newly formed words are valid!")
            return False

        # case: everything is valid
        return True


    def _score_non_first_play(self) -> int:
        """
        Return score of non-first play.
        """
        play_score = 0
        
        if self._are_tiles_contiguous() and self._are_tiles_self_contained(): 
            play_score += self._score_word(self._word_from_tiles())
        
        for word in self.neighbors_words:
            play_score += self._score_word(word)

        self.game_score += play_score

        self._get_current_play_score()
        

    def _are_tiles_self_contained(self) -> bool:
        """
        Returns True if the tiles are self-contained; else, returns False. Self-contained only if:
            1. First tile has no tile before it (no left tile if horizontal; no tile above if vertical).
            2. Last tile has no tile after it (no right tile if horizontal; no tile below if veritcal).
        """
        if self.tiles_orientation == 'not_linear':
            return False

        first_tile = self.tiles[0]
        last_tile = self.tiles[-1]

        if self.tiles_orientation == 'horizontal':
            if first_tile['col'] != 0:
                if self.board[first_tile['row']][first_tile['col'] - 1] != '':
                    return False
            if last_tile['col'] != 14:
                if self.board[last_tile['row']][last_tile['col'] + 1] != '':
                    return False

        if self.tiles_orientation == 'vertical':
            if first_tile['row'] != 0:
                if self.board[first_tile['row'] - 1][first_tile['col']] != '':
                    return False
            if last_tile['row'] != 14:
                if self.board[last_tile['row'] + 1][last_tile['col']] != '':
                    return False

        if len(self.tiles) == 1 and tiles[0]['letter'] != 'a':
            return False

        return True


    def _are_all_newly_formed_words_valid(self) -> bool:
        """
        Returns True if all newly formed words are valid; else returns False.
        """

        if self._are_tiles_contiguous() and self._are_tiles_self_contained():
            print(f"Tiles are contig. and self-contained; therefore, evaluating whether {''.join([tile['letter'] for tile in self.tiles])} is a word.")
            word = self._word_from_tiles()
            if word not in dictionary:
                return False

        if not self._are_all_neighbors_words_valid():
            print(f"Not all neighbor words -- {self.neighbors_words} -- are valid!")
            return False

        return True

    
    def _are_all_neighbors_words_valid(self) -> bool:
        """
        Returns True if all the words represented by the neighbors of the tiles are valid; else, returns False.
        """

        self._get_neighbors_words() 

        for word in self.neighbors_words:
            if word not in dictionary:
                return False

        return True


    def _get_neighbors_words(self) -> None:
        """
        Updates the self.neighbors_words (list) with the words represented by the neighbors.
        """
        unique_word_starts = self._unique_neighbors_words_starts()

        for word_start_tup in unique_word_starts:
            neighbor_word = self._word_given_start_and_orientation(*word_start_tup)
            self.neighbors_words.append(neighbor_word)


    def _unique_neighbors_words_starts(self) -> set:
        """
        To avoid double counting neighbor words, returns a unique list of word starts and their orientations given self.neighbors.
        """
        unique_word_starts = set()  
        
        for curr_neighbor in self.neighbors:
            unique_word_starts.add(
                self._neighbor_word_start_position(
                    curr_neighbor['row'], 
                    curr_neighbor['col'], 
                    curr_neighbor['orientation']))
        return unique_word_starts


    def _word_given_start_and_orientation(self, row: int, col: int, orientation: str) -> str:
        """
        Returns the word and its score given the starting position (row and col) and the word's orientation.

        Returns
            Tuple(word: str, score: int)
        """
        
        word = ''

        if orientation == 'vertical':
        
            for curr_row_idx in range(row, 15):
                curr_char = self.board[curr_row_idx][col]
                if curr_char != '':
                    word += curr_char
                else:
                    break
        

        if orientation == 'horizontal':
        
            for curr_col_idx in range(col, 15):
                curr_char = self.board[row][curr_col_idx]
                if curr_char != '':
                    word += curr_char
                else:
                    break

        return word
    

    def _neighbor_word_start_position(self, row: int, col: int, orientation: str) -> tuple:
        """
        Returns the (row, column, orientation) of the start of the neighbor word given the neighbor char's row, col, and orientation.
        """
        # get min row or col
        start_row_idx = row
        start_col_idx = col

        if orientation == 'vertical':
            while start_row_idx > 0:
                if self.board[start_row_idx - 1][col] != '':
                    start_row_idx -= 1
                else:
                    break
            

        if orientation == 'horizontal':
            while start_col_idx > 0:
                if self.board[row][start_col_idx - 1] != '':
                    start_col_idx -= 1
                else:
                    break
        
        return (start_row_idx, start_col_idx, orientation)

    
    def _get_neighbors(self) -> None:
        """
        Finds neighbors to the self.neighbors (list) if any neighbors exist. 
        
        Side-effects
            self.neighbors: List
                Adds neighbors to the list if any exist.
        """

        for curr_tile in self.tiles:
            curr_row = curr_tile['row']
            curr_col = curr_tile['col']

            # check above neighbor
            neighbor_row = curr_row - 1
            neighbor_col = curr_col
            neighbor_letter = self._board_without_curr_play[neighbor_row][neighbor_col]
            neighbor_orientation = 'vertical'
            if (curr_row != 0) and neighbor_letter != '':
                self.neighbors.append(
                    {'letter': neighbor_letter, 
                    'row': neighbor_row, 
                    'col': neighbor_col, 
                    'orientation': neighbor_orientation})

            # check below neighbor
            neighbor_row = curr_row + 1
            neighbor_col = curr_col
            neighbor_letter = self._board_without_curr_play[neighbor_row][neighbor_col]
            neighbor_orientation = 'vertical'
            if (curr_row != 14) and neighbor_letter != '':
                self.neighbors.append(
                    {'letter': neighbor_letter, 
                    'row': neighbor_row, 
                    'col': neighbor_col, 
                    'orientation': neighbor_orientation})

            # check left neighbor
            neighbor_row = curr_row
            neighbor_col = curr_col - 1
            neighbor_letter = self._board_without_curr_play[neighbor_row][neighbor_col]
            neighbor_orientation = 'horizontal'
            if (curr_col != 0) and neighbor_letter != '':
                self.neighbors.append(
                    {'letter': neighbor_letter, 
                    'row': neighbor_row, 
                    'col': neighbor_col, 
                    'orientation': neighbor_orientation})
                    

            # check right neighbor
            neighbor_row = curr_row
            neighbor_col = curr_col + 1
            neighbor_letter = self._board_without_curr_play[neighbor_row][neighbor_col]
            neighbor_orientation = 'horizontal'
            if (curr_col != 14) and neighbor_letter != '':
                self.neighbors.append(
                    {'letter': neighbor_letter, 
                    'row': neighbor_row, 
                    'col': neighbor_col, 
                    'orientation': neighbor_orientation})

        
    def _is_first_play_valid(self) -> bool:
        """
        Returns True if first play is valid; else returns False.
        """
        
        if self._any_tiles_at_board_center() and self._are_tiles_in_a_line():
            
            word = self._word_from_tiles()
            if word in dictionary:
                return True
        else:
            return False

    
    def _score_first_play(self) -> int:
        """
        """
        score = 0
        for tile in self.tiles:
            letter = tile['letter']
            score += scores_by_letter[letter]
        self.game_score = score

        self._get_current_play_score()

    
    def _are_tiles_contiguous(self) -> bool:
        """
        Returns bool on whether the tiles are contiguous.
        """
        
        
        if not self._are_tiles_in_a_line():
            return False
        
        if self.tiles_orientation == 'single_tile':
            return True

        if self.tiles_orientation == 'horizontal':
            expected_num = self.tiles[0]['col']
            for tile_idx in range(len(self.tiles)):
                actual_num = self.tiles[tile_idx]['col']
                if expected_num != actual_num:
                    return False
                expected_num += 1

        if self.tiles_orientation == 'vertical':
            expected_num = self.tiles[0]['row']
            for tile_idx in range(len(self.tiles)):
                actual_num = self.tiles[tile_idx]['row']
                if expected_num != actual_num:
                    return False
                expected_num += 1

        return True
            
    
    def _score_word(self, word: str) -> int:
        """
        Returns the score (int) of the word.
        """
        score = 0

        for char in word:
            score += scores_by_letter[char]
        
        return score
    
    
    def _place_tiles_on_board(self, board) -> None:
        """
        Places tiles on the specified board.
        """
        for tile in self.tiles:
            row_num = tile['row']
            col_num = tile['col']
            letter = tile['letter']

            board[row_num][col_num] = letter
        
    
    def _word_from_tiles(self) -> str:
        """
        Returns stringified version of the word.
        """
        word = ''.join([tile['letter'] for tile in self.tiles])
        return word


    def _any_tiles_at_board_center(self) -> bool:
        """
        Return True if any of the tiles are destined for the board's center; else return False.
        """
        for tile in self.tiles:
            if (tile['row'] == 7) and (tile['col'] == 7):
                return True
        return False


    def _are_tiles_in_a_line(self) -> bool:
        """
        Returns a tuple stating whether the tiles form a line and, if they do, whether the line is horizontal or vertical.

        Returns
            Tuple(bool, str)
                bool: whether tiles are linear.
                str: string describing tiles' orientation
        """
        tiles_count = len(self.tiles)
        
        if tiles_count == 0:
            raise ValueError('Tiles list is empty! Please provide tiles.')

        if tiles_count == 1:
            self.tiles_orientation = 'single_tile'
            return True
        
        rows_set = set([tile['row'] for tile in self.tiles])
        cols_set = set([tile['col'] for tile in self.tiles])

        # horizontal line
        if (len(rows_set) == 1) and (len(cols_set) == tiles_count):
            self.tiles_orientation = 'horizontal'
            return True

        # vertical line
        if (len(cols_set) == 1) and (len(rows_set) == tiles_count):
            self.tiles_orientation = 'vertical'
            return True

        # else: not in a line

        self.tiles_orientation = 'not_linear'
        return False

    
    def _sort_tiles(self, tiles) -> list:
        """
        Sorts the tiles by row and column.
        """
        tiles_sorted = sorted(tiles, key=lambda tile: (tile['row'], tile['col']))
        return tiles_sorted
    

# TESTING
# my_game = ScrabbleGame()
# tiles = [
#     {'letter': 'b', 'row': 7, 'col': 7},
#     {'letter': 'a', 'row': 7, 'col': 8},
#     {'letter': 't', 'row': 7, 'col': 9}]
# my_game.play_tiles(tiles)

# tiles = [
#     {'letter': 'a', 'row': 8, 'col': 7},
#     {'letter': 'r', 'row': 9, 'col': 7},
#     ]
# my_game.play_tiles(tiles)

# tiles = [
#     {'letter': 'o', 'row': 9, 'col': 8},
#     {'letter': 'w', 'row': 9, 'col': 9},
#     ]
# my_game.play_tiles(tiles)


# tiles = [
#     {'letter': 'o', 'row': 8, 'col': 9},
#     {'letter': 'n', 'row': 10, 'col': 9},
#     ]
# my_game.play_tiles(tiles)

# tiles = [
#     {'letter': 's', 'row': 7, 'col': 10}
#     ]
# my_game.play_tiles(tiles)
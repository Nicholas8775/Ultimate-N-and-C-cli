class Ultimate_NandC:

    board_state = []
    overall_grid_state = []

    def __init__(self):
        self.board_state = [[[[" ", " ", " "] for _ in range(3)]\
            for _ in range(3)] for _ in range(3)]
        self.overall_grid_state = [[" ", " ", " "] for _ in range(3)]

    def output_board(self, focus=None):
        """Outputs the state of the board to the terminal

        Parameters
        ----------
        focus : tuple (int, int) or None, optional
            The subgrid that the player is forced to play in if there is one, by default None
        """
        # TODO
        # 2. Properly format and comment (and maybe refactor further) the logic
        # 3. Rename some variables
        big_symbol = {
        "X" : [
            "   ╲   ╱   ",
            "    ╲ ╱    ",
            "     ╳     ",
            "    ╱ ╲    ",
            "   ╱   ╲   "
            ],
        "O" : [
            " 𜰰𜰱▔▔▔▔▔𜰲𜰳 ",
            " 𜰴       𜰷 ",
            " ▏       ▕ ",
            " 𜰸       𜰻 ",
            " 𜰼𜰽▁▁▁▁▁𜰾𜰿 "
            ],
        "-" : [
            "           ",
            " ========= ",
            "           ",
            " ========= ",
            "           "
            ]
        }

        # Constructing the output. Layers to iterate through:
        # 1. The three rows of the big board (minus the dividing lines between the rows)
        #  2. The three lines that make up each row (not counting the two lines that divide the rows of the subgrid)
        #   3. The specific grids of the row the line is intersecting (not counting the dividing lines separating each element in the subgrids)
        # Everything is then stitched together - the stuff excluded for each layer is then calculated and used to connect the other elements
        # together.

        # List to construct output
        full_output = []
        for row_num, outer_row in enumerate(self.board_state):
            row_output = []
            complete_grids_in_row = [i for i, state in enumerate(self.overall_grid_state[row_num]) if state != " "]
            for inner_row in range(3):
                inner_line_output = []
                for column_num, inner_grid in enumerate(outer_row):
                    if column_num in complete_grids_in_row:
                        inner_line_output.append(big_symbol[self.overall_grid_state[row_num][column_num]][inner_row * 2])
                    else:
                        inner_row_output = [f" {state} " for state in inner_grid[inner_row]]
                        if focus is None or (column_num == focus[0] and row_num == focus[1]):
                            inner_line_output.append("┆".join(inner_row_output))
                        else:
                            inner_line_output.append(" ".join(inner_row_output))
                row_output.append("│".join(inner_line_output))

            if focus is None:
                upper_intermediate_line = ["--- --- ---"] * 3
            else:
                upper_intermediate_line = [" " * 11] * 3
                if row_num == focus[1]:
                    upper_intermediate_line[focus[0]] = "--- --- ---"
            lower_intermediate_line = upper_intermediate_line.copy()
            for column in complete_grids_in_row:
                upper_intermediate_line[column] = big_symbol[self.overall_grid_state[row_num][column]][1]
                lower_intermediate_line[column] = big_symbol[self.overall_grid_state[row_num][column]][3]
            row_output.insert(1, "│".join(upper_intermediate_line))
            row_output.insert(-1, "│".join(lower_intermediate_line))
            full_output.append("\n".join(row_output))

        dividing_line = "\n" + "┼".join(["─" * 11] * 3) + "\n"
        print(dividing_line.join(full_output))

    def change_board(self, move, symbol):
        # move = (outer board (x, y), inner board (x, y))
        outer_board_xy = move[0]
        inner_board_xy = move[1]
        self.board_state[outer_board_xy[1]][outer_board_xy[0]]\
            [inner_board_xy[1]][inner_board_xy[0]] = symbol

    def human_move(self, player_num, context=None):
        self.output_board(context)
        print(f"\n{["X", "O"][player_num]}'s turn")

        inner_grid_choice = None
        while inner_grid_choice is None:
            outer_grid_choice = None
            if context is None:
                outer_grid_choice = self.get_grid_choice()
                forced_choice = False
            else:
                outer_grid_choice = context
                forced_choice = True

            inner_grid_choice = self.get_grid_choice(outer_grid_choice, forced_choice)

        self.change_board((outer_grid_choice, inner_grid_choice), ["X", "O"][player_num])
        return (outer_grid_choice, inner_grid_choice)

    def get_grid_choice(self, current_outer=None, forced_outer=False):
        if current_outer is not None:
            grid_scope = "Inner"
        else:
            grid_scope =  "Outer"

        while True:
            x = None
            while x is None:
                print(f"\n{grid_scope} grid column (valid input = 1 or 2 or 3", end="")
                if current_outer is None or forced_outer:
                    x = input(". r to display board)\n>>> ")
                else:
                    x = input(". 0 to change your outer grid choice. r to display the board)\n>>> ")
                if x == "r":
                    x = None
                    print("\n\n\n")
                    if forced_outer:
                        self.output_board(current_outer)
                    else:
                        self.output_board()
                elif x == "0" and current_outer is not None and not forced_outer:
                    self.output_board()
                    return None
                if x not in ["1", "2", "3"]:
                    print("\nInvalid input, try again\n")
                    if forced_outer:
                        self.output_board(current_outer)
                    else:
                        self.output_board()
                    x = None

            y = None
            while y is None:
                y = input(f"\n{grid_scope} grid row (valid input = 1 or 2 or 3. 0 to change the" \
                           " column choice. r to display the board)\n>>> ")
                if y == "r":
                    y = None
                    print("\n\n\n")
                    if forced_outer:
                        self.output_board(current_outer)
                    else:
                        self.output_board()
                elif y not in ["0", "1", "2", "3"]:
                    print("\nInvalid input, try again\n")
                    if forced_outer:
                        self.output_board(current_outer)
                    else:
                        self.output_board()
                    y = None
                elif current_outer is not None:
                    if self.board_state[current_outer[1]][current_outer[0]][int(y)-1][int(x)-1] != " ":
                        print("\nNo overwriting an already taken space!\n")
                        if forced_outer:
                            self.output_board(current_outer)
                        else:
                            self.output_board()
                        y = "0"

            if y != "0":
                if grid_scope == "Outer" and self.overall_grid_state[int(y)-1][int(x)-1] != " ":
                    print("\nThat grid is already a completed game! Choose another\n")
                else:
                    return (int(x)-1, int(y)-1)

    def evaluate(self, grid):
        # test horizontal
        for row in grid:
            if len(set(row)) == 1 and row[0] not in [" ", "-"]:
                return row[0]

        # test vertical
        for column in range(3):
            if len(set([row[column] for row in grid])) == 1 and grid[0][column] not in [" ", "-"]:
                return grid[0][column][0]

        # test diagonal
        first_diagonal_result = len(set([grid[num][num] for num in range(3)]))
        second_diagonal_result = len(set([grid[2-num][num] for num in range(3)]))
        if (first_diagonal_result == 1 or second_diagonal_result == 1) and grid[1][1] not in [" ", "-"]:
            return grid[1][1]

        # test draw
        if " " not in [element for row in grid for element in row]:
            return "-"

        return " "

    def game_loop(self):
        current_player = 0
        previous_move = None
        while True:
            to_evaluate, previous_move = self.human_move(current_player, previous_move)
            self.overall_grid_state[to_evaluate[1]][to_evaluate[0]] = self.evaluate(self.board_state[to_evaluate[1]][to_evaluate[0]])
            if self.overall_grid_state[previous_move[1]][previous_move[0]] != " ":
                previous_move = None

            if (result := self.evaluate(self.overall_grid_state)) == " ":
                current_player = 1-current_player
                continue

            print("\n\n")
            self.output_board()
            if result == "-":
                print("\nIt is a draw")
            else:
                print(f"\n{result} has won!")
            break


if __name__ == "__main__":
    game = Ultimate_NandC()
    game.game_loop()

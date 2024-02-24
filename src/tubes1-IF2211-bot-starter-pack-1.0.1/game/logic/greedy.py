from typing import Optional
from game.logic.base import BaseLogic
from game.models import Board, GameObject, Position
from game.util import get_direction



# TODO: Implement Greedy Algorithm
class GreedyLogic(BaseLogic):
    def __init__(self) -> None:
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

        # temporary
        self.moveTo = (0, 0)

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        # Analyze new state
        if props.diamonds == 5:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        else:
            # Around the board
            if (board_bot.position.x, board_bot.position.y) == (0,0):
                self.moveTo = (0, board.height - 1)
            elif (board_bot.position.x, board_bot.position.y) == (10, board.height - 1):
                self.moveTo = (board.width - 1, board.height - 1)
            elif (board_bot.position.x, board_bot.position.y) == (board.width - 1, board.height - 1):
                self.moveTo = (board.width - 1, 0)
            elif (board_bot.position.x, board_bot.position.y) == (board.width - 1, 0):
                self.moveTo = (0, 0)
            self.goal_position = Position(self.moveTo[0], self.moveTo[1])
            
        current_position = board_bot.position
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        else:
            # Roam around
            delta = self.directions[self.current_direction]
            delta_x = delta[0]
            delta_y = delta[1]
            self.current_direction = (self.current_direction + 1) % len(
                self.directions
            )
        return delta_x, delta_y
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
        self.diamond = []

        # temporary
        self.moveTo = (0, 0)

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        diamonds = board.diamonds()
        
        # Analyze new state
        if props.diamonds == 5:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        else:
            self.goal_position = self.find_nearest_diamond(board_bot, diamonds)
            
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
    
    def find_nearest_diamond(self, board_bot: GameObject, diamonds) -> Optional[Position]:
        current_position = board_bot.position
        min_distance = float("inf")
        nearest_diamond = None
        for diamond in diamonds:
            distance = abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y)
            if distance < min_distance:
                min_distance = distance
                nearest_diamond = diamond.position
        return nearest_diamond
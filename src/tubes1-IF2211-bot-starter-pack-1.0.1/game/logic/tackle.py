from typing import Optional, Tuple

from game.logic.base import BaseLogic
from game.models import Board, GameObject, Position
from game.util import get_direction, position_equals
from time import sleep
from game.board_handler import BoardHandler
from game.api import Api


class TacleLogic(BaseLogic):
    static_targeted_bot: GameObject | None = None

    def __init__(self) -> None:
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        props = board_bot.properties
        self.board = board
        self.board_bot = board_bot
        self.diamonds = board.diamonds
        self.bots = [
            d
            for d in self.board.game_objects
            if d.type == "BotGameObject" and d.id != board_bot.id
        ]
        self.base = Position(board_bot.properties.base.y, board_bot.properties.base.x)
        self.bases = [
            d
            for d in self.board.game_objects
            if d.type == "BaseGameObject" and not position_equals(d.position, self.base)
        ]
        self.teleporter = [
            d for d in self.board.game_objects if d.type == "TeleportGameObject"
        ]
        self.redButton = [
            d for d in self.board.game_objects if d.type == "DiamondButtonGameObject"
        ]

        if props.diamonds == 5:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
            self.static_temp_goals = None
        else:
            if len(self.bots) == 1:
                self.goal_position = self.bases[0].position
                if board_bot.position == self.bases[0].position:
                    # kasus udah di base musuh, siap tacle
                    self.goal_position = self.tacle_from_base(
                        self.bots[0].position,
                        board_bot.position,
                    )
            elif len(self.bots) > 1:
                # nyari bot musuh yang punya diamond >= 3
                targeted_bot = self.find_bot_have_diamonds()
                if targeted_bot != None:
                    self.goal_position = targeted_bot.properties.base
                    # next TODO = kalo bot musuh udah deket base, siap tacle
                    if board_bot.position == targeted_bot.properties.base:
                        self.goal_position = self.tacle_from_base(
                            targeted_bot.position,
                            board_bot.position,
                        )
                else:
                    # TODO stay di middle
                    self.goal_position = self.find_middle_position()
                    if board_bot.position == self.goal_position:
                        while not targeted_bot:
                            sleep(0.1)
                            self.board = BoardHandler(
                                Api("http://localhost:3000/api")
                            ).get_board(self.board.id)
                            self.bots = [
                                d
                                for d in self.board.game_objects
                                if d.type == "BotGameObject" and d.id != board_bot.id
                            ]
                            targeted_bot = self.find_bot_have_diamonds()

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
            self.current_direction = (self.current_direction + 1) % len(self.directions)
        return delta_x, delta_y

    def tacle_from_base(
        self, enemy_position: Position, my_position: Position
    ) -> Position:
        while not (
            (enemy_position.x - 1 and enemy_position.y == my_position.y)
            or (enemy_position.x + 1 and enemy_position.y == my_position.y)
            or (enemy_position.x and enemy_position.y - 1 == my_position.y)
            or (enemy_position.x and enemy_position.y + 1 == my_position.y)
        ):
            sleep(0.01)
            self.board = BoardHandler(Api("http://localhost:3000/api")).get_board(
                self.board.id
            )
            temp = [
                d
                for d in self.board.game_objects
                if d.type == "BotGameObject" and d.id != self.board_bot.id
            ]
            temp = [
                d
                for d in temp
                if position_equals(
                    Position(d.properties.base.y, d.properties.base.x), my_position
                )
            ]
            enemy_position = temp[0].position
        return enemy_position

    def find_base_from_bot(self, bot: GameObject) -> Position:
        return bot.properties.base

    def find_bot_have_diamonds(self) -> GameObject | None:
        for bot in self.bots:
            if bot.properties.diamonds >= 3:
                return bot
        return None

    def find_middle_position(self) -> Position:
        # fungsi cari posisi tengah dari semua base musuh
        # ini kondisi saat musuh belom ada yang punya diamond > 3
        avg_x = sum(base.position.x for base in self.bases) / len(self.bases)
        avg_y = sum(base.position.y for base in self.bases) / len(self.bases)
        middle_position = Position(avg_x, avg_y)
        return middle_position

    def find_nearest_base(self, position: Position) -> Position:
        nearest_base = self.bases[0].position
        for base in self.bases:
            if abs(base.position.x - position.x) + abs(
                base.position.y - position.y
            ) < abs(nearest_base.x - position.x) + abs(nearest_base.y - position.y):
                nearest_base = base.position

        return nearest_base

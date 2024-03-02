from typing import Optional, Tuple

from game.logic.base import BaseLogic
from game.models import Board, GameObject, Position
from game.util import get_direction, position_equals


class TacleLogic(BaseLogic):
    def __init__(self) -> None:
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        props = board_bot.properties
        self.board = board
        self.board_bot = board_bot
        self.diamonds = board.diamonds
        self.bots = board.bots
        self.base = Position(board_bot.properties.base.y, board_bot.properties.base.x)
        self.bases = [
            d
            for d in self.board.game_objects
            if d.type == "BaseGameObject" and not position_equals(d.position, self.base)
        ]
        # print("Base: ", self.base)
        # for b in self.bases:
        #     print("Bases: ", b.position)
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
        else:
            targeted_bot = self.find_bot_have_diamonds(board_bot)
            print("Targeted Bot: ", targeted_bot.properties.name)
            if targeted_bot:
                self.goal_position = targeted_bot.properties.base
                # next TODO = kalo bot musuh udah deket base, siap tacle
            else:
                middle_position = self.find_middle_position()
                self.goal_position = middle_position

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

    def find_base_from_bot(self, bot: GameObject) -> Position:
        return bot.properties.base

    def find_bot_have_diamonds(self, board_bot: GameObject) -> GameObject | None:
        for bot in self.bots:
            if bot.properties.diamonds >= 3 and bot.id != board_bot.id:
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

    def teleporter_on_the_path(self, current_x, current_y, dest_x, dest_y):
        for t in self.teleporter:

            # Kondisi saat teleporter sejajar dengan destinasi dalam sumbu y dan berada pada jalur current->dest
            if t.position.x == dest_x and (
                dest_y < t.position.y <= current_y or current_y <= t.position.y < dest_y
            ):

                # Kondisi saat current tidak sejajar dengan destinasi pada sumbu y
                if dest_x != current_x:
                    self.goal_position = (
                        Position(dest_y, dest_x - 1)
                        if dest_x > current_x
                        else Position(dest_y, dest_x + 1)
                    )

                # Kondisi saat current sejajar dengan destinasi pada sumbu y
                else:
                    # Handle kalo dipinggir kiri/kanan
                    if dest_x == 0:
                        self.goal_position = Position(dest_y, dest_x + 1)
                    else:
                        self.goal_position = Position(dest_y, dest_x - 1)
                self.static_temp_goals = Position(
                    self.goal_position.y, self.goal_position.x
                )

            # Kondisi saat teleporter sejajar dengan destinasi dalam sumbu x dan berada pada jalur current->dest (Tidak akan pernah terjadi)
            elif t.position.y == dest_y and (
                dest_x < t.position.x <= current_x or current_x <= t.position.x < dest_x
            ):

                # Kondisi saat current tidak sejajar dengan destinasi pada sumbu x
                if dest_y != current_y:
                    self.goal_position = (
                        Position(dest_y - 1, dest_x)
                        if dest_y > current_y
                        else Position(dest_y + 1, dest_x)
                    )

                # Kondisi saat current sejajar dengan destinasi pada sumbu x
                else:
                    # Handle kalo dipinggir atas/bawah
                    if dest_y == 0:
                        self.goal_position = Position(dest_y + 1, dest_x)
                    else:
                        self.goal_position = Position(dest_y - 1, dest_x)

            # Kondisi saat teleporter sejajar dengan current dalam sumbu x dan berada pada jalur current->dest
            elif t.position.y == current_y and (
                dest_x < t.position.x <= current_x or current_x <= t.position.x < dest_x
            ):
                # Kondisi saat current tidak sejajar dengan destinasi pada sumbu x
                if dest_y != current_y:
                    self.goal_position = Position(dest_y, current_x)

                # Kondisi saat current sejajar dengan destinasi pada sumbu y
                else:
                    # Handle kalo dipinggir kiri/kanan
                    if current_y == 0:
                        self.goal_position = Position(current_y + 1, current_x)
                    else:
                        self.goal_position = Position(current_y - 1, current_x)
                self.static_temp_goals = Position(
                    self.goal_position.y, self.goal_position.x
                )

            # Kondisi saat teleporter sejajar dengan current dalam sumbu y dan berada pada jalur current->dest (TIDAK TERPAKAI KARENA TIDAK AKAN PERNAH TERJADI)
            elif t.position.x == current_x and (
                dest_y < t.position.y <= current_y or current_y <= t.position.y < dest_y
            ):
                if current_x == 0:
                    self.goal_position = Position(dest_y, current_x + 1)
                else:
                    self.goal_position = Position(dest_y, current_x - 1)
                self.static_temp_goals = Position(
                    self.goal_position.y, self.goal_position.x
                )

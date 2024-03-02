from typing import Optional, Tuple
from game.logic.base import BaseLogic
from game.models import Board, GameObject, Position
from game.util import get_direction



# TODO: Implement Simple Diamond Greedy Algorithm
class GreedyDiamondLogic(BaseLogic):
    static_goals : list[Position] = []
    static_temp_goals : Position = None

    def __init__(self) -> None:
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        self.board = board
        self.board_bot = board_bot
        self.diamonds = board.diamonds
        self.bots = board.bots
        self.teleporter = [d for d in self.board.game_objects if d.type == "TeleportGameObject"]
        self.redButton = [d for d in self.board.game_objects if d.type == "DiamondButtonGameObject"]

        # print(self.static_goals)
        # print(self.static_temp_goals)
        if (self.board_bot.position in self.static_goals):
            self.static_goals.remove(self.board_bot.position)
        if (self.board_bot.position == self.static_temp_goals):
            self.static_temp_goals = None

        # Analyze new state
        if props.diamonds == 5:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
            self.static_goals = []
        elif self.static_temp_goals:
            self.goal_position = self.static_temp_goals
        else:
            if (len(self.static_goals) == 0):
                self.find_best_block()
            self.goal_position = self.find_nearest_goal()
            
        current_position = board_bot.position
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
            if (not self.static_temp_goals):
                self.teleporter_on_the_path(
                    current_position.x,
                    current_position.y,
                    self.goal_position.x,
                    self.goal_position.y,
                )
            if (props.diamonds == 4):
                self.red_diamond_on_the_path(
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
    

    def find_nearest_goal(self):
        current_position = self.board_bot.position
        nearest_goal = None
        nearest_distance = float("inf")
        for goal in self.static_goals:
            distance = abs(current_position.x - goal.x) + abs(current_position.y - goal.y)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_goal = goal
        return nearest_goal
    
    def find_best_block(self):
        self.find_best_block_around()

    def find_best_block_around(self):
        # y = i
        # x = j
        current_position = self.board_bot.position
        blockH = 3
        blockW = 3
        topLeft = (current_position.y - blockH//2 - blockH, current_position.x - blockW//2 - blockW) # (y,x)
        blockAroundValue = [[0 for i in range(3)] for j in range(3)]
        blockAroundDiamonds = [[[] for i in range(3)] for j in range(3)]
        bestValue = 0
        bestBlockIndex = (0,0)
        for diamond in self.diamonds:
            if (diamond.properties.points == 2 and self.board_bot.properties.diamonds == 4):
                continue
            if diamond.position.x >= topLeft[1] and diamond.position.x < topLeft[1] + blockW*3 and diamond.position.y >= topLeft[0] and diamond.position.y < topLeft[0] + blockH*3:
                # print(diamond.position)
                blockAroundValue[(diamond.position.y - topLeft[0])//blockH][(diamond.position.x - topLeft[1])//blockW] += diamond.properties.points
                blockAroundDiamonds[(diamond.position.y - topLeft[0])//blockH][(diamond.position.x - topLeft[1])//blockW].append(diamond.position)
                tempIndex = ((diamond.position.y - topLeft[0])//blockH, (diamond.position.x - topLeft[1])//blockW)
                temp = blockAroundValue[tempIndex[0]][tempIndex[1]]
                if (temp > bestValue):
                    bestValue = temp
                    bestBlockIndex = (tempIndex[0],tempIndex[1])
        if (bestValue > 0):
            self.static_goals = blockAroundDiamonds[bestBlockIndex[0]][bestBlockIndex[1]]
        else:
            # print("GAKETEMU")
            self.find_best_block_map()

    def find_best_block_map(self):
        blockW = self.board.width//3
        blockH = self.board.height//3
        blockAroundValue = [[0 for i in range(3)] for j in range(3)]
        blockAroundDiamonds = [[[] for i in range(3)] for j in range(3)]
        bestValue = 0
        bestBlockIndex = (0,0)
        for diamond in self.diamonds:
            blockAroundValue[diamond.position.y//blockH][diamond.position.x//blockW] += diamond.properties.points
            blockAroundDiamonds[diamond.position.y//blockH][diamond.position.x//blockW].append(diamond.position)
            tempIndex = (diamond.position.y//blockH, diamond.position.x//blockW)
            temp = blockAroundValue[tempIndex[0]][tempIndex[1]]
            if (temp > bestValue):
                bestValue = temp
                bestBlockIndex = (tempIndex[0],tempIndex[1])
        if (bestValue > 0):
            self.static_goals = blockAroundDiamonds[bestBlockIndex[0]][bestBlockIndex[1]]
        else:
            # print("GAKETEMU LAGI")
            self.static_goals.append(self.redButton[0].position)
        
        
    def teleporter_on_the_path(self, current_x, current_y, dest_x, dest_y):
        for t in self.teleporter:
            # Kondisi saat teleporter sejajar dengan destinasi dalam sumbu y dan berada pada jalur current->dest
            if t.position.x == dest_x and (dest_y < t.position.y <= current_y or current_y <= t.position.y < dest_y):

                # Kondisi saat current tidak sejajar dengan destinasi pada sumbu y
                if (dest_x != current_x):
                    self.goal_position = Position(dest_y,dest_x-1) if dest_x > current_x else Position(dest_y,dest_x+1)

                # Kondisi saat current sejajar dengan destinasi pada sumbu y
                else:
                    # Handle kalo dipinggir kiri/kanan
                    if (dest_x == 0):
                        self.goal_position = Position(dest_y,dest_x+1)
                    else:
                        self.goal_position = Position(dest_y,dest_x-1)
                self.static_temp_goals = Position(self.goal_position.y,self.goal_position.x)

            # Kondisi saat teleporter sejajar dengan destinasi dalam sumbu x dan berada pada jalur current->dest (Tidak akan pernah terjadi)
            elif t.position.y == dest_y and (dest_x < t.position.x <= current_x or current_x <= t.position.x < dest_x):

                # Kondisi saat current tidak sejajar dengan destinasi pada sumbu x
                if (dest_y != current_y):
                    self.goal_position = Position(dest_y-1,dest_x) if dest_y > current_y else Position(dest_y+1,dest_x)

                # Kondisi saat current sejajar dengan destinasi pada sumbu x
                else:
                    # Handle kalo dipinggir atas/bawah
                    if (dest_y == 0):
                        self.goal_position = Position(dest_y+1,dest_x)
                    else:
                        self.goal_position = Position(dest_y-1,dest_x)
                        
            # Kondisi saat teleporter sejajar dengan current dalam sumbu x dan berada pada jalur current->dest
            elif t.position.y == current_y and (dest_x < t.position.x <= current_x or current_x <= t.position.x < dest_x): 

                # Kondisi saat current tidak sejajar dengan destinasi pada sumbu x
                if (dest_y != current_y):
                    self.goal_position = Position(dest_y,current_x)

                # Kondisi saat current sejajar dengan destinasi pada sumbu y
                else:
                    # Handle kalo dipinggir kiri/kanan
                    if (current_y == 0):
                        self.goal_position = Position(current_y+1,current_x)
                    else:
                        self.goal_position = Position(current_y-1,current_x)
                self.static_temp_goals = Position(self.goal_position.y,self.goal_position.x)

            # Kondisi saat teleporter sejajar dengan current dalam sumbu y dan berada pada jalur current->dest (TIDAK TERPAKAI KARENA TIDAK AKAN PERNAH TERJADI)
            elif t.position.x == current_x and (dest_y < t.position.y <= current_y or current_y <= t.position.y < dest_y):
                if (current_x == 0):
                    self.goal_position = Position(dest_y,current_x+1)
                else:
                    self.goal_position = Position(dest_y,current_x-1)
                self.static_temp_goals = Position(self.goal_position.y,self.goal_position.x)

    def red_diamond_on_the_path(self, current_x, current_y, dest_x, dest_y):
        for t in self.diamonds:
            if (t.properties.points == 2 and self.board_bot.properties.diamonds == 4):
                # Kondisi saat redDiamond sejajar dengan destinasi dalam sumbu y dan berada pada jalur current->dest
                if t.position.x == dest_x and (dest_y < t.position.y <= current_y or current_y <= t.position.y < dest_y):

                    # Kondisi saat current tidak sejajar dengan destinasi pada sumbu y
                    if (dest_x != current_x):
                        self.goal_position = Position(dest_y,dest_x-1) if dest_x > current_x else Position(dest_y,dest_x+1)

                    # Kondisi saat current sejajar dengan destinasi pada sumbu y
                    else:
                        # Handle kalo dipinggir kiri/kanan
                        if (dest_x == 0):
                            self.goal_position = Position(dest_y,dest_x+1)
                        else:
                            self.goal_position = Position(dest_y,dest_x-1)
                    self.static_temp_goals = Position(self.goal_position.y,self.goal_position.x)

                # Kondisi saat redDiamond sejajar dengan destinasi dalam sumbu x dan berada pada jalur current->dest (Tidak akan pernah terjadi)
                elif t.position.y == dest_y and (dest_x < t.position.x <= current_x or current_x <= t.position.x < dest_x):

                    # Kondisi saat current tidak sejajar dengan destinasi pada sumbu x
                    if (dest_y != current_y):
                        self.goal_position = Position(dest_y-1,dest_x) if dest_y > current_y else Position(dest_y+1,dest_x)

                    # Kondisi saat current sejajar dengan destinasi pada sumbu x
                    else:
                        # Handle kalo dipinggir atas/bawah
                        if (dest_y == 0):
                            self.goal_position = Position(dest_y+1,dest_x)
                        else:
                            self.goal_position = Position(dest_y-1,dest_x)
                            
                # Kondisi saat redDiamond sejajar dengan current dalam sumbu x dan berada pada jalur current->dest
                elif t.position.y == current_y and (dest_x < t.position.x <= current_x or current_x <= t.position.x < dest_x): 

                    # Kondisi saat current tidak sejajar dengan destinasi pada sumbu x
                    if (dest_y != current_y):
                        self.goal_position = Position(dest_y,current_x)

                    # Kondisi saat current sejajar dengan destinasi pada sumbu y
                    else:
                        # Handle kalo dipinggir kiri/kanan
                        if (current_y == 0):
                            self.goal_position = Position(current_y+1,current_x)
                        else:
                            self.goal_position = Position(current_y-1,current_x)
                    self.static_temp_goals = Position(self.goal_position.y,self.goal_position.x)

                # Kondisi saat redDiamond sejajar dengan current dalam sumbu y dan berada pada jalur current->dest (TIDAK TERPAKAI KARENA TIDAK AKAN PERNAH TERJADI)
                elif t.position.x == current_x and (dest_y < t.position.y <= current_y or current_y <= t.position.y < dest_y):
                    if (current_x == 0):
                        self.goal_position = Position(dest_y,current_x+1)
                    else:
                        self.goal_position = Position(dest_y,current_x-1)
                    self.static_temp_goals = Position(self.goal_position.y,self.goal_position.x)
            
            
# TODO: HANDLE SAME BEST VALUE (PICK NEAREST BLOCK)
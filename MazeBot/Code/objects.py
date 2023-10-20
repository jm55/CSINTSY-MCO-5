class tile:
    def __init__(self, x:int, y:int, tile_type:chr):
        self.x = x
        self.y = y
        self.s_dist = 0
        self.g_dist = 0
        self.priority = 0
        self.type = tile_type
        self.parent = None
    
    def dist_s(self, prev_tile):
        self.s_dist = prev_tile.s_dist + 1
        return self.s_dist
    
    def dist_g(self, tile):
        """Compute tile's distance from g[x,y]"""
        self.g_dist = get_manhattan((self.x, self.y), (tile.x, tile.y))
        return self.g_dist

    #Returns tile's x,y coor as tuple
    def get_coor(self):
        return self.x, self.y

    #Checks if the tile is a Goal or not
    def isGoal(self):
        return 'G' in self.type

    #Checks if the tile is a Start or not
    def isStart(self):
        return 'S' in self.type

    #Checks if the tile is a Bot or not
    def isBot(self):
        return 'B' in self.type
    
    def get_pos(self):
        """Returns the coordinate of this tile object"""
        return (self.x, self.y)
    
    def updatePriority(self):
        self.priority = self.s_dist + self.g_dist

    def __str__(self):
        return f"Type: {self.type} - x:{self.x} y:{self.y}"
        
class grid:
    def __init__(self, tiles:tile):
        self.tiles = tiles #2D array of tile objects
    
    def get_tiles(self):
        return self.tiles

    def get_size(self):
        return len(self.tiles)
    
    #Returns a tile object based on the given value
    def get_tile(self, value:chr):
        x = 0
        y = 0
        for row in self.tiles:
            for col in row:
                if value in col.type:
                    return col
                y += 1       
            y = 0
            x += 1
    
    #Returns the type of the tile in the grid
    def get_type(self, x:int, y:int):   
        return self.tiles[x][y].type
    
    #Checks if the tile coordinate for an action is valid and appends it to the action list
    def check_action(self, x:int, y:int, actions:list, parent_pos):
        if self.get_type(x, y) != '#':
            actions.append(self.tiles[x][y])
            if self.tiles[x][y].parent == None and "S" not in self.tiles[x][y].type:
                self.tiles[x][y].parent = self.tiles[parent_pos[0]][parent_pos[1]]
    
    #Returns a list of valid tile objects to explore 
    def get_actions(self, tile:tile):
        actions = []
        if tile.x-1 >= 0:
            self.check_action(tile.x-1, tile.y, actions, tile.get_pos())   
        if tile.y-1 >= 0:
            self.check_action(tile.x, tile.y-1, actions, tile.get_pos())
        if tile.x+1 < len(self.tiles):
            self.check_action(tile.x+1, tile.y, actions, tile.get_pos())
        if tile.y+1 < len(self.tiles):  
            self.check_action(tile.x, tile.y+1, actions, tile.get_pos())
        return actions
    
    #Update bot's position given it's new x and y pos
    def update_bot(self, x:int,y:int):
        b_loc = self.locate_bot()
        s_loc = self.locate_s()
        g_loc = self.locate_g()

        #Reset current tile to initial
        if b_loc == s_loc: #Bot at S
            self.tiles[s_loc[0]][s_loc[1]].type = 'S'
        elif b_loc == g_loc: #Bot at G
            self.tiles[g_loc[0]][g_loc[1]].type = 'G'
        else: #Bot at .
            self.tiles[b_loc[0]][b_loc[1]].type = '.'
        
        if (x,y) == s_loc:
            self.tiles[x][y].type = 'SB'
        elif (x,y) == g_loc:
            self.tiles[x][y].type = 'GB'
        else:
            self.tiles[x][y].type = 'B'
    
    #Locate the Goal assuming that tiles are not empty
    def locate_g(self):
        if len(self.tiles) == 0:
            return None
        for row in self.tiles:
            for col in row:
                if col.isGoal():
                    return col.get_coor()
    
    #Locate the Bot assuming that tiles are not empty
    def locate_bot(self):
        if len(self.tiles) == 0:
            return None
        for row in self.tiles:
            for col in row:
                if col.isBot():
                    return col.get_coor()
    
    #Locate the Start assuming that tiles are not empty
    def locate_s(self):
        if len(self.tiles) == 0:
            return None
        for row in self.tiles:
            for col in row:
                if col.isStart():
                    return col.get_coor()
    
    #Get Bot Tile Object
    def get_bot(self):
        b_loc = self.locate_bot()
        return self.tiles[b_loc[0]][b_loc[1]]
    
    #Get grid as string
    def grid_as_string(self):
        output = ""
        size = self.get_size()
        for y in range(size):
            for x in range(size):
                output += self.get_tiles()[x][y].type + " "
            output += "\n"
        return output

            
class bot:
    def __init__(self, pos=None):
        self.pos = pos
        
    def __str__(self):
        return f"Bot is at position: {self.pos[0]}, {self.pos[1]}"
    
class State():
    def __init__(self, grid, bot_pos):
        # add bot character to grid
        grid[bot_pos[0]][bot_pos[1]][0] = "X" # Temp bot char
        self.grid = grid

def get_manhattan(pos1, pos2):
    """Returns the manhattan distance between two points"""
    return (abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]))

import copy

from objects import *
import utilities as utils
import gui

def getPriority(tile:tile):
    return tile.priority

def astar(grid, rapid_search:bool=False, cont:bool=False, test:bool=False):
    if rapid_search and not test:
        utils.cls()
        gui.header()
        print("Searching...")

    frontier = []
    explored = []
    # Get the tile object of the starting and goal tile
    start_tile = grid.get_tile("S")
    end_tile = grid.get_tile("G")

    # Append the initial state S to the frontier
    frontier.append(start_tile)
    while len(frontier) > 0:
        current_tile = frontier[0]
        current_index = 0
        for index, next_tile in enumerate(frontier):
            if next_tile.priority < current_tile.priority:
                current_tile = next_tile
                current_index = index
        
        # Pop from frontier and append it in explored
        frontier.pop(current_index)
        explored.append(current_tile)
        
        # If the goal is found
        if current_tile == end_tile:
            final_path = []
            current = current_tile
            # Iterate to find the path taken
            while current is not None:
                final_path.append(current)
                current = current.parent
            return [final_path[::-1], frontier, explored]

        # Get the actions
        actions = grid.get_actions(current_tile)

        # Iterate through the action list
        for action_tile in actions:
            is_explored = False
            is_frontier = False
            # Minimize exploration of nodes in the explored list
            for explored_tile in explored:
                if action_tile == explored_tile:
                    is_explored = True
                    break
            
            if is_explored:
                continue
            # Compute for the priority using the total cost from starting tile (s_dist) and manhattan distance to the 
            # Goal tile (g_dist)
            action_tile.dist_s(current_tile)
            action_tile.dist_g(end_tile)
            action_tile.updatePriority()

            # Check if the action tiles is present in the frontier list
            for frontier_tile in frontier:
                # If the action tile is present and its total cost is greater than the one in the frontier, 
                # do not append the action tile to the frontier list
                # if action_tile == frontier_tile and action_tile.s_dist > frontier_tile.s_dist and action_tile.g_dist < frontier_tile.g_dist:
                if action_tile == frontier_tile and action_tile.priority < frontier_tile.priority:
                    frontier_tile.priority = action_tile.priority
                    is_frontier = True
                    break
            
            # Append to frontier if the current action tile is not present
            if not is_frontier: 
                frontier.append(action_tile)

        #frontier = list(dict.fromkeys(frontier))
        #explored = list(dict.fromkeys(explored))

        frontier = list(set(frontier))
        explored = list(set(explored))
        
        frontier.sort(key=getPriority, reverse=False)
        explored.sort(key=getPriority, reverse=False)
        
        if not rapid_search:
            gui.main(copy.deepcopy(grid), frontier, explored, rapid_search, cont)
    # If a path leading to the goal tile is not found, return an empty list     
    return [[], frontier, explored]
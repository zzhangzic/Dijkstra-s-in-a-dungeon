#CMPM146:Game AI
#Name: Zijie Zhang
#Partner Name: Elias Ramirez
#ID:zzhang40
#School ID:1402410

from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush


def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.
    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.
    """
    cost_so_far = {}
    came_from = {}
    queue = []

    heappush(queue,initial_position)
    cost_so_far[initial_position] = 0

    while len(queue) != 0:
        current = heappop(queue)
        
        if current == destination:
            path = []
    
            while current != initial_position:
                path.append(current)
                current = came_from[current]
            path.append(current)
            return path

        edges = navigation_edges(graph, current)
        edges.sort(key = lambda x: x[1])
        
        while len(edges) != 0:
            minedge = edges.pop(0)
            cost = cost_so_far[current] + minedge[1]
            
            if minedge[0] not in cost_so_far:
                heappush(queue, minedge[0])
                cost_so_far[minedge[0]] = cost
                came_from[minedge[0]] = current
            else:
                if cost < cost_so_far[minedge[0]]:
                    #heappush(queue, minedge[0])
                    cost_so_far[minedge[0]] = cost
                    came_from[minedge[0]] = current


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
	cost_so_far ={}
	came_from = {}
	queue = []
	heappush(queue,(0,initial_position))
	came_from[initial_position] = None
	cost_so_far[initial_position] = 0
	while queue:
		currentcost,currentnode = queue.pop()
		nearby = adj(graph,currentnode)
		for cell,nearbycost in nearby:
			new_cost = currentcost+nearbycost
			if cell not in cost_so_far or new_cost <cost_so_far[cell]:
				cost_so_far[cell] = new_cost
				came_from[cell] = currentnode
				heappush(queue,(new_cost,cell))
	return cost_so_far


def navigation_edges(level, cell):
	temp1 = [(1,0),(0,1),(-1,0),(0,-1)]
	temp2 = [(1,1),(1,-1),(-1,-1),(-1,1)]
	result = []
	for temp in temp1:
		neighborxy = (cell[0]+temp[0], cell[1]+temp[1])
		if neighborxy in level['spaces']:
			cost = level['spaces'].get(neighborxy)*0.5+level['spaces'].get(cell)*0.5
			result.append((neighborxy,cost))
	
	for temp in temp2:
		neighborxy = (cell[0]+temp[0], cell[1]+temp[1])
		if neighborxy in level['spaces']:
			cost = level['spaces'].get(neighborxy)*0.5*sqrt(2)+level['spaces'].get(cell)*0.5*sqrt(2)
			result.append((neighborxy,cost))
	return result
	

def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'my_maze.txt', 'a','d'

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_maze_costs.csv')

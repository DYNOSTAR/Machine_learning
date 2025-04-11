# the python script of a supply chain optimization
# system that help users determine the optimal route
# to minimise csot and time of deliveries from suppliers to customers
import heapq

class Route: # this class for reusability
    def __init__(self, destination, cost, time):
        self.destination = destination
        self.cost = cost
        self.time = time

    def __lt__(self, other):  # For heapq comparison
        return (self.cost + self.time) < (other.cost + other.time)


def expert_system(graph, start, end):
    """
    Finds the optimal route using A* search.

    Args:
        graph: A dictionary representing the network of routes.
        start: The starting point.
        end: The destination.
    """

    open_set = []  # Priority queue to store routes to explore
    heapq.heappush(open_set, (0, [start]))  # Start with initial route

    visited = set()  # Keep track of visited nodes
    g_scores = {start: 0}  # Cost from start to each node

    while open_set:
        current_score, path = heapq.heappop(open_set)
        current_location = path[-1]

        if current_location == end:
            return path, g_scores[current_location]

        if current_location in visited:
            continue

        visited.add(current_location)

        # Explore neighboring nodes
        if current_location in graph:
            for route in graph[current_location]:
                new_cost = g_scores[current_location] + route.cost
                new_path = list(path)
                new_path.append(route.destination)

                if route.destination not in g_scores or new_cost < g_scores[route.destination]:
                    g_scores[route.destination] = new_cost
                    # f_score is a heuristic estimate (cost + time)
                    f_score = new_cost + route.time
                    heapq.heappush(open_set, (f_score, new_path))
    return None, float('inf') #No path found


# Example usage of the knowledge base

# Define the graph to enable the machine to learn from
graph = {
    'A': [Route('B', 10, 5), Route('C', 5, 2)],
    'B': [Route('D', 7, 3), Route('E', 12, 7)],
    'C': [Route('D', 4, 1), Route('E', 9, 4)],
    'D': [Route('F', 3, 2)],
    'E': [Route('F', 6, 3)],
    'F': []
}

start_point = input("Enter the starting location: ").upper()
end_point = input("Enter the destination location: ").upper()


best_route, total_cost = expert_system(graph, start_point, end_point)

if best_route:
    print("Best route:", " -> ".join(best_route))
    print("Total cost (Cost + Time):", total_cost)
else:
    print("No route found between the specified locations.")
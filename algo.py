from typing import List

def find_water_flow(heights: List[List[int]]) -> List[List[int]]:
    """
    Returns a list of coordinates where water can flow to both the Northwest and Southeast regions.
    
    Water can flow from a cell to another if the next cell is at the same or lower elevation.
    The Northwest region touches the left and top edges, while the Southeast region touches the right and bottom edges.

    Args:
        heights (List[List[int]]): A matrix representing the elevation map of the grid.

    Returns:
        List[List[int]]: Coordinates of the cells where water can flow to both regions.
    """
    if not heights or not heights[0]:
        return []
    
    rows, cols = len(heights), len(heights[0])
    northwest_reachable, southeast_reachable = set(), set()

    def dfs(r: int, c: int, visited: set, prev_height: int):
        if (
            (r, c) in visited or
            r < 0 or c < 0 or
            r >= rows or c >= cols or
            heights[r][c] < prev_height
        ):
            return
        
        visited.add((r, c))
        
        # Explore all four directions: down, up, right, left
        dfs(r + 1, c, visited, heights[r][c])
        dfs(r - 1, c, visited, heights[r][c])
        dfs(r, c + 1, visited, heights[r][c])
        dfs(r, c - 1, visited, heights[r][c])

    # Start DFS from borders connected to the Northwest (top and left)
    for c in range(cols):
        dfs(0, c, northwest_reachable, heights[0][c])  # Top border
        dfs(rows - 1, c, southeast_reachable, heights[rows - 1][c])  # Bottom border
    
    for r in range(rows):
        dfs(r, 0, northwest_reachable, heights[r][0])  # Left border
        dfs(r, cols - 1, southeast_reachable, heights[r][cols - 1])  # Right border

    # Cells reachable from both regions
    return [[r, c] for r in range(rows) for c in range(cols) if (r, c) in northwest_reachable and (r, c) in southeast_reachable]

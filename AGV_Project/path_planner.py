import heapq

class WarehouseMap:
    def __init__(self, width=20, height=20):
        """初始化栅格地图，0=空闲, 1=障碍物"""
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(height)] for _ in range(width)]
        
    def add_obstacle_block(self, x, y, w, h):
        """添加矩形障碍物区域"""
        for i in range(x, min(x+w, self.width)):
            for j in range(y, min(y+h, self.height)):
                self.grid[i][j] = 1

    def is_valid(self, pos):
        """检查坐标是否越界或碰撞"""
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height and self.grid[x][y] != 1

def heuristic(a, b):
    """启发函数：采用曼哈顿距离以适应仓储直角巷道"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(game_map, start, goal):
    """A* 路径搜索核心算法"""
    if not game_map.is_valid(goal):
        return None

    # 优先队列 (f_score, current_node)
    open_list = []
    heapq.heappush(open_list, (0, start))
    
    came_from = {start: None}
    cost_so_far = {start: 0}
    
    while open_list:
        current = heapq.heappop(open_list)[1]
        
        if current == goal:
            return reconstruct_path(came_from, start, goal)
        
        # 遍历上下左右四个邻居
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in neighbors:
            next_node = (current[0] + dx, current[1] + dy)
            
            if game_map.is_valid(next_node):
                new_cost = cost_so_far[current] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + heuristic(goal, next_node)
                    heapq.heappush(open_list, (priority, next_node))
                    came_from[next_node] = current
    return None

def reconstruct_path(came_from, start, goal):
    """从终点回溯生成路径列表"""
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path
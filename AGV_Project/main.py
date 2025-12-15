import matplotlib.pyplot as plt
import matplotlib.patches as patches
from path_planner import WarehouseMap, a_star_search
from ga_scheduler import GeneticScheduler

class AGVSystem:
    def __init__(self):
        """初始化AGV系统，设定地图和障碍物"""
        self.width = 20
        self.height = 20
        self.map = WarehouseMap(self.width, self.height)
        # 添加障碍物 (模拟货架布局)
        self.map.add_obstacle_block(5, 5, 2, 8) 
        self.map.add_obstacle_block(12, 5, 2, 8)
        self.map.add_obstacle_block(5, 15, 10, 2)
        
        self.battery = 100
        self.current_pos = (0, 0) # 起点
        self.status = "IDLE" 

    def strips_planner(self, target_pos, action_type="PICK"):
        """
        STRIPS规划器：将高层指令分解为原子动作序列
        Action: MOVE_TO, PICK_UP, DROP, CHARGE
        """
        plan_logs = []
        path = []
        
        # 1. 前提检查与移动规划 (Precondition: At Location)
        if self.current_pos != target_pos:
            path = a_star_search(self.map, self.current_pos, target_pos)
            if path:
                plan_logs.append(f"OP: MOVE_TO {target_pos} | Cost: {len(path)} steps")
                self.current_pos = target_pos # 更新虚拟位置
                self.battery -= len(path) * 0.5
            else:
                return ["ERROR: Target Unreachable"], []
        
        # 2. 执行具体动作 (Effect)
        if action_type == "PICK":
            plan_logs.append(f"OP: PICK_UP item at {target_pos}")
        elif action_type == "DROP":
            plan_logs.append(f"OP: DROP item at {target_pos}")
        elif action_type == "CHARGE":
            plan_logs.append(f"OP: CONNECT_CHARGER")
            
        return plan_logs, path

    def visualize(self, full_path, tasks):
        """
        使用 Matplotlib 绘制仿真结果图
        """
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # 1. 绘制网格和障碍物
        for x in range(self.width):
            for y in range(self.height):
                if self.map.grid[x][y] == 1:
                    # 黑色代表障碍物
                    ax.add_patch(patches.Rectangle((x, y), 1, 1, facecolor='black'))
                else:
                    # 白色代表通路
                    ax.add_patch(patches.Rectangle((x, y), 1, 1, fill=False, edgecolor='#ddd'))

        # 2. 绘制路径轨迹
        if full_path:
            # 坐标转换：Matplotlib坐标需要中心对齐(+0.5)
            px = [p[0] + 0.5 for p in full_path]
            py = [p[1] + 0.5 for p in full_path]
            #ax.plot(px, py, color='red', linewidth=2, alpha=0.8, label='AGV Path')

        # 3. 绘制起点、终点和任务点
        start = full_path[0] if full_path else (0,0)
        ax.plot(start[0]+0.5, start[1]+0.5, 'bo', markersize=10, label='Start')
        
        for i, t in enumerate(tasks):
            ax.plot(t[0]+0.5, t[1]+0.5, 'g*', markersize=15, label='Task' if i==0 else "")
            ax.text(t[0], t[1], str(i+1), color='white', fontweight='bold')

        # 设置图表属性
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_title(f"AGV Simulation Result (Final Battery: {self.battery}%)")
        ax.legend(loc='upper right')
        plt.grid(False)
        plt.axis('equal')
        
        print(">>> 仿真图已生成，请查看弹窗。")
        plt.show()

    def run_simulation(self, task_list):
        print("========== 系统启动 ==========")
        print(f"初始电量: {self.battery}%")
        
        # 1. 遗传算法调度 (GA)
        print("\n[Step 1] 正在进行遗传算法任务调度...")
        # 简单模拟距离矩阵用于GA计算
        mock_dist = [[abs(p1[0]-p2[0])+abs(p1[1]-p2[1]) for p2 in task_list] for p1 in task_list]
        ga = GeneticScheduler(task_list, mock_dist)
        best_order_indices = ga.run()
        ordered_tasks = [task_list[i] for i in best_order_indices]
        print(f"优化后的访问顺序: {ordered_tasks}")

        # 2. 顺序执行并记录全路径
        full_trajectory = [self.current_pos]
        
        print("\n[Step 2] 开始执行任务规划...")
        for i, task in enumerate(ordered_tasks):
            # 专家系统规则检查 (Expert System Rules)
            if self.battery < 20:
                print("!!! ALERT: 触发低电量保护规则，中断任务 !!!")
                logs, path = self.strips_planner((0, 0), "CHARGE") # 假设(0,0)是充电桩
                self.battery = 100
                if path: full_trajectory.extend(path[1:])
            
            # STRIPS 规划与执行
            print(f"Task {i+1}: Target {task}")
            logs, path = self.strips_planner(task, "PICK")
            
            # 输出规划日志
            for log in logs:
                print(f"  -> {log}")
            
            if path:
                full_trajectory.extend(path[1:]) # 记录路径用于画图
            else:
                print(f"  Error: 无法到达 {task}")

        # 3. 可视化结果
        print("\n[Step 3] 启动可视化引擎...")
        self.visualize(full_trajectory, ordered_tasks)

if __name__ == "__main__":
    # 实例化系统
    sys = AGVSystem()
    
    # 定义待访问的任务点列表
    tasks_to_visit = [(2, 18), (10, 12), (18, 2), (8, 8), (15, 15)]
    
    # 运行主程序
    sys.run_simulation(tasks_to_visit)
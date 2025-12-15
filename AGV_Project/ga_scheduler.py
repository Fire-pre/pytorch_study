import random

class GeneticScheduler:
    def __init__(self, task_points, distance_matrix, pop_size=50, generations=100):
        self.tasks = task_points 
        self.dist_mat = distance_matrix # 预计算的两两距离矩阵
        self.pop_size = pop_size
        self.generations = generations
        self.mutation_rate = 0.05

    def calculate_fitness(self, route_indices):
        """适应度函数：路径总长度的倒数"""
        total_dist = 0
        for i in range(len(route_indices) - 1):
            u = route_indices[i]
            v = route_indices[i+1]
            total_dist += self.dist_mat[u][v]
        return 1 / total_dist if total_dist > 0 else 0

    def create_population(self):
        """初始化种群"""
        population = []
        indices = list(range(len(self.tasks)))
        for _ in range(self.pop_size):
            individual = indices[:]
            random.shuffle(individual)
            population.append(individual)
        return population

    def crossover(self, parent1, parent2):
        """部分匹配交叉 (PMX) 算子"""
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))
        child = [-1] * size
        child[start:end] = parent1[start:end]
        
        pointer = 0
        for gene in parent2:
            if gene not in child:
                while child[pointer] != -1:
                    pointer += 1
                child[pointer] = gene
        return child

    def mutate(self, individual):
        """交换变异算子"""
        if random.random() < self.mutation_rate:
            idx1, idx2 = random.sample(range(len(individual)), 2)
            individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
        return individual

    def run(self):
        """执行遗传算法迭代"""
        population = self.create_population()
        
        for _ in range(self.generations):
            new_population = []
            # 精英保留策略
            population.sort(key=lambda x: self.calculate_fitness(x), reverse=True)
            new_population.append(population[0])
            
            # 繁殖下一代
            while len(new_population) < self.pop_size:
                p1 = random.choice(population[:10]) # 简单的优选
                p2 = random.choice(population[:10])
                child = self.crossover(p1, p2)
                child = self.mutate(child)
                new_population.append(child)
            population = new_population
            
        return population[0] # 返回最优序列
import math
import random
import copy
import time
random.seed(42) #for reproduction of result

def read_city():
    file_path = 'input.txt'
    try:
        with open(file_path, 'r') as file:
            number_cities = int(file.readline())
            coordinates = []
            for lines in file:
                coordinates.append([int(num) for num in lines.split(' ')])
            return coordinates
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")

def Create_Initial_Population_Nearest_Neighbor(cities,size):
    initial_population = [[] for _ in range(size)]
    for k in range(size):
        initial_city = random.choice(cities)
        cities_temp = copy.deepcopy(cities)
        initial_population[k].append(initial_city)
        cities_temp.remove(initial_city)
        while len(cities_temp)!=0:
            distance = {}
            for i in range(len(cities_temp )):
                distance[i] = math.sqrt((initial_city[0] - cities_temp [i][0]) ** 2 + (initial_city[1] - cities_temp [i][1]) ** 2 + (initial_city[2] - cities_temp [i][2]) ** 2)
            sorted_distance = sorted(list(distance.items()), key=lambda x: x[1])
            initial_population[k].append(cities_temp [sorted_distance[0][0]])
            initial_city = copy.deepcopy(cities_temp [sorted_distance[0][0]])
            cities_temp.remove(initial_city)
            distance = {}
        initial_population[k].append(initial_population[k][0])
    return initial_population

def Create_Initial_Population_Randomly(cities, size):
    initial_population = []
    for i in range(size):
        c = cities.copy()
        random.shuffle(c)
        initial_population.append(c)
        initial_population[i].append(c[0])
    return initial_population

def distance_matrix(population):
    dist_matrix = [[0] * len(population) for _ in range(len(population))]
    for i in range(len(population)):
        for j in range(len(population)):
            dist_matrix[i][j]=math.sqrt((population[i][0] - population[j][0]) ** 2 + (population[i][1] - population[j][1]) ** 2 +(population[i][2] - population[j][2]) ** 2)
    return dist_matrix

def Fitness(population_array):
    dist_dict = {}
    for i in range(len(population_array)):
        dist_dict[i]=0
        for j in range(len(population_array[i])-1):
                dist_dict[i] += math.sqrt((population_array[i][j][0] - population_array[i][j+1][0]) ** 2 + (population_array[i][j][1] - population_array[i][j+1][1]) ** 2 +(population_array[i][j][2] - population_array[i][j+1][2]) ** 2)
        #dist_dict[i] = dist_dict[i]/2
    sorted_dist_list = sorted(list(dist_dict.items()), key=lambda x: x[1])
    #sorted_dist_tuple = tuple(sorted_dist_list)
    fitness_score = [(1/i[1])*max(dist_dict.values()) if i[1]!=0 else float('inf') for i in sorted_dist_list ]
    return fitness_score, sorted_dist_list

def Create_Mating_Pool(population, Rank_List,number_selected_for_mating):
    mating_pool = []
    parents = []
    
    #Roulette Wheel
    
    total = sum(item for item in Rank_List)
    #probability = [(item/total) for item in Rank_List]
    for _ in range(number_selected_for_mating):
        S = random.uniform(0,total)
        partial_sum = 0
        for j in range(len(Rank_List)):
            partial_sum+=Rank_List[j]
            if partial_sum>S:
                parents.append(j)
                break
    mating_pool.extend(population[i] for i in parents)
    return mating_pool

def Crossover(parent1, parent2, start_index, end_index):
    child = []
    child = copy.deepcopy(parent1)
    while start_index<=end_index:
        child[start_index] = parent2[start_index]
        start_index+=1
    return child

def valid_child(parent1, parent2, child):
    #unique_cities = set(map(tuple, child))
    temp_child = copy.deepcopy(child)
    need_cities = [list(t) for t in list(set(map(tuple, parent1)) - set(map(tuple, child)))]
    if len(need_cities)!=0:
        for i in range(0,len(child)-1):
            for j in range(i+1,len(child)-1):
                if child[i]==child[j]:
                    temp_child[j] = need_cities.pop()
                    if len(need_cities)==0:
                        return temp_child
    else:
        return temp_child
                
def Mutation(child):
    index1 = random.randint(1, len(child) - 2)
    index2 = random.randint(1, len(child) - 2)
    while index1 == index2:
        index2 = random.randint(1, len(child) - 2)
    child[index1], child[index2] = child[index2], child[index1]
    return child

def Genetic_Algorithm(cities,population_size,crossover_rate,mutation_rate,start_index,end_index,trials,tic,cutoff):
    #population_array = Create_Initial_Population_Randomly(cities, population_size)         #this constructs the initial population randomly
    population_array = Create_Initial_Population_Nearest_Neighbor(cities,population_size)   #this constructs the initial population using the nearest neighbor heuristic
    rank_list, sorted_list_tuple = Fitness(population_array)
    for i in range(0,trials-1):
        mating_pool = Create_Mating_Pool(population_array, rank_list,number_selected_for_mating)
        parent1 = mating_pool[0]
        parent2 = mating_pool[1]

        if random.random() < crossover_rate:
            child = Crossover(parent1, parent2, start_index, end_index)
            #checks if the child is valid. removes duplication.
            child = valid_child(parent1, parent2, child)
            population_array.append(child)
        #if crossover does not take place, then randomly shuffle
        else: 
            child = cities.copy()
            random.shuffle(child)
            child.append(child[0])
            population_array.append(child)

        if random.random() < mutation_rate:
            child_mutated = Mutation(child)
            population_array.remove(child)
            population_array.append(child_mutated)
        rank_list, sorted_list_tuple = Fitness(population_array)
        best_so_far = (sorted_list_tuple[0][1],population_array[sorted_list_tuple[0][0]])
        del population_array[sorted_list_tuple[-1][0]]
        del rank_list[-1]
        if i%100==0:
            toc = time.perf_counter() 
            if toc-tic > cutoff:
                return best_so_far,toc
    return best_so_far,toc
if __name__ == "__main__":
    tic = time.perf_counter()
    cities = read_city()
    l = len(cities)
    #edge cases
    if l == 0:
        with open('../work/output.txt', 'w') as file:
            file.write(f'{0}\n')
    elif l==1:
        with open('../work/output.txt', 'w') as file:
            file.write(f'{0}\n')
            result = ' '.join(map(str, cities[0]))
            file.write(f'{result}\n')
    elif l==2:
        with open('../work/output.txt', 'w') as file:
            cost = math.sqrt((cities[0][0] - cities[1][0]) ** 2 + (cities[0][1]-cities[1][1]) ** 2 +(cities[0][2] - cities[1][2]) ** 2)
            file.write(f'{cost}\n')
            for item in cities:
                result = ' '.join(map(str, item))
                file.write(f'{result}\n')
            result = ' '.join(map(str, cities[0]))
            file.write(f'{result}\n')
    else:
    #these are to make sure we dont run out of time for different cases
        trials = int(l*1000)
        if trials < 15000:
            trials = 15000
        if l <= 50:
            cutoff = 50
        elif l > 50 and l <= 100:
            cutoff = 65
        elif l > 100 and l <= 200:
            cutoff = 110
        elif l > 200:
            cutoff = 190
        population_size = 10
        if population_size > l:
            population_size = l
        
        #Usually mutation rate and crossover rates are not this high. But the nearest neighbor heuristic is pretty good. So 
        #I tried to introduce more variation in the genome to get possibly more drastic reduction of costs through genetic algorithm.
        
        mutation_rate = 0.9
        crossover_rate = 0.8
        number_selected_for_mating = 2
        start_index = 1 
        end_index =1
        while start_index>=end_index:
            start_index = random.randint(1,l-1)
            end_index = random.randint(1,l-1)
        best_so_far,toc = Genetic_Algorithm(cities,population_size,crossover_rate,mutation_rate,start_index,end_index,trials,tic,cutoff)

        with open('../work/output.txt', 'w') as file:
            file.write(f'{best_so_far[0]}\n')
            for item in best_so_far[1]:
                i = ' '.join(str(x) for x in item)
                file.write(f'{i}\n')
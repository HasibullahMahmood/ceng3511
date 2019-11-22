import numpy
import random
import math
from more_itertools import locate


# ------------------FUNCTIONS----------------------------------
def read_file(file_name):
    file = open(file_name, "r")
    lists = []
    for line in file:
        lists.append(int(line))
    file.close()
    return lists


def fitness_calculator():
    sum_w_list.clear()
    sum_v_list.clear()
    sum_fitness_list.clear()
    for ch in population:
        index_pos = list(locate(ch, lambda a: a == 1))
        sum_w_ch = sum([weights[i] for i in index_pos])
        sum_v_ch = sum([values[i] for i in index_pos])
        if sum_w_ch > allowed_weight:
            fitness_ch = 0
        else:
            fitness_ch = sum_v_ch
        sum_w_list.append(sum_w_ch)
        sum_v_list.append(sum_v_ch)
        sum_fitness_list.append(fitness_ch)
        # print(ch, sum_w_ch, sum_v_ch, fitness_ch)


def maximum(lists):
    index = 0
    maxi = lists[0]
    for i in range(len(lists)):
        if lists[i] > maxi:
            maxi = lists[i]
            index = i
    return [maxi, index]


def minimum(lists):
    index = 0
    mini = lists[0]
    for i in range(len(lists)):
        if lists[i] < mini:
            mini = lists[i]
            index = i
    return [mini, index]


# pop = population, n = number of parents
def roulette_wheel_selection(n=2):
    index_of_selected_parent = []
    for i in range(n):
        rand = random.randrange(0, sum(sum_fitness_list))
        x1, x2 = 0, 0
        for j in range(len(sum_fitness_list)):
            x1 = x2
            x2 = x2 + sum_fitness_list[j]
            if x1 <= rand < x2:
                index_of_selected_parent.append(j)
                break
    return index_of_selected_parent


# pop = population, n = number of parents, k = number of random selected
def tournament_selection(n=2):
    index_of_selected_parent = []
    for i in range(n):
        rand_list = random.sample(range(len(population)), k_tor_sel)
        par = maximum([sum_fitness_list[j] for j in rand_list])
        index_of_selected_parent.append(par[1])
    return index_of_selected_parent


def cross_over(parents, n):
    children = []
    num_of_genes = len(parents[0])
    piece_length = math.floor(num_of_genes / n)
    old_child1 = parents[0]
    old_child2 = parents[1]
    for j in range(2):
        new_child = []
        i = 0
        while i < num_of_genes:
            z = piece_length + i
            while i < num_of_genes and i < z:
                new_child.append(old_child1[i])
                i += 1
            z = piece_length + i
            while i < num_of_genes and i < z:
                new_child.append(old_child2[i])
                i += 1
        children.append(new_child)
        # changing the place of children
        old_child1 = parents[1]
        old_child2 = parents[0]
    return children


# print(cross_over(selected_parents, 4))


def bit_flip_mutate(ch, mutation_rate):
    for i in range(len(ch)):
        if random.random() < mutation_rate:
            if ch[i] == 1:
                ch[i] = 0
            elif ch[i] == 0:
                ch[i] = 1
    return ch


# Survival Selections
def age_based_selection():
    for i in range(len(ages)):
        ages[i] += 1
    for i in range(len(new_children)):
        index_tobe_deleted = maximum(ages)[1]
        if elitism and index_tobe_deleted == maximum(sum_fitness_list)[1]:
            tmp = ages[index_tobe_deleted]
            ages[index_tobe_deleted] = -99
            tmp_idx = index_tobe_deleted
            index_tobe_deleted = maximum(ages)[1]
            population[index_tobe_deleted] = new_children[i]
            ages[index_tobe_deleted] = 0
            ages[tmp_idx] = tmp
        else:
            population[index_tobe_deleted] = new_children[i]
            ages[index_tobe_deleted] = 0


def fitness_based_selection():
    for i in range(len(new_children)):
        index_tobe_deleted = minimum(sum_fitness_list)[1]
        population[index_tobe_deleted] = new_children[i]
        sum_fitness_list[index_tobe_deleted] = 0


# .........Main Program......................
# Assigning file's data to variables
values = read_file("v.txt")
allowed_weight = read_file("c.txt")[0]
weights = read_file("w.txt")
f_out = open('./out.txt', 'w')
print('Capacity :', allowed_weight)
print('Weight :', weights)
print('Value : ', values)
# ..................Input Menu.................
sol_per_pop = int(input('Size of population : '))
num_of_generation = int(input('Max number of generation : '))
print('\nParent Selection\n---------------------------')
print('(1) Roulette-wheel Selection')
print('(2) K-Tournament Selection')
parentSelection = int(input('Which one? '))
if parentSelection == 2:
    k_tor_sel = int(input('k=? (between 1 and ' + str(len(weights)) + ') '))

print('\nN-point Crossover\n---------------------------')
n_point_crossover = int(input('n=? (between 1 and ' + str(len(weights) - 1) + ') '))

print('\nMutation Probability\n---------------------------')
mutProb = float(input('prob=? (between 0 and 1) '))

print('\nSurvival Selection\n---------------------------')
print('(1) Age-based Selection')
print('(2) Fitness-based Selection')
survivalSelection = int(input('Which one? '))
elitism = bool(input('Elitism? (Y or N) '))

# Initial lists
sum_w_list = []
sum_v_list = []
sum_fitness_list = []

print('\n----------------------------------------------------------')
print('Initializing population')
# Creating the initial population.
num_of_gen_per_ch = len(values)
pop_size = (sol_per_pop, num_of_gen_per_ch)
population = numpy.random.randint(2, size=pop_size)
ages = [0] * sol_per_pop

for gen in range(num_of_generation):
    print("Generation ", gen + 1)
    fitness_calculator()
    idx_of_sel_par = []
    if parentSelection == 1:
        idx_of_sel_par = roulette_wheel_selection()
    elif parentSelection == 2:
        idx_of_sel_par = tournament_selection()
    new_children = cross_over([population[idx_of_sel_par[0]], population[idx_of_sel_par[1]]], n_point_crossover)
    random_ch_idx = numpy.random.randint(2)
    new_children[random_ch_idx] = bit_flip_mutate(new_children[random_ch_idx], mutProb)
    if survivalSelection == 1:
        age_based_selection()
    elif survivalSelection == 2:
        fitness_based_selection()
    max_idx = maximum(sum_fitness_list)[1]
    print("chromosome: ", population[max_idx])
    print("weight: ", sum_w_list[max_idx])
    print("value: ", sum_v_list[max_idx])
    print("\n")
max_idx = maximum(sum_fitness_list)[1]
f_out.write("chromosome: " + str(population[max_idx]) + "\n")
f_out.write("weight: " + str(sum_w_list[max_idx]) + "\n")
f_out.write("value: " + str(sum_v_list[max_idx]))
f_out.close()

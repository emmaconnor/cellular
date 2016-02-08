# THIS IS A HACKED TOGETHER SCRIPT 
# THAT RELIES ON A VERY SPECIFIC STRUCTURE
# USE AT YOUR OWN RISK

# imports
import os
import glob
import numpy
import matplotlib.pyplot as plt

def print_blank_classes(list1, classes, name):
    print("{} : class".format(name))
    if len(list1) != len(classes):
        print("SIZE ERROR: len({}) != len(classes)".format(name))
        return
    for i in range(0, len(list1)):
        print("{} : {}".format(list1[i], classes[i]))

def graph_this(sim_list):
    plt.ylim(-1, 3)
    class_dict = {1:0, 2:0, 4:1, 3:2}
    # plot the lams
    for sim_set in sim_list:
        lams = [i.lam for i in sim_set]
        classes = [class_dict[i.classification] for i in sim_set]
        plt.plot(lams, classes, '-o')
    plt.savefig("graphs/graph_lams.png")
    plt.clf()
    
    # plot the lam_t
    for sim_set in sim_list:
        lam_ts = [i.lam_t for i in sim_set]
        classes = [class_dict[i.classification] for i in sim_set]
        plt.plot(lam_ts, classes, "-o")
    plt.savefig("graphs/graph_lam_ts.png")

    # plot the ent
    for sim_set in sim_list:
        ents = [i.ent for i in sim_set]
        classes = [class_dict[i.classification] for i in sim_set]
        plt.plot(ents, classes, '-o')
    plt.savefig("graphs/graph_ents.png")
    plt.clf()

    # plot the ent_ts
    for sim_set in sim_list:
        ent_ts = [i.lam for i in sim_set]
        classes = [class_dict[i.classification] for i in sim_set]
        plt.plot(ent_ts, classes, '-o')
        print_blank_classes(ent_ts, classes, "ent_ts")
    plt.savefig("graphs/graph_ent_ts.png")
    plt.clf()

def print_avs_stds(value_strings, averages, stddevs):
    print("AVERAGES")
    print(("{:<20}"*4).format(value_strings[0], value_strings[1], value_strings[2], value_strings[3]))
    print(("{:<20}"*4).format(averages[0], averages[1], averages[2], averages[3]))
    print()
    print("STD DEVS")
    print(("{:<20}"*4).format(value_strings[0], value_strings[1], value_strings[2], value_strings[3]))
    print(("{:<20}"*4).format(stddevs[0], stddevs[1], stddevs[2], stddevs[3]))

# returns a list of simulations
def read_entry(filename):
    data_file = open(filename + "data.txt", 'r')
    classification_file = open(filename + "classification.txt", 'r')

    data_file = data_file.read().split('\n')
    classification_file = classification_file.read().split('\n')
    local_sim_list = []
    class_4_list = []

    # process classifications into a dict
    class_dict = dict()
    for line in classification_file:
        if line == "":
            break
        class_dict[int(line.split()[0])] = int(line.split()[1])

    for i in range(0, len(data_file)-1, 9):
        iteration = int(data_file[i])
        rules = data_file[i+1]
        lam, lam_t, ent, ent_t = data_file[i+3].split()
        lam, lam_t, ent, ent_t = float(lam), float(lam_t), float(ent), float(ent_t)
        sim = simulation(iteration, rules, lam, lam_t, ent, ent_t, class_dict[iteration])
        local_sim_list += [sim] 
            

    return local_sim_list

# class to contain the info for each simulation
class simulation:
    def __init__(self, iteration, rules, lam, lam_t, ent, ent_t, classification):
        self.iteration = iteration
        self.rules = rules
        self.lam = lam
        self.lam_t = lam_t
        self.ent = ent
        self.ent_t = ent_t
        self.classification = classification
    def __str__(self):
        return self.rules + ", class=" +str(self.classification)
    __repr__ = __str__

# read in all the simulation data as stored in the tmp folder
data_files = glob.glob("tmp/*/")
data_files += glob.glob("tmp2/*/")

data_files.sort()

sim_list = []
full_list = []

# read data files and populate the list
for name in data_files:
    tmp = read_entry(name)
    # sim_list makes a list of lists 
    sim_list += [tmp]
    full_list += tmp


# now that you have all the simulation data....
# compute average lam, lam_t, ent, ent_t and std dev for class 4
class_4_list = [i for i in full_list if i.classification == 4]

lam_av = numpy.mean([i.lam for i in class_4_list])
lam_t_av = numpy.mean([i.lam_t for i in class_4_list])
ent_av = numpy.mean([i.ent for i in class_4_list])
ent_t_av = numpy.mean([i.ent_t for i in class_4_list])

lam_std = numpy.std([i.lam for i in class_4_list])
lam_t_std = numpy.std([i.lam_t for i in class_4_list])
ent_std = numpy.std([i.ent for i in class_4_list])
ent_t_std = numpy.std([i.ent_t for i in class_4_list])

value_strings = ("lambda", "lambda_t", "entropy", "entropy_t")

averages = (lam_av, lam_t_av, ent_av, ent_t_av)
stddevs = (lam_std, lam_t_std, ent_std, ent_t_std)

print_avs_stds(value_strings, averages, stddevs)

# Make the different graphs

graph_this(sim_list)

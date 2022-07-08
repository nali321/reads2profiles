import os
import profiled_meta
import argparse
import switch_maker

parser = argparse.ArgumentParser()

# parser.add_argument("-1", "--read_1", type=str,
#                     help="Filepath to read pair 1")

# parser.add_argument("-2", "--read_2", type=str,
#                     help="Filepath to read pair 2")

parser.add_argument("-f", "--folder", type=str,
                    help="Filepath of folder containing read pairs")               

# parser.add_argument("-b", "--bowtie", type=str,
#                     help="Directory where metagenome.bowtie2.bz2 will go")

parser.add_argument("-c", "--cpus", type=int,
                    help="Number of cpus to use for metaphlan")

parser.add_argument("-i", "--input_type", type=str,
                    help="Filetype of reads for metaphlan")

parser.add_argument("-d", "--depth", type=str,
                    help="What level of taxonomy to start pulling information")

parser.add_argument("-o", "--outdir", type=str,
                    help="Directory where profiled_metagenome.txt will go")

#assign user input to variables

args = parser.parse_args()

folder = args.folder
# r1 = args.read_1
# r2 = args.read_2
# bowtie_path = args.bowtie

#default cpus to use are 12
if args.cpus is None:
    cpus = 12
else:
    cpus = args.cpus

#default input type is fastq
if args.input_type is None:
    input_type = "fastq"
else:
    input_type = args.input_type

#area to figure out user specified depth variable based on taxa
#k, p, c, o, f, g, s
taxa = {
    "k": 'k__',
    "p": 'p__',
    "c": 'c__',
    "o": 'o__',
    "f": 'f__',
    "g": 'g__',
    "s": 's__',
    }

#if the user supplied depth doesn't match a taxa level
#then send error message
if args.depth is None:
    depth = "g"

else:
    depth = args.depth
    try:
        level = taxa[depth]
    except KeyError as error:
        print(error)

#if output directory already exists, send error message
path = args.outdir
try:
    os.mkdir(path)
except OSError as error:
    print(error)

#make the switches directory to create the mpa command
switches = os.path.join(path, "switches").replace("\\", "/")
os.mkdir(switches)

#make the profiled_metagenome.txt folder
profiles = os.path.join(path, "profiles").replace("\\", "/")
os.mkdir(profiles)

#make the bowtie folder
bowtie = os.path.join(path, "bowtie").replace("\\", "/")
os.mkdir(bowtie)

#iterate over folder and collect filepaths of read pairs
reads = []
for filename in os.listdir(folder):
    reads.append(os.path.join(folder, filename).replace("\\", "/"))
reads = sorted(reads)

#sort the reads into pairs
sorted_pairs = []
for i in range(len(reads)):
    #take the previous read and current read if remainder is 1 (since index starts at 0)
    if i%2 == 1:
        sorted_pairs.append((reads[i-1], reads[i]))

#remember numeric ordering of read pairs
#to properly label data collected afterwards
order = []

#run mpa on each pair
for pair in sorted_pairs:
    read_pair_1 = pair[0]
    read_pair_2 = pair[1]

    pair_number = os.path.basename(read_pair_1).split("_")[0]
    order.append(pair_number)

    #create mpa bash switch
    switch_maker.mpa_switch(switches, pair_number, read_pair_1,
    read_pair_2, bowtie, cpus, input_type, profiles)

    #run mpa bash switch for current pair
    os.system(f"bash {switches}/{pair_number}_mpa.sh")

#extract information from all the .txt files
data = profiled_meta.extractor(profiles, taxa, depth)

read_pair_count = 0

#create profiles.txt and write tab delimited columns
f = open(f"{path}/profiles.txt", "w+")
f.write("Read Pair\tClade Name\tRelative Abundance\n")

#go over the read pairs
for profile in data:
    for line in profile:
        clade = line[0]
        abundance = line[1]
        f.write(f"{order[read_pair_count]}\t{clade}\t{abundance}\n")

    read_pair_count+=1
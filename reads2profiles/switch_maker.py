#make prokka switch
def mpa_switch(switches, pair_number, one, two, bowtie, cpus, input_type, profiles):
    f = open(f"{switches}/{pair_number}_mpa.sh", "w+")

    #shebang statement
    f.write("#!/bin/bash")
    f.write("\n")

    #conda profile
    f.write("source /mmfs1/home/4565alin/miniconda3/etc/profile.d/conda.sh")
    f.write("\n")

    #activate tool
    f.write("conda activate mpa")
    f.write("\n")

    #prokka code
    f.write(f"metaphlan {one},{two} --bowtie2out {bowtie}/{pair_number}_metagenome.bowtie2.bz2 --nproc {cpus} --input_type {input_type} -o {profiles}/{pair_number}_profiled_metagenome.txt")
    f.write("\n")

    f.write("conda deactivate")
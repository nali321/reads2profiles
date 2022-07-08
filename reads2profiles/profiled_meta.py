import os

#extract data from profiled_metagenome.txt files
def extractor(filepath, taxa, depth):
    profiles = []
    #iterate over each .txt file, going line by line
    for filename in os.listdir(filepath):
        full = os.path.join(filepath, filename)

        inner = []
        with open (full) as file:
            #line[0] = taxa breakdown | line[2] = abundance
            line_count = 0
            for line in file:
                #only look at 4th line and onwards
                if line_count > 3:
                    split = line.split('\t')
                    clade = split[0]

                    if line_count ==  4:
                        abundance = split[2]
                    
                    else:
                        abundance = split[2]

                    #take clade,abundance pairs that at least match user depth
                    if taxa[depth] in clade:
                        inner.append((clade, abundance))
                    
                line_count+=1

            profiles.append(inner)

    return profiles
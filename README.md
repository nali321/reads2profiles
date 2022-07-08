# reads2profiles

Used to automate MetaPhlAn taxonomy profile generation for metagenomic read pairs produced through whole genome shotgun sequencing. Compiles and extracts data at a taxa level specified by the user.

Inputs:

-f: Filepath to the folder of metagenomic read pairs (must be ordered pairs inside folder)

-c: Number of cpus for metaphlan (OPTIONAL: default value is 12)

-i: Input type for metaphlan (Default value is "fastq")

-d: User specified taxa depth. Will only extract clade data and abundance at or after the specified depth (Default value is "g"). List of accepted inputs:

    k: kingdom (will grab everything output by metaphlan)
    p: phylum
    c: class
    o: order
    f: family
    g: genus
    s: species

-o: Filepath to where output folder will be created

Example: 

    python ~/reads2profiles.py -f ~/read_pairs -c 12 -i fastq -d g -o ~/output

Citation:

[Integrating taxonomic, functional, and strain-level profiling of diverse microbial communities with bioBakery 3](https://elifesciences.org/articles/65088)

Francesco Beghini, Lauren J McIver, Aitor Blanco-Míguez, Leonard Dubois, Francesco Asnicar, Sagun Maharjan, Ana Mailyan, Paolo Manghi, Matthias Scholz, Andrew Maltez Thomas, Mireia Valles-Colomer, George Weingart, Yancong Zhang, Moreno Zolfo, Curtis Huttenhower, Eric A Franzosa, Nicola Segata. eLife (2021)
    

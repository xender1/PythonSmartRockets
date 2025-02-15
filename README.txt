'Smart Rockets': Simple Genetic algorithms

Given a target there will be a Population of Rockets with Genes.
    Genes give the Rocket a velocity and duration

Rockets start with random set of Genes. The goal is to hit a Target.
Based off of time/distance/hitting the target the Rockets get a fitness score.

After set time/all Rockets have crashed/hit the target we use the fitness score
    to create a new generation of Rockets. Higher fitness higher chance to reproduce.

Mutations (.more.)

Fitness Score: thoughts on what to include in the calc
    -if it hit the target mega points
        -more points the faster it got there? (include a time element?)

    -distance to target if it didnt hit
    -# of genes it had to go through to get there (less = better)
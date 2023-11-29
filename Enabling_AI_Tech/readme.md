# Enabling AI Technology: Evolutionary Computation

The project contained in this github repository is to satisfy the AI Enabling Technology project requirement for EN.705.603 Fall semester. In the repository, an implementation of an evolutionary algorithm known as a genetic algorithm is explained in detail and demonstrations are given. The contents of the github repository files are as follow:

## **Summary Notebook**
*Evolutionary_Computation.ipynb:* Overall summary notebook. Contains the flow of the project and to answers to requirements outlined in the rubric. References to the relevant discussion are linked in the subject they pertain to.

*Animate_Evolution:* Executable python code that will search process in an animation. Provides interesting insight into the evolutionary search.

## **Demonstrations**

In the demonstrations folders, several supporting notebooks are contained. If you want to run the code within, you will need to pull the notebook the the top level of the project where the summary notebook is contained.

*GA_Demonstration.ipynb:* Demonstration showing the genetic algorithm iteratively improve itself and a comparison with the original unoptimized graph.

*Genetic_Operator_Demo.ipynb:* Demonstration showing the genetic operators that the project's algorithm uses.

*Random_Search_Compare.ipynb:* Demonstration showing the effectiveness of the genetic algorithm vs a random search.


## **Code**

Under Optimize Layout, the following code is provided.

*Bi_Graph.py:* Class containing the graph that is used to manipulate. Class is made up of a networkx digraph along with some custom calculated parameters that are used in the genetic algorithm.

*Gen_Bipartite_Graph.py:* Helper functions for generating a random bipartite graph* 

*Genetic_Operators.py:* Functions for the genetic operatons that are applied to the population.

*Population.py:* Class containing the collection of individuals and the various functions required to manipulate the population for the genetic operations.

*Optimize_Line_Crossings.py:* The main function used to loop throughout generations and update the population while keeping track of the population's individuals performance at each generation.

*GA_Visualization:* Helper functions to assist in plotting and printing results.

*GA_Operator_Plot:* Helper code to plot the comparison plots. Comparison plots are used for the genetic operator demo. The genetic operator demo displays the crossover and mutation operations used by the genetic algorithm.

*Random_Search.py:* Random search algorithm used for comparison against the genetic algorithm.

## **Images**

*Crossover.png:* Image showing examples of crossover operations.
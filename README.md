<p align="center">
  <img src="https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/documentation/NIA.png" />
</p>

# NatureInspiredAlgorithms

From scratch implementation of nature-inspired algorithms in the programming language python. Based on the book by Jason Brownlee called "Clever Algorithms Nature-Inspired Programming Recipes"
  
## Stochastic Optimization
The majority of the algorithms to be described in this book are comprised
of probabilistic and stochastic processes. What differentiates the ‘stochastic
algorithms’ in this chapter from the remaining algorithms is the specific lack
of 1) an inspiring system, and 2) a metaphorical explanation. Both ‘inspiration’
and ‘metaphor’ refer to the descriptive elements in the standardized
algorithm description.
These described algorithms are predominately global optimization algorithms
and metaheuristics that manage the application of an embedded
neighborhood exploring (local) search procedure. As such, with the exception
of ‘Stochastic Hill Climbing’ and ‘Random Search’ the algorithms may
be considered extensions of the multi-start search (also known as multirestart
search). This set of algorithms provide various different strategies by
which ‘better’ and varied starting points can be generated and issued to a
neighborhood searching technique for refinement, a process that is repeated
with potentially improving or unexplored areas to search.

- [Random Search](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/stochastic/random_search.py)
- [Adaptive Random Search](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/stochastic/adaptive_random_search.py)
- [Stochastic Hill Climbing](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/stochastic/stochastic_hill_climbing.py)
- [Iterated Local Search](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/stochastic/iterated_local_search.py)
- [Guided Local Search](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/stochastic/guided_local_search.py)
- [Variable Neighborhood Search](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/stochastic/variable_neighborhood_search.py)
- [Scatter Search](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/stochastic/scatter_search.py)
- [Tabu Search](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/stochastic/tabu_search.py)
- [Reactive Tabu Search](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/stochastic/reactive_tabu_search.py)

## Evolutionary Algorithms
Evolutionary Algorithms belong to the Evolutionary Computation field of
study concerned with computational methods inspired by the process and
mechanisms of biological evolution. The process of evolution by means
of natural selection (descent with modification) was proposed by Darwin
to account for the variety of life and its suitability (adaptive fit) for its
environment. The mechanisms of evolution describe how evolution actually
takes place through the modification and propagation of genetic material
(proteins). Evolutionary Algorithms are concerned with investigating computational
systems that resemble simplified versions of the processes and
mechanisms of evolution toward achieving the effects of these processes
and mechanisms, namely the development of adaptive systems. Additional
subject areas that fall within the realm of Evolutionary Computation are
algorithms that seek to exploit the properties from the related fields of
Population Genetics, Population Ecology, Coevolutionary Biology, and
Developmental Biology.
- [Genetic Algorithm](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/evolutionary/genetic_programming.py)
- [Genetic Programming](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/evolutionary/genetic_programming.py)
- [Evolution Strategies](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/evolutionary/evolution_strategies.py)
- [Differential Evolution](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/evolutionary/differential_evolution.py)
- [Evolutionary Programming](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/evolutionary/evolutionary_programming.py)
- [Grammatical Evolution](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/evolutionary/grammatical_evolution.py)
- [Learning Classifier System](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/evolutionary/learning_classifier_system.py)

## Physical Algorithms
Physical algorithms are those algorithms inspired by a physical process. The
described physical algorithm generally belong to the fields of Metaheustics
and Computational Intelligence, although do not fit neatly into the existing
categories of the biological inspired techniques (such as Swarm, Immune,
Neural, and Evolution). In this vein, they could just as easily be referred to
as nature inspired algorithms.
The inspiring physical systems range from metallurgy, music, the interplay
between culture and evolution, and complex dynamic systems such as
avalanches. They are generally stochastic optimization algorithms with a
mixtures of local (neighborhood-based) and global search techniques.
- [Simulated Annealing](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/physical/simulated_annealing.py)
- [Extremal Optimization](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/physical/extremal_optimization.py)
- [Harmony Search](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/physical/harmony_search.py)
- [Cultural Algorithm](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/physical/cultural_algorithm.py)
- [Memetic Algorithm](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/physical/memetic_algorithm.py)

## Probabilistic Algorithms
Probabilistic Algorithms are those algorithms that model a problem or
search a problem space using an probabilistic model of candidate solutions.
Many Metaheuristics and Computational Intelligence algorithms may be
considered probabilistic, although the difference with algorithms is the
explicit (rather than implicit) use of the tools of probability in problem
solving. The majority of the algorithms described in this Chapter are
referred to as Estimation of Distribution Algorithms.
- [Population-Based Incremental Learning](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/probabilistic/population_based_incremental_learning.py)
- [UnivariateMarginal Distribution Algorithm](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/probabilistic/univariate_marginal_distribution_algorithm.py)
- [Compact Genetic Algorithm](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/probabilistic/compact_genetic_algorithm.py)
- [Bayesian Optimization Algorithm](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/probabilistic/bayesian_optimization_algorithm.py)
- [Cross-Entropy Method](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/probabilistic/cross_entropy_method.py)


## Swarm Algorithms
Swarm intelligence is the study of computational systems inspired by the
‘collective intelligence’. Collective Intelligence emerges through the cooperation
of large numbers of homogeneous agents in the environment. Examples
include schools of fish, flocks of birds, and colonies of ants. Such intelligence
is decentralized, self-organizing and distributed through out an environment.
In nature such systems are commonly used to solve problems such as effective
foraging for food, prey evading, or colony re-location. The information
is typically stored throughout the participating homogeneous agents, or is
stored or communicated in the environment itself such as through the use
of pheromones in ants, dancing in bees, and proximity in fish and birds.
The paradigm consists of two dominant sub-fields 1) Ant Colony Optimization
that investigates probabilistic algorithms inspired by the stigmergy
and foraging behavior of ants, and 2) Particle Swarm Optimization that
investigates probabilistic algorithms inspired by the flocking, schooling and
herding. Like evolutionary computation, swarm intelligence ‘algorithms’ or
‘strategies’ are considered adaptive strategies and are typically applied to
search and optimization domains.
- [Particle Swarm Optimization](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/swarm/particle_swarm_optimization.py)
- [Ant System](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/swarm/ant_system.py)
- [Ant Colony System](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/swarm/ant_colony_sistem.py)
- [Bees Algorithm](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/swarm/bees_algorithm.py)
- [Bacterial Foraging Optimization Algorithm](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/swarm/bacterial_foraging_optimization_algorithm.py)


## Immune Algorithms
Artificial Immune Systems (AIS) is a sub-field of Computational Intelligence
motivated by immunology (primarily mammalian immunology) that
emerged in the early 1990s (for example [1, 15]), based on the proposal in the
late 1980s to apply theoretical immunological models to machine learning
and automated problem solving (such as [9, 12]). The early works in the
field were inspired by exotic theoretical models (immune network theory)
and were applied to machine learning, control and optimization problems.
The approaches were reminiscent of paradigms such as Artificial Neural
Networks, Genetic Algorithms, Reinforcement Learning, and Learning Classifier
Systems. The most formative works in giving the field an identity
were those that proposed the immune system as an analogy for information
protection systems in the field of computer security. The classical examples
include Forrest et al.’s Computer Immunity [10, 11] and Kephart’s Immune
Anti-Virus [17, 18]. These works were formative for the field because they
provided an intuitive application domain that captivated a broader audience
and assisted in differentiating the work as an independent sub-field.
Modern Artificial Immune systems are inspired by one of three subfields:
clonal selection, negative selection and immune network algorithms.
The techniques are commonly used for clustering, pattern recognition,
classification, optimization, and other similar machine learning problem
domains.
The seminal reference for those interested in the field is the text book by
de Castro and Timmis “Artificial Immune Systems: A New Computational
Intelligence Approach” [8]. This reference text provides an introduction
to immunology with a level of detail appropriate for a computer scientist,
followed by a summary of the state of the art, algorithms, application areas, and case studies.
- [Clonal Selection Algorithm](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/immune/clonal_selection_algorithm.py)
- [Negative Selection Algorithm](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/immune/negative_selection_algorithm.py)
- [Artificial Immune Recognition System](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/immune/artificial_immune_recognition_system.py)
- [Immune Network Algorithm](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/immune/immune_network_algorithm.py)
- [Dendritic Cell Algorithm](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/immune/dendritic_cell_algorithm.py)

## Neural Algorithms
A Biological Neural Network refers to the information processing elements of
the nervous system, organized as a collection of neural cells, called neurons,
that are interconnected in networks and interact with each other using
electrochemical signals. A biological neuron is generally comprised of an
axon which provides the input signals and is connected to other neurons via
synapses. The neuron reacts to input signals and may produce an output
signal on its output connection called the dendrites.
The study of biological neural networks falls within the domain of
neuroscience which is a branch of biology concerned with the nervous
system. Neuroanatomy is a subject that is concerned with the the structure
and function of groups of neural networks both with regard to parts of the
brain and the structures that lead from and to the brain from the rest of the
body. Neuropsychology is another discipline concerned with the structure
and function of the brain as they relate to abstract psychological behaviors.
For further information, refer to a good textbook on any of these general
topics. The field of Artificial Neural Networks (ANN) is concerned with the investigation
of computational models inspired by theories and observation
of the structure and function of biological networks of neural cells in the
brain. They are generally designed as models for addressing mathematical,
computational, and engineering problems. As such, there is a lot of interdisciplinary research in mathematics, neurobiology and computer
science.
An Artificial Neural Network is generally comprised of a collection
of artificial neurons that are interconnected in order to performs some
computation on input patterns and create output patterns. They are
adaptive systems capable of modifying their internal structure, typically
the weights between nodes in the network, allowing them to be used for a
variety of function approximation problems such as classification, regression,
feature extraction and content addressable memory.
Given that the focus of the field is on performing computation with
networks of discrete computing units, the field is traditionally called a
‘connectionist’ paradigm of Artificial Intelligence and ‘Neural Computation’.
There are many types of neural networks, many of which fall into one of
two categories:
Feed-forward Networks where input is provided on one side of the
network and the signals are propagated forward (in one direction)
through the network structure to the other side where output signals
are read. These networks may be comprised of one cell, one layer
or multiple layers of neurons. Some examples include the Perceptron,
Radial Basis Function Networks, and the multi-layer perceptron
networks.
Recurrent Networks where cycles in the network are permitted
and the structure may be fully interconnected. Examples include the
Hopfield Network and Bidirectional Associative Memory.
Artificial Neural Network structures are made up of nodes and weights
which typically require training based on samples of patterns from a problem
domain. Some examples of learning strategies include:
Supervised Learning where the network is exposed to the input
that has a known expected answer. The internal state of the network
is modified to better match the expected result. Examples of this
learning method include the Back-propagation algorithm and the Hebb
rule.
Unsupervised Learning where the network is exposed to input
patterns from which it must discern meaning and extract features.
The most common type of unsupervised learning is competitive learning
where neurons compete based on the input pattern to produce
an output pattern. Examples include Neural Gas, Learning Vector
Quantization, and the Self-Organizing Map.
Artificial Neural Networks are typically difficult to configure and slow
to train, but once prepared are very fast in application. They are generally used for function approximation-based problem domains and prized for their
capabilities of generalization and tolerance to noise. They are known to
have the limitation of being opaque, meaning there is little explanation to
the subject matter expert as to why decisions were made, only how.
There are many excellent reference texts for the field of Artificial Neural
Networks, some selected texts include: “Neural Networks for Pattern Recognition”
by Bishop [1], “Neural Smithing: Supervised Learning in Feedforward
Artificial Neural Networks” by Reed and Marks II [8] and “An Introduction
to Neural Networks” by Gurney [2].
- [Perceptron](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/neural/perceptron.py)
- [Back-propagation](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/neural/back-propagation.py)
- [Hopfield Network](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/neural/hopfield_network.py)
- [Learning Vector Quantization](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/neural/learning_vector_quantization.py)
- [Self-Organizing Map](https://github.com/UPocek/NatureInspiredAlgorithms/blob/main/neural/self-organizing_map.py)

## References

[https://github.com/clever-algorithms/CleverAlgorithms](https://github.com/clever-algorithms/CleverAlgorithms)

import pyomo_mps.parse
from pyomo.kernel import SolverFactory
import pynauty
from collections import defaultdict
from pyomo.repn import generate_standard_repn

model = pyomo_mps.parse('/Users/michaelradigan/pyomo-mps-parser/mps/enlight4.mps')

num_vertices = 0
obj_var_coefs = {}

# Going to make this really easy initially by iterating through once initially and building up an index map
graph_indices = {}
for n, constraint in model.c.items():
    print(constraint.name)
    graph_indices[constraint.name] = num_vertices
    num_vertices += 1

for n, variable in model.vd.items():
    print(variable.name)
    graph_indices[variable.name] = num_vertices
    num_vertices += 1


# I think that first, we go through the objective function build a map from variable->onj_coeff
standard_objective = generate_standard_repn(model.o)
for i, (variable, coefficient) in enumerate(zip(standard_objective.linear_vars, standard_objective.linear_coefs)):
    obj_var_coefs[variable.name] = coefficient

# Should probably look up a slightly nicer way to do this?
adjacency_dict = defaultdict(list)

for name, constraint in model.c.items():
    # variables that share a coefficient within a constraint can coalesce their intermediate nodes
    coalesce_dict = {}
    repn = generate_standard_repn(constraint.body)
    constraint_index = graph_indices[constraint.name]
    for coefficient, variable in zip(repn.linear_coefs, repn.linear_vars):
        # So, first we want an intermediate node 
        variable_index = graph_indices[variable.name]
        if coefficient == 1:
            # For now, if the coefficient is one, we will not use an intermediate node    
            adjacency_dict[constraint_index].append(variable_index)
        elif coefficient in coalesce_dict:
            intermediate_vertex_index = coalesce_dict[coefficient]
            # The intermediate vertex is already connected to the constraint vertex, so here we just need to connect it to this variable
            adjacency_dict[variable_index].append(intermediate_vertex_index)
        else:
            # We do not yet have an intermediate node for this coefficient and vertex, let's make one
            intermediate_vertex_index = num_vertices
            coalesce_dict[coefficient] = intermediate_vertex_index
            adjacency_dict[constraint_index].append(intermediate_vertex_index)
            adjacency_dict[variable_index].append(intermediate_vertex_index)
            num_vertices += 1
       
# We haven't yet done the vertex_colourings yet but let's see what we get now 
graph = pynauty.Graph(num_vertices, False, adjacency_dict, {})
aut = pynauty.autgrp(graph)
print(aut[3])
#print(aut)





#print(model.o())

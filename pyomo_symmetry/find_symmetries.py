import pyomo_mps.parse
from pyomo.kernel import SolverFactory
import pynauty
from collections import defaultdict
from pyomo.repn import generate_standard_repn


def find_symmetries(model):
    """ Given a pyomo model, find the symmetry groups in its constraints and vertices"""

    num_vertices = 0
    obj_var_coefs = {}

    # Going to make this really easy initially by iterating through once initially and building up an index map
    graph_indices = {}
    for n, constraint in model.c.items():
        graph_indices[constraint.name] = num_vertices
        num_vertices += 1

    for n, variable in model.vd.items():
        graph_indices[variable.name] = num_vertices
        num_vertices += 1
        
    # I think that first, we go through the objective function build a map from variable->onj_coeff
    standard_objective = generate_standard_repn(model.o)
    for i, (variable, coefficient) in enumerate(zip(standard_objective.linear_vars, standard_objective.linear_coefs)):
        obj_var_coefs[variable.name] = coefficient

    # Should probably look up a slightly nicer way to do this?
    adjacency_dict = defaultdict(list)

    for name, constraint in model.c.items():
        # variables that share a coefficient within a constraint can coalesce their intermediate vertices
        coalesce_dict = {}
        repn = generate_standard_repn(constraint.body)
        constraint_index = graph_indices[constraint.name]
        for coefficient, variable in zip(repn.linear_coefs, repn.linear_vars):
            # So, first we want an intermediate vertex 
            variable_index = graph_indices[variable.name]
            if coefficient == 1:
                # For now, if the coefficient is one, we will not use an intermediate vertex    
                adjacency_dict[constraint_index].append(variable_index)
            elif coefficient in coalesce_dict:
                intermediate_vertex_index = coalesce_dict[coefficient]
                # The intermediate vertex is already connected to the constraint vertex, so here we just need to connect it to this variable
                adjacency_dict[variable_index].append(intermediate_vertex_index)
            else:
                # We do not yet have an intermediate vertex for this coefficient and vertex, let's make one
                intermediate_vertex_index = num_vertices
                coalesce_dict[coefficient] = intermediate_vertex_index
                adjacency_dict[constraint_index].append(intermediate_vertex_index)
                adjacency_dict[variable_index].append(intermediate_vertex_index)
                num_vertices += 1
        
    # So, in building the adjacency dict, we want to colour constraints in one colour (maybe this changes in the future).
    # We then want to partition the variables by their upper bound, lower bound and their value (if any) in the objective function

    # Inefficient to itereate through yet again but want it to be as obvious as possible what's going on
    # I think that we may also need to consider constraint colourings!
    variable_colouring_dict = defaultdict(set)
    for n, variable in model.vd.items():
        variable_index = graph_indices[variable.name]
        obj_coef = obj_var_coefs[variable.name] if variable.name in obj_var_coefs else 0
        variable_colouring_dict[(variable.lb, variable.ub, obj_coef)].add(variable_index)    

    # Let's look at some constraint colourings
    constraint_colouring_dict = defaultdict(set)
    for n, constraint in model.c.items():
        constraint_index = graph_indices[constraint.name]
        constraint_colouring_dict[(constraint.lb, constraint.ub, constraint.rhs)].add(constraint_index)

    vertex_colourings = []
    vertex_colourings.extend(variable_colouring_dict.values())
    vertex_colourings.extend(constraint_colouring_dict.values())

    # We haven't yet done the vertex_colourings yet but let's just see what we get for now 
    graph = pynauty.Graph(num_vertices, False, adjacency_dict, vertex_colourings)
    aut = pynauty.autgrp(graph)

    return aut
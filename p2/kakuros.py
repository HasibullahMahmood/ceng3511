from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from ortools.sat.python import cp_model


def kakuro_solver(list1):
    # Creates the model.
    model = cp_model.CpModel()

    # Creates the variables.
    x1 = model.NewIntVar(1, 9, 'x1')
    x2 = model.NewIntVar(1, 9, 'x2')
    x3 = model.NewIntVar(1, 9, 'x3')
    y1 = model.NewIntVar(1, 9, 'y1')
    y2 = model.NewIntVar(1, 9, 'y2')
    y3 = model.NewIntVar(1, 9, 'y3')
    z1 = model.NewIntVar(1, 9, 'z1')
    z2 = model.NewIntVar(1, 9, 'z2')
    z3 = model.NewIntVar(1, 9, 'z3')

    # Creates the constraints.
    model.Add((x1 + x2 + x3) == list1[3])
    model.Add((y1 + y2 + y3) == list1[4])
    model.Add((z1 + z2 + z3) == list1[5])
    model.Add((x1 + y1 + z1) == list1[0])
    model.Add((x2 + y2 + z2) == list1[1])
    model.Add((x3 + y3 + z3) == list1[2])

    model.AddAllDifferent([x1,x2,x3])
    model.AddAllDifferent([y1, y2, y3])
    model.AddAllDifferent([z1, z2, z3])
    model.AddAllDifferent([x1, y1, z1])
    model.AddAllDifferent([x2, y2, z2])
    model.AddAllDifferent([x3, y3, z3])

    # Creates a solver and solves the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.FEASIBLE:
        return [solver.Value(x1), solver.Value(x2), solver.Value(x3),
                solver.Value(y1), solver.Value(y2), solver.Value(y3),
                solver.Value(z1), solver.Value(z2), solver.Value(z3)]



# read from input file
with open("kakuro_input.txt", "r") as inputFile:
    items = []
    for line in inputFile.readlines():
        line = line.replace("\n", "")
        line = line.split(", ")
        for item in line:
            items.append(int(item))


result = kakuro_solver(items)

#write to output file
with open("kakuro_output.txt", "w+")as outputFile:
    outputFile.write("x" + ", " + str(items[0]) + ", " + str(items[1]) + ", " + str(items[2]) + "\n" +
                     str(items[3]) + ", " + str(result[0]) + ", " + str(result[1]) + ", " + str(result[2]) + "\n" +
                     str(items[4]) + ", " + str(result[3]) + ", " + str(result[4]) + ", " + str(result[5]) + "\n" +
                     str(items[5]) + ", " + str(result[6]) + ", " + str(result[7]) + ", " + str(result[8]) )

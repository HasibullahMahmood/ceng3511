from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from ortools.sat.python import cp_model


def futoshiki_solver(list1):
    # Creates the model.
    model = cp_model.CpModel()

    # Creates the variables.
    A1 = model.NewIntVar(1, 4, "A1")
    A2 = model.NewIntVar(1, 4, "A2")
    A3 = model.NewIntVar(1, 4, "A3")
    A4 = model.NewIntVar(1, 4, "A4")
    B1 = model.NewIntVar(1, 4, "B1")
    B2 = model.NewIntVar(1, 4, "B2")
    B3 = model.NewIntVar(1, 4, "B3")
    B4 = model.NewIntVar(1, 4, "B4")
    C1 = model.NewIntVar(1, 4, "C1")
    C2 = model.NewIntVar(1, 4, "C2")
    C3 = model.NewIntVar(1, 4, "C3")
    C4 = model.NewIntVar(1, 4, "C4")
    D1 = model.NewIntVar(1, 4, "D1")
    D2 = model.NewIntVar(1, 4, "D2")
    D3 = model.NewIntVar(1, 4, "D3")
    D4 = model.NewIntVar(1, 4, "D4")



    # Creates the constraints.
    model.AddAllDifferent([A1, A2, A3, A4])
    model.AddAllDifferent([B1, B2, B3, B4])
    model.AddAllDifferent([C1, C2, C3, C4])
    model.AddAllDifferent([D1, D2, D3, D4])

    model.AddAllDifferent([A1, B1, C1, D1])
    model.AddAllDifferent([A2, B2, C2, D2])
    model.AddAllDifferent([A3, B3, C3, D3])
    model.AddAllDifferent([A4, B4, C4, D4])

    dic = {"A1": A1,"A2": A2,"A3": A3,"A4": A4,"B1": B1,"B2": B2,"B3": B3,"B4": B4,"C1": C1,"C2": C2,"C3": C3,"C4": C4,
           "D1": D1,"D2": D2,"D3": D3,"D4": D4}

    for item1, item2 in list1:
        if item2.isdigit():
            model.Add(dic[item1] == int(item2))
        else:
            model.Add(dic[item1] > dic[item2])

    # Creates a solver and solves the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.FEASIBLE:
        return [solver.Value(A1), solver.Value(A2), solver.Value(A3), solver.Value(A4)
                , solver.Value(B1), solver.Value(B2), solver.Value(B3), solver.Value(B4)
                , solver.Value(C1), solver.Value(C2), solver.Value(C3), solver.Value(C4)
                , solver.Value(D1), solver.Value(D2), solver.Value(D3), solver.Value(D4)]



# read from input file
with open("futoshiki_input.txt", "r") as inputFile:
    items = []
    for line in inputFile.readlines():
        line = line.replace("\n", "")
        line = line.split(", ")
        tuple1 = (line[0],line[1])
        items.append(tuple1)


result = futoshiki_solver(items)

#write to output file
with open("futoshiki_output.txt", "w+")as outputFile:
    outputFile.write(str(result[0]) + ", " + str(result[1]) + ", " + str(result[2]) + ", " + str(result[3]) + "\n" +
                     str(result[4]) + ", " + str(result[5]) + ", " + str(result[6]) + ", " + str(result[7]) + "\n" +
                     str(result[8]) + ", " + str(result[9]) + ", " + str(result[10]) + ", " + str(result[11]) + "\n" +
                     str(result[12]) + ", " + str(result[13]) + ", " + str(result[14]) + ", " + str(result[15]))

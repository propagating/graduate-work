from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
status = solver.Solve()
objective = solver.Objective()
objective.SetMaximization()

budgetConstraint = solver.Constraint(0, 48, 'maxDollar')

positions = ['qb', 'wr', 'rb', 'te', 'k', 'def']
players = ['ryan', 'john']

for player in players:
    playerIndicator = solver.Constraint(0, 1, player+'active')
    va = solver.IntVar(0, 1, player + 'qb active')
    vb = solver.IntVar(0, 1, player + 'qb bench')
    playerIndicator.SetCoefficient(va, 1)
    playerIndicator.SetCoefficient(vb, 1)
    budgetConstraint.SetCoefficient(va, 12)
    budgetConstraint.SetCoefficient(vb, 12)
    objective.SetCoefficient(va, 24)
    objective.SetCoefficient(vb, 12)


solver.Solve()
if status == pywraplp.Solver.OPTIMAL:

    print('Solution:')
    print('Maximum Profit =', solver.Objective().Value())
else:
    print('The problem does not have an optimal solution.')


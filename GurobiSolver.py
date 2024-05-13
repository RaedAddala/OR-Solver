import gurobipy as gp
from gurobipy import GRB


class GurobiSolverBuilder:
    def __init__(self):
        self.decision_variables = []
        self.constraints_RHS = []
        self.constraints_LHS = []
        self.objectives = []
        self.model = gp.Model()

    def set_objective(self, coeffs, senses):
        self.objectives.append((coeffs, senses))
        return self

    def set_objectives(self, objectives):
        self.objectives = objectives
        return self

    def set_objective_multiple(self):
        for count ,(coeffs, senses) in enumerate(self.objectives):
            if count == 0:
                self.model.setObjective(gp.quicksum(
                coeffs[i] * self.decision_variables[i] for i in range(len(self.decision_variables))), sense=senses)
            else:
                self.model.setObjectiveN(gp.quicksum(
                coeffs[i] * self.decision_variables[i] for i in range(len(self.decision_variables))), index=count,priority=count)

    def set_constraints_LHS(self, LHS):
        self.constraints_LHS = LHS
        return self

    def set_constraints_RHS(self, RHS):
        self.constraints_RHS = RHS
        return self

    def add_constraint(self, expr, sense, rhs, name=""):
        self.model.addConstr(expr, sense, rhs, name=name)
        return self

    def add_constraints(self, name="constraints"):
        self.model.addConstrs((gp.quicksum(self.constraints_LHS[i][j]*self.decision_variables[i] for i in range(
            len(self.decision_variables))) <= self.constraints_RHS[j] for j in range(len(self.constraints_RHS))), name=name)
        return self

    def add_variable(self, name, lb=0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS):
        self.decision_variables.append(self.model.addVar(
            name=name, lb=lb, ub=ub, vtype=vtype))
        return self

    def add_variables(self, number_of_variables, names=None, lbs=None, ubs=None, vtypes=None):
        if names is None:
            names = [("x " + str(i)) for i in range(number_of_variables)]
        if lbs is None:
            lbs = [0 for i in range(number_of_variables)]
        if ubs is None:
            ubs = [GRB.INFINITY for i in range(number_of_variables)]
        if vtypes is None:
            vtypes = [GRB.CONTINUOUS for i in range(number_of_variables)]
        for i in range(number_of_variables):
            self = self.add_variable(names[i], lbs[i], ubs[i], vtypes[i])
        return self

    def build(self):
        self = self.add_constraints()
        self.set_objective_multiple()
        return GurobiSolver(self.model, self.decision_variables)


class GurobiSolver:
    def __init__(self, model, decision_variables):
        self.model = model
        self.decision_variables = decision_variables 

    def solve(self):
        self.model.optimize()

    def get_solution_status(self):
        return self.model.status

    def get_variable(self, name):
        return self.model.getVarByName(name).X

    def get_variables(self):
        vars = {}
        for var in self.model.getVars():
            print(var.varName, '=', var.X)
            vars[var.varName] = var.X
        return vars

    def get_objective_value(self):
        return self.model.objVal
    
    def add_constraint(self, expr, sense, rhs, name=""):
        self.model.addConstr(expr, sense, rhs, name=name)
        return self

# Example usage
# builder = GurobiSolverBuilder()
# builder.add_variables(2, names=['x1', 'x2'])
# builder.set_constraints_LHS([[1, 0], [0, 1]])  # x1 <= 10, x2 <= 20
# builder.set_constraints_RHS([10, 20])
# objectives = [
#     ([1, 0], GRB.MINIMIZE),  # Minimize x1
#     ([0, 1], GRB.MAXIMIZE)   # Maximize x2
# ]
# for coeffs, sense in objectives:
#     builder.set_objective(coeffs, sense)
# solver = builder.build()
# solver.solve()
# optimal_solution = solver.get_variables()
# print("Optimal Solution:")
# print(optimal_solution)
# objective_values = solver.get_objective_value()
# print("Objective Values:")
# print(objective_values)

"""
####  PROCESS SYNTHESIS EXAMPLE #####

"""




from pyomo.environ import *


# Create model object
model = ConcreteModel()

""" # 01 # Set declarations"""
I = model.I = Set(initialize = [i+1 for i in range(8)], doc = 'Process streams')
J = model.J = Set(initialize = [1, 2, 3], doc = 'Process units')



# Set declarations
#	> Fixed cost
CF = {1: 1000, 2: 1500, 3: 2000}

#	> Variable cost
CV = {1: 250, 2:400, 3: 550}


# Variable declarations
# > Continuous Variables
x = model.x = Var(I, domain = NonNegativeReals, doc = 'Process stream mass flows')
C = model.C = Var(J, domain = NonNegativeReals, doc = 'Process total cost')

# > Binary Variables
y = model.y = Var(J, domain = Binary, doc = '1 if process j is selected. 0 otherwise')





#-------------------------------------------------------------------------------
# ### MODEL EQUATIONS ###
#-------------------------------------------------------------------------------

# Material balances (global constraints)
model.massbal1 = Constraint( expr =  x[2] + x[3] == x[4] +x[5])
model.massbal2 = Constraint( expr =  x[6] + x[7] == x[8])

# Disjunction I. Hull Reformulation
model.dis1_1 = Constraint( expr =  C[1] == CF[1] * y[1] + CV[1] * x[1])
model.dis1_2 = Constraint( expr =  x[2] == 0.90 * x[1])
model.dis1_3 = Constraint( expr =  x[1] <= 16 * y[1])
model.dis1_4 = Constraint( expr =  x[2] <= (16*0.90) * y[1])

# Disjunction II. Hull Reformulation
model.dis2_1 = Constraint( expr =  C[2] == CF[2] * y[2] + CV[2] * x[4])
model.dis2_2 = Constraint( expr =  x[6] == 0.82 * x[4])
model.dis2_3 = Constraint( expr =  x[4] <= (10/0.82) * y[2])
model.dis2_4 = Constraint( expr =  x[6] <= 10 * y[2])

# Disjunction III. Hull Reformulation
model.dis3_1 = Constraint( expr =  C[3] == CF[3] * y[3] + CV[3] * x[5])
model.dis3_2 = Constraint( expr =  x[7] == 0.95 * x[5])
model.dis3_3 = Constraint( expr =  x[5] <= (10/0.95) * x[3])
model.dis3_4 = Constraint( expr =  x[7] <= 10 * y[3])

# Logic Propositions
model.log1 = Constraint( expr =  y[2] + y[3] == 1)


# Objective function. Length of the strip
model.Profit = Objective(expr = 1800 * x[8]
						 - ( sum(C[j] for j in J) + 550 * x[1] + 950 * x[3] ),
				         sense = maximize)

# Bounds on variables
A_availability = 16 # ton/h
C_demand       = 10 # ton/h
x_ubs = {1: A_availability, 2: 50, 3: 50, 4: 50, 5: 50, 6: 50, 7: 50, 8: C_demand}



for i in x_ubs:
	x[i].setub(x_ubs[i])

# Solver call
SolverFactory('glpk').solve(model, tee = True)
#SolverFactory('gams').solve(model, tee = True, solver = 'cplex', keepfiles = True)

model.pprint()

#Venti, lvl90, lvl10 talent

from gekko import GEKKO
m = GEKKO() # Initialize gekko
m.options.SOLVER=1  # APOPT is an MINLP solver

# optional solver settings with APOPT
m.solver_options = ['minlp_maximum_iterations 5000', \
                    # minlp iterations with integer solution
                    'minlp_max_iter_with_int_sol 5000', \
                    # treat minlp as nlp
                    'minlp_as_nlp 0', \
                    # nlp sub-problem max iterations
                    'nlp_maximum_iterations 50', \
                    # 1 = depth first, 2 = breadth first
                    'minlp_branch_method 1', \
                    # maximum deviation from whole number
                    'minlp_integer_tol 0.05', \
                    # covergence tolerance
                    'minlp_gap_tol 0.001']

atkpercentmainstat = m.Var(value=0, lb=0,ub=3, integer=True)
critratemainstat = m.Var(value=0, lb=0,ub=1, integer=True)
critdmgmainstat =  m.Var(value=0, lb=0,ub=1, integer=True)
EMmainstat = m.Var(value=0, lb=0,ub=3, integer=True)
HPpercentmainstat = m.Var(value=0, lb=0,ub=3, integer=True)
dmgbonusmainstat = m.Var(value=0, lb=0,ub=1, integer=True)
ERmainstat = m.Var(value=0, lb=0,ub=3, integer=True)

atkpercentsubstat = m.Var(value=0, lb=0,ub=30, integer=True)
atkflatsubstat = m.Var(value=0, lb=0,ub=24, integer=True)
HPflatsubstat = m.Var(value=0, lb=0,ub=24, integer=True)
HPpercentsubstat = m.Var(value=0, lb=0,ub=30, integer=True)
critratesubstat= m.Var(value=0, lb=0,ub=30, integer=True)
critdmgsubstat= m.Var(value=0, lb=0,ub=30, integer=True)
EMsubstat= m.Var(value=0, lb=0,ub=30, integer=True)
ERsubstat = m.Var(value=0, lb=0,ub=30, integer=True)

atkbasechar=263
atkbaseweapon=510
#atkbaseweapon=510
atkbase=atkbasechar+atkbaseweapon
atkpercentother=0*0.32 #windblume ode
#atkpercentother=0
atkflatother=0
dmgbonusother=1*0.24 #stringless
critdmgother=0
critrateother=0
EMother=165 #stringless
HPbase=13050
ERbase=1

atkbase=m.Const(value=atkbasechar+atkbaseweapon)
atkpercentother=m.Const(value=atkpercentother)
atkflatother=m.Const(value=atkflatother)
dmgbonusother=m.Const(value=dmgbonusother) 
critdmgother=m.Const(value=critdmgother)
critrateother=m.Const(value=critrateother)
EMother=m.Const(value=EMother)
HPbase=m.Const(value=HPbase)
vape=m.Const(value=1)
ERbase=m.Const(value=ERbase)

# Equations
m.Equation(atkpercentmainstat+critratemainstat+critdmgmainstat+EMmainstat+HPpercentmainstat+dmgbonusmainstat+ERmainstat == 3)
m.Equation(atkpercentsubstat+atkflatsubstat+critratesubstat+critdmgsubstat+EMsubstat+HPpercentsubstat+HPflatsubstat+ERsubstat==25)
m.Equation(critratemainstat+critdmgmainstat <= 1) #helmet is either crit damage or rate
m.Equation(EMsubstat <= (5-EMmainstat)*6)
m.Equation(critratesubstat <= (5-critratemainstat)*6)
m.Equation(critdmgsubstat <= (5-critdmgmainstat)*6)
m.Equation(atkpercentsubstat <= (5-atkpercentmainstat)*6)
m.Equation(HPpercentsubstat <= (5-HPpercentmainstat)*6)
m.Equation(ERsubstat <= (5-ERmainstat)*6)
#m.Equation(EMmainstat*187+EMsubstat*23 <= 10)
m.Equation(0.05+critratemainstat*0.311+critratesubstat*0.039+critrateother <= 1)
m.Obj(-0.487*20*0.677*(atkbase*(1+atkpercentmainstat*0.466+atkpercentsubstat*0.058+atkpercentother)+(311+atkflatsubstat*19+atkflatother))*(1+0.15+dmgbonusmainstat*0.466+dmgbonusother)*(1+(0.05+critratemainstat*0.311+critratesubstat*0.039+critrateother)*(0.5+critdmgmainstat*0.622+critdmgsubstat*0.078+critdmgother))
      -0.487*(115/90)*17*0.338*(atkbase*(1+atkpercentmainstat*0.466+atkpercentsubstat*0.058+atkpercentother)+(311+atkflatsubstat*19+atkflatother))*(1+dmgbonusother)*(1+(0.05+critratemainstat*0.311+critratesubstat*0.039+critrateother)*(0.5+critdmgmainstat*0.622+critdmgsubstat*0.078+critdmgother))
      -14*(115/90)*722*1.2*(1+0.6+16*(EMmainstat*187+EMsubstat*23+EMother)/(2000+(EMmainstat*187+EMsubstat*23+EMother))))# Objective
m.solve(disp=False) # Solve

print('Results')
print('critratemainstat: ' + str(critratemainstat.value))
print('critdmgmainstat: ' + str(critdmgmainstat.value))
print('atkpercentmainstat: ' + str(atkpercentmainstat.value))
print('dmgbonusmainstat: ' + str(dmgbonusmainstat.value))
print('EMmainstat: ' + str(EMmainstat.value))
#print('ERmainstat: ' + str(ERmainstat.value))
print('HPpercentmainstat: ' + str(HPpercentmainstat.value))

print('critratesubstat: ' + str(critratesubstat.value))
print('critdmgsubstat: ' + str(critdmgsubstat.value))
print('atkpercentsubstat: ' + str(atkpercentsubstat.value))
print('atkflatsubstat: ' + str(atkflatsubstat.value))
print('EMsubstat: ' + str(EMsubstat.value))
#print('ERsubstat: ' + str(ERsubstat.value))
print('HPpercentsubstat: ' + str(HPpercentsubstat.value))
print('HPflatsubstat: ' + str(HPflatsubstat.value))

print('critrate: ' + str(0.05+critrateother.value+critratesubstat.value[0]*0.039+critratemainstat[0]*0.311))
print('critdmg: ' + str(0.5+critdmgother.value+critdmgsubstat.value[0]*0.078+critdmgmainstat[0]*0.622))
print('atkpercent: ' + str(atkpercentother.value+atkpercentsubstat.value[0]*0.058+atkpercentmainstat.value[0]*0.466))
print('dmgbonusgoblet: ' + str(dmgbonusmainstat.value[0]*0.466))
print('EMartifacts:' + str(EMmainstat.value[0]*187+EMsubstat.value[0]*23))
print('EM:' + str(EMmainstat.value[0]*187+EMsubstat.value[0]*23+EMother.value))
#print('ER:' + str(1.0+ERmainstat.value[0]*0.518+ERsubstat.value[0]*0.065))
print('HPpercent:' + str(HPpercentmainstat.value[0]*0.466+HPpercentsubstat.value[0]*0.058))
print('HPflat:' + str(4780+HPflatsubstat.value[0]*299))
print('atkflat:' + str(311+atkflatsubstat.value[0]*19))

print('damage: ' + str(m.options.objfcnval))

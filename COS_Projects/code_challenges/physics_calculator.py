# My Algorithm
# Physics formula from a scratch quantity given by the user 
# Use the initial quantity to build larger more complex derived quantities
# to get the larger more complex quantities, I give the possible quantities that can be calculated with the current quantity 
# then the user choose the one he/she wants
# The initial quantities to be given by the user are the  are mass and acceleration

from physics_formulas import *
print("Welcome to israel's physics calcultor")
print("15 quantites can be calculated within the current scope of this program using the following fundamental quantities")
print("""
      Length
      Mass
      Time
      electric current
      temperature""")
print("""
1   Velocity	
2	Acceleration	
3	Force	
4	Momentum	
5	Pressure	
6	Work Done
7	Power	
8	Density	
9	Frequency	
10	Charge	
11	Electric Potential (Voltage)	
12	Resistance	
13	Capacitance	
14	Thermal Energy (Heat)	
15	Specific Heat Capacity	
16    Area
""")

def quantity_calc(phy_quantity) : 
      print(f"The value of {phy_quantity} = {value[phy_quantity][0]}{value[phy_quantity][1]}")







value = {
'ke' : ke,
'acceleration' : acceleration,
'force' : force
}   
phy_quantity = input("Enter the quantity you want to calculate: ")
quantity_calc(phy_quantity)



from anastruct import SystemElements
import numpy as np
import csv

ss = SystemElements()
element_type = 'truss'

cost = 0.0
supportNum = 0
lanaisdumb = 0
memberNum = 0
#first two rows- support 1 location, support 2 location
#third row - #vertices
#every other row, vertices + force applied ++

#truss name; start x location; start y location; end x location, end y location
with open('bridge.csv', newline='') as csvfile:
    bridge = csv.reader(csvfile, delimiter=',')
    memberNum = memberNum + 1
    for row in bridge:
        print("test %s", row)
        ss.add_truss_element(location=[[float(row[1]), float(row[2])], [float(row[3]), float(row[4])]])
        size = pow(pow((float(row[3]) - float(row[1])),2) + pow((float(row[4]) - float(row[2])),2), 1/2)
        cost = cost + 10*size
        if(size < 1):
            print("Failed: Member %f less than a meter", row[0])
with open('supports.csv', newline='') as csvfile:
    supports = csv.reader(csvfile, delimiter=',')
    for row in supports:
        lanaisdumb = lanaisdumb +1
        if(lanaisdumb <3):
            node_id_temp = ss.find_node_id(vertex =[row[0], row[1]])
            ss.add_support_hinged(node_id=node_id_temp)
        elif(lanaisdumb == 3):
            supportNum = row[0]
        else:
            node_id_temp = ss.find_node_id(vertex =[row[0], row[1]])
            ss.point_load(node_id=ss.find_node_id(vertex =[row[0], row[1]]), Fy= float(row[2]))            
    
cost  = float(cost) + float(supportNum) * 5

if(2*int(supportNum) - 3 != memberNum):
     print("Failed: Not a simple truss")
     print("Num of Supports: %s", supportNum)
     print("Num of Members: %f", memberNum)

print("Cost: %f $", cost)
ss.solve()

with open('bridge.csv', newline='') as csvfile:
    bridge = csv.reader(csvfile, delimiter=',')
    memberNum = bridge.line_num
    id = 0
    for row in bridge:
        id = id +1
        print("Member", row[0], "values", ss.get_element_results(id))


#print(ss.get_node_results_system(node_id=0), ss.get_node_results_system(node_id=-0))

ss.show_structure(annotations=True)
ss.show_reaction_force()
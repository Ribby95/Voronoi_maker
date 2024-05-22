# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 19:28:01 2024

@author: rwstu
"""
import random
import tkinter as tk
import numpy as np
scale=2

def unique(collection):
    temp=[]
    for i in collection:
        if i not in temp:
            temp.append(i)
    return temp

def geop(vector1,vector2):#geometric product
    return np.linalg.det([np.array(vector1),np.array(vector2)])

def intriangle(point,vertex1,vertex2,vertex3):
    temp=set()
    temp.add(np.sign(geop(point-vertex1,vertex2-vertex1)))
    temp.add(np.sign(geop(point-vertex2,vertex3-vertex2)))
    temp.add(np.sign(geop(point-vertex3,vertex1-vertex3)))
    return len(temp)==1

def linecross(segment1,segment2):
    temp=set()
    temp.add(np.sign(geop(segment1[0]-segment2[0],segment2[1]-segment2[0])))
    temp.add(np.sign(geop(segment1[1]-segment2[0],segment2[1]-segment2[0])))
    return len(temp)!=1

def segmentcross(segment1,segment2):
    return linecross(segment1,segment2) and linecross(segment2,segment1)

def in_incircle(point,triangle):
    triangle=[np.array(x) for x in triangle]
    first_point=np.array(triangle[0])
    if geop(triangle[1]-triangle[0],triangle[2]-triangle[0])>0:#lists points in clockwise order
        second_point=triangle[1]
        third_point=triangle[2]
    else:
        second_point=triangle[2]
        third_point=triangle[1]
    M=np.matrix([[first_point[0],first_point[1],first_point[0]**2+first_point[1]**2,1],
                 [second_point[0],second_point[1],second_point[0]**2+second_point[1]**2,1],
                 [third_point[0],third_point[1],third_point[0]**2+third_point[1],1],
                 [point[0],point[1],point[0]**2+point[1]**2,1]
                 ])
    return np.linalg.det(M)>0#if the determinant is positive the points are in the circumcircle

def yorder(coordinate_list):
    return(coordinate_list[1])



root=tk.Tk()
root.title("test title")
root.geometry("550x550")
root.resizable(True,True)
canvas=tk.Canvas(root,bg="white",height=360,width=360)

""" bowyer watson algorithm https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm """

number_of_points=100
points=[]
triangles=[]
limit=360

#sorted_list=[(random.randrange(limit),random.randrange(limit)) for i in range(0,number_of_points)] 
sorted_list=[(12,12),(300,12),(180,180),(50,200)]#,(12,348)]
sorted_list.sort(key=yorder) #sorts the list to make the algorithm faster

names=['A','B','C','D','E','F','G','H','I']

bigtriangle={(-0.5*canvas.winfo_reqheight(),0),(0.5*canvas.winfo_reqwidth(),2*canvas.winfo_reqheight()),(1.5*canvas.winfo_reqheight(),0)}
#must be large enough to completely contain all the points in pointList
triangles=[bigtriangle]

for i in sorted_list: #add all the points one at a time to the triangulation
    bad_triangles=[]
    points.append(i)
    print(i)
    for j in triangles:#first find all the triangles that are no longer valid due to the insertion      
        #print(j)
        if in_incircle(i,j):
            bad_triangles.append(j)
            #print(j)
            triangles.remove(j)
    polygon=[]
    for j in bad_triangles: #find the boundary of the polygonal hole
        for k in unique([{x,y} for x in j for y in j if x!=y]):#iterates through the edges of the triangles
            #print(k)
            if sum([k.issubset(l) for l in bad_triangles])==1:#the sum should be 1 if k is an edge in only one triangle
                polygon.append(k) #if an edge is only in one triangle it is on the outside
    print(polygon)
    for j in polygon:#turns the edges into triangles
        j.add(i)
        triangles.append(j) #adds the new triangles to the triangulation
    #x=input()
    print(triangles)
#print([x for x in triangles if not any([y in x for y in bigtriangle])])

""" puts triangulation on canvas """
colors={0:'cyan',1:'blue', 2:'yellow',3:'green',4:'red',5:'magenta'}
temp=0
for i in triangles:
    if any([x in i for x in bigtriangle]):
        #canvas.create_polygon(*[x for sub in i for x in sub], outline='blue',fill='')
        continue
    canvas.create_polygon(*[x for sub in i for x in sub], outline='blue',fill='')#colors[temp])
    temp=(temp+1)%6
    
canvas.pack()
root.mainloop()
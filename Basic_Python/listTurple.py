list =["pheak", "mony", "many"]
print(list[0])
turple =("pheak", "mony", "many")
print(tuple[0])
#list of number
numbers = [1,2,3,4,5]
list=[]
print(numbers*2)
for i in numbers:
    list.append(i*2)
print(list)

#use operator in list
numbers = [1,2,3,4,5]
list=[]
print(numbers*2)
for i in numbers:
    if i&2:
        list.append(i*2)
    else:
        list.append(str(i)+" is odd number")
print(list)

#list comprehension - sorten code
numbers = [1,2,3,4,5]
list= [i*2 for i in numbers]
print(list)
#list comprehension with control flow
numbers = [1,2,3,4,5]
list=[]
print(numbers*2)
for i in numbers:
    if i&2:
        list.append(i*2)
    else:
        list.append(str(i)+" is odd number")
list= [i*2 if i%2==0 else str(i)+" is odd number" for i in numbers]
print(list)
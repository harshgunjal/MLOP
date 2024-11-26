l=["Apple","Banana","Orange","Pineapple"]

print(l)

for i in l:
    if i == "Orange":
        print("Found at location:",l.index(i))
line=5
for i in range(1,line):
    for j in range(1, i -1):
        print("*",end="")
    print(" ")

print("=========================================")
lines = 5

for i in range(1, lines + 1):
    print(' ' * (lines - i), end='')
    print('*' * i)

print("=========================================")
def fun(a,b):
    try:
        c=a/b
        print(c)
    except ZeroDivisionError:
        print("Cant Divide by zero")
    finally:
        print("code ended")
fun(10,0)

print("=========================================")

dict={"Name": "Dhiraj", "Roll": 71,"Class":"B.tech TY"}
x=id(dict)
print(x)

dict.update({"City":"Ahmednagar"})
y=id(dict)
print(y)

print("hence , we can observe that the id before i.e",x,"and the id after i.e ",y," \n adding the element in the dict are same therefore we can conclude that it is mutable or changeable")
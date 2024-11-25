def return_short_words(word_list):

    return[word for word in word_list if(len(word)<3)]

word =  ["hi", "I","am","new","python", "programmer"]
#
print(return_short_words(word))



def short(word_list):
    short_list=[]
    for word in word_list:
        if(len(word) <3):
            short_list.append(word)
    return short_list

word=["hi","i","am","Python","Programmer"]
print(short(word))


print("=========================================")
cubes = []
for i in range(1, 10):
    a= i ** 3
    cubes.append(a)

print(cubes)

cube=[a**3 for a in range(1,10)]
print(cube)

print("=========================================")

string = "Hello This is python Programming class"

print("Reversed List: "+ string[::-1])


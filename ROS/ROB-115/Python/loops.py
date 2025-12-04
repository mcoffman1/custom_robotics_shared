import time

# Define an array
my_array = [10, 20, 30, 40, 50]

# loop
for i in my_array:
    print(i)

print('===============')

# range loop
for i in range(0,5):
    #print(i*10)
    print(my_array[i])

print('===============')

# while loop
index = 0
while True:
    if index > 4:
        break
    print(my_array[index])
    index+=1

print('===============')

# while loop
index = 0
while True:
    print(my_array[index]) if index < 5 else print('test')
    index+=1
    if index > 6:
        break

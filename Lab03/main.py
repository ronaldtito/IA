import random

def numRam(min, max):
	num = random.randint(min, max)
	return num

def generarBits(arr,n):
	print("generando bits")
	i = 0
	while( i < n):
		arr.append(numRam(0,1))
		i += 1

def mutacionBasadaPos(arr):
	print("mutacion")
	n1 = numRam(1, len(arr) - 2)
	n2 = numRam(1, len(arr) - 2)
	while(n1 == n2):
		n2 = numRam(0, len(arr) - 2)
	print(str(n1) + '\t' + str(n2))
	
	tem = arr[n1]
	arr[n1] = arr[n2]
	arr[n2] = tem


def cargarArray(arr, n):
	i = 0
	while (i < n-1):
		arr.append("*")
		i += 1

def cruzamiento(arr1, arr2):
	print("cruzamiento")
	bits = []
	generarBits(bits,len(arr1))
	#bits = [1,0,1,1,0]
	print(bits)

	size = len(arr1)
	tem1 = []
	cargarArray(tem1, size + 1)
	tem2 = []
	cargarArray(tem2, size + 1)
	tem1[0] = arr1[0]
	tem1[size - 1] = arr1[size - 1]
	tem2[0] = arr2[0]
	tem2[size - 1] = arr2[size - 1]
	print(tem1)
	print(tem2)	
	
	i = 1 
	while(i < size - 1):
		if(bits[i] == 1):
			pos = arr2.index(arr1[i])
			#print(pos)
			tem1[pos] = arr2[pos]
		i += 1	
	i = 1 
	while(i < size - 1):
		if(bits[i] == 0):
			pos = tem1.index("*")
			tem1[pos] = arr1[i]
		i += 1	


	i = 1 
	while(i < size - 1):
		if(bits[i] == 1):
			pos = arr1.index(arr2[i])
			#print(pos)
			tem2[pos] = arr1[pos]
		i += 1
	i = 1 
	while(i < size - 1):
		if(bits[i] == 0):
			pos = tem2.index("*")
			tem2[pos] = arr2[i]
		i += 1	
	
	print(tem1)
	print(tem2)
		


####################################

arr = ["A","B","C","D","A"]

print(arr)
mutacionBasadaPos(arr)
print(arr)

arr2 = ["A","B","C","D","A"]
arr3 = ["A","C","B","D","A"]


cruzamiento(arr2 , arr3)


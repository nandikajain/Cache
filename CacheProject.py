#Name- Nandika Jain
#Roll no- 2019064
#Section- A(CSE)

def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

install_and_import('tabulate')
install_and_import('math')
import math
from tabulate import tabulate

def isPowerOf2(a):	
#This function checks if the value entered by the user is a power of 2 or not 
	while(a%2==0  and a!=1):
		a=a/2
	if(a==1):
		return True
	else:
		return False

def binaryToDecimal(b):
#This function converts a binary number to decimal by taking a String input
	return int(b,2)

def whatPowerOf2(a):
#This function returns what power of 2 is the given number 
	power=0
	while(a%2==0 and a!=1):
		a=a/2
		power+=1
	return power

def DM_read(tagArray,dataArray,address,blockOffset,cacheLineOffset):
#This function reads the data from the cache and looks if the address is present in the cache.
#In case the address is found, it prints Cache Hit along with the data found on the address.
#In case the address is not found, it print Cache Miss
	whatWord=address%(2**blockOffset)	#Extracting the lower bits which tell the word index inside a block
	whatCL=(address//(2**blockOffset))%(2**cacheLineOffset) #Extracting the required bits for the cache line index
	taglength=32-blockOffset-cacheLineOffset
	whatTag=(address//(2**(blockOffset+cacheLineOffset)))%(2**taglength) #Extracting the tag address
	if(tagArray[whatCL]==whatTag):   #Desired block found in the cache
		print("Cache hit!")
		print("Data found on the address is:", end=" ")
		data=dataArray[whatCL][whatWord]
		print(data)
	else:	#Desired block not found in the cache
		print("Cache Miss!")

def DM_write(tagArray,dataArray,address,data,blockOffset,cacheLineOffset):
#This function writes to the desired cache line the data that was entered by the user
	whatWord=address%(2**blockOffset)	#Extracting bits to calculate index for word no
	whatCL=(address//(2**blockOffset))%(2**cacheLineOffset)	#Extracting bits to compute index of cache line
	taglength=32-blockOffset-cacheLineOffset
	whatTag=(address//(2**(blockOffset+cacheLineOffset)))%(2**taglength)	#Extracting th tag address
	if(tagArray[whatCL]==None):	#The required block was empty,so we write to the block
		tagArray[whatCL]=whatTag
		dataArray[whatCL][whatWord]=data
		for i in range(2**blockOffset):	#Iniliasing the remaining words in the cache to 0
			if(i==whatWord):
				continue
			else:
				dataArray[whatCL][i]=0

	elif(tagArray[whatCL]==whatTag):	#Required block is already present inside the cache and is written to
		dataArray[whatCL][whatWord]=data
	else:
		print("Block is being replaced having tag address(in decimal):",end=" ")
		print(tagArray[whatCL])
		tagArray[whatCL]=whatTag	#We replace the existing block in the cache 
		dataArray[whatCL][whatWord]=data
		for i in range(2**blockOffset):#Iniliasing the remaining words in the cache to 0
			if(i==whatWord):
				continue
			else:
				dataArray[whatCL][i]=0

def DM_fullCache(dataArray,CL,tagArray):
#This function prints the entire cache 
	print(tabulate([["L"+str(i), tagArray[i], dataArray[i]] for i in range(CL)], headers=["Cache Line", "Tag", "Data"],tablefmt="fancy_grid"))

def directMappedCache(CL,B):
#This function implements the direct mapping of the cache
	tagArray=[None]*CL
	word_each_block=B//4	#Since one word is 4 bytes
	blockOffset=whatPowerOf2(word_each_block)	#Computing offset for block 
	cacheLineOffset=whatPowerOf2(CL)	#Computing offset for cacheline
	dataArray=[[None for i in range(word_each_block)]for j in range(CL)]
	q=int(input("Enter no of queries: "))
	print()
	print("Enter 1 to read the data")
	print("Enter 2 to write the data")
	print("Enter 3 if you want to print the whole cache")
	for k in range(0,q):
		operation=int(input("Enter your choice: "))
		if(operation==1):
			address=input("Enter the address of the data to be read: ")
			address=binaryToDecimal(address)
			DM_read(tagArray,dataArray,address,blockOffset,cacheLineOffset)
		elif(operation==2):
			address=input("Enter the address where you wish to write: ")
			address=binaryToDecimal(address)
			data=int(input("Enter the data to be written: "))
			DM_write(tagArray,dataArray,address,data,blockOffset,cacheLineOffset)
		elif(operation==3):
			DM_fullCache(dataArray,CL,tagArray)
		else:
			print("Oops! Invalid choice")
		print()

def AM_write(tagArray,dataArray,blockOffset,address,data,CL,word_each_block): 
#This function writes to the address inputted by the user where it finds empty space
#If there is no space empty,i.e cache is full, it replaces according to LRU replacement scheme following temporal locality
	whatWord=address%(2**blockOffset)	#Extracting bits to know the idex of the word where data is to be written
	taglength=32-blockOffset
	whatTag=(address//(2**(blockOffset)))%(2**taglength)	#Extracting the bits to compute tag address
	LRU_value=math.inf
	LRU_index=0	#It stores the index of the cache line which is least access according to LRU
	LRU_max=1
	count=0	#Tells if replacement needs to be done, replace if count=0
	for i in range(CL):

		if(tagArray[i][1]<LRU_value):
			LRU_value=tagArray[i][1]
			LRU_index=i

		if(tagArray[i][1]>LRU_max):
			LRU_max=tagArray[i][1]

		if(tagArray[i][0]==None):#No data is written to a block
			tagArray[i][0]=whatTag
			dataArray[i][whatWord]=data
			tagArray[i][1]=LRU_max	#Since it is a new block, maximum priority,i.e maximum value of the counter according to LRU
			for j in range(2**blockOffset): #Initailising the rest of the words to 0
				if(j==whatWord):
					continue
				else:
					dataArray[i][j]=0
			count+=1

			break
		elif(tagArray[i][0]==whatTag):#Required Tag already present inside the cache
			dataArray[i][whatWord]=data#Updating data
			tagArray[i][1]+=1	#Increased access increases value of LRU counter
			count+=1
			break

	if(count==0):
		print("Block is being replaced having tag address(in decimal) :",end=" ")
		print(tagArray[LRU_index][0])
		index_desired=LRU_index
		tagArray[index_desired][1]=LRU_max+1	#Setting the highest priority in accordance to tamporal locality
		tagArray[index_desired][0]=whatTag	#Replacing the least accessed block with the new required block
		for i in range(word_each_block):	#Iniliasing the rest of the words to 0
			dataArray[index_desired][i]=0
		dataArray[index_desired][whatWord]=data


def AM_read(tagArray,dataArray,blockOffset,address,CL):
#This function reads the data from the cache through Associative Memory Cache
#If it is able to find the address in the cache, it print Cache Hit! along with the contents of the address
#If the address is not present in the cache, it print Cache Miss!
	whatWord=address%(2**blockOffset)	#Extracting the bits to know index of the word
	taglength=32-blockOffset
	whatTag=(address//(2**(blockOffset)))%(2**taglength)	#Extracting the tag address
	count=0	#Tells if the required block is present inside the cache
	for i in range(CL):
		if(tagArray[i][0]==whatTag):	#Block is present in the cache
			print("Cache Hit!")
			data=dataArray[i][whatWord]
			tagArray[i][1]+=1	#Increasing the LRU counter due to the increased access of the block
			print("Data found in the address is : ", end="")
			print(data)
			count+=1
			break
	if(count==0): #Block is not present in the cache
		print("Cache Miss!")


def AM_printCache(dataArray,CL,tagArray):
#This function prints the entire cache 
	print(tabulate([["L"+str(i), tagArray[i], dataArray[i]] for i in range(CL)], headers=["Cache Line", "Tag (Tag Address,LRU counter)", "Data"],tablefmt="fancy_grid"))

def associativeMemoryCache(CL,B):
#This function implements the cache by associative memory mapping
	tagArray=[ [None, 0] for i in range(CL)]	#The tag array contains the tag as well as the frequency of a particular block for LRU replacement
	word_each_block=B//4	#Since one word is 4 bytes
	blockOffset=whatPowerOf2(word_each_block)	#Offset for block
	dataArray=[[None for i in range(word_each_block)]for j in range(CL)]
	q=int(input("Enter no of queries: "))
	print()
	print("Enter 1 to read the data")
	print("Enter 2 to write the data")
	print("Enter 3 if you want to print the whole cache")
	for k in range(0,q):
		operation=int(input("Enter your choice: "))
		if(operation==1):
			address=input("Enter the address of the data to be read: ")
			address=binaryToDecimal(address)
			AM_read(tagArray,dataArray,blockOffset,address,CL)

		elif(operation==2):
			address=input("Enter the address where you wish to write: ")
			address=binaryToDecimal(address)
			data=int(input("Enter the data to be written: "))
			AM_write(tagArray,dataArray,blockOffset,address,data,CL,word_each_block)
		elif(operation==3):
			AM_printCache(dataArray,CL,tagArray)
		else:
			print("Oops! Invalid choice")
		print()

def n_way_AM_write(tagArray,dataArray,address,blockOffset,SetOffset,data,block_each_set):
#This function writes the data to the address specified by the user.
#In case of replacement, it follows LRU replacement scheme
	whatWord=address%(2**blockOffset)	#Computing index for word
	whatSet=(address//(2**blockOffset))%(2**SetOffset) #Calculating the required set
	taglength=32-blockOffset-SetOffset
	whatTag=(address//(2**(blockOffset+SetOffset)))%(2**taglength)	#Getting the required tag 
	LRU_index=0 #Keeps the index of the least accessed block to replace it with the new block
	LRU_value=math.inf
	LRU_max=1
	count=0#Tells if replacement needs to be done, replace if count=0
	for i in range(block_each_set):
		if(tagArray[whatSet][i][1]<LRU_value):
			LRU_value=tagArray[whatSet][i][1]
			LRU_index=i
		if(tagArray[whatSet][i][1]>LRU_max):
			LRU_max=tagArray[whatSet][i][1]
	
		if(tagArray[whatSet][i][0]==whatTag):#Required block already exists in the cache 
			data_index=whatSet*block_each_set+i
			dataArray[data_index][whatWord]=data #Computing corresponding index in data array
			tagArray[whatSet][i][1]+=1#Incrementing the LRU counter due to increased access
			count+=1
			break
		elif(tagArray[whatSet][i][0]==None):#Block space is empty and block can be inserted in the cache
			tagArray[whatSet][i][0]=whatTag
			tagArray[whatSet][i][1]=LRU_max #Setting the LRU counter in accordance to LRU replacement and temporal locality
			data_index=whatSet*block_each_set+i#Computing corresponding index in data array
			dataArray[data_index][whatWord]=data
			count+=1
			for j in range(2**blockOffset):#Iniliasing the rest of the words in the block to 0
				if(j==whatWord):
					continue
				else:
					dataArray[data_index][j]=0
			break

	if(count==0):
		index_desired=whatSet*block_each_set+LRU_index#Computing corresponding index in data array
		print("Block is being replaced having tag address(in decimal): ",end="")
		print(tagArray[whatSet][LRU_index][0])
		tagArray[whatSet][LRU_index][1]=LRU_max+1
		tagArray[whatSet][LRU_index][0]=whatTag
		for i in range(2**blockOffset):#Iniliasing the rest of the words in the block to 0
			dataArray[index_desired][i]=0
		dataArray[index_desired][whatWord]=data

def n_way_AM_read(tagArray,dataArray,address,blockOffset,SetOffset,block_each_set):
#This function reads the data on the address specified by the user
#It prints Cache Hit! along with the data if the block is present in the cache
#It prints Cache Miss! if the address is not in the cache
	whatWord=address%(2**blockOffset)	#Computes index of required word to be read
	whatSet=(address//(2**blockOffset))%(2**SetOffset)	#computes the set of the tag to be read
	taglength=32-blockOffset-SetOffset
	whatTag=(address//(2**(blockOffset+SetOffset)))%(2**taglength) #Computes the tag address
	count=0 #Tells if the quired block is present inside the cache or not
	for i in range(block_each_set):
		if (tagArray[whatSet][i][0]==whatTag):#Required block found in the set
			tagArray[whatSet][i][1]+=1	#Incrementing the block LRU due to increased access
			data_index=whatSet*block_each_set+i   #Calculating corresponding data address index
			data=dataArray[data_index][whatWord]
			print("Cache Hit!")
			print("Data found in the address is : ", end="")
			print(data)
			count+=1
			break
	if(count==0):#Required block not found in the set
		print("Cache Miss! ")

def n_way_AM_print(dataArray,CL,tagArray,n):
#This function prints the entire cache 
	print(tabulate([["L"+str(i), tagArray[i//n][i%n], dataArray[i]] for i in range(CL)], headers=["Cache Line", "Tag (Tag Address,LRU counter)", "Data"],tablefmt="fancy_grid"))
def n_way_AssociativeMemoryCache(CL,B,n):
#This function implements the n-way associative memory cache
	word_each_block=B//4	#Since one word is 4 bytes
	blockOffset=whatPowerOf2(word_each_block)	#Block Offset
	no_of_sets=CL//n    #Computing no of sets 
	SetOffset=whatPowerOf2(no_of_sets)	#Set Offset
	block_each_set=n #block each set is same as the size of each set 
	tagArray=[[ [None, 0] for i in range(block_each_set)] for j in range(no_of_sets)]
	dataArray=[[None for j in range(word_each_block)]for i in range(CL)]
	q=int(input("Enter no of queries: "))
	print()
	print("Enter 1 to read the data")
	print("Enter 2 to write the data")
	print("Enter 3 if you want to print the whole cache")
	for k in range(0,q):

		operation=int(input("Enter your choice: "))
		if(operation==1):
			address=input("Enter the address of the data to be read: ")
			address=binaryToDecimal(address)
			n_way_AM_read(tagArray,dataArray,address,blockOffset,SetOffset,block_each_set)

		elif(operation==2):
			address=input("Enter the address where you wish to write: ")
			address=binaryToDecimal(address)
			data=int(input("Enter the data to be written: "))
			n_way_AM_write(tagArray,dataArray,address,blockOffset,SetOffset,data,block_each_set)

		elif(operation==3):
			n_way_AM_print(dataArray,CL,tagArray,n)
		else:
			print("Oops! Invalid choice")
		print()


print("Cache Project")
print()
print("We take the size of 1 word to be 4 bytes")
print("Enter no of cache lines CL(should be in power of 2) :", end=" ")
CL=int(input())
check=isPowerOf2(CL)
while(check==False):
	print("Enter no of cache lines CL(should be in power of 2) :", end=" ")
	CL=int(input())
	check=isPowerOf2(CL)

print("Enter size of the block B in bytes(should be in the power of 2) and size greater than equal to 4 :" ,end=" ")
B=int(input())
check=isPowerOf2(B)
while(check==False):
	print("Enter size of the block B in bytes(should be in the power of 2) and size greater than equal to 4 :" ,end=" ")
	B=int(input())
	check=isPowerOf2(B)
while(B<4):
	print("Enter size of the block B in bytes(should be in the power of 2) and size greater than equal to 4 :" ,end=" ")
	B=int(input())

print("Enter the following to compute the set of Cache Mapping :")
print()
print("Enter 1 for Direct Mapping ")
print("Enter 2 for Associative Memory Mapping")
print("Enter 3 for n-way Associative Memory Mapping")
choice=int(input('Enter your choice: '))
print()
if(choice==1):
	directMappedCache(CL,B)
elif(choice==2):
	associativeMemoryCache(CL,B)
elif(choice==3):
	n=int(input("Enter the value of n(should be a power of 2) : "))
	check=isPowerOf2(n)
	while(check==False):
		n=int(input("Enter the value of n(should be a power of 2) : "))
		check=isPowerOf2(n)
	n_way_AssociativeMemoryCache(CL,B,n)
else:
	print("Oops! Invalid choice")

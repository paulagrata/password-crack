#Single Core Password Table Generator

#import standard libraries
import hashlib # Hashing the results
import time # Timing the operation
import itertools # Creating controled combinations

#create a list of lower case, upper case, numbers and special characters to include in the password table
lowerCase = ['a','b','c','d','e','f','g','h']
upperCase = ['G','H','I','J','K','L']
numbers = ['0','1','2','3']
special = ['!','@','#','$']

#combine to create a final list
allCharacters = []
allCharacters = lowerCase + upperCase + numbers + special

#define directory path for the password file
#DIR = ('C:\\U\\')
DIR = 'shadow.txt'
#define a hypothetical SALT value
SALT = b"&45Bvx9"

#define the allowable range of password length
PW_LOW = 2
PW_HIGH = 6

#mark the start time
startTime = time.time()

#create an empty list to hold the final passwords
pwList = []

#create a loop to include all passwords within the allowable range
for r in range(PW_LOW, PW_HIGH):
    #apply the standard library interator
    #the product interator will generate the cartesian product for allCharacters repeating for the range of PW_LOW to PW_HIGH
    for s in itertools.product(allCharacters, repeat=r):
        #append each generated password to the final list
        pwList.append(''.join(s))

#for each password in the list generate generate a file containing the hash, password pairs one per line
try:
    #open the output file
    fp = open(DIR+'all','w')
    #process each generated password
    for pw in pwList:
        #perform hashing of the password
        sha256Hash = hashlib.sha256()
        sha256Hash.update(SALT+pw.encode())
        sha256Digest = sha256Hash.hexdigest()
        #write the hash, password pair to the file
        fp.write(sha256Digest +' '+ pw +'\n')
        del(sha256Hash)
except:
    print('File Processing Error')
    fp.close()
    
#now create a dictionary to hold the hash, password pairs for easy lookup
pwDict = {}

try:
    #open each of the output file
    fp = open(DIR+'all','r')
    #process each line in the file which contains key, value pairs
    for line in fp:
        #print(line)
        #extract the key value pairs and update the dictionary
        pairs = line.split()
        pwDict.update({pairs[0] : pairs[1]})
        #fp.close()
except:
    print('File Handling Error')
    fp.close()
    
#when complete calculate the elapsed time
elapsedTime = time.time() - startTime
print('Elapsed Time:', elapsedTime)
print('Passwords Generated:', len(pwDict))
print()

#print out a few of the dictionary entries as an example
cnt = 0
for key,value in (pwDict.items()):
    print (key, value)
    cnt += 1
    if cnt > 10:
        break;
print()

#demonstrate the use of the Dictionary to Lookup a password using a known hash
#lookup a Hash Value
pw = pwDict.get('1dbdfd6de15b28f247ec7e1ec571b9f49098b82a6be400baa0fe0e44aedc4e1c')
#pw = pwDict.get('6b5139a19e725fc0f8b7c2d7ca156e0b237e5f88424f1e9279a2cbf4fdc3c486')
print('Hash Value Tested = 1dbdfd6de15b28f247ec7e1ec571b9f49098b82a6be400baa0fe0e44aedc4e1c')
if pw is None:
    print('Associated Password Not Found')
else:
    print('Associated Password='+ pw)

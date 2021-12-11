#multi-Core Password Table Generator

#import standard libraries
import hashlib # Hashing the results
import time # Timing the operation
import itertools # Creating controled combinations
import multiprocessing # Multiprocessing Library

#create a list of lower case, upper case, numbersand special characters to include in the password table
lowerCase = ['a','b','c','d','e','f','g','h']
upperCase = ['G','H','I','J','K','L']
numbers = ['0','1','2','3']
special = ['!','@','#','$']

#combine to create a final list
allCharacters = []
allCharacters = lowerCase + upperCase + numbers + special

#define Directory Path for the password files
DIR = 'shadow.txt'

#define a hypothetical SALT value
SALT = b"&45Bvx9"

#define the allowable range of password length
PW_LOW = 2
PW_HIGH = 6

def pwGenerator(size):
    pwList = []
    #create a loop to include all passwords
    #with a length of 3-5 characters
    
    for r in range(size, size+1):
        #apply the standard library interator
        for s in itertools.product(allCharacters, repeat=r):
            #append each generated password to the final list
            pwList.append(''.join(s))
            #for each password in the list generate an associated sha256 hash and utilize the hash as the key
            try:
                #open the output file
                fp = open(DIR+str(size),'w')
                #process each generated password
                for pw in pwList:
                    #perform hashing of the password
                    sha256Hash = hashlib.sha256()
                    sha256Hash.update(SALT+pw.encode())
                    sha256Digest = sha256Hash.hexdigest()
                    #write the hash, password pair to the file
                    fp.write(sha256Digest +' '+ pw +'\n')
                    del sha256Hash
            except:
                print('File Processing Error')
            finally:
                fp.close()

#create Main Function
if __name__ =='__main__':
    #mark the starting time of the main loop
    startTime = time.time()
    #create a process Pool with 4 processes
    corePool = multiprocessing.Pool(processes=4)
    #map corePool to the Pool processes
    results = corePool.map(pwGenerator, (2, 3, 4, 5))
    #create a dictionary for easy lookups
    pwDict = {}
    #for each file
    for i in range(PW_LOW, PW_HIGH):
        try:    
            #open each of the output files
            fp = open(DIR+str(i),'r')
            #process each line in the file which contains key, value pairs
            for line in fp:
                # extract the key value pairs and update the dictionary
                pairs = line.split()
                pwDict.update({pairs[0] : pairs[1]})
                fp.close()
        except:
            print('File Handling Error')
            fp.close()
    #once all the files have been hashed calculate the elapsed time
    elapsedTime = time.time() - startTime
    print('Elapsed Time:', elapsedTime,'Seconds')
          
    # print out a few of the dictionary entries as an example
    print('Passwords Generated:', len(pwDict))
    print()
    cnt = 0
    for key,value in (pwDict.items()):
        print(key, value)
        cnt += 1
        if cnt > 10:
            break;
    print()
#demonstrate the use of the Dictionary to Lookup a password using a known hash value
pw = pwDict.get('c6f1d6b1d33bcc787c2385c19c29c208')
print('Hash Value Tested = \ 2bca9b23eb8419728fdeca3345b344fc')
print('Associated Password='+ pw)
import urllib2
 
def getPaddingOracleData(s):
  url = '[REMOTE LOCATION of your oracle]' + str(s)					# Replace with the locatin of your challenge
  return urllib2.urlopen(url).read()[30:]      					 	# Cut the first characters of the response, as they are of no use for our attack

def printAsBlocks(blockInput, length):
    result =""
    counter = 0
    for character in blockInput:
        result += character
        counter += 1
        if((counter % length) == 0):              					# After each block print some spaces (or \t)
            result += " "      
    return result 

# Variables
charAttackCounter = 0                  								# needed to determine in what block the result is
blockPointer = 64
lengtOfDataToDecrypt = 37               							# Flag pattern for this specific challenge: CTF{32-hex}
blockLengthPadding = 8
blocklength = 16                         							# This challenge has an 8 byte cipher, so 16 'characters' will be returned (because hex presentation of a character doubles the result: A = 41)
alphabet = "CTF{}0987654321abcdef"      							# Knowing the flag pattern we could optimise the space we use for our attack
intermediateResult = ""                 							# Nothing found yet (altough we could optimse by putting: CTF{ (and removing those chars 
																	# from  the alphabet), as we know the first 4 characters of the flag anyway, but they
																	# are also usefull for verification of the algorithm so,. decided not to do this.

prefixMaxLength = lengtOfDataToDecrypt     							# Make sure we can work with a full block to be able to 'decrypt' the last symbols
while (prefixMaxLength % blockLengthPadding) != 0:
    prefixMaxLength +=1
prefixLength = prefixMaxLength - len(intermediateResult) -1     	#-1 because we want to make room for the first byte of the encrypted flag

# Start of the attack
for charactersLeftToTest in range(lengtOfDataToDecrypt , 0, -1):
    blockStart = blockPointer    
    charAttackCounter += 1      
    prefix = 'A' * prefixLength    
    dataContainingCharacterToAttack = getPaddingOracleData(prefix)
    resultBlockForCharacterComparison = dataContainingCharacterToAttack[blockStart:blockStart + blocklength]

	# Provide some debugging data	
    print "\n" + "*" * 45 + " Attacking " + "*" * 45
    print "Prefix: " + prefix
    print "Attachking the: " + str(charAttackCounter) + " th character"
    print "Focus Block content: " + resultBlockForCharacterComparison
    print "_: " + printAsBlocks(dataContainingCharacterToAttack, 8)
    print "*" * 101 + "\n"

    for charToGuess in alphabet:
        stringWithPrefixAndCharacterToTuess = getPaddingOracleData(prefix + intermediateResult + charToGuess)
        print charToGuess + ": " + printAsBlocks(stringWithPrefixAndCharacterToTuess,8)
        print "\tRequest: " + prefix + intermediateResult + charToGuess
        if(stringWithPrefixAndCharacterToTuess[blockStart:blockStart + blocklength] == resultBlockForCharacterComparison):
            intermediateResult += charToGuess            
            print "\tSucces, character found: " + charToGuess + " Results so far: " + intermediateResult
            prefixLength -= 1
            break

from owlready2 import *
from nltk import *
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize, sent_tokenize
from decimal import Decimal
import string

#Ontology-enabled Plant Identification System
#Developed by Maxwell Alexander for Master's Capstone - University of Wisconsin - Milwaukee

#Holders for the possibilities to be returned by the system
currentPossibilities = []
possibilitiesIn = []
possibilitiesOut = []

#booleans used to track whether a certain attribute has been considered 
usedColor = False
usedCluster = False
usedPosition = False
usedFlowerShape = False
usedFlowerSymmetry = False
usedLeafArrangement = False
usedLeafDivision = False
usedLeafMargin = False
usedLeafLength = False
usedLeafShape = False
usedPetalLength = False
usedPetalNumber = False
'''usedPlantEnvironment = False'''
usedPlantSize = False

#Load the ontology from the .owl file and establish a reasoner to support queries
onto_path.append(".")
onto = get_ontology("file://Rubiaceae_of_WI.owl").load
#sync_reasoner(infer_property_values = True)


#not currently implemented - wordnet was not specific enough for botany terminology. Currently using a custom list of synonyms
'''
syns = wordnet.synsets("WORDTOFIND")
'''

#dictionary to translate words to ints
numbers = ['one',
               'two',
               'three',
               'four',
               'five',
               'six',
               'seven',
               'eight',
               'nine',
               'ten',
               'eleven',
               'twelve',
               'teen',
               'twenty',
               'thirty',
               'forty']

#Function to print a nicely-formatted list of species from the returned ontology queries
def printFlowerList(inList):
    for x in inList:
        guess = str(x)
        guess = guess.replace("Rubiaceae_of_WI.", "")
        guess = guess.replace("_"," ")
        print("   " + guess)

#Function to identify which questions have yet to be asked, and to return questions to ask the user    
def askQuestions():
    global usedColor
    global usedCluster
    global usedPosition
    global usedFlowerShape
    global usedFlowerSymmetry
    global usedLeafArrangement
    global usedLeafDivision
    global usedLeafMargin
    global usedLeafLength
    global usedLeafShape
    global usedPetalLength
    global usedPetalNumber
    global usedPlantEnvironment
    global usedPlantSize
    
    print(onto().search(is_a = onto().LooseFlower_Cluster))
    
    if not usedColor:
        print("\n   What color are the flowers?\n")
    elif not usedCluster:
        print("\n   How are the flowers clustered together?")
        print("   Are they clustered together like a ball? A spike? Or are they loose / sparsely clustered?\n")
    elif not usedPosition:
        print("\n   How are the flowers positioned on the plant?\n")
        print("   Are they apical (at the top of the plant)? Or axillary (at the bottom)?\n")
    elif not usedLeafLength:
        print("\n   How long (in cm) roughly are the plant's leaves?")
    elif not usedFlowerShape:
        print("\n   What shape are the flowers?\n")
        print("   Do they look like a bell? Trumpet? Or more like a disc?\n")
    elif not usedLeafShape:
        print("\n   What shape are the plant's leaves?")
        print("   Are they larger near the tip or the base? Are they round? Straight?\n")
    elif not usedFlowerSymmetry:
        print("\n   Is there any notable symmetry to the flowers?\n")
    elif not usedPetalLength:
        print("\n   How long (in mm) roughly are the petals on the flowers?\n")
    elif not usedPetalNumber:
        print("\n   How many petals are there on each flower?\n")   
    elif not usedLeafArrangement:
        print("\n   How are the leaves arranged on the stalk?")
    elif not usedLeafDivision:
        print("\n   Do the leaves have lobes, or are they 'simple' looking?")
    elif not usedLeafMargin:
        print("\n   Is there anything noticeable about the edges of the leaves?")  
    elif not usedPlantSize:
        print("\n   About how tall (in cm) is the plant?")
    else:
        print("\nI can't think of any more questions to ask... you should start over!")
    '''if not usedPlantEnvironment:
        print("   Do you know what environment the plant is growing in?")
    '''

#Built-in NLTK sentence tokenize function
def sentTokenize(text):
    sents = sent_tokenize(text)
    return sents

#Check all flower-adjacent sentences to determine if any of the identified synonyms are present
#Add appropriate ontology queries for each found color
def checkFlowerColor(sents):
    vals = ["blue","green","orange","pink","purple","red","transparent","white","yellow"]
    
    valDict = {"blue" : ["blue","aqua", "navy", "marine", "cornflower", "midnight", "royal"],
                 "green" : ["green","lime", "forest", "moss", "olive", "sage"],
                 "orange": ["orange","salmon", "coral", "sienna"],
                 "pink" : ["pink", "orchid", "magenta", "grapefruit"],
                 "purple": ["purple", "plum", "violet", "indigo"],
                 "red": ["red","maroon", "scarlet", "vermillion"],
                 "transparent":["transparent","clear","see-through","see through"],
                 "white":["white","gray", "snow", "silver"],
                 "yellow":["yellow", "goldenrod", "khaki", "wheat", "tan"]}
    
    toSearch = []
    
    for sent in sents:
        for x in vals:
            for syns in valDict[x]:
                if syns in sent:
                    toSearch.append(x)
    
    return toSearch

#Function to parse number words to numbers 
def parse_int(textnum, numwords={}):    
    '''
    Function collected from text2int package via github
    '''
    if textnum.isdigit():
        return int(textnum)
    # create our default word-lists
    if not numwords:

        # singles
        units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
        ]

        # tens
        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        
        # larger scales
        scales = ["hundred", "thousand", "million", "billion", "trillion"]
        
        # divisors
        numwords["and"] = (1, 0)

        # perform our loops and start the swap
        for idx, word in enumerate(units):    numwords[word] = (1, idx)
        for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    # primary loop
    current = result = 0
    # loop while splitting to break into individual words
    for word in textnum.replace("-"," ").split():
        # if problem then fail-safe
        if word not in numwords:
            raise Exception("Illegal word: " + word)

        # use the index by the multiplier
        scale, increment = numwords[word]
        current = current * scale + increment
        
        # if larger than 100 then push for a round 2
        if scale > 100:
            result += current
            current = 0

    # return the result plus the current
    return result + current

#Check all flower-adjacent sentences to determine if any of the identified synonyms are present
#Add appropriate ontology queries for each found clustering
def checkFlowerCluster(sents):
    vals = ["ball","few","loose","spike"]
    
    valDict = {"ball" : ["ball","round","sphere","circle"],
               "few" : ["few","solo","alone","apart","corumb","cyme"],
               "loose": ["loose","separate","panicle","thyrse"],
               "spike" : ["spike", "cone", "rod", "vertical","raceme"]}

    toSearch = []
    
    for sent in sents:
        for x in vals:
            for syns in valDict[x]:
                if syns in sent:
                    toSearch.append(x)
    
    return toSearch

#Check all flower-adjacent sentences to determine if any of the identified synonyms are present
#Add appropriate ontology queries for each location found
def checkFlowerPosition(sents):
    
    vals = ["apical","axillary"]
    
    valDict = {"apical" : ["apical","tip","on top"],
               "axillary" : ["axillary","at bottom", "bottom of"]}

    
    toSearch = []
    
    for sent in sents:
        for x in vals:
            for syns in valDict[x]:
                if syns in sent:
                    toSearch.append(x)
    
    return toSearch

#Check all flower-adjacent sentences to determine if any of the identified synonyms are present
#Add appropriate ontology queries for each found shape
def checkFlowerShape(sents):
    vals = ["bell","rayed"]
    
    valDict = {"bell" : ["bell","tubular","cup","saucer","trumpet","funnel"],
               "rayed" : ["rayed","flat","stellate","salverform","disc"]}

    
    toSearch = []
    
    for sent in sents:
        for x in vals:
            for syns in valDict[x]:
                if syns in sent:
                    toSearch.append(x)
    
    return toSearch


#Check all flower-adjacent sentences to determine if any of the identified synonyms are present
#Add appropriate ontology queries for each found symmetry
def checkFlowerSymmetry(sents):
    vals = ["radial","none"]
    
    valDict = {"radial" : ["radial"],
               "none" : ["asymmetrical"]}

    
    toSearch = []
    
    for sent in sents:
        for x in vals:
            for syns in valDict[x]:
                if syns in sent:
                    toSearch.append(x)
    
    return toSearch


#Check all leaf-adjacent sentences to determine if any of the identified synonyms are present
#Add appropriate ontology queries for each found arrangement
def checkLeafArrangement(sents):
    
    vals = ["basal","opposite","whorled"]
    
    valDict = {"basal" : ["basal","bottom","ground","base"],
               "opposite" : ["opposite","matched","symmetrical"],
               "whorled" : ["whorled","circular","circle"]}

    
    toSearch = []
    
    for sent in sents:
        for x in vals:
            for syns in valDict[x]:
                if syns in sent:
                    toSearch.append(x)
    
    return toSearch

#Check all leaf-adjacent sentences to determine if any of the identified synonyms are present
#Add appropriate ontology queries for each found division
def checkLeafDivision(sents):
    vals = ["simple"]
    
    valDict = {"simple" : ["simple","unlobed"],
               "complex" : ["complex"]}

    
    toSearch = []
    for sent in sents:
        for x in vals:
            for syns in valDict[x]:
                if syns in sent:
                    toSearch.append(x)
    
    return toSearch

#Check all leaf-adjacent sentences to determine if any of the identified synonyms are present
#Add appropriate ontology queries for each found margin type
def checkLeafMargin(sents):
    vals = ["hairy"]
    
    valDict = {"hairy" : ["hairy","fuzzy",]}
    
    toSearch = []
    
    for sent in sents:
        for x in vals:
            for syns in valDict[x]:
                if syns in sent:
                    toSearch.append(x)
    
    return toSearch


#Check all leaf-adjacent sentences to determine if any length data is present
#Add appropriate ontology queries for each found leaf length
def checkLeafLength(sents):
    vals = ["millimeter","inch","centimeter","cm ","mm "]
    global numbers
    toSearch = []
    lastNum = 0
    
    for sent in sents:
        words = sent.split()

        for word in words:

            if (not word.isalpha()) and (not word.isdigit()):
                justDigs = ""
                justLetters = ""
                for x in word:
                    if x.isdigit():
                        justDigs = justDigs + x
                    else:
                        justLetters = justLetters + x
                lastNum = justDigs        
                if justLetters == "millimeter" or justLetters == "mm":
                    lastNum = lastNum/10
                elif justLetters == "inch" or justLetters == "inches":
                    lastNum = lastNum*2.54
                else:
                    lastNum = lastNum
               
                toSearch.append(lastNum)
                return toSearch
                    
            for eachNum in numbers:
                if (eachNum == word) or (word.isdigit()):
                    lastNum = parse_int(word)
                    for x in vals:
                        if x in sent:
                            if x == "millimeter" or x == "mm ":
                                lastNum = lastNum/10
                            elif x == "inch":
                                lastNum = lastNum*2.54
                            else:
                                lastNum = lastNum
                                
                            toSearch.append(lastNum)        
    return toSearch


#Check all leaf-adjacent sentences to determine if any of the identified synonyms are present
#Add appropriate ontology queries for each found shape
def checkLeafShape(sents):
    vals = ["heart","linear","widerMiddle","widerTip"]
    
    valDict = {"heart" : ["heart","round","cordate","sinuate","orbicular","reniform"],
               "linear" : ["linear","elliptic","sessile","lanceolate","oblong"],
               "widerMiddle":["middle","ovate","rhomboid"],
               "widerTip":["tip","obovate"]}

    toSearch = []
    
    for sent in sents:
        for x in vals:
            for syns in valDict[x]:
                if syns in sent:
                    toSearch.append(x)
    
    return toSearch


#Check all petal-adjacent sentences to determine if any length data is available
#Add appropriate ontology queries for the appropriate petal length
def checkPetalLength(sents):
    vals = ["millimeter","inch","centimeter","cm ","mm "]
    global numbers
    toSearch = []
    lastNum = 0
    
    for sent in sents:
        words = sent.split()
        for word in words:

            if (not word.isalpha()) and (not word.isdigit()):
                justDigs = ""
                justLetters = ""
                for x in word:
                    if x.isdigit():
                        justDigs = justDigs + x
                    else:
                        justLetters = justLetters + x
                lastNum = justDigs        
                if justLetters == "centimeters" or justLetters == "cm":
                    lastNum = lastNum*10
                elif justLetters == "inch" or justLetters == "inches":
                    lastNum = lastNum*25.4
                else:
                    lastNum = lastNum

               
                toSearch.append(lastNum)

                return toSearch
                    
            for eachNum in numbers:
                if (eachNum == word) or (word.isdigit()):
                    lastNum = parse_int(word)
                    
                    for x in vals:
                        if x in sent:
                            if x == "centimeters" or x == "cm ":
                                lastNum = lastNum*10
                            elif x == "inch":
                                lastNum = lastNum*2.54
                            else:
                                lastNum = lastNum
                                
                            toSearch.append(lastNum)        

    return toSearch


#Check all petal-adjacent sentences to determine if any of the identified number of petals are present
#Add appropriate ontology queries for each found numbert
def checkPetalNumber(sents):
     
    numbers = ['one',
               'two',
               'three',
               'four',
               'five',
               'six',
               'seven',
               'eight',
               'nine',
               'ten',
               'eleven',
               'twelve',
               'teen',
               'twenty',
               'thirty',
               'forty']   
    
    numPetals = 0
    
    for sent in sents:
        sent = sent.replace('one','1')
        sent = sent.replace('two','2')
        sent = sent.replace('three','3')
        sent = sent.replace('four','4')
        sent = sent.replace('five','5')
        sent = sent.replace('six','6')
        sent = sent.replace('seven','7')
        sent = sent.replace('eight','8')
        sent = sent.replace('nine','9')
        sent = sent.replace('ten','10')
        
        sent = sent.split()
        prevWord = sent[0]
        for word in sent:

            if "petals" in word.lower():
                isNum = False
                if prevWord.isdigit():
                    isNum = True
                if isNum:
                    numPetals = int(prevWord)
            prevWord = word

          
    if numPetals is not 0:
        return numPetals
    else:
        return None


'''
def checkPlantEnvironment(sents):
    
    vals = ["creeping","erect"]
    
    valDict = {"creeping" : ["creeping","vines","groundcover","spreading"],
               "erect" : ["erect","upright","standing"]}
    toSearch = []
    
    for sent in sents:
        for x in vals:
            for syns in valDict[x]:
                if syns in sent:
                    toSearch.append(x)
    
    return toSearch
'''

#Check sentences to determine if any plant size information is found
#Add appropriate ontology queries for the appropriate size
def checkPlantSize(sents):
    vals = ["millimeter","inch","centimeter","cm ","mm "]
    global numbers
    toSearch = []
    lastNum = 0
    
    for sent in sents:
        words = sent.split()
        for word in words:
            
            if (not word.isalpha()) and (not word.isdigit()):
                justDigs = ""
                justLetters = ""
                for x in word:
                    if x.isdigit():
                        justDigs = justDigs + x
                    else:
                        justLetters = justLetters + x
                lastNum = justDigs        
                if justLetters == "millimeter" or justLetters == "mm":
                    lastNum = lastNum/10
                elif justLetters == "inch" or justLetters == "inches":
                    lastNum = lastNum*2.54
                else:
                    lastNum = lastNum
               
                toSearch.append(lastNum)
                return toSearch
                    
            for eachNum in numbers:
                if (eachNum == word) or (word.isdigit()):
                    lastNum = parse_int(word)
                    
                    for x in vals:
                        if x in sent:
                            if x == "millimeter" or x == "mm ":
                                lastNum = lastNum/10
                            elif x == "inch":
                                lastNum = lastNum*2.54
                            else:
                                lastNum = lastNum
                                
                            toSearch.append(lastNum)        

    return toSearch
    

#Main function for the program, launches and runs interface with the user
def interface():
    global currentPossibilities
    global possibilitiesOut
    global possibilitiesIn
    
    global usedColor
    global usedCluster
    global usedPosition
    global usedFlowerShape
    global usedFlowerSymmetry
    global usedLeafArrangement
    global usedLeafDivision
    global usedLeafMargin
    global usedLeafLength
    global usedLeafShape
    global usedPetalLength
    global usedPetalNumber
    global usedPlantEnvironment
    global usedPlantSize
    
    
    resolved = False
    
    print()
    print()
    print()
    print("---")
    print("------")
    print("---------")
    print("---------")
    print("------------------")
    print()
    print("Hello! Welcome to the text-based identification system for Rubiaceae wildflowers in Wisconsin!")
    print()
    print("------------------")
    print("---------")
    print("---------")
    print("------")
    print("---")    
    
    print()
    print()
    print("This system uses your description of a wildflower to identify which Wisconsin-native member of the Rubiaceae family - if any - it is.")
    print("I'll guide you along in your identification and provide suggestions on additional detail you could provide to help identify your wildflower.")
    print()
    print()
    print("Please provide a description of the plant, including details on the appearance and orientation of its leaves and flowers,\n as well as general information on the plant itself:")
    
    while not resolved:
        userText = input("")
        print()
        sentences = sentTokenize(userText)
        strippedSent = []
        for x in sentences:
            x = x.translate(str.maketrans('', '', string.punctuation))
            strippedSent.append(x.lower())
        sentences = strippedSent
        
        
        flowerSents = []
        petalSents = []
        plantSents = []
        leafSents = []
        
        for sent in sentences:
            if "flower" in sent or "flor" in sent:
                flowerSents.append(sent)
            
            elif "leaf" in sent:
                leafSents.append(sent)
                
            elif "leaves" in sent:
                leafSents.append(sent)
                
            elif "petal" in sent:
                petalSents.append(sent)
                
            else:
                plantSents.append(sent)
        
                
        '''
        "blue","green","orange","pink","purple","red","transparent","white","yellow"
        '''
        
        if usedColor is False:
            
            flowerColors = checkFlowerColor(flowerSents)
            petalColors = checkFlowerColor(petalSents)
            flowerColors = flowerColors + petalColors
            
            colorQueryResults = []
            if ("blue") in flowerColors:
                colorQueryResults.append(onto().search(is_a = onto().BlueFlower_Color))
            if ("green") in flowerColors:
                colorQueryResults.append(onto().search(is_a = onto().GreenFlower_Color))    
            if ("orange") in flowerColors:
                colorQueryResults.append(onto().search(is_a = onto().OrangeFlower_Color))
            if ("pink") in flowerColors:
                colorQueryResults.append(onto().search(is_a = onto().PinkFlower_Color))
            if ("purple") in flowerColors:
                colorQueryResults.append(onto().search(is_a = onto().PurpleFlower_Color))
            if ("red") in flowerColors:
                colorQueryResults.append(onto().search(is_a = onto().RedFlower_Color))
            if ("transparent") in flowerColors:
                colorQueryResults.append(onto().search(is_a = onto().TransparentFlower_Color))
            if ("white") in flowerColors:
                colorQueryResults.append(onto().search(is_a = onto().WhiteFlower_Color))
            if ("yellow") in flowerColors:
                colorQueryResults.append(onto().search(is_a = onto().YellowFlower_Color))
            
            if len(colorQueryResults) > 0:
                print("Flower colors:")
                print(flowerColors) 
                print("Flowers retrieved from ontology by color:")
                printFlowerList(colorQueryResults)
                print()
        
        if usedCluster is False:
            
            flowerClusters = checkFlowerCluster(flowerSents)
            
            clusterQueryResults = []
            if ("ball") in flowerClusters:
                clusterQueryResults.append(onto().search(is_a = onto().BallFlower_Cluster))
            if ("few") in flowerClusters:
                clusterQueryResults.append(onto().search(is_a = onto().FewFlower_Cluster))    
            if ("loose") in flowerClusters:
                clusterQueryResults.append(onto().search(is_a = onto().LooseFlower_Cluster))
            if ("spike") in flowerClusters:
                clusterQueryResults.append(onto().search(is_a = onto().SpikeFlower_Cluster))
            
            if len(clusterQueryResults) > 0:
                print("Flower clusters:")
                print(flowerClusters)
                print("Flowers retrieved from ontology by cluster type:")
                printFlowerList(clusterQueryResults)
                print()
        
        if usedPosition is False:
            
            flowerPosition = checkFlowerPosition(flowerSents)
            
            positionQueryResults = []
            if ("apical") in flowerPosition:
                positionQueryResults.append(onto().search(is_a = onto().Apical_at_TipFlower_Position))
            if ("axillary") in flowerPosition:
                positionQueryResults.append(onto().search(is_a = onto().Axillary_at_BaseFlower_Position))
                
            if len(positionQueryResults) > 0:
                print("Flower position:")
                print(flowerPosition)
                print("Flowers retrieved from ontology by flower position:")
                printFlowerList(positionQueryResults)
                print()
        
        if usedFlowerShape is False:
            
            flowerShape = checkFlowerShape(flowerSents)
            
            shapeQueryResults = []
            if ("bell") in flowerShape:
                shapeQueryResults.append(onto().search(is_a = onto().BellFlower_Shape))
            if ("rayed") in flowerShape:
                shapeQueryResults.append(onto().search(is_a = onto().RayedFlower_Shape))
            
            if len(shapeQueryResults) > 0:
                print("Flower shape:")
                print(flowerShape)
                print("Flowers retrieved from ontology by flower shape:")
                printFlowerList(shapeQueryResults)
                print()
        
        if usedFlowerSymmetry is False:
            
            flowerSymmetry = checkFlowerSymmetry(flowerSents)
            
            symmetryQueryResults = []
            if ("radial") in flowerSymmetry:
                symmetryQueryResults.append(onto().search(is_a = onto().RadialFlower_Symmetry))
                
            if len(symmetryQueryResults) > 0:
                print("Flower symmetry:")
                print(flowerSymmetry)
                print("Flowers retrieved from ontology by flower symmetry:")
                printFlowerList(symmetryQueryResults)
                print()
        
        if usedLeafArrangement is False:
            
            leafArrangement = checkLeafArrangement(leafSents)
            
            leafArrangementQueryResults = []
            if ("basal") in leafArrangement:
                leafArrangementQueryResults.append(onto().search(is_a = onto().BasalLeaf_Arrangement))
            if ("opposite") in leafArrangement:
                leafArrangementQueryResults.append(onto().search(is_a = onto().OppositeLeaf_Arrangement))
            if ("whorled") in leafArrangement:
                leafArrangementQueryResults.append(onto().search(is_a = onto().WhorledLeaf_Arrangement))
            
            if len(leafArrangementQueryResults) > 0:
                print("Leaf arrangement:")
                print(leafArrangement)
                print("Flowers retrieved from ontology by leaf arrangement:")
                printFlowerList(leafArrangementQueryResults)
                print()
        
        if usedLeafDivision is False:
            
            leafDivision = checkLeafDivision(leafSents)
            
            leafDivisionQueryResults = []
            if ("simple") in leafDivision:
                leafDivisionQueryResults.append(onto().search(is_a = onto().Simple))
            
            if len(leafDivisionQueryResults) > 0:
                print("Leaf division:")
                print(leafDivision)
                print("Flowers retrieved from ontology by leaf division:")
                printFlowerList(leafDivisionQueryResults)
                print()
        
        if usedLeafMargin is False:
            leafMargin = checkLeafMargin(leafSents)
            leafMarginQueryResults = []
            if ("simple") in leafMargin:
                leafDivisionQueryResults.append(onto().search(is_a = onto().Hairy))
            
            if len(leafMarginQueryResults) > 0:
                print("Leaf margin:")
                print(leafMargin)
                print("Flowers retrieved from ontology by leaf margin:")
                printFlowerList(leafMarginQueryResults)
                print()
        
        if usedLeafLength is False:
            leafLength = checkLeafLength(leafSents)
            leafLengthQueryResults = []
            if leafLength:
                leafLength = float(leafLength[0])
                if leafLength <= 10:
                    if leafLength <= 5:
                        if leafLength >= 1:
                            leafLengthQueryResults.append(onto().search(is_a = onto().FiveLeaf_MaxLengthInCM))
                            leafLengthQueryResults.append(onto().search(is_a = onto().OneLeaf_MinLengthInCM))
                        else:
                            leafLengthQueryResults.append(onto().search(is_a = onto().FiveLeaf_MaxLengthInCM))
                            leafLengthQueryResults.append(onto().search(is_a = onto().ZeroLeaf_MinLengthInCM))
                    else:
                        if leafLength >= 1:
                            leafLengthQueryResults.append(onto().search(is_a = onto().TenLeaf_MaxLengthInCM))
                            leafLengthQueryResults.append(onto().search(is_a = onto().OneLeaf_MinLengthInCM))
                        else:
                            leafLengthQueryResults.append(onto().search(is_a = onto().TenLeaf_MaxLengthInCM))
                            leafLengthQueryResults.append(onto().search(is_a = onto().ZeroLeaf_MinLengthInCM))
            
            if len(leafLengthQueryResults) > 0:
                print("Leaf length in cm:")
                print(leafLength)
                print("Flowers retrieved from ontology by leaf length:")
                printFlowerList(leafLengthQueryResults)
                print()
        
        if usedLeafShape is False:
            leafShape = checkLeafShape(leafSents)
            leafShapeQueryResults = []
            if ("heart") in leafShape:
                leafShapeQueryResults.append(onto().search(is_a = onto().Heart_RoundLeaf_Shape))
            if ("linear") in leafShape:
                leafShapeQueryResults.append(onto().search(is_a = onto().LiinearLeaf_Shape))
            if ("widerMiddle") in leafShape:
                leafShapeQueryResults.append(onto().search(is_a = onto().Wider_Near_MiddleLeaf_Shape))
            if ("widerTip") in leafShape:
                leafShapeQueryResults.append(onto().search(is_a = onto().Wider_Near_TipLeaf_Shape))
            
            if len(leafShapeQueryResults) > 0:
                print("Leaf shape:")
                print(leafShape)
                print("Flowers retrieved from ontology by leaf shape:")
                printFlowerList(leafShapeQueryResults)
                print()
        
        if usedPetalLength is False:
            petalLength = checkPetalLength(petalSents)
            petalLengthQueryResults = []
            if petalLength:
                petalLength = float(petalLength[0])
                if petalLength <= 3:
                    petalLengthQueryResults.append(onto().search(is_a = onto().ThreePetal_MaxLengthInMM))
                elif petalLength <= 10:
                    petalLengthQueryResults.append(onto().search(is_a = onto().TenPetal_MaxLengthInMM))
                elif petalLength <= 20:
                    petalLengthQueryResults.append(onto().search(is_a = onto().TwentyPetal_MaxLengthInMM))
                elif petalLength <= 30:
                    petalLengthQueryResults.append(onto().search(is_a = onto().ThirtyPetal_MaxLengthInMM))
            
            if len(petalLengthQueryResults) > 0:
                print("Petal length in mm:")
                print(petalLength)
                print("Flowers retrieved from ontology by petal length:")
                printFlowerList(petalLengthQueryResults)
                print()
        
        if usedPetalNumber is False:
            petalNumber = checkPetalNumber(petalSents)
            petalNumberQueryResults = []
            if(petalNumber):
                petalNumber = int(petalNumber)
                
                if petalNumber == 3:
                    petalNumberQueryResults.append(onto().search(is_a = onto().ThreePetal_Number))
                elif petalNumber == 4:
                    petalNumberQueryResults.append(onto().search(is_a = onto().FourPetal_Number))
                elif petalNumber == 5:
                    petalNumberQueryResults.append(onto().search(is_a = onto().FivePetal_Number))
                    
            if len(petalNumberQueryResults) > 0:
                print("Petal number:")
                print(petalNumber)
                
                print("Flowers retrieved from ontology by petal number:")
                printFlowerList(petalNumberQueryResults)
                print()
        
        '''
        if usedPlantEnvironment is False:
            
            plantEnvironment = checkPlantEnvironment(plantSents)
            plantEnvironmentQueryResults = []
            if ("creeping") in plantEnvironment:
                plantEnvironmentQueryResults.append(onto().search(is_a = onto().Land_Creeping))
            if ("erect") in plantEnvironment:
                plantEnvironmentQueryResults.append(onto().search(is_a = onto().Land_Erect))
            
            if len(plantEnvironmentQueryResults) > 0:
                
                print("Plant environment:")
                print(plantEnvironment)
                
                print("Flowers retrieved from ontology by plant environment:")
                printFlowerList(plantEnvironmentQueryResults)
                print()
        
        '''
        if usedPlantSize is False:
            
            plantSize = checkPlantSize(plantSents)
            
            
            plantSizeQueryResults = []
            if plantSize:
                plantSize = float(plantSize[0])
                if plantSize <= 200:
                    if plantSize <= 10:
                        plantSizeQueryResults.append(onto().search(is_a = onto().TenWildflower_MaxSizeInCM))
                    
                    if plantSize <= 30:
                        plantSizeQueryResults.append(onto().search(is_a = onto().ThirtyWildflower_MaxSizeInCM))
                    
                    if plantSize <= 50:
                        plantSizeQueryResults.append(onto().search(is_a = onto().FiftyWildflower_MaxSizeInCM))
                    
                    
                    if plantSize <= 70:
                        plantSizeQueryResults.append(onto().search(is_a = onto().SeventyWildflower_MaxSizeInCM))
                    
                    
                    if plantSize <= 100:
                        plantSizeQueryResults.append(onto().search(is_a = onto().OneHundredWildflower_MaxSizeInCM))
                    if plantSize <= 200:
                        plantSizeQueryResults.append(onto().search(is_a = onto().TwoHundredWildflower_MaxSizeInCM))
                        
                if plantSize >= 1:
                    if plantSize >= 1:
                        plantSizeQueryResults.append(onto().search(is_a = onto().OneWildflower_MinSizeInCM))
                    
                    if plantSize >= 10:
                        plantSizeQueryResults.append(onto().search(is_a = onto().TenWildflower_MinSizeInCM))
                    
                    if plantSize >= 30:
                        plantSizeQueryResults.append(onto().search(is_a = onto().ThirtyWildflower_MinSizeInCM))
                    
                    if plantSize >= 100:
                        plantSizeQueryResults.append(onto().search(is_a = onto().OneHundredWildflower_MinSizeInCM))
                                   
            if len(plantSizeQueryResults) > 0:
                print("Plant size in cm:")
                print(plantSize)
                
                print("Flowers retrieved from ontology by plant size:")
                printFlowerList(plantSizeQueryResults)
                print()
        
        if len(possibilitiesIn) < 1:
            wildflowers = onto().search(is_a = onto().Wildflower)
            print(wildflowers)
            listOfResults = []
            listOfResults.append(wildflowers)
            outputSet = listOfResults[0]
            possibilitiesIn = outputSet
            possibilitiesOut = []
        
        if colorQueryResults and not usedColor:
            usedColor = True
            tempList = []
            print(tempList)
            if any(isinstance(i, list) for i in colorQueryResults):
                tempList = [item for sublist in colorQueryResults for item in sublist]
            else:
                tempList = colorQueryResults   
            possibilities = possibilitiesIn
            possibilitiesOut = []
            for x in tempList:
                if x in possibilities:
                    possibilitiesOut.append(x)
            print("Current list of possibilities after considering flower color:")
            printFlowerList(possibilitiesOut)
            possibilitiesIn = possibilitiesOut
            print()
                
        if clusterQueryResults and not usedCluster:
            usedCluster = True
            tempList = []
            if any(isinstance(i, list) for i in clusterQueryResults):
                tempList = [item for sublist in clusterQueryResults for item in sublist]
            else:
                tempList = clusterQueryResults
            
            
            print(tempList)    
            possibilities = possibilitiesIn
            possibilitiesOut = []
            for x in tempList:
                if x in possibilities:
                    possibilitiesOut.append(x)
            print("Current list of possibilities after considering cluster type:")
            printFlowerList(possibilitiesOut)
            possibilitiesIn = possibilitiesOut
            print()
            
            
                
        if positionQueryResults and not usedPosition:
            usedPosition = True
            tempList = []
            if any(isinstance(i, list) for i in positionQueryResults):
                tempList = [item for sublist in positionQueryResults for item in sublist]
            else:
                tempList = positionQueryResults
            
            print(tempList)    
            possibilities = possibilitiesIn
            possibilitiesOut = []
            for x in tempList:
                if x in possibilities:
                    possibilitiesOut.append(x)
            print("Current list of possibilities after considering flower position:")
            printFlowerList(possibilitiesOut)
            possibilitiesIn = possibilitiesOut
            print()
            
        
        
        if shapeQueryResults and not usedFlowerShape:
            usedFlowerShape = True
            tempList = []
            if any(isinstance(i, list) for i in shapeQueryResults):
                tempList = [item for sublist in shapeQueryResults for item in sublist]
            else:
                tempList = shapeQueryResults
            
            print(tempList)    
            possibilities = possibilitiesIn
            possibilitiesOut = []
            for x in tempList:
                if x in possibilities:
                    possibilitiesOut.append(x)
            print("Current list of possibilities after considering flower shape:")
            printFlowerList(possibilitiesOut)
            possibilitiesIn = possibilitiesOut
            print()  
        
        
        if symmetryQueryResults and not usedFlowerSymmetry:
            
            usedFlowerSymmetry = True
            tempList = []
            if any(isinstance(i, list) for i in symmetryQueryResults):
                tempList = [item for sublist in symmetryQueryResults for item in sublist]
            else:
                tempList = symmetryQueryResults
            print(tempList)    
            possibilities = possibilitiesIn
            possibilitiesOut = []
            for x in tempList:
                if x in possibilities:
                    possibilitiesOut.append(x)
            print("Current list of possibilities after considering flower symmetry:")
            printFlowerList(possibilitiesOut)
            possibilitiesIn = possibilitiesOut
            print()
        
        
        if leafArrangementQueryResults and not usedLeafArrangement:
            
            usedLeafArrangement = True
            tempList = []
            if any(isinstance(i, list) for i in leafArrangementQueryResults):
                tempList = [item for sublist in leafArrangementQueryResults for item in sublist]
            else:
                tempList = leafArrangementQueryResults
            print(tempList)    
            possibilities = possibilitiesIn
            possibilitiesOut = []
            for x in tempList:
                if x in possibilities:
                    possibilitiesOut.append(x)
            print("Current list of possibilities after considering leaf arrangement:")
            printFlowerList(possibilitiesOut)
            possibilitiesIn = possibilitiesOut
            print()
        
        
        if leafDivisionQueryResults and not usedLeafDivision:
            
            usedLeafDivision = True
            tempList = []
            if any(isinstance(i, list) for i in leafDivisionQueryResults):
                tempList = [item for sublist in leafDivisionQueryResults for item in sublist]
            else:
                tempList = leafDivisionQueryResults
            print(tempList)    
            possibilities = possibilitiesIn
            possibilitiesOut = []
            for x in tempList:
                if x in possibilities:
                    possibilitiesOut.append(x)
            print("Current list of possibilities after considering leaf division:")
            printFlowerList(possibilitiesOut)
            possibilitiesIn = possibilitiesOut
            print()
        
        
        if leafMarginQueryResults and not usedLeafMargin:
            
            usedLeafMargin = True
            tempList = []
            if any(isinstance(i, list) for i in leafMarginQueryResults):
                tempList = [item for sublist in leafMarginQueryResults for item in sublist]
            else:
                tempList = leafMarginQueryResults
            print(tempList)    
            possibilities = possibilitiesIn
            possibilitiesOut = []
            for x in tempList:
                if x in possibilities:
                    possibilitiesOut.append(x)
            print("Current list of possibilities after considering leaf margin:")
            printFlowerList(possibilitiesOut)
            possibilitiesIn = possibilitiesOut
            print()
        
        
        if leafLengthQueryResults and not usedLeafLength:
            
            usedLeafLength = True
            tempList = []
            if any(isinstance(i, list) for i in leafLengthQueryResults):
                tempList = [item for sublist in leafLengthQueryResults for item in sublist]
            else:
                tempList = leafLengthQueryResults
            print(tempList)    
            possibilities = possibilitiesIn
            possibilitiesOut = []
            for x in tempList:
                if x in possibilities:
                    possibilitiesOut.append(x)
            print("Current list of possibilities after considering leaf length:")
            printFlowerList(possibilitiesOut)
            possibilitiesIn = possibilitiesOut
            print()
        
        
        if leafShapeQueryResults and not usedLeafShape:

            usedLeafShape = True
            tempList = []
            if any(isinstance(i, list) for i in leafShapeQueryResults):
                tempList = [item for sublist in leafShapeQueryResults for item in sublist]
            else:
                tempList = leafShapeQueryResults
            print(tempList)   
            possibilities = possibilitiesIn
            possibilitiesOut = []
            for x in tempList:
                if x in possibilities:
                    possibilitiesOut.append(x)
            print("Current list of possibilities after considering leaf shape:")
            printFlowerList(possibilitiesOut)
            possibilitiesIn = possibilitiesOut
            print()
        
        
        if petalLengthQueryResults and not usedPetalLength:

            usedPetalLength = True                
            tempList = []
            if any(isinstance(i, list) for i in petalLengthQueryResults):
                tempList = [item for sublist in petalLengthQueryResults for item in sublist]
            else:
                tempList = petalLengthQueryResults
            print(tempList)    
            possibilities = possibilitiesIn
            possibilitiesOut = []
            for x in tempList:
                if x in possibilities:
                    possibilitiesOut.append(x)
            print("Current list of possibilities after considering petal length:")
            printFlowerList(possibilitiesOut)
            print(possibilitiesOut)
            possibilitiesIn = possibilitiesOut
            print()
        
        
        if petalNumberQueryResults and not usedPetalNumber:
            
            usedPetalNumber = True                
            tempList = []
            if any(isinstance(i, list) for i in petalNumberQueryResults):
                tempList = [item for sublist in petalNumberQueryResults for item in sublist]
            else:
                tempList = petalNumberQueryResults
            print(tempList)    
            possibilities = possibilitiesIn
            possibilitiesOut = []
            for x in tempList:
                if x in possibilities:
                    possibilitiesOut.append(x)
            print("Current list of possibilities after considering petal number:")
            printFlowerList(possibilitiesOut)
            possibilitiesIn = possibilitiesOut
            print()
        
        '''
        if plantEnvironmentQueryResults and not usedPlantEnvironment:
            
            usedPlantEnvironment = True
            tempList = []
            if any(isinstance(i, list) for i in plantEnvironmentQueryResults):
                tempList = [item for sublist in plantEnvironmentQueryResults for item in sublist]
            else:
                tempList = plantEnvironmentQueryResults
            print(tempList)    
            possibilities = possibilitiesIn
            possibilitiesOut = []
            for x in tempList:
                if x in possibilities:
                    possibilitiesOut.append(x)
            print("Current list of possibilities after considering plant environment:")
            printFlowerList(possibilitiesOut)
            possibilitiesIn = possibilitiesOut
            print()
        
        '''
        if plantSizeQueryResults and not usedPlantSize:
            
            usedPlantSize = True    
            tempList = []
            if any(isinstance(i, list) for i in plantSizeQueryResults):
                tempList = [item for sublist in plantSizeQueryResults for item in sublist]
            else:
                tempList = plantSizeQueryResults
            print(tempList)    
            possibilities = possibilitiesIn
            possibilitiesOut = []
            for x in tempList:
                if x in possibilities:
                    possibilitiesOut.append(x)
            print("Current list of possibilities after considering plant size:")
            printFlowerList(possibilitiesOut)
            possibilitiesIn = possibilitiesOut
            print()
        
        '''    
        colorSet = set(colorQueryResults)
        clusterSet = set(clusterQueryResults)
        positionSet = set(positionQueryResults)
        shapeSet = (shapeQueryResults)
        symmetrySet = (symmetryQueryResults)  
        leafArrangementSet = set(leafArrangementQueryResults)
        leafDivisionSet = set(leafDivisionQueryResults)
        leafMarginSet = set(leafMarginQueryResults)
        leafLengthSet = set(leafLengthQueryResults)
        leafShapeSet = set(leafShapeQueryResults)
        petalLengthSet = set(petalLengthQueryResults)
        petalNumberSet = set(petalNumberQueryResults)
        plantEnvironmentSet = set(plantEnvironmentQueryResults)
        plantSizeSet = set(plantSizeQueryResults)
        '''
        guessList = []
        
        for x in possibilitiesOut:
            guessList.append(x)
        
        currentPossibilities = possibilitiesIn
            
        print("------------------------------------------------------------------------------------------")
        print()
        print("Best guess at plant species:")
        printFlowerList(guessList)
        print()
        print("------------------------------------------------------------------------------------------")
        
        if len(currentPossibilities) > 1:
            resolved = False
            print()
            print("It looks like we don't quite have a match just yet.")
            print("Let's take a look at some additional info that will help us zero in on the correct species.")
            
            askQuestions()
            print()
            
        else:
            resolved = True
            
            if len(guessList) > 0:
                print("Looks like we found a matching species! Thank you for using this identification system.")
            else:
                print("There doesn't seem to be a matching species for the combination of characteristics you provided.")
                print("Please try identification again.")
            
interface()

input('Press ENTER to exit')

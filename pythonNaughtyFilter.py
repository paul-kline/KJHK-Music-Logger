import re
import functools
import random
#The lists at the top of this file determine what is filtered!
#There are 4 lists:
#    1. anywherebad
#    2. onlybylonesomebad
#    3. thsesOK
#    4. entireStringOk
#The names were attempted to be appropriate. 'anywherebad' and
# 'onlybylonesomebad' are for listing naughty words to be removed.
# THESE TWO LISTS ARE CASE IN-SENSITIVE.
# So putting "ass" in a list would detect and replace all the following
# occurances:
#   "ass", "ASS", "AsS", etc.
# Perserving the original capitalization where possible.

#If you want a curse word to be edited in a specific way, instead of
#just listing the word, you can make a tuple where the first entry
#is the curse word, and the second is what you want to replace it with.
#i.e. ("asshole","@$$h0l3") for instance. If no tuple is given and you simply
#put "asshole" in the list, the generic replace is used which is "a******"
#(the first letter of the word and the rest starred out).
#To keep things fresh, the second part of the tuple can be a list of possible
# substitutions for a naughty word and one is chosen at random.
#i.e. ("asshole", ["@$$h0l3", "***hole", "@$$hole"]) indicates that "asshole"
#should be replaced with any of the 3 substitutions given in the list.
#Notes about supplying substitution options:
#     1. If you supply a substitution that is NOT the same length as the word
# you are replacing, no capitalization is perserved.
# i.e. the entry ("ass","butt") when applied to the title: "ASS SURFERS"
# will result in the string "butt SURFERS". Whereas if the entry had been
# ("ass", "a$$"), the title would be filtered to "A$$ SURFERS". See the difference?
# Wherever possible, capitalization is perserved, but if substitutions are given,
# capitalization is preservance is only possible if they are the same length!
#          2. Note that if you do provide a substitution for a word (list or not),
# the default first letter followed by all stars is never chosen. If you want this as
# an option still, manually include it in the list. i.e.
#                 ("asshole", ["@$$h0l3", "***hole", "@$$hole", "a******"])
# anywherebad:
# words in this list are filtered out no matter where they appear.
# this is important to distinguish from words that are only bad when
# they occur by themselves ('onlybylonesomebad'). For instance
# "cock" when used by itself it typically bad, but we wouldn't
# want a band called "Cockpit" to show up as "C***pit". But certain
# words are pretty much always bad and never appear as 'innocent'
# subwords. Words like "fuck", "shit", "bastard", etc are pretty much
# always bad.

# http://www.wordfind.com/contains/WORDHERE is a great url for checking if a
# word occurs as part of any others. So if I wanted to see what English words
# have "asshole" in them, go to: http://www.wordfind.com/contains/asshole

# onlybylonesomebad:
# As the name suggests, only when these words appear as a single word
# are they edited out. 

# theseOK:
# These are EXCEPTIONS. Words (or phrases) that, when found, should
# be left alone. For instance the Australian band "Dick Diver",
# taken from a character in the F. Scott Fitzgerald novel Tender Is the Night,
# is just the name dick. There are others ways to be able to still edit songs
# like "dick sucker" and allow "Dick Diver", but having a list of exceptions
# (that is probably frequently added to). Seemed like the most logical choice.
# It is better in my mind to acidentally edit an innocent occurance once or
# twice than to let a bad one slip through.
# Note that 'theseOK' search the subtext for the occurance and allow it through.
# for instance if Dick Diver got together with The Heartbreakers for the title,
# "Dick Diver and the Heartbreakers", the title would pass through the filter
# unchanged.

# entireStringOk:
# However, if "Dick Diver" were put in this list and not the previous (theseOK),
# then the title "Dick Diver and the Heartbreakers" would become something like:
# "D*** Diver and the Heartbreakers" because this list of exceptions only applies
# to the ENTIRE string that is being filtered. So if "Dick Diver" is in this list
# (and NOT theseOK) and we filtering the title "Dick Diver " the result would be
# "D*** Diver " because some dumdum named the band with a tailing space.
# Note that unlike the other 3 lists, this list IS CASE SENSITIVE. So if "Dick Diver"
# is in this list (and NOT theseOK) and we run the title "DICK Diver" through the filter,
# we would get "D*** Diver" because the strings weren't EXACTLY the same. This was a design choice.
# Wouldn't be hard to change, but wanting to specifically match capitalization may be desired.

#these are the words that are bad NO MATTER what!!
#even when they appear as parts of other words.
#i.e. "Shitface" -> "S***face" if "shit" is in this list.
anywherebad = [("asshole", ["***hole", "@$$hole"]),
               "bastard",
               "bitch",
               "boner",
               "clit",
               "cocksucker",
               "cunt",
               "dickhead"
               "fuck",
               "niggar",
               "nigger",
               "pussy",
               "shit"
               ]
#these are the words that are only bad when they appear by themselves
onlybylonesomebad = [("ass", ["@$$", "a--", "a**"]),
                     "cock",
                     ("dick", ["d***"]),
                     "dicks",
                     "prick" ]
#here are the exceptions that are ignored should they show up somewhere
theseOK = [ "Dick Diver",
            "Dick Dale",
            "Dick Cheney",
            "dicker",
            "medick", #it's an herb..
            "Donkey is an ass"

            ]

#Decided capitalization matters when matching the entire string!!~~~~~~~~~~
entireStringOk = ["Dick"]          


 
print("this is the the python naughty filter")
replacement=""

#this is the name method that does all the filters.
#in other words, everything else in this file is used
#to run this one method. 
def filterNaughty(str):
  if str in entireStringOk:
    return str
  
  (str,stack) = removeOkayparts(str)
  for bad in onlybylonesomebad:
    str= filterExact(str,bad) 

  for bad in anywherebad:
    str = filterAnywhere(str,bad)

  #now put back the exceptions:
  for i in range(0,len(stack)):
    (w,place) = stack.pop()
    str = insertStr(str,w,place)
  return (str)

def insertStr(originalStr,insertStr,index):
  return originalStr[:index] + insertStr + originalStr[index:]
  
def filterAnywhere(str,mTuple):
  (word,replacement) = getWordAndReplacement(mTuple)
  matches = re.findall(word,str,re.IGNORECASE)
  for m in matches:
    str = str.replace(m,calcFinalReplacement(m,replacement))
  return str

def filterExact(str,mTuple):
  (word,replacement) = getWordAndReplacement(mTuple)
  #what if it is the word?
  if word.lower() == str.lower():
    return (calcFinalReplacement(str,replacement))
  
  #search for at beginning. note the tacked on space so we
  # aren't looking for word that just starts with it.
  # i.e. 'assassin' is okay. but "Ass kicker" not
  wordbeg = "^"+word + " "
  match1 = re.match(wordbeg,str,re.IGNORECASE)
  if match1:
    #we want to perserve capitalization so get the exact match.
    #and get rid of that space. 
    #plus we need the actual occurance for replace to work!
    naughty = match1.group().strip()
    #must be limited to ONLY replace 1. Otherwise it gets.. excited and does more
    str = str.replace(naughty,calcFinalReplacement(naughty,replacement),1)
    print( "str begining edits:" + str)
  # now check for middle occurances
  wordmid = " " + word 
  match2 = re.finditer(wordmid,str,re.IGNORECASE)
  if match2:
    for m in match2:
      m_ = m.group().strip()
      print(m)
      # this weird stuff is needed because regex only finds
      # "non-overlapping" instances.
      itocheck = m.end()
      if itocheck < len(str):
        l = str[itocheck]
        print("following letter:" + l)
        if l == ' ':
         #before = str[:m.start()]
         print(":m.start() = " + str[:m.start()])
         str =str[:m.start() + 1] + calcFinalReplacement(m.group().strip(),replacement) + str[m.end():] #str.replace(m.group(), " " + (calcFinalReplacement(m_,replacement)))
          
        #else: it's just the beginning of a word like "assassin"
      else: #then this is the last word.
        str =str[:m.start() + 1] + calcFinalReplacement(m.group().strip(),replacement)
  #rationale for the above:
  # Note searching for " word " will only detect one "asshole" in the title
  # "hello, asshole asshole man" because "asshole asshole" share that space between them.
  # regex only fins "non-overlapping" instances. Therefore, we search for " word" and then
  # do the check if the next char is a space.
  # Also,I can't use re.sub because inside the function I can pass re.sub, I don't have the context
  # of the match. Normally, this isn't a problem, but since I can't search for " word " and only " word"
  # I need to know the context of the match to see if the next character is a space or not. Therefore, I
  # am stuck doing the above.
  return str


#this function is mainly necessary for capitalization integrity.
#for example, if a band is named: "ASSHOLE" we would want to edit it
#something like "***HOLE" and not "***hole"
def calcFinalReplacement(badword,initreplacement):
  res = ""
  if len(badword) == len(initreplacement):
    for i,val in enumerate(badword):
      if badword[i].lower() == initreplacement[i].lower():
        res += badword[i]
      else:
        res += initreplacement[i]
  else:
    res = initreplacement
  return res
   
def getWordAndReplacement(mTuple):
  word=""
  replacement=""
  if isinstance(mTuple, tuple):
    word = fst(mTuple)
    mLS = snd(mTuple)
    if isinstance(mLS, list):
      # choose one randomly
      replacement = random.choice(mLS)
    else:
      replacement = mLS
  else:
    word = mTuple
    replacement = defaultStars(word)
  return (word,replacement)  
def removeOkayparts(str):
  #remove the parts that we know are okay, but remember where we got them from.
  okayparts = map(lambda x: re.findall(x, str,re.IGNORECASE),theseOK)
  #print(list(okayparts))
  #remove no matches.
  listofokayparts=filter(lambda x: x!=[],okayparts)
  #print(list(listofokayparts))
  stack = []
  str2=str
  for ls in listofokayparts:
    for w in ls:
      i= str2.index(w)
      pair =(w,i)
      #print("here in the pair!!!: " + pair)
      stack.append(pair)
      str2=str2.replace(w,"")
  return (str2, stack)


def defaultStars(str):  
   return str[0] + ('*' * (len(str) -1))

def fst(pair):
   (x,_) = pair
   return x 

def snd(pair):
   (_,x) = pair
   return x  

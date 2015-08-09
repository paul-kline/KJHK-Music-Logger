import xml.etree.ElementTree as ET
import re
#tree = ET.fromstring(data)

print("NowPlayingXMLParser")
test1="<nowplaying><sched_time>79720400</sched_time><air_time>70006000</air_time><stack_pos></stack_pos><title>7/4 (Shoreline)</title><artist>Broken Social Scene</artist><trivia>Broken Social Scene</trivia><category>RCK</category><cart>0G43</cart><intro>0</intro><end></end><station>KJHK</station><duration>293900</duration><media_type>SONG</media_type><milliseconds_left></milliseconds_left><DNP></DNP><RIYL></RIYL><Recommended Tracks></Recommended Tracks><Review></Review><Sub-Genre(s)></Sub-Genre(s)><Track Number></Track Number></nowplaying>"
def mainParse(str):
    maybetree = tryParseXML(preparse(str))
    if maybetree == -1:
        return -1
    else:
      artist
def myparse(str):
  str = preparse(str)
  str = tryParseXML(str)
  return str
#remove the xml fields that break stuff. there must be a better way to do this.
def preparse(str):
    str = re.sub("<Sub-Genre\(s\)>(.*?)</Sub-Genre\(s\)>","",str)
    str = re.sub("<Recommended Tracks>(.*?)</Recommended Tracks>","",str)
    str = re.sub("<Track Number>(.*?)</Track Number>","",str)
    return str
def tryParseXML(str):
  try:
    tree = ET.fromstring(str)
    return tree
  except:
     print("nooooooo parse failure")
     return -1

nonsongCategories = ["DON", "RTR", "EVR", "PRO", "PSA", "IDS"]
def isSong(tree):
    #assumed successful tree parse.
    category = getCategory(tree)
    return not (category in nonsongCategories)
def getCategory(tree):
    return tree.find("category").text
def didAir(tree):
    return tree.find("air_time").text != None
    
#TODO make this smarter. i.e. check the central server to see
# if this song is actually currently in rotation since we keep
# a copy of the song in non-rot category as well.
# In other words, see if the DJ played a rotation song not from
# the rotation category. Stupid DJs...
def isRot(tree):
    return getCategory(tree) == "ROT"
def getSongData(tree):
    song  = tree.find("title").text
    album = tree.find("trivia").text
    band  = tree.find("artist").text
    airtime = int(tree.find("air_time").text)
    duration = int(tree.find("duration").text)
    isrot = isRot(tree)
    return (band,album,song,airtime,duration,isrot)
def toSeconds(mill):
    return mill / 1000
def toMinutes(mill):
    return (toSeconds(mill)/60)
def toHours(mill):
    return (toMinutes(mill)/60)

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
    str = re.sub("&", "&amp;",str)
    #specifically replace instances of '<' and '>' that show up in titles.
    #without doing this parsing the xml will fail if those chars are there.
    str = re.sub("<artist>(.*?)>(.*?)</artist>","<artist>\\1&gt;\\2</artist>",str)
    str = re.sub("<artist>(.*?)<(.*?)</artist>","<artist>\\1&lt;\\2</artist>",str)
    str = re.sub("<trivia>(.*?)>(.*?)</trivia>","<trivia>\\1&gt;\\2</trivia>",str)
    str = re.sub("<trivia>(.*?)<(.*?)</trivia>","<trivia>\\1&lt;\\2</trivia>",str)
    str = re.sub("<title>(.*?)>(.*?)</title>","<title>\\1&gt;\\2</title>",str)
    str = re.sub("<title>(.*?)<(.*?)</title>","<title>\\1&lt;\\2</title>",str)
    
    return str
def tryParseXML(str):
  try:
    tree = ET.fromstring(str)
    return tree
  except:
     print("nooooooo parse failure")
     return -1

nonsongCategories = ["DON", "RTR", "EVR", "PRO", "PSA", "IDS", "VTK", "DIS", "EVT", "LIN"]
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
    song  = handleNone(tree.find("title").text)
    album = handleNone(tree.find("trivia").text)
    band  = handleNone(tree.find("artist").text)
    airtime = int(tree.find("air_time").text)
    duration = int(tree.find("duration").text)
    isrot = isRot(tree) 
    r = (band,album,song,airtime,duration,isrot)
    n = handleNone(None)
    if (song == n or album == n or band == n):
        handleMissingData(r)
    return r
def handleNone(x):
    if x == None:
        return "[NA]"
    else:
        return x
def handleMissingData(x):
    (band,album,song,airtime,duration,isrot) = x
    sub = "Automated msg: Missing Song Data"
    bod = "The following song information appears to have missing data in WideOrbit:\n"
    bod += "Song:\t" + song + "\n"
    bod += "Album:\t" + album + "\n"
    bod += "Artist:\t" + band + "\n"
    bod += "\n\nThis message was send automatically by the KJHK music logger. "
    bod += "Please contact Paul Kline (pauliankline@gmail.com) or Erick Oduniyi "
    bod += "(it@kjhk.org) to edit whom receives this email or to report 'false alarms'."
    recips=["pauliankline@gmail.com", "music@kjhk.org", "musicassistant@kjhk.org"]        
    try:
        sendEmail(recips,sub,bod)
        print("successfully reported missing song data.")
    except:
        print("error sending email!!!")
        
        
    print("HANDLING MISSING DATA") 
def toSeconds(mill):
    return mill / 1000
def toMinutes(mill):
    return (toSeconds(mill)/60)
def toHours(mill):
    return (toMinutes(mill)/60)

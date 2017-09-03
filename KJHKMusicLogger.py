
import sys
sys.path += "./"
import NowPlayingXMLParser as xmlp
import pythonNaughtyFilter as nf
import hmac as h1
import hashlib as h2
import base64 as b64
import urllib.parse
import urllib.request
import calendar
import time
import acorns as s
#KJHK music auto-logger

announcementBreakHandled = False
def handleDataBurst(str):
    maybetree = xmlp.myparse(str)
    if maybetree == -1:
        print("error parsing the xml")
        return -1
    tree = maybetree
    global announcementBreakHandled
    if xmlp.didAir(tree):

      #maybe keep track of air gaps.
      #
      if xmlp.isSong(tree):
        announcementBreakHandled = False
        (artist,album,song,airtime,duration,isrot) = xmlp.getSongData(tree)
        artist = nf.filterNaughty(artist)
        album = nf.filterNaughty(album)
        song = nf.filterNaughty(song)
        handleLogSong(artist,album,song,isrot)
      else:
        if not announcementBreakHandled:
          announcementBreakHandled = True
          urltoLog = "http://air.radiotime.com/Playing.ashx?partnerId=" + s.secrets['partnerID']
          urltoLog += "&partnerKey=" + s.secrets['partnerKey']
          urltoLog += "&id=" + s.secrets['id']
          urltoLog += "&commercial=true"
          tuneinresponse = urllib.request.urlopen(urltoLog).read()
          print(tuneinresponse)
def testGET():
    base_url = "http://kjhk.org/web/gravityformsapi/" 
    api_key = s.secrets['api']
    private_key = s.secrets['priv']
    method = 'GET'
    route = 'forms/10/entries'
    expires =  str(calendar.timegm(time.gmtime()) + 60*60)
    string_to_sign = api_key + ":" +  method + ":" + route + ":" + expires
    sig = sign(string_to_sign, private_key )

    url = base_url + route + '?api_key=' + api_key + '&signature=' + sig + '&expires=' + expires
    print(url + "\n")
    responseData = urllib.request.urlopen(url).read()
    print(responseData)

def handleLogSong(artist,album,song,isrot):
    try:
        print("handleLogSong stub method.")
        print("Song: " + song )
        print("Album: " + album)
        print("Artist: " + artist)
        print("Is Rotation: " + str(isrot))
    except:
        print("\n\nFAILED TO PRINT SONG INFO IN HANDLELOGSONG\n\n")
    base_url = "http://kjhk.org/web/gravityformsapi/"

    api_key = s.secrets['api']
    private_key = s.secrets['priv']

    method = 'POST'
    route = 'entries'
    expires =  str(calendar.timegm(time.gmtime()) + 60*60)
    string_to_sign = api_key + ":" +  method + ":" + route + ":" + expires
    sig = sign(string_to_sign, private_key )

    url = base_url + route + '?api_key=' + api_key + '&signature=' + sig + '&expires=' + expires
    rotName = '"6"'
    rotVal = '"Everything Other Than Rotation"'
    if isrot:
        rotVal = '"Rotation"'

    artistName = '"2"'
    albumName = '"3"'
    trackName = '"4"'
    jstring = '[{"form_id":"10",' + rotName + ':' + rotVal + ',' + artistName + ':"' + artist + '",' + albumName+ ':"' + album + '",' + trackName + ':"' + song + '"' + '}]'
    print("connecting to: ")
    print(url)
    responseData = urllib.request.urlopen(url,bytes(jstring,'utf-8')).read()
    print(responseData)
    return jstring

def rawurlencode(str):
    return urllib.parse.quote(str)
apik = 'apik'
def sign(obj,k):
    return rawurlencode(b64.b64encode(h1.new(bytes(k,'UTF-8'),bytes(obj,'utf-8'), h2.sha1).digest()))

if __name__ == "__main__":
#    import sys
    handleDataBurst(sys.argv[0])

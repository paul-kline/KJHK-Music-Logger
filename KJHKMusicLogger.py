
import sys
sys.path += "./"
import NowPlayingXMLParser as xmlp
import pythonNaughtyFilter as nf
#KJHK music auto-logger


def handleDataBurst(str):
    maybetree = xmlp.myparse(str)
    if maybetree == -1:
        print("error parsing the xml")
        return -1
    tree = maybetree
    if xmlp.didAir(tree):
      (artist,album,song,airtime,duration,isrot) = xmlp.getSongData(tree)
      #maybe keep track of air gaps.
      #  
      if xmlp.isSong(tree):
        artist = nf.filterNaughty(artist)
        album = nf.filterNaughty(album)
        song = nf.filterNaughty(song)
        handleLogSong(artist,album,song,isrot)
        
def handleLogSong(artist,album,song,isrot):
    print("handleLogSong stub method.")
    print("Song: " + song )
    print("Album: " + album)
    print("Artist: " + artist)
    print("Is Rotation: " + str(isrot))
    
    
if __name__ == "__main__":
#    import sys
    handleDataBurst(sys.argv[0])

import urllib.request
from bs4 import BeautifulSoup
from os import system
import sys
import subprocess


def titleCase(s):
    words = s.split()
    title = words[0].capitalize()
    for word in words[1:]:
        if word.lower() in ['in', 'the', 'for', 'of', 'a', 'at', 'an', 'is', 'and']:
            title += ' ' + word.lower()
        else:
            title += ' ' + word.capitalize()
    return title

pathToSave = "~/Music/"

def getVidID(song, URL):
    search = song + ' lyrics'
    searchQuery = '+'.join(search.split())
    searchURL = URL + searchQuery

    response = urllib.request.urlopen(searchURL)
    soup = BeautifulSoup(response.read(), "lxml")

    # More modern selector to find video links
    link_tag = soup.find("a", href=True)
    while link_tag and not link_tag["href"].startswith("/watch?v="):
        link_tag = link_tag.find_next("a", href=True)

    if not link_tag:
        raise Exception("No video found!")

    return link_tag["href"]

def doStuff(song):
    print("Downloading " + titleCase(song))

    # Let yt-dlp search for the song itself
    query = f"ytsearch1:{song} lyrics"
    output_template = f"{pathToSave}{titleCase(song)}.%(ext)s"

    subprocess.run([
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "-q",
        "-o", output_template,
        query
    ])

    print("Downloaded " + titleCase(song) + "\n")

def main():
    print('-------------------------------------------------------------')
    if len(sys.argv) == 3 and sys.argv[1].lower() == '-i':
        for song in open(sys.argv[2]).readlines():
            doStuff(song.strip())
    else:
        for song in sys.argv[1:]:
            doStuff(song)

if __name__ == '__main__':
    main()

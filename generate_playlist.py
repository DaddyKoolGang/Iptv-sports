import requests
import re

# ========================
# CONFIGURATION
# ========================

SERVER = "http://TONSERVEUR:8080"
USERNAME = "TONUSER"
PASSWORD = "TONPASS"

OUTPUT = "sports_today_ultra.m3u"

QUALITY_ORDER = ["4K","UHD","FHD","1080","HD","720"]

NBA_KEYWORDS = ["NBA","LEAGUE PASS","NBA TV","TNT","ESPN","ABC"]
BASKET_EUROPE = ["EUROLEAGUE","EUROCUP","ACB","LNB","BBL"]
FOOTBALL = ["CANAL","DAZN","SKY","BEIN","SPORTKLUB","ARENA","SUPERSPORT"]

# ========================
# TELECHARGER PLAYLIST
# ========================

url = f"{SERVER}/get.php?username={USERNAME}&password={PASSWORD}&type=m3u_plus&output=ts"

print("Téléchargement IPTV...")

r = requests.get(url)

with open("playlist.m3u","wb") as f:
    f.write(r.content)

print("Playlist téléchargée")

# ========================
# PARSER CHAÎNES
# ========================

channels = []

with open("playlist.m3u","r",encoding="utf8",errors="ignore") as f:
    lines = f.readlines()

for i in range(len(lines)):

    if "#EXTINF" in lines[i]:

        info = lines[i]
        stream = lines[i+1]

        text = info.upper()

        channels.append({
            "info": info,
            "url": stream,
            "text": text
        })

# ========================
# FILTRER SPORTS
# ========================

def filter_channels(keywords):

    result = []

    for c in channels:

        if any(k in c["text"] for k in keywords):

            result.append(c)

    return result

nba_channels = filter_channels(NBA_KEYWORDS)
basket_channels = filter_channels(BASKET_EUROPE)
football_channels = filter_channels(FOOTBALL)

# ========================
# TRI QUALITE
# ========================

def sort_quality(list_channels):

    ordered = []

    for q in QUALITY_ORDER:

        for c in list_channels:

            if q in c["text"]:

                ordered.append(c)

    for c in list_channels:

        if c not in ordered:

            ordered.append(c)

    return ordered

nba_channels = sort_quality(nba_channels)
basket_channels = sort_quality(basket_channels)
football_channels = sort_quality(football_channels)

# ========================
# GENERER PLAYLIST
# ========================

with open(OUTPUT,"w",encoding="utf8") as f:

    f.write("#EXTM3U\n")

    f.write("\n######## NBA ########\n")

    for c in nba_channels:

        f.write(c["info"])
        f.write(c["url"])

    f.write("\n######## BASKET EUROPE ########\n")

    for c in basket_channels:

        f.write(c["info"])
        f.write(c["url"])

    f.write("\n######## FOOTBALL ########\n")

    for c in football_channels:

        f.write(c["info"])
        f.write(c["url"])

print("Playlist générée :", OUTPUT)

import requests

channel = "backgroundguy02"
twitchapiclientid = ""
searchterm = ""

# Don't edit below this line #

kraken_url = "https://api.twitch.tv/kraken/channels/" + channel + "/videos?broadcasts=true&limit=100&client_id=" \
                   + twitchapiclientid
while(True):
    try:
        req = requests.get(kraken_url)
        reqjson = req.json()
        for x in reqjson['videos']:
            vid_id = str(x['_id']).translate(None, 'v')
            url = "https://api.twitch.tv/v5/videos/" +  vid_id + "/comments?content_offset_seconds=0" \
                  + "&client_id=" + twitchapiclientid
            while(True):
                try:
                    req = requests.get(url)
                    resp = req.json()
                    #print url, resp
                    for v in resp['comments']:
                        try:
                            if (searchterm.lower() in v['message']['body'].lower()) or (searchterm.lower() in \
                                    v['commenter']['name'].lower()):
                                print "URL: {:42}  User: {:32}  Seconds In: {:16}  Said: {:120}".format( \
                                    x['url'],v['commenter']['name'], v['content_offset_seconds'], v['message']['body'])
                        except:
                            pass
                    url = "https://api.twitch.tv/v5/videos/" + vid_id + "/comments?cursor=" + resp['_next'] \
                          + "&client_id=" + twitchapiclientid
                except:
                    break
        if reqjson['_total'] is 100:
            kraken_url = reqjson['_links']['next'] + "&client_id=" + twitchapiclientid
        else:
            quit()
    except:
        break

import json, cfscrape, time, pyglet

scraper = cfscrape.create_scraper()
previous_status = "bad"
notification = pyglet.media.load('./res/notification.wav', streaming=False)
returned = pyglet.media.load('./res/returned.wav', streaming=False)
offline = pyglet.media.load('./res/gone_offline.wav', streaming=False)
minor = pyglet.media.load('./res/minor_issues.wav', streaming=False)
while(True):
    time.sleep(60)
    try:
        status_json = scraper.get("https://crowbar.steamdb.info/Barney")
        status_json = json.loads(str(status_json.text))
        steam_status = status_json["services"]["dota2"]["status"]
        print(previous_status + "->" + steam_status)
        # IF THINGS ARE OKAY
        if steam_status == "good":
            if previous_status == "good":
                continue
            else:
                notification.play()
                time.sleep(1)
                returned.play()
                time.sleep(3)
                
        # IF THERE ARE SLIGHT PROBLEMS
        elif  steam_status == "minor":
            if previous_status == "minor":
                continue
            else:
                notification.play()
                time.sleep(1)
                minor.play()
                time.sleep(3)
                
        # IF THERE ARE MAJOR ISSUES
        else:
            if previous_status == "major":
                continue
            else:
                notification.play()
                time.sleep(1)
                offline.play()
                time.sleep(3)


        previous_status = steam_status
    except Exception as e:
        print("There was an issue checking the status: " + str(e))
        print("The following is the website:")
        print(status_json)
        pass

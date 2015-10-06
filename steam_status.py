import json, cfscrape, time, pyglet

scraper = cfscrape.create_scraper()
previous_status = "bad"
notification = pyglet.media.load('./res/notification.wav', streaming=False)
returned = pyglet.media.load('./res/returned.wav', streaming=False)
major = pyglet.media.load('./res/major_issues.wav', streaming=False)
minor = pyglet.media.load('./res/minor_issues.wav', streaming=False)
still_major = pyglet.media.load('./res/major_issues.wav', streaming=False)
still_minor = pyglet.media.load('./res/minor_issues.wav', streaming=False)
error_count = 0
while(True):
    time.sleep(60)
    try:
        status_json = scraper.get("https://crowbar.steamdb.info/Barney")
        status_json = json.loads(str(status_json.text))
        steam_status = status_json["services"]["dota2"]["status"]
        print(previous_status + "->" + steam_status)
        
        
        # IF THINGS ARE OKAY
        if steam_status == "good":
            error_count = 0
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
                error_count =+ 1
                if error_count >= 10:
                    notification.play()
                    time.sleep(1)
                    still_minor.play()
                    time.sleep(3)
                    error_count = 0
            else:
                notification.play()
                time.sleep(1)
                minor.play()
                time.sleep(3)
                
        # IF THERE ARE MAJOR ISSUES
        else:
            if previous_status == "major":
                error_count =+ 1
                if error_count >= 10:
                    notification.play()
                    time.sleep(1)
                    still_major.play()
                    time.sleep(3)
                    error_count = 0
            else:
                notification.play()
                time.sleep(1)
                major.play()
                time.sleep(3)


        previous_status = steam_status
    except Exception as e:
        print("There was an issue checking the status: " + str(e))
        print("The following is the website:")
        print(status_json)
        pass

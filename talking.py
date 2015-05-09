import random

class Talking:
    @staticmethod
    def getWrongTitle():
        strings = ["It looks like you got your request title wrong. Read the [url=\"https://ipwnage.com/s/2pJK8\"]sticky[/url] and try again.",
                "Bzzt. You didn't follow naming conventions for your title. Read the [url=\"https://ipwnage.com/s/2pJK8\"]sticky[/url] and try again.",
                "Congrats, you didn't follow directions. Read the [url=\"https://ipwnage.com/s/2pJK8\"]sticky[/url] again, you didn't name your request properly",
                "Sorry, but you didn't format your promotion properly. Please read the [url=\"https://ipwnage.com/s/2pJK8\"]sticky[/url] an try again.",
                "Uh-oh. Looks like you didn't follow instructions on proper request format. Please read the [url=\"https://ipwnage.com/s/2pJK8\"]sticky[/url] and try again.",
                ]
        return random.choice(strings)
        
    @staticmethod
    def getDenied():
        strings = ["Sorry! Your promotion request was denied. Try again some other time.",
                "Your promotion has been denied. At least you tried.",
                "Welp, this sucks. Your promotion has been denied. You can try again some other time.",
                ":(",
                "Dont worry, you can always try again later.",
                "Look on the brightside, ... yeah I got nothing. Sorry, A for effort though?",
                ]
        return random.choice(strings)
    
    @staticmethod
    def getApproval():
        strings = ["Congrats, your promotion has been approved. Your rank has been updated accordingly.",
                "Sweet, you've been promoted. Your rank change is in immediate effect.",
                "Rank get! You've been promoted!",
                "Rank up! You're one step closer to being a total shut-in with no life!",
                "Woop woop! Your promotion was accepted, congrats!",
                "Looks like today is your day, your promotion has been approved!",
                "Looks like you're a rank higher now. Congrats!",
                "Sick one, you got promoted! Congrats!",
                "*le ironic shitposting* *le approved* :^)",
                "Congrats! Your promotion was approved!",
                "Congrats, your promotion request was accepted!",
                "One rank higher, one social rank lower. Sick one.",
                ":D",
                ]
        return random.choice(strings)
         
    @staticmethod    
    def getIntro():
        hello = ["Hiya, %s! My name is Spark, and I'm an assistant AI on iPwnAge to aid users.",
                "Howdy there, %s! I'm Spark, an artificial intelligence dedicated to aiding iPwnAge users.",
                "Heyo, %s. My name is Spark, a kind of artificial intelligence to automate this server.",
                "Hey there, %s! I'm an artificial intelligence named Spark, and I'm here to help you and other players.",
                ]
        info = ["""Some information to assist users reading your promotion request:
                [code]%s[/code]""",
                """Here's some information to help the players reading your promotion request:
                [code]%s[/code]""",
                """Here's a bit of info to help users reading your promotion request:
                [code]%s[/code]""",
                ]
                
        closing = ["Now that your request has passed initial checking, you'll have to wait for others to give their opinions of your request. \
         Afterwards, a staff member or I will either approve or deny your request based on feedback.",
         "While you've passed basic checking (you can follow instructions!), you'll still have to wait for other players to give their opinions of your request. \
         Afterwards, either myself or a staff member will approve or deny your request based on feedback.",
                    ]
                
        sentence = "%s\r\n\r\n%s\r\n\r\n\r\n%s" % (random.choice(hello), random.choice(info), random.choice(closing))
        return sentence
                
                

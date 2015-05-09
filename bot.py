import re, os, mechanize, time, random
from bs4 import BeautifulSoup
from talking import Talking
from utils.config import Config
from utils.console import Console
class Spark:
    def __init__(self):
        self.page = mechanize.Browser()
        self.page.open("https://ipwnage.com/index.php?app=core&module=global&section=login")
        assert self.page.viewing_html()
        print self.page.title()
        self.page.form = list(self.page.forms())[1]
        self.page["ips_username"] = Config.FORUM_USER
        self.page["ips_password"] = Config.FORUM_PASSWORD
        self.page.submit()
        name_regex = "(?s)(?<=[\{\[]Promo[\}\]].{1}).+?(?=[ -]{1,3})"
        self.nameregex = re.compile(name_regex, re.IGNORECASE)
        title_regex = "[\{\[]Promo[\}\]].{1}([a-z0-9_])+[ -]{1,3}((Commoner)|(Trusted)|(Veteran)|(Senior)|(Elder))"
        self.titleregex = re.compile(title_regex, re.IGNORECASE)
        approved = "approved"
        denied = "denied"
        self.approved_regex = re.compile(approved, re.IGNORECASE)
        self.denied_regex = re.compile(denied, re.IGNORECASE)
        rank = "((Commoner)|(Trusted)|(Veteran)|(Senior)|(Elder))"
        self.rank_regex = re.compile(rank, re.IGNORECASE)
    
    
    def processNewPromotions(self):
        storage = open(Config.SEEN_PROMOS_LOCATION, "a+")
        currentlyopen = open(Config.OPEN_PROMOS_LOCATION, "a+")
        openpromos = currentlyopen.readlines()
        names = storage.readlines()
        print self.page.title()
        html = self.page.open("https://ipwnage.com/forum/16-promotions-requests/")
        soup = BeautifulSoup(html)
        title = soup.find_all('a', {'class':'topic_title'})
        for promo in title:
            name = promo.text.rstrip("\n")
            name = name.lstrip("\n")
            if promo['href'] + "\n" not in names:
                if not self.titleregex.search(name):
                    print "Not right!"
                    self.page.open(promo['href'])
                    self.denyPromotion(Config.DENY_WRONG_TITLE)
                if self.titleregex.search(name):
                    print "Correct."
                    username = self.nameregex.search(name).group(0)
                    Console.executeCommand("whois -o " + username)
                    time.sleep(0.3)
                    Console.grabPane()
                    file = open(Config.TMUX_BUFFER_LOCATION, 'r')
                    lines = file.readlines()
                    findtime = re.compile("Name: " + username + " - Page", re.IGNORECASE)
                    findrighttime = re.compile("First joined", re.IGNORECASE)
                    for i, line in enumerate(lines):
                        if findtime.search(line):
                            if findrighttime.search(lines[i+1]):
                                timeon = lines[i+1][17:]
                            else: 
                                timeon = lines[i+2][17:]
                            break
                    timeon = timeon.replace("; ", "\n")
                    self.page.open(promo['href'])
                    currentlyopen.write(promo['href'])
                    currentlyopen.write("\n")
                    self.page.form = list(self.page.forms())[2]
                    postgen = Talking.getIntro() % (username, timeon)
                    self.page["Post"] = postgen
                    self.page.submit()
                storage.write(promo['href'])
                storage.write("\n")
                print "added " + name
        
            else:
                print "already seen " + name
        storage.close()
        currentlyopen.close()
        
        
    def processOpenPromotions(self):
        currentlyopen = open(Config.OPEN_PROMOS_LOCATION, "a+")
        openpromos = currentlyopen.readlines()
        currentlyopen.truncate(0)
        username_regex = "(?s)(?<=<span class=\"hide\" itemprop=\"name\">).+?(?=</span>)"
        postname = re.compile(username_regex)
        digits = "\d+"
        digits_regex = re.compile(digits)
        for promo in openpromos:
            html =  self.page.open(promo)
            soup = BeautifulSoup(html)
            postcount = soup.find('span', {'class': 'ipsType_small'})
            count = int(digits_regex.search(postcount.text).group(0))
            pages = (count / 20) + 1
            completed = False
            for pagenum in range(1, pages+1):
                html = self.page.open(promo.rstrip("\n") + "/page-" + str(pagenum))
                soup = BeautifulSoup(html)
                post = soup.find_all('div', {'class':'post_block'})
                for comment in post:
                    name = postname.search(str(comment)).group(0)
                    if name == "Chozo_GST" or name == "ArcNologia" or name == "Flareon":
                        text = BeautifulSoup(str(comment))
                        innerpost = text.find('div', {'itemprop': 'commentText'})
                        if self.approved_regex.search(innerpost.text):
                            self.approvePromotion()
                            completed = True
                        if self.denied_regex.search(innerpost.text):
                            self.denyPromotion(Config.DENY_OTHER_REASON)
                            completed = True
            if completed is False:
                currentlyopen.write(promo)
                
                            
                        
                        
    def approvePromotion(self):
        self.page.form = list(self.page.forms())[2]
        self.page["Post"] = Talking.getApproval()
        self.page.submit()
        html = self.page.response()
        soup = BeautifulSoup(html)
        title = soup.find('h1', {'class': 'ipsType_pagetitle'})
        rank = self.rank_regex.search(title.text).group(0).lower()
        username = self.nameregex.search(title.text).group(0)
        Console.executeCommand("pex user " + username)
        time.sleep(0.3)
        Console.grabPane()
        file = open(Config.TMUX_BUFFER_LOCATION, 'r')
        lines = file.readlines()
        findpex = re.compile(username + "\' is a member of:", re.IGNORECASE)
        for i, line in enumerate(lines):
            if findpex.search(line):
                    timeon = lines[i+1][20:]
        if timeon[0] == 'd':
            rank = 'd' + rank
        Console.executeCommand("pex user " + username + " group set " + rank)
        menu = soup.find('ul', {'id': 'topic_mod_options_menucontent'})
        move = list(menu.find_all('li'))[3].a.get('href')
        self.page.open(move)
        self.page.form = list(self.page.forms())[2]
        self.page["move_id"] = ['8']
        self.page.submit()
        
    def denyPromotion(self, reason):
        self.page.form = list(self.page.forms())[2]
        if reason == Config.DENY_WRONG_TITLE:
            self.page["Post"] = Talking.getWrongTitle()
        if reason == Config.DENY_OTHER_REASON:
            self.page["Post"] = Talking.getDenied()
        self.page.submit()
        html = self.page.response()
        soup = BeautifulSoup(html)
        menu = soup.find('ul', {'id': 'topic_mod_options_menucontent'})
        move = list(menu.find_all('li'))[3].a.get('href')
        self.page.open(move)
        self.page.form = list(self.page.forms())[2]
        self.page["move_id"] = ['7']
        self.page.submit()
    
    
if __name__ == "__main__":
    Spark = Spark()
    Spark.processNewPromotions()
    Spark.processOpenPromotions()

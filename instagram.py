from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
import requests
import urllib.request
import os
import shutil

username = ""#write here 
password = ""
target = "" 
Follow = ""
unFollow = ""
class Instagram:
    def __init__(self,username,password):
        # self.browserProfile = webdriver.ChromeOptions()
        # self.browserProfile.add_experimental_option("prefers",{"int.accept_language":"en,en_US"})"chromedriver.exe",chrome_options=self.browserProfile
        self.browser = webdriver.Chrome()
        self.username = username
        self.password = password
        self.actions = ActionChains(self.browser)

    def signIn(self):
        self.browser.get("https://instagram.com")
        time.sleep(2)

        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(self.username)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(self.password)
        time.sleep(1)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').send_keys(Keys.ENTER)
        time.sleep(10)

    def getFollowers(self,target):
        self.browser.get("https://www.instagram.com/"+target)
        time.sleep(4)

        self.browser.find_element_by_xpath('//a[text()=" takipçi"]').click()
        time.sleep(4)

        dialog = self.browser.find_element_by_css_selector("div[role=dialog] ul")
        followerCount = len(dialog.find_elements_by_css_selector("li"))

        print(f"Firs count {followerCount}")

        action = webdriver.ActionChains(self.browser)

        a=0
        dialog.click()
        while True:
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(3)

            newCount = len(dialog.find_elements_by_css_selector("li"))

            if followerCount != newCount:
                followerCount = newCount
                print(f"second count {newCount},{a}")
                time.sleep(1)

            else:
                a=a+1
                dialog.click()

            if a==5:
                break

        print(f"Last count {followerCount}")

        followers = dialog.find_elements_by_css_selector("li")

        followerList = []
        for user in followers:
            link = user.find_element_by_css_selector("span a")
            print(link.text)
            followerList.append(link.text)

        with open("followers.txt","w",encoding="UTF-8") as file:
            for item in followerList:
                file.write(item+"\n")

    def getFollowing(self,target):
        self.browser.get("https://www.instagram.com/"+target)
        time.sleep(4)

        self.browser.find_element_by_xpath('//a[text()=" takip"]').click()
        time.sleep(4)

        dialog = self.browser.find_element_by_css_selector("div[role=dialog] ul")
        followCount = len(dialog.find_elements_by_css_selector("li"))

        print(f"Firs count {followCount}")

        action = webdriver.ActionChains(self.browser)

        a=0
        dialog.click()
        while True:
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(3)

            newCount = len(dialog.find_elements_by_css_selector("li"))

            if followCount != newCount:
                followCount = newCount
                print(f"second count {newCount},{a}")
                time.sleep(1)

            else:
                a=a+1
                dialog.click()

            if a==5:
                break

        print(f"Last count {followCount}")

        follows = dialog.find_elements_by_css_selector("li")

        followList = []
        for user in follows:
            link = user.find_element_by_css_selector("span a")
            print(link.text)
            followList.append(link.text)

        with open("follows.txt","w",encoding="UTF-8") as file:
            for item in followList:
                file.write(item+"\n")

    def followUser(self,Follow):
        self.browser.get("https://www.instagram.com/"+Follow)
        time.sleep(4)

        followButton = self.browser.find_element_by_tag_name("section section div div div button")
        if followButton.text == "Takip Et":
            followButton.click()
            time.sleep(5)

        else:
            print("Zaten takiptesin")

    def unfollowUser(self,unFollow):
        self.browser.get("https://www.instagram.com/"+unFollow)
        time.sleep(4)

        followButton = self.browser.find_element_by_tag_name("section section span span button")
        if followButton.text != "Takip Et":
            followButton.click()
            time.sleep(2)
            confirmButton = self.browser.find_element_by_xpath('//button[text()="Takibi Bırak"]').click()

        else:
            print("Zaten takip etmiyorsun")

    def getCompare(self):
        compareFollowerList = []
        compareFollowList = []

        commonFollower = []

        with  open("followers.txt","r",encoding="utf-8") as followers:
            for personFollower in followers:
                compareFollowerList.append(personFollower)

            with  open("follows.txt","r",encoding="utf-8") as follows:
                for personFollow in follows:
                    compareFollowList.append(personFollow)

        for o in range(0,len(compareFollowerList)):
            if compareFollowerList[o] in compareFollowList:
                if compareFollowerList[o] not in commonFollower:
                    commonFollower.append(compareFollowerList[o])

        for o in range(len(compareFollowerList),-1,-1):
            if o<len(compareFollowerList):
                if compareFollowerList[o] in commonFollower:
                    compareFollowerList.pop(o)

        for o in range(len(compareFollowList),-1,-1):
            if o<len(compareFollowList):
                if compareFollowList[o] in commonFollower:
                    compareFollowList.pop(o)

        with open("serefsizler.txt","w",encoding="UTF-8") as file:
            file.write(f"Ortak takipleştiğin kişilerin sayisi : {len(commonFollower)}\n")
            for item in commonFollower:
                file.write(item)

            file.write("\n")

            file.write(f"Onların seni takip edip senin onları takip etmediğin kişilerin sayisi : {len(compareFollowerList)}\n")
            for item in compareFollowerList:
                file.write(item)

            file.write("\n\n")

            file.write(f"Onların seni takip etmeyip senin onları takip ettiğin kişilerin sayisi : {len(compareFollowList)}\n")
            for item in compareFollowList:
                file.write(item)

    def likePost(self,target):
        self.browser.get("https://www.instagram.com/"+target)
        time.sleep(4)

        postCount = int("".join(self.browser.find_element_by_tag_name("section ul li span span").text.split('.')))
        print(postCount)

        self.browser.find_element_by_tag_name("article a div").click()
        time.sleep(3)

        a=0
        while True:
            if self.browser.find_element_by_tag_name("article section svg").get_attribute("aria-label") == "Beğen":
                self.browser.find_element_by_tag_name("article section svg").click()
                time.sleep(2)

            a=a+1
            print(a)
            if a == postCount:
                print("Post bitti")
                break

            self.browser.find_element_by_xpath('//a[text()="Sonraki"]').click()
            time.sleep(5)

    def downLoadPost(self,target):
        self.browser.get("https://www.instagram.com/"+target)
        time.sleep(3)

        profilePicture = self.browser.find_element_by_tag_name("section main header span img").get_attribute("src")
        time.sleep(4)

        if os.path.exists("C:/Users/Egroses/Desktop/HECKIR/İnstagram/"+target) == True:
            os.chdir("C:/Users/Egroses/Desktop/HECKIR/İnstagram/")
            shutil.rmtree(target)

        time.sleep(3)
        os.chdir("C:/Users/Egroses/Desktop/HECKIR/İnstagram/")
        os.mkdir(target)
        os.listdir()

        a=1
        downloadPlace = "C:/Users/Egroses/Desktop/HECKIR/İnstagram/"+target+"/"+str(a)+".jpg"

        urllib.request.urlretrieve(profilePicture,downloadPlace)

        postCount = int("".join(self.browser.find_element_by_tag_name("section ul li span span").text.split('.')))
        print(postCount)

        self.browser.find_element_by_tag_name("article a div").click()
        time.sleep(3)


        sayac=0
        while True:
            a=a+1
            if len(self.browser.find_elements_by_tag_name('article[role="presentation"] div ul li.Ckrof'))>0:
                try:
                    try:
                        downloadPlace = "C:/Users/Egroses/Desktop/HECKIR/İnstagram/"+target+"/"+str(a)+".mp4"
                        postLink = self.browser.find_element_by_tag_name('article[role="presentation"] div ul li.Ckrof video').get_attribute("src")
                        time.sleep(2)
                    except:
                        downloadPlace = "C:/Users/Egroses/Desktop/HECKIR/İnstagram/"+target+"/"+str(a)+".jpg"
                        postLink = self.browser.find_element_by_tag_name('article[role="presentation"] div ul li.Ckrof img').get_attribute("src")
                        time.sleep(2)

                        urllib.request.urlretrieve(postLink,downloadPlace)
                        print("ilki indi")

                except:
                    print("İstisnai durum!")

                while len(self.browser.find_elements_by_tag_name('article[role="presentation"] button._6CZji'))>0:
                    a=a+1
                    self.browser.find_element_by_tag_name('article[role="presentation"] button._6CZji').click()
                    time.sleep(2)

                    coklu = self.browser.find_elements_by_tag_name('article[role="presentation"] div ul li.Ckrof')

                    try:
                        try:
                            downloadPlace = "C:/Users/Egroses/Desktop/HECKIR/İnstagram/"+target+"/"+str(a)+".mp4"
                            postLink = coklu[1].find_element_by_tag_name('video').get_attribute("src")
                            time.sleep(2)
                        except:
                            downloadPlace = "C:/Users/Egroses/Desktop/HECKIR/İnstagram/"+target+"/"+str(a)+".jpg"
                            postLink = coklu[1].find_element_by_tag_name('img').get_attribute("src")
                            time.sleep(2)
                            print("ikinci indi")

                        urllib.request.urlretrieve(postLink,downloadPlace)
                    
                    except:
                        print("İstisnai durum!")
    
            else:
                try:
                    try:
                        downloadPlace = "C:/Users/Egroses/Desktop/HECKIR/İnstagram/"+target+"/"+str(a)+".mp4"
                        postLink = self.browser.find_element_by_tag_name('article[role="presentation"] video').get_attribute("src")
                        time.sleep(2)
                    except:
                        downloadPlace = "C:/Users/Egroses/Desktop/HECKIR/İnstagram/"+target+"/"+str(a)+".jpg"
                        postLink = self.browser.find_element_by_tag_name('article[role="presentation"] div div div div img').get_attribute("src")
                        time.sleep(2)


                    urllib.request.urlretrieve(postLink,downloadPlace)

                except:
                    print("İstisnai durum!")

            sayac=sayac+1
            print(sayac)
            if sayac == postCount:
                print("Post bitti")
                break

            self.browser.find_element_by_xpath('//a[text()="Sonraki"]').click()
            time.sleep(5)




insta = Instagram(username,password)
insta.signIn()
insta.followUser(Follow)
insta.getFollowers(target)
insta.getFollowing(target)
insta.getCompare()
insta.likePost(target)
insta.downLoadPost(target)
insta.unfollowUser(unFollow)





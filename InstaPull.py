from email import message
import json
from operator import contains
import requests
import datetime
from datetime import datetime
import csv
import pytz
from pytz import timezone
import os
from datetime import date
import subprocess
import config
from configparser import ConfigParser
from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import messagebox
import sys
from tkinter.messagebox import showinfo
from os.path import exists
from time import sleep



#RUN NEW CONFIG
def newConfig():
    
    userToken = tk.StringVar()
    username = tk.StringVar()
    igUserID = tk.StringVar()
    configName = tk.StringVar()




    #THE  NEW WINDOW
    configWindow = tk.Tk()
    configWindow.geometry("500x500")
    configWindow.title("New Config")

    queryUserToken = tk.Label(configWindow, text = "Insert your User Access token: ")
    queryUserToken.grid(row = 1, column = 0)
    entryUsertoken = ttk.Entry(configWindow, textvariable = userToken)
    entryUsertoken.grid(row = 1, column = 1)

    queryUsername = tk.Label(configWindow, text = "Insert your Instagram handle (without @): ")
    queryUsername.grid(row = 2, column = 0)
    entryUsername = ttk.Entry(configWindow, textvariable = username)
    entryUsername.grid(row = 2, column = 1)

    queryigUserID = tk.Label(configWindow, text = "Insert your Instagram User ID:  ")
    queryigUserID.grid(row = 3, column = 0)
    entryigUserID = ttk.Entry(configWindow, textvariable = igUserID)
    entryigUserID.grid(row = 3, column = 1)

    queryconfigName = tk.Label(configWindow, text = "Enter the profile name: ")
    queryconfigName.grid(row = 4, column = 0)
    entryconfigName = ttk.Entry(configWindow, textvariable = configName)
    entryconfigName.grid(row = 4, column = 1)

    ##### SAVE BUTTON
    buttonSave = tk.Button(configWindow, text = 'Save', command = lambda : save_config())
    buttonSave.grid(row=5, columnspan=2)



    def save_config():
        resultUserToken = entryUsertoken.get()
        resultUsername = entryUsername.get()
        resultUserID = entryigUserID.get()
        resultConfigName = entryconfigName.get()

        onfig = ConfigParser()
        config.read(config_file)

        config.add_section(resultConfigName)
        config.set(resultConfigName, "User Token", resultUserToken)
        config.set(resultConfigName, "Username", resultUsername)
        config.set(resultConfigName, "Instagram User ID", resultUserID)

        with open(config_file, "w") as confile:
            config.write(confile)
        config.read(config_file)
        messagebox.showinfo( "Config Saved", "Please restart the computer to see the new config.")

        configurations = config.sections()
        configWindow.destroy()




if not os.path.isdir("Configs"):
        os.makedirs("Configs")

if exists("Configs/config.ini") == True:
    pass
else:
    with open("Configs/config.ini","w") as config:
        pass
    newConfig()
    sleep(10)
    




today = date.today()
now = datetime.now()
current_time = now.strftime("%H.%M.%S")
current_datetime = now.strftime("%m-%d-%Y %H.%M.%S")

desktop = os.path.join(os.path.expanduser("~"), "Desktop")
downloads = os.path.join(os.path.expanduser("~"), "Downloads")


##### THE TOP LEVEL WINDOW
root = tk.Tk()
root.geometry("500x500")
greeting = ttk.Label(text = "Instagram Ddata Pull")
root.title("InstaPull")




##### CONFIG SETTINGS + DROPDOWN

global config_file
global configurations

config_file = "Configs/config.ini"
config = ConfigParser()
config.read(config_file)
configurations = config.sections()
print(configurations)


configuration = StringVar()
configuration.set("Select the Page")

if configurations != []:
    dropdownConfig = tk.OptionMenu(
        root,
        configuration,
        *configurations
)
    dropdownConfig.grid(row=0, columnspan=2)




def hashtagListFormat(hashtagList):
    hashtagString = "".join(hashtagList)

    hashtagsSplit = hashtagString.split("#")
    newHashtagList = []

    for word in hashtagsSplit:
        if word == "":
            pass
        elif " " in word:
            word = word[:-1]
            word = "#" + word
            newHashtagList.append(word)
        else:
            word = "#" + word
            newHashtagList.append(word)
            
    return newHashtagList




def pullData():
    try:
        limit = entryLimit.get()
    except:
        limit = 10

    currentConfig = configuration.get()
    currentUserToken = config[currentConfig]["User Token"]
    currentUsername = config[currentConfig]["Username"]
    currentUserID = config[currentConfig]["Instagram User ID"]


    exportFolderPath = os.path.join(downloads, "{} Export".format(current_datetime))
    errorFolderPath = os.path.join(downloads, "{} Export/ErrorLog".format(current_datetime))

    imageCSV_url = os.path.join(downloads, "{} Export/images.csv".format(current_datetime))
    reelsCSV_url = os.path.join(downloads, "{} Export/reels.csv".format(current_datetime))



    if not os.path.isdir(exportFolderPath):
        os.makedirs(exportFolderPath)

    


    imageCSV_header = ["Media ID", "Time Posted","Image URL","Instagram Post ","Caption","Media Type","Engagement","Followers","Impressions","Reach","Likes","Comments","Saves","Video Views", "LinkIn.bio", "Revenue", "Hashtags", "Hashtag Count"]
    reelsCSV_header = ["Media ID", "Time Posted","Image URL","Instagram Post","Caption","Media Type","Reach", "Plays", "Total Interactions", "Likes","Comments","Saves","Shares", "Hashtags", "Hashtag Count"]

    imageCSV = open(imageCSV_url, 'w', encoding='utf-8')
    reelsCSV = open(reelsCSV_url, 'w', encoding='utf-8')

    writerImages = csv.writer(imageCSV)
    writerReels = csv.writer(reelsCSV)

    writerImages.writerow(imageCSV_header)
    writerReels.writerow(reelsCSV_header)

    errorsCSV_url = os.path.join(downloads, "{} Export/ErrorLog/errors.csv".format(current_datetime))
    if not os.path.isdir(errorFolderPath):
        os.makedirs(errorFolderPath)

    errorsCSV = open(errorsCSV_url, 'w', encoding='utf-8')
    writerErrorsCSV = csv.writer(errorsCSV)
    errorsCSV_header = ["Message ID", "Info"]
    writerErrorsCSV.writerow(errorsCSV_header)

    
    id_url = "https://graph.facebook.com/v14.0/{}/media".format(currentUserID)
    id_payload = {
        "access_token": currentUserToken,
        "limit": limit
        }

    r = requests.get(id_url, id_payload)
    id_results = json.loads(r.text)



    for ids in id_results['data']:
        media_id = ids['id']
        print(media_id)
        print("\n")

        postInfo_url = "https://graph.facebook.com/v14.0/{}".format(media_id)
        postInfo_payload = {
            "fields": "caption,comments_count,id,like_count,media_type,permalink,media_product_type,media_url,shortcode,thumbnail_url,timestamp",
            "access_token": currentUserToken
        }

        postInfo = requests.get(postInfo_url, postInfo_payload)
        post = json.loads(postInfo.text)

        try: 
            ##PARAMETERS FROM post
            type = post['media_type']                   ###(carousel_album, image, video)
            postType = post['media_product_type']       ###(ad, feed, story, reels)
            permalink = post['permalink']
            
            if "caption" not in post:
                caption = ""
            else:
                caption = post['caption']
            likes = post['like_count']
            comments = post['comments_count']
            print(comments)

            #HASHTAGS


            hashtags = ""
            hashtagCount = 0
            hashtagList = []





            
            ####### PULL HASHTAGS + COUNT FROM CAPTION
            

            if "#" in caption:
                captionWords = caption.split()
                for word in captionWords:
                    if word[0] == "#":
                        hashtagList.append(word)
                



            ####### PULL HASHTAGS + COUNT FROM COMMENTS


            if int(comments) > 0:
                
                commentsInfo_url = "https://graph.facebook.com/v14.0/{}/comments".format(media_id)
                commentsInfo_payload = {
                "access_token": currentUserToken,
                "fields": "username,text,timestamp,like_count"
                }

                commentsInfo = requests.get(commentsInfo_url, commentsInfo_payload)
                commentsList = json.loads(commentsInfo.text)

                try:
                    while hashtagCount < 30:
                        for comment in commentsList['data']:
                            if "#" in comment['text']:
                                if comment['username'] == currentUsername:
                                    commentWords = comment['text'].split()
                                    for word in commentWords:
                                        if word[0] == "#":
                                            hashtagList.append(word)
                                else:
                                    pass
                            else:
                                pass
                        if 'paging' in commentsList:
                            nextCommentsPage = requests.get(commentsList['paging']['next'])
                            commentsList = json.loads(nextCommentsPage.text)
                        else:
                            break        
                except:
                    print("---ERROR---")



            formattedHashtagsList = hashtagListFormat(hashtagList)
            
            hashtagCount = len(formattedHashtagsList)
            hashtags = " ".join(formattedHashtagsList)



            
            ###TIMESTAMP CONVERSION
            timestamp = post['timestamp']
            timestamp = timestamp
            timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
            timestamp = timestamp.astimezone(timezone('US/Pacific'))
            timestamp = timestamp.strftime("%m-%d-%Y %H:%M:%S")

            
            ###THUMBNAIL SELECTION
            if "thumbnail_url" in post:
                thumbnail = post['thumbnail_url']
            else:
                thumbnail = post['media_url']
            




            ####### VARIABLES FOR SECOND API CALL

            followers = ""
            reach = ""
            saves = ""
            engagement = ""              ###IMAGES ONLY
            impressions = ""             ###IMAGES ONLY
            videoViews = ""              ###IMAGES ONLY

            total_interactions = ""      ###REELS ONLY
            plays = ""                   ###REELS ONLY

            print(type)
            print(timestamp)
            print("\n")


            insights_url = "https://graph.facebook.com/{}/insights".format(media_id)
            
            

            ######## CAROUSEL FEED POSTS

            if type == "CAROUSEL_ALBUM": 
                thumbnail = permalink + "media/?size=l"
                metrics = "carousel_album_engagement,carousel_album_impressions,carousel_album_reach,carousel_album_saved"

                insights_payload = {
                    "period": "day",
                    "metric": metrics,
                    "access_token": currentUserToken
                }

                insightsInfo = requests.get(insights_url, insights_payload)
                insights = json.loads(insightsInfo.text)
                
                for dataPoint in insights['data']:
                    if dataPoint['name'] == "carousel_album_engagement":
                        engagement = dataPoint['values'][0]["value"]
                    elif dataPoint['name'] == "carousel_album_impressions":
                        impressions = dataPoint['values'][0]["value"]
                    elif dataPoint['name'] == "carousel_album_reach":
                        reach = dataPoint['values'][0]["value"]
                    elif dataPoint['name'] == "carousel_album_saved":
                        saves = dataPoint['values'][0]["value"]

                newRow = [media_id, timestamp,thumbnail,permalink,caption,type,engagement,followers,impressions,reach,likes,comments,saves,videoViews,"", "", hashtags, str(hashtagCount)]
                writerImages.writerow(newRow)



            ######## IMAGE FEED POSTS

            elif type == "IMAGE":
                metrics = "engagement,impressions,reach,saved"
                thumbnail = permalink + "media/?size=l"

                insights_payload = {
                    "period": "day",
                    "metric": metrics,
                    "access_token": currentUserToken
                }

                insightsInfo = requests.get(insights_url, insights_payload)
                insights = json.loads(insightsInfo.text)

                for dataPoint in insights['data']:
                    if dataPoint['name'] == "engagement":
                        engagement = dataPoint['values'][0]["value"]
                    elif dataPoint['name'] == "impressions":
                        impressions = dataPoint['values'][0]["value"]
                    elif dataPoint['name'] == "reach":
                        reach = dataPoint['values'][0]["value"]
                    elif dataPoint['name'] == "saved":
                        saves = dataPoint['values'][0]["value"]

                newRow = [media_id, timestamp,thumbnail,permalink,caption,type,engagement,followers,impressions,reach,likes,comments,saves,videoViews, "", "", hashtags, str(hashtagCount)]
                writerImages.writerow(newRow)



            ########## VIDEO FEED POSTS

            elif type == "VIDEO":
                if "instagram.com/tv" in permalink:
                    metrics = "reach,saved"
                    insights_payload = {
                        "period": "day",
                        "metric": metrics,
                        "access_token": currentUserToken
                    }
        
                    insightsInfo = requests.get(insights_url, insights_payload)
                    insights = json.loads(insightsInfo.text)

                    for dataPoint in insights['data']:
                        if dataPoint['name'] == "saved":
                            saves = dataPoint['values'][0]["value"]
                        elif dataPoint['name'] == "reach":
                            reach = dataPoint['values'][0]["value"]

                    newRow = [media_id, timestamp,thumbnail,permalink,caption,type,reach,"n/a","n/a",likes,comments,saves,"n/a",hashtags, str(hashtagCount)]
                    writerReels.writerow(newRow)



                #######VIDEO FEED POSTS (OLDER)
                
                elif "instagram.com/p/" in permalink:
                    metrics = "engagement,reach,saved,video_views"
                    insights_payload = {
                        "period": "day",
                        "metric": metrics,
                        "access_token": currentUserToken
                    }

        
                    insightsInfo = requests.get(insights_url, insights_payload)
                    insights = json.loads(insightsInfo.text)

                    for dataPoint in insights['data']:
                        if dataPoint['name'] == "saved":
                            saves = dataPoint['values'][0]["value"]
                        elif dataPoint['name'] == "reach":
                            reach = dataPoint['values'][0]["value"]
                        elif dataPoint['name'] == "engagement":
                            engagement = dataPoint['values'][0]["value"]
                        elif dataPoint['name'] == "video_views":
                            plays = dataPoint['values'][0]["value"]

                    newRow = [media_id, timestamp,thumbnail,permalink,caption,type,reach,plays,engagement,likes,comments,saves,"n/a",hashtags, str(hashtagCount)]
                    writerReels.writerow(newRow)


                else:
                    metrics = "plays,reach,saved,shares,total_interactions"

                    insights_payload = {
                        "period": "day",
                        "metric": metrics,
                        "access_token": currentUserToken
                    }

            
                    insightsInfo = requests.get(insights_url, insights_payload)
                    insights = json.loads(insightsInfo.text)


                    for dataPoint in insights['data']:
                        if dataPoint['name'] == "plays":
                            plays = dataPoint['values'][0]["value"]
                        elif dataPoint['name'] == "reach":
                            reach = dataPoint['values'][0]["value"]
                        elif dataPoint['name'] == "saved":
                            saves = dataPoint['values'][0]["value"]
                        elif dataPoint['name'] == "shares":
                            shares = dataPoint['values'][0]["value"]
                        elif dataPoint['name'] == "total_interactions":
                            total_interactions = dataPoint['values'][0]["value"]
                    newRow = [media_id, timestamp,thumbnail,permalink,caption,type,reach,plays,total_interactions,likes,comments,saves,shares, hashtags, str(hashtagCount)]
                    writerReels.writerow(newRow)

        except:
            errorRow = [media_id, post]
            writerErrorsCSV.writerow(errorRow)


    imageCSV.close()
    reelsCSV.close()

    errorsCSV.close()
    subprocess.call(["open", exportFolderPath])

    
    





buttonNewConfig = tk.Button(
    root,
    text = "New Config",
    width = 25,
    height = 2,
    bg = "blue",
    fg = "black",
    command = newConfig
    )
buttonNewConfig.grid(row = 1, columnspan=2)



limitVar = tk.StringVar()

queryLimit = tk.Label(root, text = "How many posts do you want to pull? ")
queryLimit.grid(row = 2, column = 0)
entryLimit = ttk.Entry(root, textvariable = limitVar)
entryLimit.grid(row = 2, column = 1)



buttonPullData = tk.Button(
    root,
    text = "Pull Data",
    width = 50,
    height = 5,
    bg = "blue",
    fg = "black",
    command = pullData
    )
buttonPullData.grid(row = 3, columnspan=2)


root.mainloop()






""" Progress Bar (in progress)
class Family(object):
    def parent(self):
        self.test = 0
        self.child()
    
    def child(self):
        self.test += 1
        print(self.test)


def launchProgressBar():
    
    try:
        limit = entryLimit.get()
    except:
        limit = 10


    progressBar = tk.Toplevel(root)
    progressBar.geometry("300x120")
    progressBar.title("Progress")

    progressCount = 0

    def update_progress_label():
        return f"Current Progress: {str(progressCount)} / {str(limit)}"

    def progress():
        if pb['value'] < 100:
            pb['value'] = int(progressCount)/int(limit)
            value_label['text'] = update_progress_label()
        else:
            showinfo(message='The process is complete!')

    def stop():
        pb.stop()
        value_label['text'] = update_progress_label()


    pb = ttk.Progressbar(
        progressBar,
        orient='horizontal',
        mode='determinate',
        length=280
    )

    pbLabel = tk.Label(progressBar, text="Hello")
    pbLabel.grid(row=0)
    pb.grid(column=0, row=1, columnspan=2, padx=10, pady=20)

    value_label = ttk.Label(progressBar, text=update_progress_label())
    value_label.grid(column=0, row=12, columnspan=2)
    
    





"""


""" Terminal Readout (in progress)
class Redirect():
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert('end', text)

    def flush(self):
        pass


def test():
    print("Hello world")
    p = subprocess.run("ping -c 4 stackoverflow.com", shell=True, stdout=subprocess.PIPE)
    print(p.stdout.decode())


text = tk.Text(root)
text.grid(row=6, columnspan=5)

button = tk.Button(root, text="TEST", command=test)
button.grid(row=5, columnspan=2)

old_stdout = sys.stdout
sys.stdout = Redirect(text)

"""



""" Terminal Readout2 (in progress)
if __name__ == '__main__':        
    def printLog():
        print(media_id)
        print(permalink)
    
    console = tk.Text(root)
    console.grid(row=5, columnspan=3)

    pl = PrintLogger(console)

if __name__ == '__main__':
    def do_something():
        print('I did something')
        root.after(1000, do_something)
    
    t = tk.Text(root)
    t.grid(row=5)

    pl = PrintLogger(t)

    sys.stdout = pl

    root.after(1000, do_something)
"""



        
""" This writes individual to JSON file (doesn't add them all)
    jsonFile = "/Users/davidwills/Dropbox/_New File Structure/Files/1) Coding/1) Projects/Python/Instagram Graph API/insights.json"
    with open(jsonFile, "w") as outfile:
        json.dump(insights, outfile, indent=2)
"""


""" OPEN CSV using WITH command
with open(imageCSV_url, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(imageCSV_header)

with open(reelsCSV_url, 'w', encoding='UTF8', newline='') as g:
    writer = csv.writer(g)
    writer.writerow(reelsCSV_header)
"""

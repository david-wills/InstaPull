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

today = date.today()
now = datetime.now()
current_time = now.strftime("%H.%M.%S")
current_datetime = now.strftime("%m-%d-%Y %H.%M.%S")

desktop = os.path.join(os.path.expanduser("~"), "Desktop")
downloads = os.path.join(os.path.expanduser("~"), "Downloads")



"""
global config_file
config_file = "Configs/config.ini"
config = ConfigParser()
config.read(config_file)
configurations = config.sections()
"""



##### CONFIG PARAMETERS
long_lived_user_token = "EAAHHfZCdfvGcBAN7mOuv5PRgKsb3gPzcoCDcyTY52XCBop49wodzKA2t7RHs3ftt0BMQUqoOZCePDTpEtTZCWx16qOBZCVgOdLf9tL9mZBjV1tlB0xnYzEVc3jKNWCnDBkDVDaaqVrW8R1wPZAKjbRafRcMIcAQW5JgSB9FtgWdQZDZD"
igUsername = "totalnerd_"
ig_user_id = "17841400068127870"




limit = "10"




long_lived_tn_page_access_token = "EAAHHfZCdfvGcBAPZAfgqui1JJAgjH7y1Aq74ZA2fGGXtZAKNO5YQpAqUOflYstc5ZBW64LzQjZAU8o3X1OzAmZBMtPMbgT9VlviIdZAaBFf0CSFyBDdyvg0z0yKrvP0HEYj5xT4lsqbhpzN2MWDIHtmpUDqOEGFf0zZCfZAUkIduR1Tz3AaBX05pN4"
long_lived_wh_page_access_token = "EAAHHfZCdfvGcBAIiOpbe8K6yYNN7JZBxsLZAfkjrvpnPATdOePeojwjEwVCZA69BB9enwFRF3cuP4jtMum5VXNDIwZCK1PsLzhF29rG46zDqV7P83plYZCQtMhtCOqgnOUPevWr3zaZB6rfUv8nvZBL1gtHngEVogpPNkWpn1ih5yClPPQVRnJvC"
long_lived_gs_page_access_token = "EAAHHfZCdfvGcBAFgywVBqRC18JlcdnHLCzxYLh2FT8o4xChTUxGSd8155hoXzwsOf6KTWN4GAOS86s8UQSZAuASzZCaYLSeyFY9ZCEZAEndWBvFTSXjVmTAJQ371nbNPJkc3iZCaFqcvdP1dTUbfzeaBQTZBUjCNaTej53QQL5P2qj2S8nLM2dT"


gs_facebook_id = "1011190218967434"
wh_facebook_id = "642850749204637"
tn_facebook_id = "763663430350503"

gs_ig_id = "17841405694374055"
wh_ig_id = "17841405465779649"
tn_ig_id = "17841400068127870"





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



    
    id_url = "https://graph.facebook.com/v14.0/{}/media".format(ig_user_id)
    id_payload = {
        "access_token": long_lived_user_token,
        "limit": limit
        }

    r = requests.get(id_url, id_payload)
    id_results = json.loads(r.text)



    for ids in id_results['data']:
        media_id = ids['id']
        print("\nNew ID")
        print(media_id)
        print("\n")

        postInfo_url = "https://graph.facebook.com/v14.0/{}".format(media_id)
        postInfo_payload = {
            "fields": "caption,comments_count,id,like_count,media_type,permalink,media_product_type,media_url,shortcode,thumbnail_url,timestamp",
            "access_token": long_lived_user_token
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


            #HASHTAGS


            hashtags = ""
            hashtagCount = 0
            hashtagList = []



            
            print(comments + "comments")



            
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
                "access_token": long_lived_user_token,
                "fields": "username,text,timestamp,like_count"
                }

                commentsInfo = requests.get(commentsInfo_url, commentsInfo_payload)
                commentsList = json.loads(commentsInfo.text)

                try:
                    while hashtagCount < 30:
                        for comment in commentsList['data']:
                            if "#" in comment['text']:
                                if comment['username'] == igUsername:
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
                    "access_token": long_lived_user_token
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
                    "access_token": long_lived_user_token
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
                        "access_token": long_lived_user_token
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
                        "access_token": long_lived_user_token
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
                        "access_token": long_lived_user_token
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



    

        
pullData()



        
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

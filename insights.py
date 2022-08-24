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

today = date.today()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
downloads = os.path.join(os.path.expanduser("~"), "Downloads")

imagesFilePath = os.path.join(downloads, "{} Export/images.csv".format(current_time))
reelsFilePath = os.path.join(downloads, "{} Export/reels.csv".format(current_time))
errorsFilePath = os.path.join(downloads, "{} Export/ErrorLog/errors.csv".format(current_time))

long_lived_user_token = "EAAHHfZCdfvGcBAN7mOuv5PRgKsb3gPzcoCDcyTY52XCBop49wodzKA2t7RHs3ftt0BMQUqoOZCePDTpEtTZCWx16qOBZCVgOdLf9tL9mZBjV1tlB0xnYzEVc3jKNWCnDBkDVDaaqVrW8R1wPZAKjbRafRcMIcAQW5JgSB9FtgWdQZDZD"

long_lived_tn_page_access_token = "EAAHHfZCdfvGcBAPZAfgqui1JJAgjH7y1Aq74ZA2fGGXtZAKNO5YQpAqUOflYstc5ZBW64LzQjZAU8o3X1OzAmZBMtPMbgT9VlviIdZAaBFf0CSFyBDdyvg0z0yKrvP0HEYj5xT4lsqbhpzN2MWDIHtmpUDqOEGFf0zZCfZAUkIduR1Tz3AaBX05pN4"
long_lived_wh_page_access_token = "EAAHHfZCdfvGcBAIiOpbe8K6yYNN7JZBxsLZAfkjrvpnPATdOePeojwjEwVCZA69BB9enwFRF3cuP4jtMum5VXNDIwZCK1PsLzhF29rG46zDqV7P83plYZCQtMhtCOqgnOUPevWr3zaZB6rfUv8nvZBL1gtHngEVogpPNkWpn1ih5yClPPQVRnJvC"
long_lived_gs_page_access_token = "EAAHHfZCdfvGcBAFgywVBqRC18JlcdnHLCzxYLh2FT8o4xChTUxGSd8155hoXzwsOf6KTWN4GAOS86s8UQSZAuASzZCaYLSeyFY9ZCEZAEndWBvFTSXjVmTAJQ371nbNPJkc3iZCaFqcvdP1dTUbfzeaBQTZBUjCNaTej53QQL5P2qj2S8nLM2dT"


gs_facebook_id = "1011190218967434"
wh_facebook_id = "642850749204637"
tn_facebook_id = "763663430350503"

gs_ig_id = "17841405694374055"
wh_ig_id = "17841405465779649"
tn_ig_id = "17841400068127870"


ig_user_id = "17841400068127870"

def pullData():
    
    imageCSV_url = "/Users/davidwills/Dropbox/_New File Structure/Files/1) Coding/1) Projects/Python/Instagram Graph API/images.csv"
    reelsCSV_url = "/Users/davidwills/Dropbox/_New File Structure/Files/1) Coding/1) Projects/Python/Instagram Graph API/reels.csv"

    imageCSV_header = ["Time Posted","Image URL","Instagram Post ","Caption","Media Type","Engagement","Followers","Impressions","Reach","Likes","Comments","Saves","Video Views", "LinkIn.bio", "Revenue", "Hashtags", "Hashtag Count"]
    reelsCSV_header = ["Time Posted","Image URL","Instagram Post","Caption","Media Type","Reach", "Plays", "Total Interactions", "Likes","Comments","Saves","Shares", "Hashtags", "Hashtag Count"]

    imageCSV = open(imageCSV_url, 'w', encoding='utf-8')
    reelsCSV = open(reelsCSV_url, 'w', encoding='utf-8')

    writerImages = csv.writer(imageCSV)
    writerReels = csv.writer(reelsCSV)

    writerImages.writerow(imageCSV_header)
    writerReels.writerow(reelsCSV_header)



    errorsCSV_url = "/Users/davidwills/Dropbox/_New File Structure/Files/1) Coding/1) Projects/Python/Instagram Graph API/errors.csv"
    errorsCSV = open(errorsCSV_url, 'w', encoding='utf-8')
    writerErrorsCSV = csv.writer(errorsCSV)
    errorsCSV_header = ["Message ID", "Info"]
    writerErrorsCSV.writerow(errorsCSV_header)





    
    id_url = "https://graph.facebook.com/v14.0/{}/media".format(ig_user_id)
    id_payload = {
        "access_token": long_lived_user_token,
        "limit": "10"
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
            print(comments)

            #HASHTAGS

            hashtags = ""
            hashtagCount = ""
            print(int(comments))



            ####### PULL HASHTAGS + COUNT FROM CAPTION

            if "#" in caption:
                captionWords = caption.split()
                hashtagList = []
                n = 0
                for word in captionWords:
                    if word[0] == "#":
                        n += 1
                        hashtagList.append(word)
                hashtags = " ".join(hashtagList)
                hashtagCount = str(n)



            ####### PULL HASHTAGS + COUNT FROM COMMENTS


            elif int(comments) > 0:
                commentsInfo_url = "https://graph.facebook.com/v14.0/{}/comments".format(media_id)
                commentsInfo_payload = {
                    "access_token": long_lived_user_token,
                    "fields": "user,text,timestamp,like_count"
                }

                commentsInfo = requests.get(commentsInfo_url, commentsInfo_payload)
                commentsList = json.loads(commentsInfo.text)
                print(commentsList)

                for comment in commentsList['data']:
                    if "#" in comment['text']:
                        if comment['username'] == 'totalnerd_':
                            hashtags = comment['text']
                            x = hashtags.split()
                            n = 0
                            for word in x:
                                if word[0] == "#":
                                    n += 1
                            hashtagCount = str(n)

                    else:
                        pass





            
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
            
            
            """insights_payload = {
                "period": "day",
                "metric": metrics,
                "access_token": long_lived_user_token
            }
            
            insightsInfo = requests.get(insights_url, insights_payload)
            insights = json.loads(insightsInfo.text)
            print(insights)
            """








            """ OPEN CSV using WITH command
            with open(imageCSV_url, 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(imageCSV_header)
            
            with open(reelsCSV_url, 'w', encoding='UTF8', newline='') as g:
                writer = csv.writer(g)
                writer.writerow(reelsCSV_header)
            """
        
            


            ######## CAROUSEL FEED POSTS

            if type == "CAROUSEL_ALBUM": 
                metrics = "carousel_album_engagement,carousel_album_impressions,carousel_album_reach,carousel_album_saved"

                insights_payload = {
                    "period": "day",
                    "metric": metrics,
                    "access_token": long_lived_user_token
                }


                insightsInfo = requests.get(insights_url, insights_payload)
                insights = json.loads(insightsInfo.text)

                print(insights)

                
                for dataPoint in insights['data']:
                    if dataPoint['name'] == "carousel_album_engagement":
                        engagement = dataPoint['values'][0]["value"]
                    elif dataPoint['name'] == "carousel_album_impressions":
                        impressions = dataPoint['values'][0]["value"]
                    elif dataPoint['name'] == "carousel_album_reach":
                        reach = dataPoint['values'][0]["value"]
                    elif dataPoint['name'] == "carousel_album_saved":
                        saves = dataPoint['values'][0]["value"]
                newRow = [timestamp,thumbnail,permalink,caption,type,engagement,followers,impressions,reach,likes,comments,saves,videoViews,"", "", hashtags, hashtagCount]
                writerImages.writerow(newRow)
                #csv.append() -- csvImageCells = (timestamp,thumbnail,permalink,caption,type,engagement,followers,impressions,reach,likes,comments,saves,videoViews)




            ######## IMAGE FEED POSTS

            elif type == "IMAGE":
                metrics = "engagement,impressions,reach,saved"


                insights_payload = {
                    "period": "day",
                    "metric": metrics,
                    "access_token": long_lived_user_token
                }

                insightsInfo = requests.get(insights_url, insights_payload)
                insights = json.loads(insightsInfo.text)
                print(insights)
                for dataPoint in insights['data']:
                    if dataPoint['name'] == "engagement":
                        engagement = dataPoint['values'][0]["value"]
                    elif dataPoint['name'] == "impressions":
                        impressions = dataPoint['values'][0]["value"]
                    elif dataPoint['name'] == "reach":
                        reach = dataPoint['values'][0]["value"]
                    elif dataPoint['name'] == "saved":
                        saves = dataPoint['values'][0]["value"]

                newRow = [timestamp,thumbnail,permalink,caption,type,engagement,followers,impressions,reach,likes,comments,saves,videoViews, "", "", hashtags, hashtagCount]
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

                    print(insights)


                    for dataPoint in insights['data']:
                        if dataPoint['name'] == "saved":
                            saves = dataPoint['values'][0]["value"]
                        elif dataPoint['name'] == "reach":
                            reach = dataPoint['values'][0]["value"]

                    newRow = [timestamp,thumbnail,permalink,caption,type,reach,"n/a","n/a",likes,comments,saves,"n/a",hashtags, hashtagCount]
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

                    print(insights)

                    for dataPoint in insights['data']:
                        if dataPoint['name'] == "saved":
                            saves = dataPoint['values'][0]["value"]
                        elif dataPoint['name'] == "reach":
                            reach = dataPoint['values'][0]["value"]
                        elif dataPoint['name'] == "engagement":
                            engagement = dataPoint['values'][0]["value"]
                        elif dataPoint['name'] == "video_views":
                            plays = dataPoint['values'][0]["value"]


                    newRow = [timestamp,thumbnail,permalink,caption,type,reach,plays,engagement,likes,comments,saves,"n/a",hashtags, hashtagCount]
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

                    print(insights)


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
                    newRow = [timestamp,thumbnail,permalink,caption,type,reach,plays,total_interactions,likes,comments,saves,shares, hashtags, hashtagCount]
                    writerReels.writerow(newRow)

            else:
                pass ##note that I need to add something for stories or else it might get screwed up
        except:
            errorRow = [media_id, post]
            writerErrorsCSV.writerow(errorRow)



    imageCSV.close()
    reelsCSV.close()

    errorsCSV.close()
    



        



    """
        print("\nJSON PARSING\n")


        #####IMAGE POSTS########
        for dataPoint in insights['data']:
            if dataPoint['name'] == "engagement":
                engagement = dataPoint['values'][0]["value"]
            elif dataPoint['name'] == "impressions":
                impressions = dataPoint['values'][0]["value"]
            elif dataPoint['name'] == "reach":
                reach = dataPoint['values'][0]["value"]
            elif dataPoint['name'] == "saved":
                saves = dataPoint['values'][0]["value"]
        

        #####VIDEO POSTS########
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
                totalInteractions = dataPoint['values'][0]["value"]


        #####CAROUSEL POSTS#####
        for dataPoint in insights['data']:
            if dataPoint['name'] == "carousel_album_engagement":
                carouselEngagement = dataPoint['values'][0]["value"]
            elif dataPoint['name'] == "carousel_album_impressions":
                carouselImpressions = dataPoint['values'][0]["value"]
            elif dataPoint['name'] == "carousel_album_reach":
                carouselReach = dataPoint['values'][0]["value"]
            elif dataPoint['name'] == "carousel_album_saved":
                carouselSaves = dataPoint['values'][0]["value"]
            else:
                pass

        """




#    csvImageCells = (timestamp,thumbnail,permalink,caption,type,engagement,followers,impressions,reach,likes,comments,saves,videoViews)
#    csvReelCells = (timestamp,thumbnail,permalink,caption,type,total_interactions,followers,plays,reach,likes,comments,saves,shares)






        
    """ This writes individual to JSON file (doesn't add them all)
        jsonFile = "/Users/davidwills/Dropbox/_New File Structure/Files/1) Coding/1) Projects/Python/Instagram Graph API/insights.json"
        with open(jsonFile, "w") as outfile:
            json.dump(insights, outfile, indent=2)
        """

        
        
    









    """
        print("\n")
        print(json.loads(postInfo.text))
        print("\n")

        


        #full_insights_url = "https://graph.facebook.com/{}/insights?metric=comments&period=day&access_token=EAAHHfZCdfvGcBALle96LVO0zPfE0qwIl8Je9xnLHzd30wMI7OgO5pD57y409dWbfecP5tZBYNy2DwGU5xHQB7bpey2Mv9c8OMlJOOQztTFKZA1r5jYEYJBYU0PIz72KIBVkTTarCJ8fGfYGwSKrHAaVY4nlZBqQ4xayvpXHtGAZDZD"
        
        insights = requests.get(insights_url, insights_payload)
        if "error" in json.loads(insights.text):

            pass
        else:
            print(json.loads(insights.text))
    """
        


        
pullData()


"""
print("\nTestinig\n")
test = requests.get("https://graph.facebook.com/17851565306798151/insights?metric=likes&period=day&access_token=EAAHHfZCdfvGcBALle96LVO0zPfE0qwIl8Je9xnLHzd30wMI7OgO5pD57y409dWbfecP5tZBYNy2DwGU5xHQB7bpey2Mv9c8OMlJOOQztTFKZA1r5jYEYJBYU0PIz72KIBVkTTarCJ8fGfYGwSKrHAaVY4nlZBqQ4xayvpXHtGAZDZD")
print(test)
test_json = json.loads(test.text)
print(test_json)

"""

"""
    post_url = "https://graph.facebook.com/v14.0/{}/insights".format(media_id)
    payload = {
        "image_url": image_url,
        "caption": "This is a caption",
        "access_token": config.instsagram_access_token
    }

    r = requests.post(post_url, data = img_payload)
    print(r.text)

    
    result = json.loads(r.text)
    if 'id' in result:


"""


"""
                creation_id = result['id']

        second_post_url = "https://graph.facebook.com/v14.0/{}}/media_publish".format(config.ig_user_id)
        second_post_payload = {
            "creation_id": creation_id,
            "access_token": config.instagram_access_token
        }
        p = requests.post(second_post_url, data = second_post_payload)
        print(p)
"""


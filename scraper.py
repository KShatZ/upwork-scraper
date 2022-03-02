import json
import datetime
import requests
import os
import ssl
import functions as function
from slack import WebClient
from slack.errors import SlackApiError
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

# JSON for each RSS Feed
with open("time.json") as f:
    jsonFile    = json.load(f)
    jsJSON      = jsonFile["jsLastTime"]
    phpJSON     = jsonFile["phpLastTime"]
    vueJSON     = jsonFile["vueLastTime"]
    reactJSON   = jsonFile["reactLastTime"]
    laravelJSON = jsonFile["laravelLastTime"]
    angularJSON = jsonFile["angularLastTime"]

# Soups for each RSS Feed
php         = function.getSoup("https://www.upwork.com/ab/feed/topics/rss?securityToken=aac8bc33a4022dd757438311fa4125b2342a4655a4c094a3e44a66aa651c3f82b587b574a888f824d09cb3fc0de60145eb13f423c8066618733bec09d1796399&userUid=1142251170251407360&orgUid=1142251170255601665&sort=local_jobs_on_top&topic=4768890")
vue         = function.getSoup("https://www.upwork.com/ab/feed/topics/rss?securityToken=aac8bc33a4022dd757438311fa4125b2342a4655a4c094a3e44a66aa651c3f82b587b574a888f824d09cb3fc0de60145eb13f423c8066618733bec09d1796399&userUid=1142251170251407360&orgUid=1142251170255601665&sort=local_jobs_on_top&topic=4768894")
react       = "Nothing Yet"
laravel     = function.getSoup("https://www.upwork.com/ab/feed/topics/rss?securityToken=aac8bc33a4022dd757438311fa4125b2342a4655a4c094a3e44a66aa651c3f82b587b574a888f824d09cb3fc0de60145eb13f423c8066618733bec09d1796399&userUid=1142251170251407360&orgUid=1142251170255601665&sort=local_jobs_on_top&topic=4768889")
angular     = function.getSoup("https://www.upwork.com/ab/feed/topics/rss?securityToken=aac8bc33a4022dd757438311fa4125b2342a4655a4c094a3e44a66aa651c3f82b587b574a888f824d09cb3fc0de60145eb13f423c8066618733bec09d1796399&userUid=1142251170251407360&orgUid=1142251170255601665&sort=local_jobs_on_top&topic=4768893")
javascript  = function.getSoup("https://www.upwork.com/ab/feed/topics/rss?securityToken=aac8bc33a4022dd757438311fa4125b2342a4655a4c094a3e44a66aa651c3f82b587b574a888f824d09cb3fc0de60145eb13f423c8066618733bec09d1796399&userUid=1142251170251407360&orgUid=1142251170255601665&sort=local_jobs_on_top&topic=4768891")

# Lists to hold the tag values for each RSS Feed
rssTime         = []
rssTitle        = []
rssLink         = []
rssBudget       = []
rssDescription  = []

# Bools for whether or not message needs to be sent. Default is FALSE.
sendBools = {
    "php":          False,
    "vue":          False,
    "react":        False,
    "laravel":      False,
    "angular":      False,
    "javascript":   False
}

# How many new jobs were posted and need to be sent. Defualt is ZERO.
sendCount = {
    "php":          0,
    "vue":          0,
    "react":        0,
    "laravel":      0,
    "angular":      0,
    "javascript":   0
}

# Checks if most recent job post time is later then time stored in JSON. And if true, then checks how many new jobs there actually is. #
client = WebClient(token= os.environ.get("slack-token")) #WILL NEED TO CHANGE THIS TO MORE SECURE METHOD

# PHP
rssTime = function.rssPubDate(php)
if(function.compareTime(phpJSON, rssTime[0])):
    sendBools["php"] = True
    sendCount["php"] += 1

    i = 1
    while (function.compareTime(phpJSON, rssTime[i])): # Getting the amount of new jobs posted
        sendCount["php"] += 1
        i += 1
        if(i == 30):
            break

    rssTitle = function.rssTitle(php) # Getting Project Titles
    rssLink  = function.rssLink(php)  # Getting Project Links
    msgTitle = "PHP - New Job Posted"
    
    function.sendSlack(client, sendCount["php"], rssTitle, rssLink, msgTitle)

    with open("time.json", "r+") as f:
        jsonFile = json.load(f)
        jsonFile["phpLastTime"] = rssTime[0]
        f.truncate(0)
        f.seek(0)
        json.dump(jsonFile, f)

# JavaScript
rssTime = function.rssPubDate(javascript)
if(function.compareTime(jsJSON, rssTime[0])):
    sendBools["javascript"] = True
    sendCount["javascript"] += 1

    i = 1
    while (function.compareTime(jsJSON, rssTime[i])):
        sendCount["javascript"] += 1
        i += 1
        if(i == 30):
            break

    rssTitle = function.rssTitle(javascript) # Getting Project Titles
    rssLink  = function.rssLink(javascript)  # Getting Project Links
    msgTitle = "Javascript - New Job Posted"
    
    function.sendSlack(client, sendCount["javascript"], rssTitle, rssLink, msgTitle)

    with open("time.json", "r+") as f:
        jsonFile = json.load(f)
        jsonFile["jsLastTime"] = rssTime[0]
        f.truncate(0)
        f.seek(0)
        json.dump(jsonFile, f)

# Laravel
rssTime = function.rssPubDate(laravel)
if(function.compareTime(laravelJSON, rssTime[0])):
    sendBools["laravel"] = True
    sendCount["laravel"] += 1

    i = 1
    while (function.compareTime(laravelJSON, rssTime[i])):
        sendCount["laravel"] += 1
        i += 1
        if(i == 30):
            break

    rssTitle = function.rssTitle(laravel) # Getting Project Titles
    rssLink  = function.rssLink(laravel)  # Getting Project Links
    msgTitle = "Laravel - New Job Posted"
    
    function.sendSlack(client, sendCount["laravel"], rssTitle, rssLink, msgTitle)

    with open("time.json", "r+") as f:
        jsonFile = json.load(f)
        jsonFile["laravelLastTime"] = rssTime[0]
        f.truncate(0)
        f.seek(0)
        json.dump(jsonFile, f)

    
# React
# rssTime = function.rssPubDcate(react)
# if(function.compareTime(reactJSON, rssTime[0])):
#     sendBools["react"] = True
#     sendCount["react"] += 1

#     i = 1
#     while (function.compareTime(reactJSON, rssTime[i])):
#         sendCount["react"] += 1
#         i += 1
#         if(i == 30):
#             break
    
#     rssTitle = function.rssTitle(react) # Getting Project Titles
#     rssLink  = function.rssLink(react)  # Getting Project Links
#     msgTitle = "React - New Job Posted"
    
#     function.sendSlack(client, sendCount["react"], rssTitle, rssLink, msgTitle)

#     with open("time.json", "r+") as f:
#         jsonFile = json.load(f)
#         jsonFile["reactLastTime"] = rssTime[0]
#         f.truncate(0)
#         f.seek(0)
#         json.dump(jsonFile, f)


# Vue
rssTime = function.rssPubDate(vue)
if(function.compareTime(vueJSON, rssTime[0])):
    sendBools["vue"] = True
    sendCount["vue"] += 1

    i = 1
    while (function.compareTime(vueJSON, rssTime[i])):
        sendCount["vue"] += 1
        i += 1
        if(i == 30):
            break
    
    rssTitle = function.rssTitle(vue) # Getting Project Titles
    rssLink  = function.rssLink(vue)  # Getting Project Links
    msgTitle = "Vue - New Job Posted"
    
    function.sendSlack(client, sendCount["vue"], rssTitle, rssLink, msgTitle)

    with open("time.json", "r+") as f:
        jsonFile = json.load(f)
        jsonFile["vueLastTime"] = rssTime[0]
        f.truncate(0)
        f.seek(0)
        json.dump(jsonFile, f)


# Angular
rssTime = function.rssPubDate(angular)
if(function.compareTime(angularJSON, rssTime[0])):
    sendBools["angular"] = True
    sendCount["angular"] += 1

    i = 1
    while (function.compareTime(angularJSON, rssTime[i])):
        sendCount["angular"] += 1
        i += 1
        if(i == 30):
            break

    rssTitle = function.rssTitle(angular) # Getting Project Titles
    rssLink  = function.rssLink(angular)  # Getting Project Links
    msgTitle = "Angular - New Job Posted"
    
    function.sendSlack(client, sendCount["angular"], rssTitle, rssLink, msgTitle)

    with open("time.json", "r+") as f:
        jsonFile = json.load(f)
        jsonFile["angularLastTime"] = rssTime[0]
        f.truncate(0)
        f.seek(0)
        json.dump(jsonFile, f)
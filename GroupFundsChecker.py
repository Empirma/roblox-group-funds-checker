import requests
import time

# Getting cookies
cookiesFile = open("cookies.txt", "r")
lnumber = 1
for cookie in cookiesFile:
    # Setting cookie
    r = requests.Session()
    r.cookies[".ROBLOSECURITY"] = cookie.rstrip("\n")

    # Checking if cookie is valid
    checkCookie = r.get("https://users.roblox.com/v1/users/authenticated")
    if checkCookie.status_code == 401:
        print("Invalid cookie in line number:", lnumber)
        lnumber += 1
    else:
        lnumber += 1
        # Getting userid
        getUserInfo = r.get("https://users.roblox.com/v1/users/authenticated").json()
        userName, userID = getUserInfo['name'], getUserInfo['id']
        print("Username:", userName, "User ID:", userID); print("")

        # Getting groups
        groupsTbl = r.get(f"https://groups.roblox.com/v1/users/{userID}/groups/roles").json()

        # Print formatting
        print("Funds \t Group ID \t Group Name"); print("-------------------------------------")

        # Robux amount
        robuxTotal = 0

        # Running through groups
        rateLimited = []
        for i in groupsTbl['data']:
            groupID, groupName = i['group']['id'], i['group']['name']
            if i['role']['rank'] == 255:
                checkFunds = r.get(f"https://economy.roblox.com/v1/groups/{groupID}/currency")
                if checkFunds.status_code == 200:
                    print(f"{checkFunds.json()['robux']:<9}{groupID}\t {groupName}")
                    robuxTotal += checkFunds.json()['robux']
                elif checkFunds.status_code == 429:
                    print(f"{'WAIT':<9}{'RATELIMITED':<9}\t WAIT")
                    rateLimited.append({"id": groupID, "name": groupName})
                    time.sleep(30)

        # Getting funds of groups that weren't checked due to ratelimit
        for i in rateLimited:
            checkFunds = r.get(f"https://economy.roblox.com/v1/groups/{i['id']}/currency")
            if checkFunds.status_code == 200:
                print(f"{checkFunds.json()['robux']:<9}{i['id']}\t {i['name']}")
                robuxTotal += checkFunds.json()['robux']
                rateLimited.remove(i)
            elif checkFunds.status_code == 429:
                print(f"{'0':<9}{'0':<9}\t RATELIMITED")
                rateLimited.append(i)
                time.sleep(30)

        # Printing total amount of robux
        print(f"Total amount of Robux is: {robuxTotal}")

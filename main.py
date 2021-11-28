import API.Presence
import argparse
import math
import time
from pypresence import Presence

parser = argparse.ArgumentParser()

parser.add_argument("-u", "--user", type=int, help = "User ID", required=True)
parser.add_argument("-r", "--refresh", type=int, default=20, help = "Refresh period")
parser.add_argument("-o", "--online", type=bool, default=False, help = "Show when you are just Online")
parser.add_argument("-s", "--security", type=str, default="", help = "A .ROBLOSECURITY token, necessary for the API to gather game info for some players")
 
args = parser.parse_args()

ClientID = 874664899035402283
UserID = args.user
ShowOnline = args.online
RefreshPeriod = args.refresh
RobloSecurity = args.security

ThisPresence = API.Presence.PresenceAPI(roblosecurity = RobloSecurity)

RPC = Presence(ClientID, pipe=0)

Connected = False
StartTime = 0

def Connect():
    global Connected
    if Connected == False:
        Connected = True
        RPC.connect()
        return True
    return False
def Disconnect():
    global Connected
    global StartTime
    if Connected == True:
        StartTime = 0
        Connected = False
        RPC.close()
        return True
    return False

print("Started!")

while True:
    CurrentPresence = ThisPresence.GetUserPresence(UserID)
    GameName = CurrentPresence["lastLocation"]
    RootPlaceID = CurrentPresence["rootPlaceId"]
    if GameName == None or GameName == "":
        GameName = ""

    Buttons = [
        {"label": "Profile", "url": "https://www.roblox.com/users/" + str(UserID) + "/profile"}
    ]
    if RootPlaceID  != "" and RootPlaceID != None:
        Buttons.append({"label": "Experience", "url": "https://www.roblox.com/games/" + str(RootPlaceID)})
    
    if CurrentPresence["userPresenceType"] == 1 and ShowOnline == True:
        if StartTime == 0:
            StartTime = math.floor(time.time())
        if Connect() == True:
            print("User went Online!")
        if GameName != "":
            RPC.update(state=GameName, details="Online", large_image="player", small_image="online", start=StartTime, buttons=Buttons)
        else:
            RPC.update(details="Online", large_image="player", small_image="online", start=StartTime, buttons=Buttons)
    elif CurrentPresence["userPresenceType"] == 2:
        if StartTime == 0:
            StartTime = math.floor(time.time())
        if Connect() == True:
            print("User opened the Player!")
        
        if GameName != "":
            RPC.update(state=GameName, details="Playing", large_image="player", small_image="playing", start=StartTime, buttons=Buttons)
        else:
            RPC.update(details="Playing", large_image="player", small_image="playing", start=StartTime, buttons=Buttons)
    elif CurrentPresence["userPresenceType"] == 3:
        if StartTime == 0:
            StartTime = math.floor(time.time())
        if Connect() == True:
            print("User opened Studio!")
        
        if GameName != "":
            RPC.update(state=GameName, details="Building", large_image="studio", small_image="building", start=StartTime, buttons=Buttons)
        else:
            RPC.update(details="Building", large_image="studio", small_image="building", start=StartTime, buttons=Buttons)
    else:
        if Disconnect() == True:
            print("User went Offline!")
    
    time.sleep(RefreshPeriod)
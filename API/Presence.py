import requests

APIURL = "https://presence.roblox.com/v1/presence/"

class PresenceAPI:
    def __init__(self, roblosecurity = ""):
        self.roblosecurity = roblosecurity
    
    def GetUsersPresence(self, UserIDs):
        Response = requests.post(APIURL + "users", data = {'userIds': UserIDs}, cookies={".ROBLOSECURITY" : self.roblosecurity})
        ResponseJSON = Response.json()
        UserPresences = {}
        for User in ResponseJSON["userPresences"]:
            UserPresences[User["userId"]] = User
        
        return UserPresences
    
    def GetUserPresence(self, UserID):
        return self.GetUsersPresence([UserID])[UserID]
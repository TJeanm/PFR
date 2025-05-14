import time
import urllib.request
import numpy as np
import cv2

URL = "http://172.20.10.2:8000/snapshot.jpg"

while True:
    # Récupère les octets de l'image
    resp = urllib.request.urlopen(URL + "?" + str(int(time.time())))
    data = resp.read()
    # Décode en image OpenCV
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    # Votre traitement ici :
    # result = process(img)
    cv2.imshow("Snapshot 1 FPS", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(1)

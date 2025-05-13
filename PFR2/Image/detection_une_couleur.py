import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv

# Fonction pour détecter la couleur dominante
def detect_color(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Dictionnaire des plages
    color_ranges = {
        "Bleu": ([100, 150, 50], [140, 255, 255]),
        "Jaune": ([20, 150, 150], [40, 255, 255]),
        "Orange": ([5, 150, 150], [15, 255, 255])
    }

    max_pixels = 0
    detected_color = "Non détecté"
    final_mask = None

    for color, (lower, upper) in color_ranges.items():
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        pixel_count = np.count_nonzero(mask)

        if pixel_count > max_pixels:
            max_pixels = pixel_count
            detected_color = color
            final_mask = mask

    return detected_color, final_mask

# Fonction pour détecter la forme et la position
def detect_shape_and_position(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 300:
            continue

        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        M = cv2.moments(contour)

        if M["m00"] == 0:
            continue
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        if len(approx) == 3:
            shape = "Triangle"
        elif len(approx) == 4:
            side_lengths = [cv2.norm(approx[i] - approx[(i + 1) % 4]) for i in range(4)]
            shape = "Carre" if max(side_lengths) - min(side_lengths) < 10 else "Rectangle"
        elif len(approx) > 4:
            shape = "Cercle"
        else:
            shape = "Non détecté"

        return shape, (cx, cy)

    # Vérifie les cercles avec Hough
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 30, param1=50, param2=30, minRadius=10, maxRadius=100)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        x, y, _ = circles[0][0]
        return "Cercle", (x, y)

    return "Non détecté", (None, None)

# Chemin de l’image
image_path = 'asss.png'
img_capture = cv2.imread(image_path)

if img_capture is None:
    print("Erreur : Impossible de charger l'image.")
    exit()

# Détection
shape, position = detect_shape_and_position(img_capture)
color, _ = detect_color(img_capture)

x, y = position
print(f"Forme détectée : {shape}")
print(f"Couleur détectée : {color}")
print(f"Position : ({x}, {y})")

# Annoter l’image
cv2.putText(img_capture, f"Forme: {shape}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
cv2.putText(img_capture, f"Couleur: {color}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
if x is not None and y is not None:
    cv2.putText(img_capture, f"Position: ({x}, {y})", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.circle(img_capture, (x, y), 5, (0, 0, 255), -1)  # Marqueur rouge sur le centre

# Enregistrer dans un fichier CSV
csv_filename = "resultat_forme_couleur_position.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Forme", "Couleur", "X", "Y"])
    writer.writerow([shape, color, x, y])

print(f"Résultat enregistré dans {csv_filename}")

# Affichage
plt.imshow(cv2.cvtColor(img_capture, cv2.COLOR_BGR2RGB))
plt.title("Détection complète")
plt.axis("off")
plt.show()

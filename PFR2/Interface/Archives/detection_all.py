import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv  

image_path = 'Casse_Noisette/photo_test/6_balle_jaune.jpg'
csv_filename = 'Casse_Noisette/detection_all.csv'


COLOR_RANGES = {
    "Bleu": ([100, 150, 50], [140, 255, 255]),
    "Jaune": ([20, 150, 150], [40, 255, 255]),
    "Orange": ([5, 150, 150], [15, 255, 255]),
    "Rose": ([160, 100, 100], [179, 255, 255])
}

# Fonction de détection de la forme
def detect_shape_from_contour(contour):
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    num_vertices = len(approx)

    if num_vertices == 3:
        return "Triangle"
    elif num_vertices == 4:
        side_lengths = [cv2.norm(approx[i] - approx[(i + 1) % 4]) for i in range(4)]
        if max(side_lengths) - min(side_lengths) < 10:
            return "Carre"
        else:
            return "Rectangle"
    elif num_vertices > 4:
        return "Cercle"
    return "Non détecté"

# Fonction principale de détection
def detect_objects(image):
    results = []
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    for color_name, (lower, upper) in COLOR_RANGES.items():
        lower_np = np.array(lower)
        upper_np = np.array(upper)
        mask = cv2.inRange(hsv, lower_np, upper_np)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))  # Nettoyage

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 300:
                continue

            shape = detect_shape_from_contour(cnt)
            M = cv2.moments(cnt)
            if M["m00"] == 0:
                continue
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # ✅ Tracer un contour qui suit mieux la forme réelle
            epsilon = 0.02 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)

            text = f"{shape}, {color_name}"
            cv2.putText(image, text, (cx - 50, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            results.append((shape, color_name, (cx, cy)))
    return results

# Chargement de l’image
image_path = 'M.png'
img_capture = cv2.imread(image_path)
if img_capture is None:
    print("Erreur : Impossible de charger l'image.")
    exit()

# Détection des objets
results = detect_objects(img_capture)

# Résumé console
if results:
    for idx, (shape, color, pos) in enumerate(results, 1):
        print(f"Objet {idx} : Forme = {shape}, Couleur = {color}, Position = {pos}")
else:
    print("Aucun objet détecté.")


csv_filename = 'resultats_detection.csv'
with open(csv_filename, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Forme', 'Couleur', 'X', 'Y'])  
    for shape, color, (x, y) in results:
        writer.writerow([shape, color, x, y])

print(f"Résultats enregistrés dans : {csv_filename}")


plt.imshow(cv2.cvtColor(img_capture, cv2.COLOR_BGR2RGB))
plt.title("Contours ajustés aux formes")
plt.axis("off")
plt.show()

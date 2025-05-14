import socket
import pickle
from scipy.optimize import minimize
import numpy as np
from scipy.ndimage import rotate
import cv2
from scipy.spatial import KDTree
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 9999))
sock.settimeout(5.0)  # max 5 sec d’attente

def add_to_map(grid, points, resolution, center):
    for x, y in points:
        xi = int(center[0] + x / resolution)
        yi = int(center[1] + y / resolution)
        if 0 <= xi < grid.shape[1] and 0 <= yi < grid.shape[0]:
            grid[yi, xi] = 255

def polar_to_cartesian(scan):
    points = []
    for _, angle, distance in scan:
        if distance == 0:
            continue
        radians = np.radians(angle)
        x = (distance / 1000.0) * np.cos(radians)
        y = (distance / 1000.0) * np.sin(radians)
        points.append([x, y])
    return np.array(points)

def center_points_in_grid(pts, grid_shape, map_resolution, center_in_meters=(0, 0)):
    """
    Transforme des points en coordonnées (mètres) pour qu'ils soient centrés
    dans une grille d'occupation de taille `grid_shape`.

    - pts: (N, 2) array de points (x, y)
    - grid_shape: tuple (H, W)
    - map_resolution: mètres/pixel
    - center_in_meters: position du centre du robot en coordonnées réelles (par défaut (0,0))
    """
    H, W = grid_shape
    cx, cy = W // 2, H // 2  # centre en pixels de la grille

    # Décalage par rapport au centre (si le robot n’est pas en (0, 0))
    dx = center_in_meters[0] / map_resolution
    dy = center_in_meters[1] / map_resolution

    # Convertir les points en pixels et centrer dans la grille
    x_pixels = pts[:, 0] / map_resolution + cx - dx
    y_pixels = pts[:, 1] / map_resolution + cy - dy

    return np.stack([y_pixels, x_pixels], axis=1)

def build_grid_from_points(points, shape):
    """Efficiently create a binary grid from a list of (y, x) points."""
    grid = np.zeros(shape, dtype=np.uint8)
    points = points.astype(int)

    # Filtrage : garder uniquement les points valides
    valid = (points[:, 0] >= 0) & (points[:, 0] < shape[0]) & \
            (points[:, 1] >= 0) & (points[:, 1] < shape[1])
    points = points[valid]

    # Remplir la grille
    grid[points[:, 0], points[:, 1]] = 255
    return grid

def transform_points(points, angle, tx, ty):
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle),  np.cos(angle)]])
    T = np.array([tx, ty])
    return (points @ R.T) + T

def rotate_grid_fast(grid, angle):
    """
    Rotation rapide d'une grille binaire (uint8) sans interpolation.
    """
    return rotate(
        grid, angle,
        reshape=False,
        order=0,
        mode='constant',
        cval=0,
        prefilter=False
    ).astype(grid.dtype)

def find_best_rotation(grid_main, grid_temp, angle_range=(-30, 30), step=1, dx_range=(-20, 20), dy_range=(-20, 20), thresh = 80):
    best_score = -1
    best_angle = 0
    best_dx = 0
    best_dy = 0

    for angle in np.arange(angle_range[0], angle_range[1]+1, step):
        rotated = rotate_grid_fast(grid_temp, angle)

        for dx in range(dx_range[0], dx_range[1]+1):
            for dy in range(dy_range[0], dy_range[1]+1):
                shifted = np.roll(rotated, shift=(dy, dx), axis=(0, 1))

                overlap = np.logical_and(grid_main == 255, shifted == 255)
                score = overlap.sum()

                if score > best_score:
                    best_score = score
                    best_angle = angle
                    best_dx = dx
                    best_dy = dy
                if best_score>=thresh:
                    return best_angle, best_score, best_dx,best_dy


    return best_angle, best_score, best_dx,best_dy

def filter_by_min_distance(points, min_dist=1.0):
    """
    Supprime les points trop proches les uns des autres.
    """
    filtered = []
    for pt in points:
        if all(np.linalg.norm(pt - f) > min_dist for f in filtered):
            filtered.append(pt)
    return np.array(filtered)


def rotate_and_translate_grid(grid, angle_deg, dx, dy):
    """
    Applique une rotation puis une translation sur une carte binaire.
    
    - grid : image 2D numpy (0-255)
    - angle_deg : angle de rotation en degrés
    - dx, dy : translation (en pixels)
    
    Retourne la nouvelle carte transformée.
    """
    dx = -dx
    dy = -dy
    h, w = grid.shape
    center = (w // 2, h // 2)

    # 1. Rotation autour du centre
    M_rot = cv2.getRotationMatrix2D(center, angle_deg, 1.0)
    rotated = cv2.warpAffine(grid, M_rot, (w, h), flags=cv2.INTER_NEAREST)

    # 2. Translation
    M_trans = np.float32([[1, 0, dx], [0, 1, dy]])
    translated = cv2.warpAffine(rotated, M_trans, (w, h), flags=cv2.INTER_NEAREST)

    return translated

def compute_overlap(grid1, grid2):
    """
    Retourne le nombre de pixels où grid1 et grid2 sont tous deux à 255.
    """
    return np.logical_and(grid1 == 255, grid2 == 255).sum()

def extract_points_from_grid(grid):
    """Extract (y, x) positions of non-zero points from the grid."""
    return np.column_stack(np.nonzero(grid))
    
def registration_error(params, source, target):
    angle, tx, ty = params
    transformed = transform_points(source, angle, tx, ty)
    tree = KDTree(target)
    dists, _ = tree.query(transformed)
    return np.mean(dists)
def recv_all(sock, length):
    """Reçoit exactement 'length' octets depuis un socket TCP."""
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError("Connexion interrompue avant réception complète.")
        data += more
    return data

# --- Boucle principale ---
MAP_SIZE_PIXELS = 500
MAP_RESOLUTION = 0.02  # m/pixel (2 cm)
center = (MAP_SIZE_PIXELS // 2, MAP_SIZE_PIXELS // 2)

THRESH = 75
started = False
ref_grid= np.zeros((MAP_SIZE_PIXELS, MAP_SIZE_PIXELS), dtype=np.uint8)
grid_main= np.zeros((MAP_SIZE_PIXELS, MAP_SIZE_PIXELS), dtype=np.uint8)
aligned_grid = np.zeros_like(grid_main)

black_cmap = ListedColormap(['white', 'black'])
green_cmap = ListedColormap(['white', 'green'])
blue_cmap = ListedColormap(['white', 'blue'])

IP_PC = '192.168.164.151'  # L'adresse IP de ton PC
PORT = 9999  # Le port à utiliser

MAX_TCP_SIZE = 65507  # Taille maximale pour un paquet TCP

# Créer un socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Lier le socket à l'adresse IP et au port
sock.bind((IP_PC, PORT))
sock.listen(1)  # Écouter les connexions entrantes

print("Serveur en attente de connexion...")

# Attendre qu'une connexion soit établie
client_socket, addr = sock.accept()  # Accepter la connexion du client
print(f"Connexion établie avec {addr}")

plt.ion()
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# Boucle pour recevoir les scans
try:
    while True:
        # Lire d'abord la taille (4 octets)
        raw_size = recv_all(client_socket, 4)
        msg_size = int.from_bytes(raw_size, byteorder='big')

        # Lire exactement msg_size octets ensuite
        data = recv_all(client_socket, msg_size)
        scan = pickle.loads(data)
        print("scan got")
        # Assurez-vous que scan est valide
        if scan:
            print("Scan reçu avec", len(scan), "points")
            
            # Traitement des données (ex. conversion en coordonnées cartesiennes, etc.)
            # ... (à adapter selon ton code existant)
            # Traiter les scans comme dans ton code original...
            print("Scan reçu avec", len(scan), "points")

            pts = polar_to_cartesian(scan)
            if (len(pts)<100):
                continue
            print(f"len pts = {len(pts)}")
            if (len(pts)<100):
                continue
            if not started and len(pts)>100:
                # 1er scan → initialisation de grid_main
                add_to_map(grid_main, pts, MAP_RESOLUTION, center)
                pts = center_points_in_grid(pts, grid_main.shape, MAP_RESOLUTION)

                add_to_map(grid_main, pts, MAP_RESOLUTION, center)
                main_pts = pts

                ref_grid = build_grid_from_points(pts, grid_main.shape)
                pts_ref = pts

                started = True
                continue
            pts = center_points_in_grid(pts, grid_main.shape, MAP_RESOLUTION)

            # 6. Re-construire la grille alignée
            aligned_grid = build_grid_from_points(pts, grid_main.shape)
            # chercher la meilleure rotation
            
            initial_guess = [0, 0, 0]  # angle, tx, ty

            result = minimize(registration_error, initial_guess, args=(pts, pts_ref))
            angle_opt, tx_opt, ty_opt = result.x
            aligned = transform_points(pts, angle_opt, tx_opt, ty_opt)


            aligned_grid = build_grid_from_points(aligned, grid_main.shape)

            angle, score, dx, dy = find_best_rotation(
                ref_grid, aligned_grid,
                angle_range=(-180, 180), step=2,
                dx_range = (-1,1), dy_range=(-1,1)
            )

            aligned_grid = rotate_and_translate_grid(aligned_grid, angle,dx,dy)

            overlap = np.logical_and(ref_grid == 255, aligned_grid == 255)
            score_final = overlap.sum()
            print(f"score_final= {score_final}")
            print(f"un scan avec un score en dessous de {THRESH} n'est pas pris en compte")
            print(f"dx = {dx}, dy = {dy}, angle = {angle}")
            if score_final >= THRESH:
                
                grid_main = (np.maximum(grid_main, aligned_grid))
                pts_end = extract_points_from_grid(grid_main)
                pts_end = filter_by_min_distance(pts_end)
                grid_main = build_grid_from_points(pts_end, grid_main.shape)
                print("Map upgrated")
            else:
                print(f"Map not upgrated")

            # Afficher la carte principale (main map)
            ax1.set_title("Main Map")
            ax1.imshow(grid_main, cmap=black_cmap, origin='lower', interpolation='nearest')
            center_x, center_y = grid_main.shape[1] // 2, grid_main.shape[0] // 2
            zoom_size = 100
            ax1.set_xlim(center_x - zoom_size, center_x + zoom_size)
            ax1.set_ylim(center_y - zoom_size, center_y + zoom_size)
            ax1.axis("off")

            # Afficher la carte alignée
            ax2.set_title("Current Scan")
            ax2.imshow(aligned_grid, cmap=blue_cmap, origin='lower', interpolation='nearest')
            ax2.set_xlim(center_x - zoom_size, center_x + zoom_size)
            ax2.set_ylim(center_y - zoom_size, center_y + zoom_size)
            ax2.axis("off")

            plt.tight_layout()
            plt.pause(0.01)  # Très important pour rafraîchir l'affichage

except Exception as e:
    print("Erreur de réception des données:", e)

finally:
    print("Fermeture de la connexion...")
    client_socket.close()  # Fermer la connexion client
    sock.close()  # Fermer le socket du serveur


from rplidar import RPLidar
import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, radians
from scipy.spatial import KDTree
from skimage import transform, registration
from scipy.ndimage import rotate
import cv2
from numpy.fft import fft2, ifft2, fftshift
import math
from scipy.signal import correlate2d
import socket
import pickle
ROTATION_THRESHOLD = 5  # Seuil de détection de rotation en degrés
DISTANCE_THRESHOLD = 1.0  # Seuil de distance pour filtrer les points (en mètres)
ALIGNMENT_SCORE_THRESHOLD = 50  # Seuil pour la fusion des cartes (nombre minimum de points alignés)

def rotate_points(points, angle_deg):
    angle_rad = np.radians(angle_deg)
    rot_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad),  np.cos(angle_rad)]
    ])
    return points @ rot_matrix.T

def phase_correlation(a, b):
    A = fft2(a)
    B = fft2(b)
    R = A * B.conj()
    R /= np.abs(R) + 1e-8  # évite division par zéro
    corr = fftshift(ifft2(R).real)
    max_corr = np.max(corr)
    return max_corr

def estimate_rotation_fft(grid1, grid2, angle_range=(0, 360), step=1):
    # Prémarques : Nous allons essayer de réduire les images à une taille plus petite et appliquer un lissage.
    # Redimensionner les grilles pour simplifier la recherche
    grid1_resized = np.resize(grid1, (grid1.shape[0] // 2, grid1.shape[1] // 2))
    grid2_resized = np.resize(grid2, (grid2.shape[0] // 2, grid2.shape[1] // 2))

    best_score = -np.inf
    best_angle = 0

    for angle in range(angle_range[0], angle_range[1] + 1, step):
        rotated = rotate(grid2_resized, angle=angle, reshape=False, order=1, mode='constant', cval=0)
        score = phase_correlation(grid1_resized, rotated)

        if score > best_score:
            best_score = score
            best_angle = angle

    return best_angle
# --- Fonction brute-force d'estimation d'angle ---
def estimate_rotation_bruteforce(curr_pts, ref_pts, angle_range=10, step=0.5):
    best_angle = 0
    min_error = float('inf')
    ref_tree = KDTree(ref_pts)

    for angle_deg in np.arange(-angle_range, angle_range + step, step):
        theta = radians(angle_deg)
        rot = np.array([
            [cos(theta), -sin(theta)],
            [sin(theta),  cos(theta)]
        ])
        rotated = (rot @ curr_pts.T).T
        dists, _ = ref_tree.query(rotated, k=1)
        error = np.mean(dists)

        if error < min_error:
            min_error = error
            best_angle = angle_deg

    return best_angle

def scan_to_points(scan):
    return np.array([
        [distance * cos(radians(angle)) / 1000.0,
         distance * sin(radians(angle)) / 1000.0]
        for (_, angle, distance) in scan if 100 < distance < 6000
    ])

def get_angles(scan):
    return np.array([
        angle
        for (_, angle, distance) in scan if 100 < distance < 6000
    ])

def is_rotating(scan_angles, prev_scan_angles):
    if prev_scan_angles is None or len(scan_angles) != len(prev_scan_angles):
        return False
    angle_diff = np.abs(scan_angles - prev_scan_angles)
    angle_diff = (angle_diff + 180) % 360 - 180  # gestion 0-360
    mean_change = np.mean(np.abs(angle_diff))
    return mean_change > ROTATION_THRESHOLD

def rotate_map(grid, angle_deg):
    return rotate(grid, angle=angle_deg, reshape=False, order=0, mode='constant', cval=0)

def add_to_map(grid, angles, distance):
    # Conversion polaire → cartésien
    radians = np.radians(angle)
    x = distance * np.cos(radians) / 1000.0  # mm → m
    y = distance * np.sin(radians) / 1000.0

    # Conversion en indices de carte
    xi = int(center[0] + x / MAP_RESOLUTION)
    yi = int(center[1] + y / MAP_RESOLUTION)

    if 0 <= xi < MAP_SIZE_PIXELS and 0 <= yi < MAP_SIZE_PIXELS:
        grid[yi, xi] = 255  # Obstacle

def insert_scan_into_grid(scan, grid, resolution, center):
    for (_, angle, distance) in scan:
        if distance == 0 or distance > 6000:
            continue
        x = (distance / 1000.0) * cos(radians(angle))
        y = (distance / 1000.0) * sin(radians(angle))

        xi = int(center[0] + x / resolution)
        yi = int(center[1] + y / resolution)

        if 0 <= xi < grid.shape[1] and 0 <= yi < grid.shape[0]:
            grid[yi, xi] = 255  # Marque un obstacle

def apply_transformation_to_points(points, transformation):
    """
    Applique la transformation (rotation + translation) à un ensemble de points.
    
    :param points: Points à transformer (Nx2)
    :param transformation: Matrice de transformation 4x4
    :return: Points transformés (Nx2)
    """
    # Ajouter une colonne de 1 pour homogénéiser les coordonnées (x, y) -> (x, y, 1)
    points_homogeneous = np.hstack((points, np.ones((points.shape[0], 1))))  # Convertir en Nx3
    
    # Appliquer la transformation à chaque point (produit matriciel)
    transformed_points_homogeneous = points_homogeneous @ transformation.T  # Transformation 4x4
    
    # Retirer la coordonnée homogène pour revenir à (x, y)
    return transformed_points_homogeneous[:, :2]  # On prend seulement x et y



def compute_alignment_score(grid, points, resolution, center, threshold):
    """
    Calcule le score d'alignement basé sur le nombre de points alignés entre le scan et la carte.
    
    :param grid: La carte initiale
    :param points: Les points à aligner
    :param resolution: Résolution de la carte (m/pixel)
    :param center: Centre de la carte (en pixels)
    :param threshold: Seuil de distance pour qu'un point soit considéré comme bien aligné
    :return: Le score d'alignement (nombre de points alignés)
    """
    score = 0
    for x, y in points:
        xi = int(center[0] + x / resolution)
        yi = int(center[1] + y / resolution)
        if 0 <= xi < grid.shape[1] and 0 <= yi < grid.shape[0]:
            if grid[yi, xi] == 255:  # Le point correspond à un obstacle sur la carte
                score += 1
    return score

def merge_maps(grid_main, grid_temp):
    """
    Fusionne les cartes en ajoutant les points du grid_temp à grid_main.
    
    :param grid_main: La carte principale
    :param grid_temp: La carte temporaire
    """
    grid_main = np.maximum(grid_main, grid_temp)  # Fusionner les cartes en prenant le maximum des valeurs
    return grid_main
def estimate_rotation_between_grids(grid1, grid2, angle_range=(-30, 30), step=1):
    best_angle = 0
    best_score = -np.inf

    for angle in range(angle_range[0], angle_range[1] + 1, step):
        rotated = rotate(grid2, angle=angle, reshape=False, order=0, mode='constant', cval=0)
        score = (grid1 * rotated).sum()  # produit scalaire (score de superposition)
        
        if score > best_score:
            best_score = score
            best_angle = angle

    return best_angle

def add_to_map(grid, points, resolution, center):
    for x, y in points:
        xi = int(center[0] + x / resolution)
        yi = int(center[1] + y / resolution)
        if 0 <= xi < grid.shape[1] and 0 <= yi < grid.shape[0]:
            grid[yi, xi] = 255
def apply_icp_transformation_with_open3d(points_2d, transformation_4x4):
    """
    Applique une transformation homogène 4x4 à un nuage de points 2D en utilisant Open3D.
    
    :param points_2d: np.ndarray de forme (N, 2)
    :param transformation_4x4: np.ndarray 4x4 (matrice de transformation ICP)
    :return: points transformés, np.ndarray de forme (N, 2)
    """
    # Convertir en PointCloud Open3D
    pcd = o3d.geometry.PointCloud()
    points_3d = np.hstack((points_2d, np.zeros((points_2d.shape[0], 1))))  # Ajouter z=0
    pcd.points = o3d.utility.Vector3dVector(points_3d)

    # Appliquer la transformation 4x4
    pcd.transform(transformation_4x4)

    # Récupérer les points transformés en 2D
    transformed_points = np.asarray(pcd.points)[:, :2]
    return transformed_points

# --- Paramètres ---
PORT = 'COM8'
MAP_SIZE = 800
RES = 0.02  # m/pixel
CENTER = MAP_SIZE // 2
N_ACCUM = 5  # Nombre de scans à accumuler avant traitement
ROTATION_THRESHOLD = 15  # Degrés, seuil de détection de rotation

# --- Initialisation ---


# --- Boucle principale ---
MAP_SIZE_PIXELS = 500
MAP_RESOLUTION = 0.02  # m/pixel (2 cm)

# Initialiser carte d’occupation
prev_grid= np.zeros((MAP_SIZE_PIXELS, MAP_SIZE_PIXELS), dtype=np.uint8)
grid_main= np.zeros((MAP_SIZE_PIXELS, MAP_SIZE_PIXELS), dtype=np.uint8)
grid_temp= np.zeros((MAP_SIZE_PIXELS, MAP_SIZE_PIXELS), dtype=np.uint8)
grid_ref= np.zeros((MAP_SIZE_PIXELS, MAP_SIZE_PIXELS), dtype=np.uint8)


grid = np.zeros((MAP_SIZE_PIXELS, MAP_SIZE_PIXELS), dtype=np.uint8)
center = (MAP_SIZE_PIXELS // 2, MAP_SIZE_PIXELS // 2)
started = False
print('Connexion au LiDAR...')

MAP_SIZE = 500
RES = 0.02
ROTATION_THRESHOLD = 5  # degré

main_grid = np.zeros((MAP_SIZE, MAP_SIZE), dtype=np.uint8)
temp_grid = np.zeros_like(main_grid)
aligned_grid = np.zeros_like(main_grid)
ref_grid = np.zeros_like(main_grid)
started = False
was_rotating = False
scan_ref_points = None
scan_prev_points = None



import open3d as o3d

def estimate_icp_angle(scan1_points, scan2_points):
    """
    Estime la rotation (et translation) entre deux ensembles de points 2D avec ICP.
    
    :param scan1_points: Nx2 numpy array (points de référence)
    :param scan2_points: Nx2 numpy array (points à aligner)
    :return: angle (en degrés), transformation matrix 4x4
    """
    # Créer nuages de points Open3D
    pcd1 = o3d.geometry.PointCloud()
    pcd2 = o3d.geometry.PointCloud()
    
    # Convertir points en 3D (ajouter une coordonnée z=0 pour utiliser Open3D)
    pcd1.points = o3d.utility.Vector3dVector(np.hstack((scan1_points, np.zeros((scan1_points.shape[0], 1)))))
    pcd2.points = o3d.utility.Vector3dVector(np.hstack((scan2_points, np.zeros((scan2_points.shape[0], 1)))))
    
    # Appliquer ICP (Point-to-Point)
    threshold = 0.5  # Distance max pour associer deux points (en m)
    reg_p2p = o3d.pipelines.registration.registration_icp(
        pcd2, pcd1, threshold, np.eye(4),
        o3d.pipelines.registration.TransformationEstimationPointToPoint())
    
    transformation = reg_p2p.transformation
    
    # Extraction de la rotation à partir de la matrice de transformation
    rotation_matrix = transformation[:2, :2]
    
    # Calcul de l'angle de rotation
    angle = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0]) * 180 / np.pi
    
    # Retourner l'angle et la matrice de transformation
    return angle, transformation
    
tour = False
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

def filter_points_by_angle_and_distance(points, prev_points, angle_threshold=ROTATION_THRESHOLD, distance_threshold=DISTANCE_THRESHOLD):
    """
    Filtre les nouveaux points en fonction de l'angle et de la distance par rapport aux points précédents.
    
    :param points: Points à filtrer
    :param prev_points: Points précédents (référence)
    :param angle_threshold: Seuil d'angle pour filtrer les rotations
    :param distance_threshold: Seuil de distance pour filtrer les points éloignés
    :return: Points filtrés
    """
    # Calculer l'angle entre les points précédents et actuels
    if prev_points is None:
        return points
    
    filtered_points = []
    for p1, p2 in zip(prev_points, points):
        distance = np.linalg.norm(p1 - p2)
        
        # Si la distance entre les points est trop grande, on ignore ce point
        if distance > distance_threshold:
            continue
        
        filtered_points.append(p2)
    
    return np.array(filtered_points)

ROTATION_THRESHOLD = 5  # degré
prev_points = None # Liste vide pour accumuler les points
i=0
def compute_overlap(grid1, grid2):
    """
    Retourne le nombre de pixels où grid1 et grid2 sont tous deux à 255.
    """
    return np.logical_and(grid1 == 255, grid2 == 255).sum()
def estimate_rotation_log_polar_skimage(grid_ref, grid_new):
    """
    Estime la rotation entre deux grilles 2D en utilisant FFT + log‑polaire + phase cross‑correlation.
    Ne nécessite pas cv2.

    :param grid_ref: np.ndarray, grille de référence (uint8 ou float)
    :param grid_new: np.ndarray, nouvelle grille à aligner
    :return: angle de rotation en degrés
    """
    # 1) Calculer le spectre de magnitude des deux images
    #    on utilise FFT pour passer dans le domaine fréquentiel
    def magnitude_spectrum(img):
        f = np.fft.fft2(img)
        fshift = np.fft.fftshift(f)
        return np.abs(fshift)

    mag1 = magnitude_spectrum(grid_ref.astype(float))
    mag2 = magnitude_spectrum(grid_new.astype(float))

    # 2) Convertir en coordonnées log‑polaire
    center = (mag1.shape[1] / 2, mag1.shape[0] / 2)
    # warp_polar avec scaling='log' produit la version log‑polaire
    log1 = transform.warp_polar(mag1, center=center, scaling='log')
    log2 = transform.warp_polar(mag2, center=center, scaling='log')

    # 3) Phase cross‑correlation pour détecter la translation entre log‑polaire
    shift, error, diffphase = registration.phase_cross_correlation(log1, log2)
    # shift est (dy, dx) dans le domaine log‑polaire. dx correspond à la rotation.
    dx = shift[1]

    # 4) Conversion du décalage en degrés
    #    un décalage de dx pixels → (dx / largeur) * 360 degrés
    angle = (dx * 360.0) / log1.shape[1]
    # normaliser dans [-180, +180]
    if angle > 180:
        angle -= 360
    elif angle < -180:
        angle += 360

    return angle
def estimate_rotation_log_polar(grid1, grid2):
    """
    Estime la rotation entre deux images/grilles 2D (numpy arrays) 
    en utilisant la transformation log-polaire + phase correlation.

    :param grid1: Référence (2D uint8)
    :param grid2: À aligner (2D uint8)
    :return: angle de rotation en degrés (float)
    """
    # 1) Convertir en float32
    img1 = grid1.astype(np.float32)
    img2 = grid2.astype(np.float32)

    # 2) Calculer leur spectre (magnitude du DFT)
    dft1 = cv2.dft(img1, flags=cv2.DFT_COMPLEX_OUTPUT)
    dft2 = cv2.dft(img2, flags=cv2.DFT_COMPLEX_OUTPUT)
    mag1 = cv2.magnitude(dft1[:,:,0], dft1[:,:,1])
    mag2 = cv2.magnitude(dft2[:,:,0], dft2[:,:,1])

    # 3) Se recentrer sur un log-polaire
    rows, cols = mag1.shape
    center = (cols/2, rows/2)
    # M = nombre de rangées / log(r_max)
    r_max = np.hypot(center[0], center[1])
    M = rows/np.log(r_max)
    logpol1 = cv2.logPolar(mag1, center, M, cv2.INTER_LINEAR+cv2.WARP_FILL_OUTLIERS)
    logpol2 = cv2.logPolar(mag2, center, M, cv2.INTER_LINEAR+cv2.WARP_FILL_OUTLIERS)

    # 4) Phase Correlation
    # La translation trouvée sur l’axe horizontal de logpol correspond à la rotation
    (dx, dy), response = cv2.phaseCorrelate(logpol1, logpol2)
    # On convertit dx (shift en colonnes) en degrés
    angle = 360.0 * dx / logpol1.shape[1]
    # Ajuster dans [-180,180]
    if angle > 180:
        angle -= 360
    elif angle < -180:
        angle += 360

    return angle
def compare_grids_similarity(grid1, grid2, threshold=128):
    """
    Compare deux grilles binaires et retourne un score de similarité.

    :param grid1: numpy array (grille 1)
    :param grid2: numpy array (grille 2)
    :param threshold: valeur pour considérer un pixel comme occupé
    :return: score (float entre 0 et 1), proportion de pixels similaires
    """
    # Binarisation : 1 si pixel occupé, 0 sinon
    bin1 = (grid1 >= threshold).astype(np.uint8)
    bin2 = (grid2 >= threshold).astype(np.uint8)

    # Intersection et union
    intersection = np.logical_and(bin1, bin2).sum()
    union = np.logical_or(bin1, bin2).sum()

    if union == 0:
        return 1.0 if intersection == 0 else 0.0

    similarity = intersection / union
    return similarity
def filter_points_by_map(rotated_pts, map_tree, dist_thresh, min_points):
    """
    Garde seulement les points de 'rotated_pts' qui sont à moins de 'dist_thresh'
    d'un obstacle existant dans la carte (indexé par map_tree).
    Si moins de 'min_points' passent le filtre, on retourne None pour indiquer
    qu'il faut ignorer ce scan.
    """
    if map_tree is None or len(rotated_pts) == 0:
        return None

    # Recherche du plus proche voisin pour chaque point
    dists, _ = map_tree.query(rotated_pts, k=1)
    mask = dists < dist_thresh
    filtered = rotated_pts[mask]

    if len(filtered) < min_points:
        return None
    return filtered

from scipy.spatial import cKDTree
from scipy.ndimage import distance_transform_edt
from skimage.transform import rotate
import numpy as np
from scipy.ndimage import rotate
import numpy as np

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
from scipy.spatial import KDTree
from sklearn.neighbors import NearestNeighbors
robot_position = np.array([grid_main.shape[1] // 2, grid_main.shape[0] // 2])
from scipy.spatial import distance_matrix
from sklearn.cluster import DBSCAN

def combine_close_points(grid, distance_thresh=3):
    # 1. Extraire les coordonnées des points actifs
    points = np.column_stack(np.nonzero(grid))  # [(y,x), ...]
    if len(points) == 0:
        return np.zeros_like(grid)

    # 2. Appliquer DBSCAN pour regrouper les points proches
    clustering = DBSCAN(eps=distance_thresh, min_samples=1).fit(points)
    labels = clustering.labels_

    # 3. Calculer les centroïdes de chaque groupe
    new_points = []
    for label in set(labels):
        group = points[labels == label]
        centroid = np.mean(group, axis=0).astype(int)
        new_points.append(centroid)

    # 4. Construire une nouvelle grille avec les points fusionnés
    new_grid = np.zeros_like(grid)
    for y, x in new_points:
        if 0 <= y < new_grid.shape[0] and 0 <= x < new_grid.shape[1]:
            new_grid[y, x] = 1

    return new_grid

# --- Helper functions ---

def extract_points_from_grid(grid):
    """Extract (y, x) positions of non-zero points from the grid."""
    return np.column_stack(np.nonzero(grid))

def find_correspondences(src_points, dst_points):
    """Find nearest neighbors from src to dst."""
    nbrs = NearestNeighbors(n_neighbors=1).fit(dst_points)
    distances, indices = nbrs.kneighbors(src_points)
    matched_src = src_points
    matched_dst = dst_points[indices[:, 0]]
    return matched_src, matched_dst, distances[:, 0]





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
def build_map_kdtree(grid, resolution, center):
    """
    Extrait les pixels occupés (==255) de la grille et construit un KD‑Tree
    en coordonnées métriques.
    """
    ys, xs = np.where(grid == 255)
    # Convertir en mètres centré
    pts = np.vstack([
        (xs - center[0]) * resolution,
        (ys - center[1]) * resolution
    ]).T
    if len(pts) == 0:
        return None

    return cKDTree(pts)
    
from sklearn.cluster import DBSCAN
from scipy.ndimage import binary_dilation, binary_erosion

def combine_close_points_from_list(points, distance_thresh=3):
    """
    Fusionne les points proches (en 2D) selon un seuil de distance.
    
    :param points: np.array of shape (N, 2)
    :param distance_thresh: distance max pour fusion
    :return: np.array des centroïdes
    """
    if len(points) == 0:
        return np.array([])

    clustering = DBSCAN(eps=distance_thresh, min_samples=1).fit(points)
    labels = clustering.labels_

    fused = []
    for label in set(labels):
        cluster = points[labels == label]
        centroid = np.mean(cluster, axis=0)
        fused.append(centroid)

    return np.array(fused)

from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import ListedColormap
def estimate_rigid_transform(src_pts, dst_pts):
    """
    Estimate 2D rigid transform (rotation + translation) using SVD.
    """
    src_mean = np.mean(src_pts, axis=0)
    dst_mean = np.mean(dst_pts, axis=0)

    src_centered = src_pts - src_mean
    dst_centered = dst_pts - dst_mean

    H = src_centered.T @ dst_centered
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T

    if np.linalg.det(R) < 0:
        Vt[1, :] *= -1
        R = Vt.T @ U.T

    t = dst_mean - R @ src_mean
    return R, t
prev_angle = 0
turned = False
black_cmap = ListedColormap(['white', 'black'])
green_cmap = ListedColormap(['white', 'green'])
blue_cmap = ListedColormap(['white', 'blue'])
grid_temp = np.zeros_like(grid_main)

aligned_grid = np.zeros_like(grid_main)

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
import numpy as np
from scipy.ndimage import binary_dilation, label

import numpy as np
from skimage.measure import label, regionprops
from scipy.spatial.distance import cdist

def remove_duplicated_lines_advanced(grid, distance_thresh=3, min_segment_length=5):
    """
    Supprime les doublons de lignes (ou traits proches) en fusionnant les segments
    qui sont à une distance donnée, tout en gardant les segments les plus représentatifs.

    - grid : np.array, la grille binaire avec 0 et 255.
    - distance_thresh : distance en pixels pour déterminer la proximité des segments.
    - min_segment_length : longueur minimale d'un segment pour qu'il soit conservé.
    """
    
    # Convertir la grille en points binaires
    points = np.argwhere(grid == 255)
    
    if len(points) == 0:
        return grid

    # Calculez toutes les paires de distances entre les points
    dist_matrix = cdist(points, points)
    
    # Créez un tableau pour marquer les segments à fusionner
    to_remove = np.zeros(len(points), dtype=bool)
    
    # Fusionner les points proches
    for i in range(len(points)):
        if to_remove[i]:
            continue  # Si ce point a déjà été fusionné, on passe
        for j in range(i + 1, len(points)):
            if to_remove[j]:
                continue
            if dist_matrix[i, j] <= distance_thresh:
                # Fusionner ces deux points, marquer l'un pour suppression
                to_remove[j] = True

    # Filtrer les points à garder
    remaining_points = points[~to_remove]

    # Recréer la grille sans les doublons
    cleaned_grid = np.zeros_like(grid)
    cleaned_grid[remaining_points[:, 0], remaining_points[:, 1]] = 255

    return cleaned_grid
def icp(src_pts, dst_pts, max_iterations=2000, tolerance=1e-7):
    """
    ICP classique : aligne src_pts (à transformer) vers dst_pts (fixes)
    """
    prev_error = float('inf')
    src = np.copy(src_pts)

    for i in range(max_iterations):
        # 1. Trouver les plus proches voisins
        tree = cKDTree(dst_pts)
        distances, indices = tree.query(src)

        matched_dst = dst_pts[indices]

        # 2. Estimer la meilleure transformation rigide
        R, t = estimate_rigid_transform(src, matched_dst)

        # 3. Appliquer la transformation
        src = transform_points(src, R, t)

        # 4. Vérifier la convergence
        mean_error = np.mean(distances)
        if abs(prev_error - mean_error) < tolerance:
            break
        prev_error = mean_error

    return R, t, src
def score_overlap(grid1, grid2):
    """
    Calcule un score de recouvrement entre deux grilles binaires (valeurs 0 ou 255).
    Le score est simplement le nombre de pixels communs (255 dans les deux grilles).
    """
    if grid1.shape != grid2.shape:
        raise ValueError("Les grilles doivent avoir la même taille.")

    intersection = np.logical_and(grid1 == 255, grid2 == 255)
    union = np.logical_or(grid1 == 255, grid2 == 255)

    # Exemple 1: score brut (nombre de pixels qui se recouvrent)
    score_raw = intersection.sum()

    # Exemple 2: IoU (Intersection over Union)
    score_iou = intersection.sum() / union.sum() if union.sum() != 0 else 0

    return score_iou
def clean_double_lines(grid, new_pts, radius=1):
    """
    Supprime les anciens traits autour des nouveaux points s'ils sont superposés
    (évite les doublons de traits causés par l'accumulation de scans).

    grid : carte binaire (uint8)
    new_pts : points du scan actuel (Nx2)
    radius : rayon autour du point pour vérifier et effacer
    """
    h, w = grid.shape

    for pt in new_pts.astype(int):
        y, x = pt
        if 0 <= y < h and 0 <= x < w:
            # Vérifie s’il y a déjà un ancien trait (valeurs 255) autour du point
            y_min = max(0, y - radius)
            y_max = min(h, y + radius + 1)
            x_min = max(0, x - radius)
            x_max = min(w, x + radius + 1)
            
            local_patch = grid[y_min:y_max, x_min:x_max]

            # S’il y a un ancien point (255) à proximité → on nettoie
            if np.any(local_patch == 255):
                grid[y_min:y_max, x_min:x_max] = 0
from scipy.optimize import minimize

def filter_by_min_distance(points, min_dist=1.0):
    """
    Supprime les points trop proches les uns des autres.
    """
    filtered = []
    for pt in points:
        if all(np.linalg.norm(pt - f) > min_dist for f in filtered):
            filtered.append(pt)
    return np.array(filtered)
def remove_parallel_lines_opencv(grid, min_dist=0, max_dist=1, angle_threshold=2):
    """
    Supprime les traits doublons (lignes parallèles proches) sur une carte binaire.
    
    - grid : numpy array 0-255 (image binaire)
    - min_dist / max_dist : intervalle de distance entre deux traits considérés comme doublons
    - angle_threshold : tolérance en degrés pour considérer deux lignes comme parallèles
    """
    # Assure que c'est binaire (au cas où)
    binary = (grid == 255).astype(np.uint8)

    # Détection de lignes avec Hough Transform
    lines = cv2.HoughLines(binary, rho=1, theta=np.pi / 180, threshold=50)
    
    if lines is None:
        return grid  # aucune ligne détectée

    lines = lines[:, 0, :]  # suppression d'une dimension inutile
    to_remove = []

    for i in range(len(lines)):
        rho1, theta1 = lines[i]
        for j in range(i + 1, len(lines)):
            rho2, theta2 = lines[j]

            # Vérifie si les angles sont similaires (donc lignes parallèles)
            angle_diff = np.abs(theta1 - theta2) * (180 / np.pi)
            if angle_diff < angle_threshold:
                dist = np.abs(rho1 - rho2)
                if min_dist <= dist <= max_dist:
                    # Marque la ligne la plus faible à supprimer
                    to_remove.append(i if abs(rho1) < abs(rho2) else j)

    # Crée un masque de suppression
    mask = np.ones_like(binary)

    for idx in set(to_remove):
        rho, theta = lines[idx]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(mask, (x1, y1), (x2, y2), 0, thickness=3)

    # Appliquer le masque pour supprimer les lignes sélectionnées
    cleaned = cv2.bitwise_and(binary, binary, mask=mask)
    return cleaned * 255  # remettre en 0 / 255

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

def transform_points(points, angle, tx, ty):
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle),  np.cos(angle)]])
    T = np.array([tx, ty])
    return (points @ R.T) + T
def registration_error(params, source, target):
    angle, tx, ty = params
    transformed = transform_points(source, angle, tx, ty)
    tree = KDTree(target)
    dists, _ = tree.query(transformed)
    return np.mean(dists)
prev_angle = 0
def clean_overlapping_points(grid, kernel_size=3, iterations=1):
    """
    Applique une érosion pour affiner les traits dans une carte binaire.
    
    Paramètres :
    - grid : numpy.ndarray (grille binaire 0/255)
    - kernel_size : taille du noyau pour l'érosion
    - iterations : nombre d'itérations d'érosion
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    eroded = cv2.erode(grid, kernel, iterations=iterations)
    return eroded
THRESH = 75


try:
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # Taille de la figure ajustable

    lidar = RPLidar(PORT, timeout=3)
    print("Connexion au LiDAR...")
    lidar.clear_input()
    main_cmap = ListedColormap(['white', 'black'])
    temp_cmap = ListedColormap(['white', 'red'])

    plt.ion()  # Mode interactif pour la mise à jour en temps réel

    l_angle = []
    l_score = []

    # … (tes imports et fonctions polar_to_cartesian, estimate_icp_angle, add_to_map, rotate_points) …
    map_tree = build_map_kdtree(grid_main, MAP_RESOLUTION, center)
    custom_cmap = LinearSegmentedColormap.from_list('white_to_black', ['white', 'black'])
    j = 0
    started = False
    for scan in lidar.iter_scans():
        pts = polar_to_cartesian(scan)
        if (len(pts)<100):
            continue
        print(f"len pts = {len(pts)}")
        if (len(pts)<200):
            continue
        if not started and len(pts)>200:
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
        print(f"angle teste = {angle}")

        prev_angle = angle


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

        grid_temp_rot = grid_temp

        # Left: grid_main
        plt.subplot(1, 2, 1)
        plt.title("Main Map")
        plt.imshow(grid_main, cmap=black_cmap, origin='lower', interpolation='nearest')
        plt.axis("off")
        plt.tight_layout()
        plt.pause(0.01)
        center_x, center_y = grid_main.shape[1] // 2, grid_main.shape[0] // 2
        zoom_size = 100
        plt.xlim(center_x - zoom_size, center_x + zoom_size)
        plt.ylim(center_y - zoom_size, center_y + zoom_size)
        plt.axis("off")
        # Right: grid_temp (aligned_grid)
        plt.subplot(1, 2, 2)
        plt.title("Current Scan")
        plt.imshow(aligned_grid, cmap=blue_cmap, origin='lower', interpolation='nearest')
        plt.axis("off")

        # Mise à jour de la visualisation

        plt.tight_layout()
        plt.pause(0.01)
        center_x, center_y = grid_main.shape[1] // 2, grid_main.shape[0] // 2
        zoom_size = 100
        plt.xlim(center_x - zoom_size, center_x + zoom_size)
        plt.ylim(center_y - zoom_size, center_y + zoom_size)
        plt.axis("off")
        plt.show()
        plt.pause(0.01)


except Exception as e:
    print(f"Erreur dans la connexion au LiDAR : {e}")
 
except KeyboardInterrupt:
    print("Interruption par l'utilisateur. Sortie du programme.")
    break  # Quitter la boucle et terminer proprement

finally:
    print("Fermeture du LiDAR.")
    try:
        lidar.stop()
        lidar.disconnect()
    except:
        pass
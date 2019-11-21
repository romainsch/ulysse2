""" Programme qui permet d'adapter la liste des waypoints voulues pour les levés à une liste de waypoints facile à suivre pour le robot Ulysse. """

from math import *
from scipy import signal
import pyproj

radius_waypoint = 3

def parse(file_name):
    """
    Extrait les différents waypoints de la mission à partir d'un fichier au format .waypoints.

    Parameters:
    file_name:
        string: chemin du fichier .waypoints
    Returns:
    WP:
        list: liste des waypoints
            i: index du waypoint
            lat: latitude du waypoint
            long: longitude du waypoint
    """
    f = open(file_name,'r+')
    L = f.readlines()
    WP = []
    for i in range(len(L)-1):
        l = L[i+1].split("\t")
        lat,long = float(l[8]),float(l[9])
        WP.append([i,lat,long])
    f.close()
    return(WP)

def cap(u):
    """
    Calcul le cap suivi à partir d'un vecteur.

    Parameters:
    u:
        tuple of float: direction suivi par le vecteur u
    Returns:
    cap:
        float: cap suivi par le vecteur u
    """
    lat1,lat2,long1,long2 = u[0],u[2],u[1],u[3]
    x = cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(long2-long1)
    y = sin(long2-long1)*cos(lat2)
    cap = atan2(y,x)
    return(cap)

def angle(u,v):
    """
    Calcul l'angle de giration suivi pour le passage d'une direction u à une direction v.

    Parameters:
    u,v:
        tuple of float: directions suivi avant et après changement de waypoint
    Returns:
    theta:
        float: angle de giration entre u et v
    """
    cap_1 = cap(u)
    cap_2 = cap(v)
    theta = (cap_2-cap_1)/(2*pi)*360
    if theta > 180:
        theta = theta - 360
    if theta < -180:
        theta = theta + 360
    return(theta)

def find_trajectory(WP):
    """
    Calcul le cap à chaque changement de waypoint. (Le premier et dernier waypoints sont exclus)

    Parameters:
    WP:
        list: liste des waypoints
            i: index du waypoint
            lat: latitude du waypoint
            long: longitude du waypoint
    Returns:
    Angle:
        list of float: liste des caps
    """
    Angle = []
    for i in range(len(WP)-2):
        u = (WP[i][1],WP[i][2],WP[i+1][1],WP[i+1][2])
        v = (WP[i+1][1],WP[i+1][2],WP[i+2][1],WP[i+2][2])
        theta = angle(u,v)
        Angle.append(theta)
    return(Angle)

def convert_GPS2L93(WP_GPS):
    """
    Convertit toutes les coordonnées des waypoints en entrée en coordonnées Lambert 93.

    Parameters:
    WP_GPS:
        list: liste des waypoints
            i: index du waypoint
            lat: latitude du waypoint
            long: longitude du waypoint
    Returns:
    WP_L93:
        list: liste des waypoints
            i: index du waypoint
            x: coordonnées horizontales du waypoint (L93)
            y: coordonnées verticales du waypoint (L93)
    """
    # Define a projection with Proj4 notation, in this case we focus on France, correspond to Lambert 93 projection
    isn2004=pyproj.Proj("+init=EPSG:2154")

    WP_L93 = []
    for wp in WP_GPS:
        lat,long = wp[1],wp[2]
        x,y = isn2004(lat,long)
        WP_L93.append([wp[0],x,y])

    return(WP_L93)

def giration(WP):
    """
    Crée des waypoints formant une giration pour placer le robot dans le bon cap avant une ligne d'acquisition.

    Parameters:
    WP:
        list: liste des waypoints
            i: index du waypoint
            lat: latitude du waypoint
            long: longitude du waypoint
    Returns:
    WP_giration:
        list: liste des waypoints
            i: index du waypoint
            lat: latitude du waypoint
            long: longitude du waypoint
    """
    WP_entree,WP_sortie = WP[1],WP[2]
    d = sqrt((WP_entree[1]-WP_sortie[1])**2+(WP_entree[2]-WP_sortie[2])**2) # ecart dans la giration entre deux WP
    r = d/2+radius_waypoint
    print(d)
    WP_giration = []
    return(WP_giration)

if __name__ == '__main__':
    file_name = "survey2.waypoints"
    waypoints = parse(file_name)
    waypoints_l93 = convert_GPS2L93(waypoints)
    angles = find_trajectory(waypoints)
    for i in range(len(angles)):
        print(i,angles[i])

    giration([waypoints_l93[1],waypoints_l93[3],waypoints_l93[4],waypoints_l93[4]])
import cv2
import numpy as np
import json
import math

def cubic_bezier_sample(p0, h0, h1, p1, n_samples=30):
    t = np.linspace(0, 1, n_samples)[:, None]
    return (1-t)**3 * p0 + 3*(1-t)**2 * t * h0 + 3*(1-t) * t**2 * h1 + t**3 * p1

def render_rive_polygon(points, shape_origin, canvas_size=(1024, 1024)):
    # points: list of dicts with x, y, cubic: {inRotation, inDistance, rotation, outDistance}
    n = len(points)
    sampled_curve = []
    sx, sy = shape_origin
    for i in range(n):
        p_curr = points[i]
        p_next = points[(i + 1) % n]
        
        p0 = np.array([sx + p_curr['x'], sy + p_curr['y']], dtype=float)
        p1 = np.array([sx + p_next['x'], sy + p_next['y']], dtype=float)
        
        # Outgoing handle from p_curr
        out_rot_rad = math.radians(p_curr['cubic']['rotation'])
        out_dist = p_curr['cubic']['outDistance']
        h0 = p0 + np.array([math.cos(out_rot_rad) * out_dist, math.sin(out_rot_rad) * out_dist])
        
        # Incoming handle to p_next
        in_rot_rad = math.radians(p_next['cubic']['inRotation'])
        in_dist = p_next['cubic']['inDistance']
        h1 = p1 + np.array([math.cos(in_rot_rad) * in_dist, math.sin(in_rot_rad) * in_dist])
        
        segment = cubic_bezier_sample(p0, h0, h1, p1, n_samples=25)
        sampled_curve.append(segment)
        
    all_pts = np.vstack(sampled_curve).astype(np.int32)
    canvas = np.zeros(canvas_size, dtype=np.uint8)
    cv2.fillPoly(canvas, [all_pts], 255)
    return canvas, all_pts

# Let's test with initial landmark-based points:
# Wing center at (224, 590)

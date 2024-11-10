# utils.py

import time
import bpy
import mathutils
from .constants import SCALE_FACTOR

def timeit(label):
    class Timer:
        def __init__(self, label):
            self.label = label
            self.start = None
            self.end = None
            self.duration = None

        def __enter__(self):
            self.start = time.perf_counter()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.end = time.perf_counter()
            self.duration = self.end - self.start
            print(f"[osu! Importer] {self.label}: {self.duration:.4f} Sekunden")

    return Timer(label)

def get_ms_per_frame():
    fps = bpy.context.scene.render.fps
    return 1000 / fps  # Milliseconds per frame

def create_collection(name):
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    return collection

def map_osu_to_blender(x, y):
    corrected_x = (x - 256) * SCALE_FACTOR  # Centering on zero
    corrected_y = 0
    corrected_z = (192 - y) * SCALE_FACTOR  # Invert and center
    return corrected_x, corrected_y, corrected_z

def evaluate_curve_at_t(curve_object, t):
    t = max(0.0, min(1.0, t))

    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_curve_object = curve_object.evaluated_get(depsgraph)
    eval_curve = eval_curve_object.data

    spline = eval_curve.splines[0]

    spline_length = spline.calc_length()

    desired_length = t * spline_length

    accumulated_length = 0.0

    points = []
    if spline.type == 'BEZIER':
        bezier_points = spline.bezier_points
        num_segments = len(bezier_points) - 1
        for i in range(num_segments):
            bp0 = bezier_points[i]
            bp1 = bezier_points[i + 1]

            p0 = bp0.co.xyz
            p1 = bp0.handle_right.xyz
            p2 = bp1.handle_left.xyz
            p3 = bp1.co.xyz

            segment_samples = 10  # Adjust for accuracy
            for j in range(segment_samples):
                s = j / segment_samples
                point = mathutils.geometry.interpolate_bezier(p0, p1, p2, p3, s)
                points.append(point)
    else:
        spline_points = spline.points
        points = [p.co.xyz for p in spline_points]

    for i in range(len(points) - 1):
        p0 = points[i]
        p1 = points[i + 1]
        segment_length = (p1 - p0).length
        if accumulated_length + segment_length >= desired_length:
            remaining_length = desired_length - accumulated_length
            local_t = remaining_length / segment_length
            position = p0.lerp(p1, local_t)
            return curve_object.matrix_world @ position
        accumulated_length += segment_length

    last_point = points[-1]
    return curve_object.matrix_world @ last_point
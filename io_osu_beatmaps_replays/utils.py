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

def create_collection(name):
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    return collection

def map_osu_to_blender(x, y):
    if not hasattr(map_osu_to_blender, 'cache'):
        map_osu_to_blender.cache = {}
    key = (x, y)
    if key in map_osu_to_blender.cache:
        return map_osu_to_blender.cache[key]
    corrected_x = (x - 256) * SCALE_FACTOR  # Centering on zero
    corrected_y = 0
    corrected_z = (192 - y) * SCALE_FACTOR  # Invert and center
    map_osu_to_blender.cache[key] = (corrected_x, corrected_y, corrected_z)
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

            segment_samples = 10
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

def get_keyframe_values(hitobject, object_type, import_type, start_frame, end_frame, early_start_frame, approach_rate,
                        osu_radius, extra_params=None, ms_per_frame=None, audio_lead_in_frames=None):
    frame_values = {}
    fixed_values = {}

    # Gemeinsame frame_values für alle Objekttypen
    frame_values["show"] = [
        (int(early_start_frame - 1), False),
        (int(early_start_frame), True),
    ]
    frame_values["was_hit"] = [
        (int(start_frame - 1), False),
        (int(start_frame), hitobject.was_hit)
    ]

    # Gemeinsame fixed_values für alle Objekttypen
    fixed_values["ar"] = approach_rate
    fixed_values["cs"] = osu_radius * SCALE_FACTOR * (2 if import_type == 'BASE' else 1)

    # Objekttyp-spezifische Anpassungen
    if object_type == 'circle':
        if import_type == 'FULL':
            frame_values["show"].append((int(start_frame + 1), False))
    elif object_type == 'slider':
        frame_values["show"].extend([
            (int(end_frame - 1), True),
            (int(end_frame), False)
        ])
        # Berechnung des Frames, an dem der Slider endet
        slider_end_frame = (hitobject.slider_end_time / ms_per_frame) + audio_lead_in_frames
        frame_values["was_completed"] = [
            (int(slider_end_frame - 1), False),
            (int(slider_end_frame), True)
        ]
        # Slider-spezifische fixed_values
        if extra_params:
            fixed_values.update(extra_params)
    elif object_type == 'spinner':
        frame_values["was_completed"] = [
            (int(end_frame - 1), False),
            (int(end_frame), True)
        ]
        # Spinner-spezifische fixed_values
        if extra_params:
            fixed_values.update(extra_params)

    # Bei 'BASE' Importtyp keine zusätzlichen 'show' Keyframes
    if import_type == 'BASE' and object_type != 'circle':
        frame_values["show"] = [
            (int(early_start_frame - 1), False),
            (int(early_start_frame), True),
            (int(end_frame - 1), True),
            (int(end_frame), False)
        ]

    return frame_values, fixed_values

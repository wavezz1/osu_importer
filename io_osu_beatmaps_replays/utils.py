# osu_importer/utils.py

import bpy
import os

SCALE_FACTOR = 0.05

def get_ms_per_frame():
    fps = bpy.context.scene.render.fps
    return 1000 / fps  # Millisekunden pro Frame

def load_hitobject_times(osu_file):
    hitobject_times = []
    try:
        with open(osu_file, 'r', encoding='utf-8') as file:
            hit_objects_section = False
            for line in file:
                line = line.strip()
                if line == '[HitObjects]':
                    hit_objects_section = True
                    continue
                if hit_objects_section and line:
                    parts = line.split(',')
                    if len(parts) >= 3:
                        time = int(parts[2])
                        hitobject_times.append(time)
    except Exception as e:
        print(f"Fehler beim Laden der HitObject-Zeiten: {e}")
    return hitobject_times

def get_first_replay_event_time(replay_data):
    total_time = 0
    for event in replay_data:
        total_time += event.time_delta
        if event.x != -256 and event.y != -256:
            return total_time
    return total_time  # Falls alle Events bei (-256, -256) sind

def get_audio_lead_in(osu_file):
    audio_lead_in = 0
    try:
        with open(osu_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith("AudioLeadIn:"):
                    audio_lead_in = int(line.split(':')[1].strip())
                    break
    except Exception as e:
        print(f"Fehler beim Lesen des AudioLeadIns: {e}")
    return audio_lead_in

def create_collection(name):
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    return collection

def shift_cursor_keyframes(cursor_object_name, offset_ms):
    cursor = bpy.data.objects.get(cursor_object_name)
    if cursor is None:
        print(f"Objekt '{cursor_object_name}' nicht gefunden.")
        return

    if cursor.animation_data is None or cursor.animation_data.action is None:
        print(f"Keine Animation gefunden für Objekt '{cursor_object_name}'.")
        return

    action = cursor.animation_data.action
    fcurves = action.fcurves

    frame_offset = offset_ms / get_ms_per_frame()

    for fcurve in fcurves:
        for keyframe in fcurve.keyframe_points:
            keyframe.co.x += frame_offset
            keyframe.handle_left.x += frame_offset
            keyframe.handle_right.x += frame_offset

        # Aktualisiere die FCurve
        fcurve.update()
# osu_importer/utils.py (fortgesetzt)

def create_circle_at_position(x, y, name, start_time_ms, global_index, circles_collection, offset, early_frames=5):
    try:
        start_frame = (start_time_ms + offset) / get_ms_per_frame()
        early_start_frame = start_frame - early_frames

        bpy.ops.mesh.primitive_circle_add(radius=0.5, location=(x * SCALE_FACTOR, -y * SCALE_FACTOR, 0))
        circle = bpy.context.object
        circle.name = f"{global_index:03d}_{name}"

        # Keyframe Sichtbarkeit
        circle.hide_viewport = True
        circle.hide_render = True
        circle.keyframe_insert(data_path="hide_viewport", frame=early_start_frame - 1)
        circle.keyframe_insert(data_path="hide_render", frame=early_start_frame - 1)

        circle.hide_viewport = False
        circle.hide_render = False
        circle.keyframe_insert(data_path="hide_viewport", frame=early_start_frame)
        circle.keyframe_insert(data_path="hide_render", frame=early_start_frame)

        # Link zum gewünschten Collection hinzufügen
        circles_collection.objects.link(circle)
        # Aus anderen Collections entfernen
        for col in circle.users_collection:
            if col != circles_collection:
                col.objects.unlink(circle)

    except Exception as e:
        print(f"Fehler beim Erstellen eines Kreises: {e}")


def create_slider_curve(points, name, start_time_ms, end_time_ms, repeats, global_index, sliders_collection, offset,
                        early_frames=5):
    try:
        start_frame = (start_time_ms + offset) / get_ms_per_frame()
        early_start_frame = start_frame - early_frames
        end_frame = (end_time_ms + offset) / get_ms_per_frame()

        # Erstelle die Kurve
        curve_data = bpy.data.curves.new(name=f"{global_index:03d}_{name}_curve", type='CURVE')
        curve_data.dimensions = '3D'
        spline = curve_data.splines.new('BEZIER')
        spline.bezier_points.add(len(points) - 1)

        for i, (x, y) in enumerate(points):
            corrected_x = x * SCALE_FACTOR
            corrected_y = -y * SCALE_FACTOR
            bp = spline.bezier_points[i]
            bp.co = (corrected_x, corrected_y, 0)
            bp.handle_left_type = 'AUTO'
            bp.handle_right_type = 'AUTO'

        slider = bpy.data.objects.new(f"{global_index:03d}_{name}_curve", curve_data)

        # Keyframe Sichtbarkeit für die Kurve
        slider.hide_viewport = True
        slider.hide_render = True
        slider.keyframe_insert(data_path="hide_viewport", frame=early_start_frame - 1)
        slider.keyframe_insert(data_path="hide_render", frame=early_start_frame - 1)

        slider.hide_viewport = False
        slider.hide_render = False
        slider.keyframe_insert(data_path="hide_viewport", frame=early_start_frame)
        slider.keyframe_insert(data_path="hide_render", frame=early_start_frame)

        sliders_collection.objects.link(slider)

        # Slider-Kopf erstellen
        create_circle_at_position(points[0][0], points[0][1], f"{name}_head", start_time_ms, global_index,
                                  sliders_collection, offset)

        # Slider-Ende erstellen
        # Bei Wiederholungen muss der Endpunkt angepasst werden
        if repeats % 2 == 0:
            # Gerade Anzahl von Wiederholungen: Endpunkt ist der Anfangspunkt
            end_x, end_y = points[0]
        else:
            # Ungerade Anzahl von Wiederholungen: Endpunkt ist der letzten Kontrollpunkt
            end_x, end_y = points[-1]

        create_circle_at_position(end_x, end_y, f"{name}_tail", end_time_ms, global_index, sliders_collection, offset)

        # Slider-Ball animieren
        animate_slider_ball(slider, start_frame, end_frame, repeats)

    except Exception as e:
        print(f"Fehler beim Erstellen eines Sliders: {e}")

def create_spinner_at_position(x, y, name, start_time_ms, global_index, spinners_collection, offset, early_frames=5):
    try:
        start_frame = (start_time_ms + offset) / get_ms_per_frame()
        early_start_frame = start_frame - early_frames

        bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=0.1, location=(x * SCALE_FACTOR, -y * SCALE_FACTOR, 0))
        spinner = bpy.context.object
        spinner.name = f"{global_index:03d}_{name}"

        # Keyframe Sichtbarkeit
        spinner.hide_viewport = True
        spinner.hide_render = True
        spinner.keyframe_insert(data_path="hide_viewport", frame=early_start_frame - 1)
        spinner.keyframe_insert(data_path="hide_render", frame=early_start_frame - 1)

        spinner.hide_viewport = False
        spinner.hide_render = False
        spinner.keyframe_insert(data_path="hide_viewport", frame=early_start_frame)
        spinner.keyframe_insert(data_path="hide_render", frame=early_start_frame)

        # Link zum gewünschten Collection hinzufügen
        spinners_collection.objects.link(spinner)
        # Aus anderen Collections entfernen
        for col in spinner.users_collection:
            if col != spinners_collection:
                col.objects.unlink(spinner)

    except Exception as e:
        print(f"Fehler beim Erstellen eines Spinners: {e}")

def load_and_create_hitobjects(osu_file, circles_collection, sliders_collection, spinners_collection, offset, speed_multiplier):
    global_index = 1
    try:
        with open(osu_file, 'r', encoding='utf-8') as file:
            hit_objects_section = False
            for line in file:
                line = line.strip()
                if line == '[HitObjects]':
                    hit_objects_section = True
                    continue
                if hit_objects_section and line:
                    parts = line.split(',')
                    if len(parts) < 5:
                        continue  # Nicht genügend Daten
                    x, y, time, hit_type = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
                    start_time_ms = time / speed_multiplier  # Anpassung hier

                    if hit_type & 1:  # Circle
                        create_circle_at_position(x, y, f"circle_{time}", start_time_ms, global_index, circles_collection, offset)
                    elif hit_type & 2:  # Slider
                        slider_points = [(x, y)]
                        if len(parts) > 5:
                            slider_data = parts[5].split('|')
                            if len(slider_data) > 1:
                                slider_type = slider_data[0]
                                slider_control_points = slider_data[1:]
                                for point in slider_control_points:
                                    if ':' in point:
                                        px_str, py_str = point.split(':')
                                        px, py = float(px_str), float(py_str)
                                        slider_points.append((px, py))
                        else:
                            continue  # Keine Slider-Daten

                        # Wiederholungen und Pixel-Länge ermitteln
                        repeat_count = int(parts[6]) if len(parts) > 6 else 1
                        pixel_length = float(parts[7]) if len(parts) > 7 else 100

                        # Slider-Dauer berechnen
                        slider_duration = calculate_slider_duration(osu_file, start_time_ms, repeat_count, pixel_length, speed_multiplier)

                        end_time_ms = start_time_ms + slider_duration

                        create_slider_curve(
                            slider_points,
                            f"slider_{time}",
                            start_time_ms,
                            end_time_ms,
                            repeat_count,
                            global_index,
                            sliders_collection,
                            offset
                        )
                    elif hit_type & 8:  # Spinner
                        create_spinner_at_position(256, 192, f"spinner_{time}", start_time_ms, global_index, spinners_collection, offset)
                    global_index += 1
    except Exception as e:
        print(f"Fehler beim Laden und Erstellen der HitObjects: {e}")

def animate_slider_ball(slider_curve, start_frame, end_frame, repeats):
    try:
        # Erstelle den Slider-Ball
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=slider_curve.location)
        slider_ball = bpy.context.object
        slider_ball.name = f"{slider_curve.name}_ball"

        # Füge einen 'Follow Path'-Constraint hinzu
        follow_path = slider_ball.constraints.new('FOLLOW_PATH')
        follow_path.target = slider_curve
        follow_path.use_curve_follow = True

        # Setze die Animationseinstellungen für die Kurve
        slider_curve.data.path_duration = end_frame - start_frame

        # Keyframe die 'offset_factor' des Constraints
        slider_ball.keyframe_insert(data_path="constraints[\"Follow Path\"].offset_factor", frame=start_frame)
        slider_ball.constraints["Follow Path"].offset_factor = repeats
        slider_ball.keyframe_insert(data_path="constraints[\"Follow Path\"].offset_factor", frame=end_frame)

        # Keyframe Sichtbarkeit
        slider_ball.hide_viewport = True
        slider_ball.hide_render = True
        slider_ball.keyframe_insert(data_path="hide_viewport", frame=start_frame - 1)
        slider_ball.keyframe_insert(data_path="hide_render", frame=start_frame - 1)

        slider_ball.hide_viewport = False
        slider_ball.hide_render = False
        slider_ball.keyframe_insert(data_path="hide_viewport", frame=start_frame)
        slider_ball.keyframe_insert(data_path="hide_render", frame=start_frame)

    except Exception as e:
        print(f"Fehler beim Animieren des Slider-Balls: {e}")

def calculate_slider_duration(osu_file, start_time_ms, repeat_count, pixel_length, speed_multiplier):
    # Parsen der Timing-Punkte und Berechnung der Slider-Geschwindigkeit
    # Dies ist ein komplexes Thema und erfordert detailliertes Parsing der .osu-Datei
    # Für eine vereinfachte Annäherung verwenden wir einen Standardwert
    slider_multiplier = 1.4  # Standard-Slider-Multiplikator, kann aus der .osu-Datei gelesen werden
    beat_duration = 500  # Annahme eines Standard-Beat-Durationswertes in ms

    slider_duration = (pixel_length / (slider_multiplier * 100)) * beat_duration * repeat_count
    slider_duration /= speed_multiplier  # Anpassung an Mods wie DT oder HT
    return slider_duration

def create_animated_cursor(cursor_collection):
    try:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=(0, 0, 0))
        cursor = bpy.context.object
        cursor.name = "Cursor"

        # Link zum gewünschten Collection hinzufügen
        cursor_collection.objects.link(cursor)
        # Aus anderen Collections entfernen
        for col in cursor.users_collection:
            if col != cursor_collection:
                col.objects.unlink(cursor)

        return cursor
    except Exception as e:
        print(f"Fehler beim Erstellen des Cursors: {e}")
        return None

def animate_cursor(cursor, replay_data, offset):
    if cursor is None:
        print("Cursor-Objekt ist None, Animation wird übersprungen.")
        return
    total_time = 0
    try:
        for event in replay_data:
            total_time += event.time_delta
            if event.x == -256 and event.y == -256:
                continue  # Cursor ist nicht auf dem Bildschirm
            corrected_x = event.x * SCALE_FACTOR
            corrected_y = -event.y * SCALE_FACTOR
            cursor.location = (corrected_x, corrected_y, 0)
            frame = (total_time + offset) / get_ms_per_frame()
            cursor.keyframe_insert(data_path="location", frame=frame)
    except Exception as e:
        print(f"Fehler beim Animieren des Cursors: {e}")

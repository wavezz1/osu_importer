# slider.py

import bpy
from .utils import map_osu_to_blender, get_ms_per_frame
from .geometry_nodes import create_geometry_nodes_modifier_slider
from .info_parser import OsuParser
from .hitobjects import HitObject

class SliderCreator:
    def __init__(self, hitobject: HitObject, global_index: int, sliders_collection, settings: dict, osu_parser: OsuParser):
        self.hitobject = hitobject
        self.global_index = global_index
        self.sliders_collection = sliders_collection
        self.settings = settings  # Enthält Slider-Multiplier usw.
        self.osu_parser = osu_parser
        self.create_slider()

    def create_slider(self):
        x = self.hitobject.x
        y = self.hitobject.y
        time_ms = self.hitobject.time
        speed_multiplier = self.settings.get('speed_multiplier', 1.0)
        start_frame = ((time_ms / speed_multiplier) / get_ms_per_frame())
        early_start_frame = start_frame - self.settings.get('early_frames', 5)

        # Slider-Daten aus den Extras extrahieren
        if self.hitobject.extras:
            slider_data = self.hitobject.extras[0].split('|')
            if len(slider_data) > 1:
                slider_type = slider_data[0] # was das
                print(f"slider_data" + f" " + str(slider_data[0]))
                slider_control_points = slider_data[1:]
                points = [(x, y)]
                for point in slider_control_points:
                    if ':' in point:
                        px_str, py_str = point.split(':')
                        px, py = float(px_str), float(py_str)
                        points.append((px, py))
            else:
                print(f"Ungültige Slider-Daten für HitObject bei {time_ms} ms")
                return
        else:
            print(f"Keine Slider-Daten für HitObject bei {time_ms} ms")
            return

        # Wiederholungen und Pixel-Länge ermitteln
        repeat_count = int(self.hitobject.extras[1]) if len(self.hitobject.extras) > 1 else 1
        pixel_length = float(self.hitobject.extras[2]) if len(self.hitobject.extras) > 2 else 100

        # Slider-Dauer berechnen
        slider_duration_ms = self.calculate_slider_duration(time_ms, repeat_count, pixel_length, speed_multiplier)
        end_time_ms = time_ms + slider_duration_ms
        end_frame = ((end_time_ms / speed_multiplier) / get_ms_per_frame())

        # Erstelle die Kurve
        curve_data = bpy.data.curves.new(name=f"{self.global_index:03d}_slider_{time_ms}_curve", type='CURVE')
        curve_data.dimensions = '3D'
        spline = curve_data.splines.new('BEZIER')
        spline.bezier_points.add(len(points) - 1)

        for i, (px, py) in enumerate(points):
            corrected_x, corrected_y, corrected_z = map_osu_to_blender(px, py)
            bp = spline.bezier_points[i]
            bp.co = (corrected_x, corrected_y, corrected_z)
            # Optional: Handle-Typen setzen
            bp.handle_left_type = 'AUTO'
            bp.handle_right_type = 'AUTO'

        slider = bpy.data.objects.new(f"{self.global_index:03d}_slider_{time_ms}", curve_data)

        # Benutzerdefiniertes Attribut "show" hinzufügen
        slider["show"] = False  # Startwert: Nicht sichtbar
        slider.keyframe_insert(data_path='["show"]', frame=(early_start_frame - 1))

        slider["show"] = True
        slider.keyframe_insert(data_path='["show"]', frame=early_start_frame)

        # Optional: Ausblenden am Ende
        slider["show"] = True
        slider.keyframe_insert(data_path='["show"]', frame=(end_frame - 1))

        slider["show"] = False
        slider.keyframe_insert(data_path='["show"]', frame=end_frame)

        # Füge "slider_duration_ms" und "slider_duration_frames" hinzu (ohne Keyframe)
        slider["slider_duration_ms"] = slider_duration_ms

        # Berechne slider_duration in Frames basierend auf der Szenen-FPS
        scene_fps = bpy.context.scene.render.fps
        slider_duration_frames = slider_duration_ms / (1000 / scene_fps)
        slider["slider_duration_frames"] = slider_duration_frames

        self.sliders_collection.objects.link(slider)
        # Aus anderen Collections entfernen
        if slider.users_collection:
            for col in slider.users_collection:
                if col != self.sliders_collection:
                    col.objects.unlink(slider)
                    
        create_geometry_nodes_modifier_slider(slider, slider.name)

    def calculate_slider_duration(self, start_time_ms, repeat_count, pixel_length, speed_multiplier):
        # Parsen der Timing-Punkte und Berechnung der Slider-Geschwindigkeit
        timing_points = self.osu_parser.timing_points
        beat_duration = 500  # Fallback-Wert, falls kein Timing Point gefunden wird
        slider_multiplier = float(self.osu_parser.difficulty_settings.get("SliderMultiplier", 1.4))

        # Finden des passenden Timing Points
        inherited_multiplier = 1.0
        current_beat_length = None
        for offset, beat_length in timing_points:
            if start_time_ms >= offset:
                if beat_length < 0:  # Inherited Timing Point (negativer BeatLength)
                    inherited_multiplier = -100 / beat_length  # Skalierung der Slidergeschwindigkeit
                else:  # Normaler Timing Point
                    current_beat_length = beat_length
            else:
                break

        if current_beat_length is not None and current_beat_length > 0:
            beat_duration = current_beat_length
        else:
            print(f"Warnung: Ungültiger Beat Length bei Startzeit {start_time_ms}. Fallback-Wert wird verwendet.")

        # Berechnung der Slider-Dauer
        slider_duration = (pixel_length / (
                    slider_multiplier * 100)) * beat_duration * repeat_count * inherited_multiplier

        # Anpassung für Mods wie DT oder HT
        slider_duration /= speed_multiplier

        return slider_duration

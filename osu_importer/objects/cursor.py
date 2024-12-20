# osu_importer/objects/cursor.py

import bpy
import math
from osu_importer.utils.utils import map_osu_to_blender, tag_imported
from osu_importer.geo_nodes.geometry_nodes import create_geometry_nodes_modifier, set_modifier_inputs_with_keyframes
from osu_importer.osu_data_manager import OsuDataManager


class CursorCreator:
    def __init__(self, cursor_collection, settings, data_manager: OsuDataManager, import_type):
        self.cursor_collection = cursor_collection
        self.settings = settings
        self.data_manager = data_manager
        self.import_type = import_type
        self.cursor = None
        self.create_cursor()

    def create_cursor(self):
        try:
            cursor_size = self.settings.cursor_size
            if self.import_type == 'FULL':
                cursor_shape = self.settings.cursor_shape
                if cursor_shape == 'SPHERE':
                    bpy.ops.mesh.primitive_uv_sphere_add(radius=cursor_size, location=(0, 0, 0))
                    cursor = bpy.context.object
                elif cursor_shape == 'CIRCLE':
                    bpy.ops.mesh.primitive_circle_add(vertices=32, radius=cursor_size, fill_type='NGON',
                                                      location=(0, 0, 0),
                                                      rotation=(math.radians(90), 0, 0))
                    cursor = bpy.context.object
                else:
                    bpy.ops.mesh.primitive_uv_sphere_add(radius=cursor_size, location=(0, 0, 0))
                    cursor = bpy.context.object
            else:
                mesh = bpy.data.meshes.new("Cursor")
                mesh.vertices.add(1)
                mesh.vertices[0].co = (0, 0, 0)
                mesh.use_auto_texspace = True

                cursor = bpy.data.objects.new("Cursor", mesh)
                cursor.location = (0, 0, 0)

                create_geometry_nodes_modifier(cursor, "cursor")

                fixed_values = {
                    "cursor_size": cursor_size
                }

                attributes = {
                    "k1": 'BOOLEAN',
                    "k2": 'BOOLEAN',
                    "m1": 'BOOLEAN',
                    "m2": 'BOOLEAN',
                    "cursor_size": 'FLOAT'
                }

                initial_frame_values = {
                    "k1": [(1, False)],
                    "k2": [(1, False)],
                    "m1": [(1, False)],
                    "m2": [(1, False)]
                }
                set_modifier_inputs_with_keyframes(cursor, attributes, initial_frame_values, fixed_values)

            cursor.name = "Cursor"
            tag_imported(cursor)

            self.cursor_collection.objects.link(cursor)
            if cursor.users_collection:
                for col in cursor.users_collection:
                    if col != self.cursor_collection:
                        col.objects.unlink(cursor)

            self.cursor = cursor
            print(f"Cursor '{cursor.name}' created successfully.")
        except Exception as e:
            print(f"Error creating cursor: {e}")

    def animate_cursor(self):
        if self.cursor is None:
            print("Cursor object is None, skipping animation.")
            return

        replay_data = self.data_manager.replay_data
        key_presses = self.data_manager.key_presses
        speed_multiplier = self.data_manager.speed_multiplier
        ms_per_frame = self.data_manager.ms_per_frame
        audio_lead_in_frames = self.data_manager.audio_lead_in_frames
        total_time = 0

        try:
            for i, event in enumerate(replay_data):
                total_time += event.time_delta
                if event.x == -256 and event.y == -256:
                    continue

                corrected_x, corrected_y, corrected_z = map_osu_to_blender(event.x, event.y)
                location = (corrected_x, corrected_y, corrected_z)

                adjusted_time_ms = total_time / speed_multiplier
                frame = (adjusted_time_ms / ms_per_frame) + audio_lead_in_frames

                if self.import_type == 'BASE':
                    set_cursor_keyframes(
                        self.cursor,
                        frame,
                        location,
                        key_presses[i]
                    )
                else:
                    self.cursor.location = location
                    self.cursor.keyframe_insert(data_path='location', frame=frame)

            print(f"Cursor '{self.cursor.name}' animated successfully.")
        except Exception as e:
            print(f"Error animating cursor: {e}")


def set_cursor_keyframes(cursor, frame, location, key_presses):
    cursor.location = location
    cursor.keyframe_insert(data_path='location', frame=frame)

    frame_values = {
        "k1": [(int(frame), bool(key_presses['k1']))],
        "k2": [(int(frame), bool(key_presses['k2']))],
        "m1": [(int(frame), bool(key_presses['m1']))],
        "m2": [(int(frame), bool(key_presses['m2']))]
    }
    set_modifier_inputs_with_keyframes(cursor, {
        "k1": 'BOOLEAN',
        "k2": 'BOOLEAN',
        "m1": 'BOOLEAN',
        "m2": 'BOOLEAN'
    }, frame_values, fixed_values=None)

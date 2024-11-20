# spinner.py

import bpy
import math
from osu_importer.utils.utils import map_osu_to_blender, timeit, get_keyframe_values
from osu_importer.utils.constants import SPINNER_CENTER_X, SPINNER_CENTER_Y
from osu_importer.geo_nodes.geometry_nodes import create_geometry_nodes_modifier, set_modifier_inputs_with_keyframes
from osu_importer.osu_replay_data_manager import OsuReplayDataManager
from osu_importer.parsers.hitobjects import HitObject

class SpinnerCreator:
    def __init__(self, hitobject: HitObject, global_index: int, spinners_collection, settings: dict, data_manager: OsuReplayDataManager, import_type):
        self.hitobject = hitobject
        self.global_index = global_index
        self.spinners_collection = spinners_collection
        self.settings = settings
        self.data_manager = data_manager
        self.import_type = import_type
        self.create_spinner()

    def create_spinner(self):
        with timeit(f"Erstellen von Spinner {self.global_index:03d}_spinner_{self.hitobject.time}"):
            data_manager = self.data_manager

            approach_rate = data_manager.adjusted_ar
            preempt_frames = data_manager.preempt_frames
            audio_lead_in_frames = data_manager.audio_lead_in_frames
            speed_multiplier = data_manager.speed_multiplier
            ms_per_frame = data_manager.ms_per_frame

            start_time_ms = self.hitobject.time / speed_multiplier
            if self.hitobject.extras:
                end_time_ms = int(self.hitobject.extras[0])
                spinner_duration_ms = (end_time_ms - self.hitobject.time) / speed_multiplier
            else:
                print(f"No end time found for spinner at {self.hitobject.time} ms.")
                return

            start_frame = start_time_ms / ms_per_frame + audio_lead_in_frames
            early_start_frame = start_frame - preempt_frames
            end_frame = (end_time_ms / speed_multiplier) / ms_per_frame + audio_lead_in_frames

            spinner_duration_frames = spinner_duration_ms / data_manager.get_ms_per_frame()

            corrected_x, corrected_y, corrected_z = map_osu_to_blender(SPINNER_CENTER_X, SPINNER_CENTER_Y)

            if self.import_type == 'FULL':
                bpy.ops.mesh.primitive_circle_add(
                    fill_type='NGON',
                    radius=4,
                    location=(corrected_x, corrected_y, corrected_z),
                    rotation=(math.radians(90), 0, 0)
                )
                spinner = bpy.context.object
            elif self.import_type == 'BASE':
                mesh = bpy.data.meshes.new(f"{self.global_index:03d}_spinner_{self.hitobject.time}")

                mesh.vertices.add(1)
                mesh.vertices[0].co = (0, 0, 0)

                mesh.use_auto_texspace = True

                spinner = bpy.data.objects.new(f"{self.global_index:03d}_spinner_{self.hitobject.time}", mesh)
                spinner.location = (corrected_x, corrected_y, corrected_z)

            spinner.name = f"{self.global_index:03d}_spinner_{self.hitobject.time}"

            spinner["ar"] = approach_rate

            self.spinners_collection.objects.link(spinner)
            if spinner.users_collection:
                for col in spinner.users_collection:
                    if col != self.spinners_collection:
                        col.objects.unlink(spinner)

            if self.import_type == 'BASE':
                create_geometry_nodes_modifier(spinner, "spinner")

            extra_params = {
                "spinner_duration_ms": spinner_duration_ms,
                "spinner_duration_frames": spinner_duration_frames
            }

            frame_values, fixed_values = get_keyframe_values(
                self.hitobject,
                'spinner',
                self.import_type,
                start_frame,
                end_frame,
                early_start_frame,
                approach_rate,
                osu_radius=0,
                extra_params=extra_params
            )

            attributes = {
                "show": 'BOOLEAN',
                "spinner_duration_ms": 'FLOAT',
                "spinner_duration_frames": 'FLOAT',
                "was_hit": 'BOOLEAN',
                "was_completed": 'BOOLEAN'
            }

            set_modifier_inputs_with_keyframes(spinner, attributes, frame_values, fixed_values)

            if self.import_type == 'FULL':
                spinner.hide_viewport = True
                spinner.hide_render = True
                spinner.keyframe_insert(data_path="hide_viewport", frame=int(early_start_frame - 1))
                spinner.keyframe_insert(data_path="hide_render", frame=int(early_start_frame - 1))

                spinner.hide_viewport = False
                spinner.hide_render = False
                spinner.keyframe_insert(data_path="hide_viewport", frame=int(early_start_frame))
                spinner.keyframe_insert(data_path="hide_render", frame=int(early_start_frame))

                if self.hitobject.was_completed:
                    spinner.hide_viewport = False
                    spinner.hide_render = False
                else:
                    spinner.hide_viewport = True
                    spinner.hide_render = True
                spinner.keyframe_insert(data_path="hide_viewport", frame=int(end_frame))
                spinner.keyframe_insert(data_path="hide_render", frame=int(end_frame))

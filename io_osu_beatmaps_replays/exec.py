# exec.py

import bpy
import os
from .osu_replay_data_manager import OsuReplayDataManager
from .import_objects import import_hitobjects
from .utils import create_collection
from .mod_functions import calculate_speed_multiplier


def main_execution(context):
    props = context.scene.osu_importer_props
    osu_file_path = bpy.path.abspath(props.osu_file)
    osr_file_path = bpy.path.abspath(props.osr_file)

    if not os.path.isfile(osu_file_path) or not os.path.isfile(osr_file_path):
        context.window_manager.popup_menu(
            lambda self, ctx: self.layout.label(text="The specified .osu or .osr file does not exist."),
            title="Error",
            icon='ERROR'
        )
        return {'CANCELLED'}, None

    data_manager = OsuReplayDataManager(osu_file_path, osr_file_path)
    data_manager.print_all_info()
    if props.import_audio:
        data_manager.import_audio()

    data_manager.check_hits()
    speed_multiplier = calculate_speed_multiplier(data_manager.mods)

    settings = {
        'speed_multiplier': speed_multiplier,
        'audio_lead_in': data_manager.beatmap_info.get("audio_lead_in", 0),
        'early_frames': 5,  # falls benötigt
    }

    import_hitobjects(data_manager, settings, props)

    # Set frame start and end based on animation
    scene = bpy.context.scene
    # Sicherstellen, dass es Objekte mit Animationen gibt
    anim_objects = [obj for obj in bpy.data.objects if obj.animation_data and obj.animation_data.action]
    if anim_objects:
        scene.frame_start = int(min([action.frame_range[0] for obj in anim_objects for action in [obj.animation_data.action]]))
        scene.frame_end = int(max([action.frame_range[1] for obj in anim_objects for action in [obj.animation_data.action]]))

    return {'FINISHED'}, data_manager

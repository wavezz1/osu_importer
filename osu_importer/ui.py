# ui.py

import bpy
from bpy.types import Panel, PropertyGroup, Operator
from bpy.props import StringProperty, BoolProperty, FloatProperty, IntProperty, EnumProperty
from osu_importer.utils.utils import update_dev_tools


class OSUImporterProperties(PropertyGroup):
    dev_tools: BoolProperty(
        name="Enable Dev Tools",
        description="Enable development tools",
        default=True,
        update=update_dev_tools
    )
    # File Paths
    osu_file: StringProperty(
        name="Beatmap (.osu) File",
        description="Path to the .osu beatmap file",
        default="",
        subtype='FILE_PATH'
    )
    osr_file: StringProperty(
        name="Replay (.osr) File",
        description="Path to the .osr replay file",
        default="",
        subtype='FILE_PATH'
    )
    # Import Type
    import_type: EnumProperty(
        name="Import Type",
        description="Choose the import type:\n- Base: Import minimal data with Geometry Nodes\n- Full: Import complete data with visibility keyframes",
        items=[
            ('BASE', "Base Map/Replay", "Import empty meshes with Geometry Nodes"),
            ('FULL', "Full Map", "Import full meshes with visibility keyframes")
        ],
        default='BASE'
    )
    include_osu_gameplay: BoolProperty(
        name="Include Osu_Gameplay",
        description="Add Osu_Gameplay mesh and Geometry Nodes setup",
        default=True
    )
    # Import Options
    import_approach_circles: BoolProperty(
        name="Approach Circles",
        description="Import approach circles for each hit object",
        default=True
    )
    import_circles: BoolProperty(
        name="Circles",
        description="Import circle hit objects",
        default=True
    )
    import_sliders: BoolProperty(
        name="Sliders",
        description="Import slider hit objects",
        default=True
    )
    import_spinners: BoolProperty(
        name="Spinners",
        description="Import spinner hit objects",
        default=True
    )
    import_slider_heads_tails: BoolProperty(
        name="Slider Heads and Tails",
        description="Import slider head and tail circles for each slider in FULL import",
        default=True
    )
    # Slider Options
    import_slider_ticks: BoolProperty(
        name="Slider Ticks",
        description="Import slider ticks",
        default=False
    )
    import_slider_balls: BoolProperty(
        name="Slider Balls",
        description="Import slider balls",
        default=True
    )
    slider_resolution: IntProperty(
        name="Slider Resolution",
        description="Defines the smoothness of sliders (higher values = smoother but more performance intensive)",
        default=12,
        min=4,
        max=50
    )
    approach_circle_bevel_depth: FloatProperty(
        name="Bevel Depth",
        description="Adjust the bevel depth of approach circles in FULL import",
        default=0.02,
        min=0.0,
        max=1.0,
        subtype='NONE',
        step=0.01,
        precision=2
    )
    approach_circle_bevel_resolution: IntProperty(
        name="Bevel Resolution",
        description="Adjust the bevel depth of approach circles in FULL import",
        default=4,
        min=1,
        max=12
    )
    # Replay Options
    import_cursors: BoolProperty(
        name="Cursor Movements",
        description="Import cursor movements from the replay",
        default=True
    )
    # Audio Options
    import_audio: BoolProperty(
        name="Audio Track",
        description="Import the audio track associated with the beatmap",
        default=True
    )
    # Beatmap Information
    title: StringProperty(
        name="Title",
        default=""
    )
    artist: StringProperty(
        name="Artist",
        default=""
    )
    difficulty_name: StringProperty(
        name="Difficulty",
        default=""
    )
    bpm: FloatProperty(
        name="BPM",
        default=0.0
    )
    base_approach_rate: FloatProperty(
        name="Base AR",
        default=0.0
    )
    adjusted_approach_rate: FloatProperty(
        name="Adjusted AR",
        default=0.0
    )
    base_circle_size: FloatProperty(
        name="Base CS",
        default=0.0
    )
    adjusted_circle_size: FloatProperty(
        name="Adjusted CS",
        default=0.0
    )
    base_overall_difficulty: FloatProperty(
        name="Base OD",
        default=0.0
    )
    adjusted_overall_difficulty: FloatProperty(
        name="Adjusted OD",
        default=0.0
    )
    total_hitobjects: IntProperty(
        name="Total HitObjects",
        default=0
    )
    # Replay Information
    formatted_mods: StringProperty(
        name="Mods",
        default="None"
    )
    accuracy: FloatProperty(
        name="Accuracy",
        default=0.0
    )
    misses: IntProperty(
        name="Misses",
        default=0
    )
    max_combo: IntProperty(
        name="Max Combo",
        default=0
    )
    total_score: IntProperty(
        name="Total Score",
        default=0
    )
    player_name: StringProperty(  # Neue Eigenschaft für den Spielernamen
        name="Player Name",
        default="Unknown"
    )
    # UI Toggles
    show_beatmap_info: BoolProperty(
        name="Show Beatmap Information",
        description="Toggle visibility of Beatmap Information",
        default=False
    )
    show_replay_info: BoolProperty(
        name="Show Replay Information",
        description="Toggle visibility of Replay Information",
        default=False
    )
    show_tool_info: BoolProperty(
        name="Show Tools",
        description="Toggle visibility of Tools",
        default=False
    )


class OSU_PT_ImporterPanel(Panel):
    bl_label = "osu! Importer"
    bl_idname = "OSU_PT_importer_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "osu! Importer"

    def draw(self, context):
        layout = self.layout
        props = context.scene.osu_importer_props

        # File Selection
        box = layout.box()
        box.label(text="File Selection", icon='FILE_FOLDER')
        if props.dev_tools:
            # Dev Tools aktiviert: Zeigt die voreingestellten Pfade an
            box.label(text="Dev Tools Activated", icon='MODIFIER')
            box.label(text=f"OSU File: {props.osu_file}", icon='FILE_BLEND')
            box.label(text=f"OSR File: {props.osr_file}", icon='FILE_BLEND')
        else:
            # Standard File Selection
            box.prop(props, "osu_file")
            box.prop(props, "osr_file")

        box.separator()
        box.operator("osu_importer.import", text="Import", icon='IMPORT')
        box.operator("osu_importer.delete", text="Delete Imported Data", icon='TRASH')

        # Import Options
        box = layout.box()
        box.label(text="Import Options", icon='IMPORT')

        # Import Type Selection
        box.prop(props, "import_type")

        # import_type 'BASE'
        if props.import_type == 'BASE':
            box.prop(props, "include_osu_gameplay", toggle=True)

        # Hit Objects Import Options
        col = box.column(align=True)
        col.label(text="Hit Objects:", icon='OBJECT_DATA')
        col.prop(props, "import_approach_circles", toggle=True)
        if props.import_type == 'FULL' and props.import_approach_circles:
            col.prop(props, "approach_circle_bevel_depth")
            col.prop(props, "approach_circle_bevel_resolution")
        row = col.row(align=True)
        row.prop(props, "import_circles", toggle=True)
        row.prop(props, "import_sliders", toggle=True)
        row.prop(props, "import_spinners", toggle=True)


        # Slider Options
        if props.import_sliders:
            col.separator()
            col.label(text="Slider Options:", icon='MOD_CURVE')
            col.prop(props, "slider_resolution")
            row = col.row(align=True)
            if props.import_type == 'FULL':
                row.prop(props, "import_slider_heads_tails", toggle=True)

            col.prop(props, "import_slider_balls", toggle=True)
            col.prop(props, "import_slider_ticks", toggle=True)

            if props.import_slider_ticks:
                col.separator()
                warning_box = col.box()
                warning_row = warning_box.row(align=True)
                warning_row.label(text="⚠️  WARNING  ⚠️", icon='NONE')
                warning_row = warning_box.row(align=True)
                warning_row.label(text="Slider Ticks are NOT recommended!", icon='NONE')
                warning_row = warning_box.row(align=True)
                warning_row.label(text="This can lead to too many objects.", icon='NONE')

        # Replay Options
        col.separator()
        col.label(text="Replay Options:", icon='REC')
        col.prop(props, "import_cursors", toggle=True)

        # Audio Options
        col.separator()
        col.label(text="Audio Options:", icon='SPEAKER')
        col.prop(props, "import_audio", toggle=True)

        # Beatmap Information Toggle
        if props.bpm != 0.0:
            box = layout.box()
            box.prop(props, "show_beatmap_info", text="Beatmap Information", icon='INFO')
            if props.show_beatmap_info:
                col = box.column(align=True)
                col.label(text=f"Title: {props.title}")
                col.label(text=f"Artist: {props.artist}")
                col.label(text=f"Difficulty: {props.difficulty_name}")
                col.separator()
                col.label(text=f"BPM: {props.bpm:.2f}")
                ar_modified = abs(props.base_approach_rate - props.adjusted_approach_rate) > 0.01
                if ar_modified:
                    col.label(text=f"AR: {props.base_approach_rate} (Adjusted: {props.adjusted_approach_rate:.1f})")
                else:
                    col.label(text=f"AR: {props.base_approach_rate}")
                cs_modified = abs(props.base_circle_size - props.adjusted_circle_size) > 0.01
                if cs_modified:
                    col.label(text=f"CS: {props.base_circle_size} (Adjusted: {props.adjusted_circle_size:.1f})")
                else:
                    col.label(text=f"CS: {props.base_circle_size}")
                od_modified = abs(props.base_overall_difficulty - props.adjusted_overall_difficulty) > 0.01
                if od_modified:
                    col.label(text=f"OD: {props.base_overall_difficulty} (Adjusted: {props.adjusted_overall_difficulty:.1f})")
                else:
                    col.label(text=f"OD: {props.base_overall_difficulty}")
                col.label(text=f"Total HitObjects: {props.total_hitobjects}")

        # Replay Information Toggle
        if props.formatted_mods != "None" or props.accuracy != 0.0 or props.misses != 0:
            box = layout.box()
            box.prop(props, "show_replay_info", text="Replay Information", icon='PLAY')
            if props.show_replay_info:
                col = box.column(align=True)
                col.label(text=f"Player Name: {props.player_name}")
                col.label(text=f"Mods: {props.formatted_mods}")
                col.label(text=f"Accuracy: {props.accuracy:.2f}%")
                col.label(text=f"Misses: {props.misses}")
                col.label(text=f"Max Combo: {props.max_combo}")
                col.label(text=f"Total Score: {props.total_score}")

        # # Tool Information Toggle
        # if props.bpm != 0.0:
        box = layout.box()
        box.prop(props, "show_tool_info", text="Tools", icon='PLUS')
        if props.show_tool_info:
            # Flip Cursor Position
            col = box.column(align=True)
            col.label(text="Cursor Transformation:", icon='CURSOR')
            row = col.row(align=True)
            row.operator("osu_importer.flip_cursor_horizontal", text="Flip Cursor Horizontal", icon='ARROW_LEFTRIGHT')
            row.operator("osu_importer.flip_cursor_vertical", text="Flip Cursor Vertical", icon='EVENT_DOWN_ARROW')

            # Flip Map
            col.separator()
            col.label(text="Map Transformation:", icon='MOD_MIRROR')
            row = col.row(align=True)
            row.operator("osu_importer.flip_map_horizontal", text="Flip Map Horizontal", icon='ARROW_LEFTRIGHT')
            row.operator("osu_importer.flip_map_vertical", text="Flip Map Vertical", icon='EVENT_DOWN_ARROW')

            # Dev Tools Toggle
            col.separator()
            box = layout.box()
            box.prop(props, "dev_tools", text="Enable Dev Tools", toggle=True)

class OSU_OT_Import(Operator):
    bl_idname = "osu_importer.import"
    bl_label = "Import"
    bl_description = "Import selected Beatmap and Replay"

    def execute(self, context):
        from .exec import main_execution
        props = context.scene.osu_importer_props

        try:
            if not (props.osu_file and props.osr_file):
                self.report({'ERROR'}, "Please specify both .osu and .osr files.")
                return {'CANCELLED'}

            context.scene.render.fps = 60
            self.report({'INFO'}, "Scene set to 60 FPS")

            result, data_manager = main_execution(context)

            if result != {'FINISHED'} or data_manager is None:
                return {'CANCELLED'}

            props.base_approach_rate = data_manager.base_ar
            props.adjusted_approach_rate = data_manager.adjusted_ar
            props.base_circle_size = data_manager.base_cs
            props.adjusted_circle_size = data_manager.adjusted_cs
            props.base_overall_difficulty = data_manager.base_od
            props.adjusted_overall_difficulty = data_manager.adjusted_od
            props.bpm = data_manager.beatmap_info["bpm"]
            props.total_hitobjects = data_manager.beatmap_info["total_hitobjects"]

            props.title = data_manager.beatmap_info["metadata"].get("Title", "")
            props.artist = data_manager.beatmap_info["metadata"].get("Artist", "")
            props.difficulty_name = data_manager.beatmap_info["metadata"].get("Version", "")

            props.formatted_mods = data_manager.replay_info["mods"]
            props.accuracy = data_manager.replay_info["accuracy"]
            props.misses = data_manager.replay_info["misses"]
            props.max_combo = data_manager.replay_info["max_combo"]
            props.player_name = data_manager.replay_info["username"]
            props.total_score = data_manager.replay_info["total_score"]

            return result

        except Exception as e:
            self.report({'ERROR'}, f"Error during import: {str(e)}")
            return {'CANCELLED'}

class OSU_OT_FlipCursorHorizontal(Operator):
    bl_idname = "osu_importer.flip_cursor_horizontal"
    bl_label = "Flip Cursor Horizontal"
    bl_description = "Spiegelt die Cursor-Positionen horizontal (X-Achse)"

    def execute(self, context):
        cursor_objects = [obj for obj in bpy.data.objects if obj.name.startswith("Cursor")]
        flipped_count = 0
        for obj in cursor_objects:
            obj.scale.x *= -1
            obj.location.x *= -1

            if obj.animation_data and obj.animation_data.action:
                for fcurve in obj.animation_data.action.fcurves:
                    if fcurve.data_path == "location" and fcurve.array_index == 0:
                        for keyframe in fcurve.keyframe_points:
                            keyframe.co.y *= -1
                            keyframe.handle_left.y *= -1
                            keyframe.handle_right.y *= -1
                    elif fcurve.data_path == "scale" and fcurve.array_index == 0:
                        for keyframe in fcurve.keyframe_points:
                            keyframe.co.y *= -1
                            keyframe.handle_left.y *= -1
                            keyframe.handle_right.y *= -1
            flipped_count +=1
        self.report({'INFO'}, f"Horizontales Spiegeln der {flipped_count} Cursor abgeschlossen.")
        return {'FINISHED'}

class OSU_OT_FlipCursorVertical(Operator):
    bl_idname = "osu_importer.flip_cursor_vertical"
    bl_label = "Flip Cursor Vertical"
    bl_description = "Spiegelt die Cursor-Positionen vertikal (Y-Achse)"

    def execute(self, context):
        cursor_objects = [obj for obj in bpy.data.objects if obj.name.startswith("Cursor")]
        flipped_count = 0
        for obj in cursor_objects:
            obj.scale.z *= -1
            obj.location.z *= -1

            if obj.animation_data and obj.animation_data.action:
                for fcurve in obj.animation_data.action.fcurves:
                    if fcurve.data_path == "location" and fcurve.array_index == 2:
                        for keyframe in fcurve.keyframe_points:
                            keyframe.co.y *= -1
                            keyframe.handle_left.y *= -1
                            keyframe.handle_right.y *= -1
                    elif fcurve.data_path == "scale" and fcurve.array_index == 2:
                        for keyframe in fcurve.keyframe_points:
                            keyframe.co.y *= -1
                            keyframe.handle_left.y *= -1
                            keyframe.handle_right.y *= -1
            flipped_count +=1
        self.report({'INFO'}, f"Vertikales Spiegeln der {flipped_count} Cursor abgeschlossen.")
        return {'FINISHED'}

class OSU_OT_FlipMapHorizontal(Operator):
    bl_idname = "osu_importer.flip_map_horizontal"
    bl_label = "Flip Map Horizontal"
    bl_description = "Spiegelt die gesamte Karte horizontal (X-Achse)"

    def execute(self, context):
        map_prefixes = ["Circle", "Slider", "Spinner", "Approach", "Osu_Gameplay", "Slider Heads Tails"]
        map_objects = [obj for obj in bpy.data.objects if any(obj.name.startswith(prefix) for prefix in map_prefixes)]
        for obj in map_objects:
            obj.scale.x *= -1
            obj.location.x *= -1
        self.report({'INFO'}, f"Horizontales Spiegeln der {len(map_objects)} Kartenobjekte abgeschlossen.")
        return {'FINISHED'}

class OSU_OT_FlipMapVertical(Operator):
    bl_idname = "osu_importer.flip_map_vertical"
    bl_label = "Flip Map Vertical"
    bl_description = "Spiegelt die gesamte Karte vertikal (Y-Achse)"

    def execute(self, context):
        map_prefixes = ["Circle", "Slider", "Spinner", "Approach", "Osu_Gameplay", "Slider Heads Tails"]
        map_objects = [obj for obj in bpy.data.objects if any(obj.name.startswith(prefix) for prefix in map_prefixes)]
        for obj in map_objects:
            obj.scale.z *= -1
            obj.location.z *= -1
        self.report({'INFO'}, f"Vertikales Spiegeln der {len(map_objects)} Kartenobjekte abgeschlossen.")
        return {'FINISHED'}
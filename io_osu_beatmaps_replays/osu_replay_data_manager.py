# osu_replay_data_manager.py

from .info_parser import OsuParser, OsrParser

class OsuReplayDataManager:
    def __init__(self, osu_file_path, osr_file_path):
        self.osu_parser = OsuParser(osu_file_path)
        self.osr_parser = OsrParser(osr_file_path)

    @property
    def beatmap_info(self):
        return {
            "approach_rate": float(self.osu_parser.difficulty_settings.get("ApproachRate", 5.0)),
            "circle_size": float(self.osu_parser.difficulty_settings.get("CircleSize", 5.0)),
            "bpm": self.osu_parser.bpm,
            "total_hitobjects": self.osu_parser.total_hitobjects,
        }

    @property
    def replay_info(self):
        return {
            "mods": ','.join(self.osr_parser.mod_list) if self.osr_parser.mod_list else "Keine",
            "accuracy": self.osr_parser.calculate_accuracy(),
            "misses": self.osr_parser.calculate_misses(),
        }

    @property
    def hitobjects(self):
        return self.osu_parser.hitobjects

    @property
    def replay_data(self):
        return self.osr_parser.replay_data

    @property
    def key_presses(self):
        return self.osr_parser.key_presses

    @property
    def mods(self):
        return self.osr_parser.mods

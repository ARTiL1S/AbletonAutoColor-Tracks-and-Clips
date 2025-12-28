import Live
from ableton.v2.control_surface import ControlSurface
from functools import partial

# Dictionary of track names and their corresponding color indices
track_colors = {
    "808": 14,
    "ambiance": 44,
    "arp": 21,
    "bass": 16,
    "bass bus": 15,
    "bell": 27,
    "brass": 33,
    "bridge": 40,
    "cello": 34,
    "clap": 14,
    "clarinet": 32,
    "crash": 14,
    "cymbal": 14,
    "drone": 41,
    "drum": 14,
    "drum bus": 14,
    "drums": 14,
    "fx": 38,
    "foley": 39,
    "flute": 30,
    "gtr": 23,
    "guitar": 23,
    "guitar bus": 23,
    "gtp bus": 24,
    "harp": 37,
    "hat": 14,
    "hook": 36,
    "horns": 33,
    "impact": 14,
    "intro": 35,
    "kalimba": 28,
    "keys": 26,
    "kick": 14,
    "mallet": 28,
    "organ": 26,
    "outro": 35,
    "pad": 21,
    "perc": 14,
    "phantom": 50,
    "piano": 25,
    "pink noise": 49,
    "pluck": 22,
    "pno": 25,
    "post": 35,
    "pre": 35,
    "region bridge": 40,
    "region chorus": 36,
    "region hook": 36,
    "region intro": 35,
    "region interlude": 35,
    "region outro": 35,
    "region post": 35,
    "region pre": 35,
    "region verse": 35,
    "return": 48,
    "rhodes": 26,
    "riser": 43,
    "rim": 14,
    "sampler": 18,
    "sfx": 38,
    "shaker": 14,
    "snap": 14,
    "snare": 14,
    "string": 31,
    "strings": 31,
    "synth": 21,
    "synth bus": 21,
    "tambourine": 14,
    "trumpet": 29,
    "viola": 31,
    "violin": 31,
    "vocal": 47,
    "vox": 47,
    "vox bus": 47,
    "white noise": 50,
    "wurl": 26

}


def get_all_tracks(doc):
    all_tracks = []
    for track in doc.tracks:
        all_tracks.append(track)
        if hasattr(track, "is_foldable") and track.is_foldable:
            all_tracks.extend(get_nested_tracks(track))
    return all_tracks


def get_nested_tracks(group_track):
    nested_tracks = []
    for track in group_track.canonical_parent.tracks:
        if hasattr(track, "is_grouped") and track.is_grouped and track.group_track == group_track:
            nested_tracks.append(track)
            if hasattr(track, "is_foldable") and track.is_foldable:
                nested_tracks.extend(get_nested_tracks(track))
    return nested_tracks


class ColorChanger(ControlSurface):
    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        app = Live.Application.get_application()
        self.doc = app.get_document()
        self.previous_track_ids = set(track._live_ptr for track in get_all_tracks(self.doc))

        # Assign colors to existing tracks on initialization
        self.schedule_message(0, self.assign_colors_to_existing_tracks)

        # Register the listener functions
        self.doc.add_tracks_listener(self.tracks_changed_listener)

        # Add name and clip listeners for all current tracks
        for track in get_all_tracks(self.doc):
            track.add_name_listener(partial(self.track_name_changed_listener, track))
            for clip_slot in getattr(track, "clip_slots", []):
                try:
                    clip_slot.add_has_clip_listener(partial(self.clip_changed_listener, track, clip_slot))
                except Exception:
                    pass

    # --------------------------------------------------------
    # CORE COLOR FUNCTION
    # --------------------------------------------------------
    def assign_track_color(self, track):
        """Assigns color to a track and its clips based on keywords in its name."""
        try:
            track_name = (track.name or "").lower()
        except Exception:
            track_name = ""

        lower_case_track_colors = {k.lower(): v for k, v in track_colors.items()}

        for keyword, color_index in sorted(lower_case_track_colors.items(), key=lambda x: -len(x[0])):
            if keyword and keyword in track_name:
                try:
                    track.color_index = color_index
                except Exception:
                    pass

                # Color all session clips
                for clip_slot in getattr(track, "clip_slots", []):
                    try:
                        if getattr(clip_slot, "has_clip", False):
                            clip = getattr(clip_slot, "clip", None)
                            if clip:
                                clip.color_index = color_index
                    except Exception:
                        pass

                # Color arrangement clips (if available)
                try:
                    for arr_clip in getattr(track, "arrangement_clips", []):
                        arr_clip.color_index = color_index
                except Exception:
                    pass

                break  # stop after first match

    # --------------------------------------------------------
    # INITIAL ASSIGNMENT
    # --------------------------------------------------------
    def assign_colors_to_existing_tracks(self):
        for track in get_all_tracks(self.doc):
            self.schedule_message(0, partial(self.assign_track_color, track))

    # --------------------------------------------------------
    # TRACK + CLIP LISTENERS
    # --------------------------------------------------------
    def tracks_changed_listener(self):
        """Called when tracks are added or deleted."""
        current_track_ids = set(track._live_ptr for track in self.doc.tracks)
        self.schedule_message(0, lambda: self.handle_track_change(current_track_ids))

    def handle_track_change(self, current_track_ids):
        new_track_ids = current_track_ids - self.previous_track_ids
        self.previous_track_ids = current_track_ids

        for track in self.doc.tracks:
            if track._live_ptr in new_track_ids:
                self.assign_track_color(track)
                track.add_name_listener(partial(self.track_name_changed_listener, track))
                for clip_slot in getattr(track, "clip_slots", []):
                    try:
                        clip_slot.add_has_clip_listener(partial(self.clip_changed_listener, track, clip_slot))
                    except Exception:
                        pass

    def track_name_changed_listener(self, track):
        """Called when a track is renamed."""
        self.schedule_message(0, lambda: self.assign_track_color(track))

    def clip_changed_listener(self, track, clip_slot):
        """Called when a clip appears/disappears in a slot."""
        def _do():
            try:
                if getattr(clip_slot, "has_clip", False):
                    clip = getattr(clip_slot, "clip", None)
                    if clip:
                        clip.color_index = getattr(track, "color_index", None)
            except Exception:
                pass

        self.schedule_message(0, _do)

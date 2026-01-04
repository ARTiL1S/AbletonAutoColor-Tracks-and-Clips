import Live
from ableton.v2.control_surface import ControlSurface
from functools import partial

# Dictionary of track names and their corresponding color indices
track_colors = {
    "808": 14,
    "ambiance": 39,
    "arp": 11,
    "bass": 14,
    "bass bus": 14,
    "bell": 2,
    "brass": 1,
    "bridge": 40,
    "bridge": 54,
    "cello": 15,
    "chime": 1,
    "chorus": 68,
    "clarinet": 1,
    "clap": 3,
    "crash": 3,
    "cymbal": 3,
    "drone": 10,
    "drum": 3,
    "drum bus": 17,
    "flute": 2,
    "foley": 30,
    "fx": 26,
    "gtr": 18,
    "gtr bus": 5,
    "guitar": 18,
    "guitar bus": 5,
    "harp": 0,
    "hat": 3,
    "hook": 68,
    "horns": 15,
    "impact": 39,
    "interlude": 51,
    "intro": 59,
    "intro": 34,
    "kalimba": 0,
    "keys": 29,
    "kick": 3,
    "mallet": 6,
    "organ": 28,
    "outro": 63,
    "pad": 10,
    "perc": 2,
    "phantom": 55,
    "piano": 0,
    "pink noise": 39,
    "pluck": 7,
    "pno": 0,
    "post": 67,
    "post": 66,
    "pre": 62,
    "pre": 67,
    "rhodes": 0,
    "rim": 3,
    "riser": 39,
    "sfx": 24,
    "shaker": 3,
    "snap": 3,
    "snare": 3,
    "string": 29,
    "synth": 7,
    "synth bus": 21,
    "tambourine": 1,
    "trumpet": 1,
    "verse": 61,
    "viola": 29,
    "violin": 29,
    "vocal": 38,
    "vocal bus": 13,
    "vox": 38,
    "vox bus": 13,
    "white noise": 39,
    "wurl": 0


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

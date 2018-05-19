import base64
from reaper_python import *

MAXLEN = 1048567
MIDI_ON = 0x90
MIDI_OFF = 0x80

DIRECTED = {
        11: "[directed_duo_kg]",
        12: "[directed_duo_kb]",
        13: "[directed_duo_gb]",
        14: "[directed_duo_kv]",
        15: "[directed_duo_bass]",
        16: "[directed_duo_guitar]",
        17: "[directed_duo_drums]",
        19: "[directed_crowd_b]",
        20: "[directed_crowd_g]",
        21: "[directed_drums_pnt]",
        26: "[directed_vocals_cls]",
        28: "[directed_crowdsurf]",
        29: "[directed_stagedive]",
        31: "[directed_bass_cam]",
        32: "[directed_keys_cam]",
        33: "[directed_guitar_cam_pt]",
        34: "[directed_guitar_cam_pr]",
        35: "[directed_vocals_cam_pt]",
        36: "[directed_vocals_cam_pr]",
        38: "[directed_keys]",
        39: "[directed_guitar]",
        40: "[directed_bass]",
        41: "[directed_vocals]",
        43: "[directed_drums]",
        45: "[directed_keys_np]",
        46: "[directed_vocals_np]",
        47: "[directed_guitar_np]",
        48: "[directed_bass_np]",
        49: "[directed_drums_np]",
        51: "[directed_brej]",
        52: "[directed_bre]",
        53: "[directed_all_yeah]",
        55: "[directed_all_cam]",
        56: "[directed_all]"
}

DIRECTED_FREEBIES = {
        10: "[directed_crowd]",
        23: "[directed_drums_kd]",
        24: "[directed_guitar_cls]",
        25: "[directed_bass_cls]",
        42: "[directed_drums_lt]",
        54: "[directed_all_lt]",
}

CAMERA = {
        58: "[coop_gk_near]",
        59: "[coop_gk_behind]",
        60: "[coop_bk_near]",
        61: "[coop_bk_behind]",
        62: "[coop_bg_near]",
        63: "[coop_bg_behind]",
        64: "[coop_kv_near]",
        65: "[coop_kv_behind]",
        66: "[coop_gv_near]",
        67: "[coop_gv_behind]",
        68: "[coop_bv_near]",
        69: "[coop_bv_behind]",
        70: "[coop_dg_near]",
        71: "[coop_bd_near]",
        72: "[coop_dv_near]",
        74: "[coop_k_closeup_head]",
        75: "[coop_k_closeup_hand]",
        76: "[coop_g_closeup_head]",
        77: "[coop_g_closeup_hand]",
        78: "[coop_b_closeup_head]",
        79: "[coop_b_closeup_hand]",
        80: "[coop_v_closeup]",
        81: "[coop_d_closeup_head]",
        82: "[coop_d_closeup_hand]",
        84: "[coop_k_near]",
        85: "[coop_k_behind]",
        86: "[coop_g_near]",
        87: "[coop_g_behind]",
        88: "[coop_b_near]",
        89: "[coop_b_behind]",
        90: "[coop_v_near]",
        91: "[coop_v_behind]",
        92: "[coop_d_near]",
        93: "[coop_d_behind]",
        95: "[coop_front_near]",
        96: "[coop_front_behind]",
        98: "[coop_all_near]",
        99: "[coop_all_far]",
        100: "[coop_all_behind]"
}

LIGHTS_SINGLE = {
        10: "[bonusfx_optional]",
        11: "[bonusfx]",
        30: "[next]",
        31: "[prev]",
        32: "[first]"
}

LIGHTING = {
        13: "[lighting (bre)]",
        14: "[lighting (flare_fast)]",
        15: "[lighting (flare_slow)]",
        16: "[lighting (blackout_spot)]",
        17: "[lighting (blackout_fast)]",
        18: "[lighting (blackout_slow)]",
        19: "[lighting (strobe_fast)]",
        20: "[lighting (strobe_slow)]",
        21: "[lighting (sweep)]",
        22: "[lighting (searchlights)]",
        23: "[lighting (silhouettes_spot)]",
        24: "[lighting (silhouettes)]",
        25: "[lighting (frenzy)]",
        26: "[lighting (harmony)]",
        27: "[lighting (loop_warm)]",
        28: "[lighting (loop_cool)]",
        34: "[lighting (stomp)]",
        35: "[lighting (dischord)]",
        36: "[lighting (manual_warm)]",
        37: "[lighting (manual_cool)]",
        38: "[lighting (chorus)]",
        39: "[lighting (verse)]"
}

POSTPROCS = {
        41: "[space_woosh.pp]",
        42: "[ProFilm_psychedelic_blue_red.pp]",
        43: "[ProFilm_mirror_a.pp]",
        44: "[photo_negative.pp]",
        45: "[horror_movie_special.pp]",
        46: "[film_contrast_red.pp]",
        47: "[film_contrast_green.pp]",
        48: "[film_contrast_blue.pp]",
        49: "[film_contrast.pp]",
        50: "[desat_posterize_trails.pp]",
        51: "[flicker_trails.pp]",
        52: "[video_trails.pp]",
        53: "[clean_trails.pp]",
        54: "[posterize.pp]",
        55: "[bright.pp]",
        57: "[video_security.pp]",
        58: "[desat_blue.pp]",
        59: "[film_blue_filter.pp]",
        60: "[photocopy.pp]",
        61: "[contrast_a.pp]",
        62: "[video_bw.pp]",
        63: "[film_b+w.pp]",
        64: "[film_silvertone.pp]",
        65: "[film_sepia_ink.pp]",
        66: "[bloom.pp]",
        67: "[shitty_tv.pp]",
        68: "[film_16mm.pp]",
        69: "[video_a.pp]",
        70: "[ProFilm_b.pp]",
        71: "[ProFilm_a.pp]"
}

class MIDINote:

    def __init__(self, rpos, apos, status, note, velocity):
        self.rpos = rpos
        self.apos = apos
        self.status = status
        self.note = note
        self.velocity = velocity

    def __repr__(self):
        return "E %d %x %x %x" % (self.rpos, self.status, self.note, self.velocity)

class MIDIEvent:

    def __init__(self, rpos, apos, status, encText):
        self.rpos = rpos
        self.apos = apos
        self.status = status
        self.encText = encText
        self.text = base64.b64decode(str(encText))[2:]

    def __repr__(self):
        s = "<X %d %x\n%s\n>" % (self.rpos, self.status, self.encText)
        return s

        
class MIDITrackData:

    def __init__(self, chunk, midi_start, midi_end, notes):
        self.chunk = chunk
        self.midi_start = midi_start
        self.midi_end = midi_end
        self.notes = notes

    def __repr__(self):
        tok = self.chunk.split('\n')
        text = '\n'.join(tok[0:self.midi_start]) + '\n'

        for note in self.notes:
            text = text + str(note) + '\n'

        text = text + '\n'.join(tok[self.midi_end:])
        return text

def dict_merge(dicts):
    merged = {}
    for d in dicts:
        for k, v in d.iteritems():
            merged.setdefault(k, []).append(v)

    return merged

def get_venuegen_item(title):
    item_names = {}
    for i in range(RPR_CountMediaItems(0)):
        m = RPR_GetMediaItem(0, i)
        mt = RPR_GetMediaItemTake(m, 0)
        name = RPR_GetSetMediaItemTakeInfo_String(mt, "P_NAME", "", 0)[3]
        if len(name) > 0: 
            item_names[name.lower().split()[0].strip()] = m

    if title in item_names:
        return item_names[title]

    return None

def get_midi_data(item):
    notes_array = []
    notes_pos = 0

    start_midi = 0
    end_midi = 0

    chunk = RPR_GetSetItemState(item, "", MAXLEN)[2].strip()
    vars_array = chunk.split('\n')

    i = 0
    while i < len(vars_array):
        note = ""
        if vars_array[i].startswith("E ") or vars_array[i].startswith("e "):
            if start_midi == 0: start_midi = i
            note = vars_array[i].split(" ")
            if len(note) >= 5:
                decval = int(note[3], 16) # MIDI note value
                notes_pos = notes_pos + int(note[1]) # Ticks since last note
                status = int(note[2], 16)
                velocity = int(note[4], 16)
                n = MIDINote(int(note[1]), notes_pos, status, decval, velocity) 
                notes_array.append(n)
        elif vars_array[i].startswith("<X") or vars_array[i].startswith("<x"):
            if start_midi == 0: start_midi = i
            note = vars_array[i].split(" ")
            if len(note) >= 2:
                notes_pos = notes_pos + int(note[1])
                encText = vars_array[i+1]
                status = int(note[2])
                e = MIDIEvent(int(note[1]), notes_pos, status, encText)
                notes_array.append(e)
                i = i + 2
        else:
            if start_midi != 0 and end_midi == 0: end_midi = i

        i = i + 1

    data = MIDITrackData(chunk, start_midi, end_midi, notes_array)

    return data

def write_midi_data(item, data):
    RPR_GetSetItemState(item, str(data), MAXLEN)

def recalculate_positions(MIDIdata):
    if len(MIDIdata.notes) < 2: return

    MIDIdata.notes[0].rpos = MIDIdata.notes[0].apos

    i = 1
    for i in range(len(MIDIdata.notes)):
        note = MIDIdata.notes[i]
        prev = MIDIdata.notes[i-1]

        # Ignore the note on/note off events
        if note.status != 0xb0 and prev.status != 0xb0:
            note.rpos = note.apos - prev.apos

def encode_text_event(text):
    hx = "ff01" + text.encode("hex")
    return base64.encodestring(hx.decode("hex")).strip()

def add_text_event(MIDIdata, apos, text):
    e = MIDIEvent(0, apos, 0, encode_text_event(text))
 
    for i in range(len(MIDIdata.notes)):
        if MIDIdata.notes[i].apos > apos:
            break

    if i == 0: e.rpos = apos
    MIDIdata.notes.insert(i, e)
    recalculate_positions(MIDIdata)


def remove_events(MIDIdata):
    new_notes = []

    for note in MIDIdata.notes:
        if isinstance(note, MIDINote):
            new_notes.append(note)

    MIDIdata.notes = new_notes
    recalculate_positions(MIDIdata)

def venue_generate(item, MIDIdata, mapping, map_range, event_on_off):
    if len(MIDIdata.notes) <= 1: return
    to_add = []
    notes = [note for note in MIDIdata.notes if isinstance(note, MIDINote) and note.note in map_range]

    for i in range(len(notes) - 1):
        note = notes[i]
        if note.note in mapping: 
            if note.status == MIDI_ON:
                to_add.append((note.apos, note.note))
            elif note.status == MIDI_OFF:
                nxt = notes[i+1]
                if event_on_off and note.apos != nxt.apos: 
                    to_add.append((note.apos, note.note))
                
    if notes[i] in mapping and notes[i].status == MIDI_ON:
        to_add.append((notes[i].apos, notes[i].note))

    for element in to_add:
        add_text_event(MIDIdata, element[0], mapping[element[1]])
    
def main():
    cam_item = get_venuegen_item("camera")

    if cam_item is None:
        RPR_MB("Could not find a CAMERA MIDI item.", "VenueGen", 0)
        return 1

    data = get_midi_data(cam_item)

    remove_events(data)
    cam_range = dict_merge((DIRECTED, DIRECTED_FREEBIES, CAMERA))
    venue_generate(cam_item, data, DIRECTED, cam_range, False)
    venue_generate(cam_item, data, DIRECTED_FREEBIES, cam_range, True)
    venue_generate(cam_item, data, CAMERA, cam_range, False)
    write_midi_data(cam_item, data)

    light_item = get_venuegen_item("lighting")

    if light_item is None:
        RPR_MB("Could not find a LIGHTING MIDI item.", "VenueGen", 0)
        return 1

    data = get_midi_data(light_item)

    remove_events(data)
    light_range = dict_merge((LIGHTS_SINGLE, LIGHTING))
    venue_generate(light_item, data, LIGHTS_SINGLE, light_range, False)
    venue_generate(light_item, data, LIGHTING, light_range, True)
    venue_generate(light_item, data, POSTPROCS, POSTPROCS, True)
    write_midi_data(light_item, data)

if __name__ == "__main__":
    main()

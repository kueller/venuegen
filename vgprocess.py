# Functions for venue generation. 
#    - Basic note->event mapping.
#    - Random camera generator.
#    - AutoStrobe.
#    - Copying events to VENUE track.

import random
from vgreaper import *
from vgmidi import (
        MIDI_ON, MIDI_OFF, MIDINote, MIDIEvent, 
        add_text_event, remove_notes, remove_events 
)

RANDOM = 102
STROBE = 8

# Dummy camera level higher than any of them
MAX_LEVEL = 9
TICKS = 480

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
        100: "[coop_all_behind]",
}

CAMERA_LEVELS = {
        58: 7,  # [coop_gk_near]
        59: 7,  # [coop_gk_behind]
        60: 6,  # [coop_bk_near]
        61: 6,  # [coop_bk_behind]
        62: 5,  # [coop_bg_near]
        63: 5,  # [coop_bg_behind]
        64: 4,  # [coop_kv_near] 
        65: 4,  # [coop_kv_behind]
        66: 3,  # [coop_gv_near] 
        67: 3,  # [coop_gv_behind] 
        68: 2,  # [coop_bv_near] 
        69: 2,  # [coop_bv_behind] 
        70: 1,  # [coop_dg_near] 
        71: 1,  # [coop_bd_near] 
        72: 0,  # [coop_dv_near] 
        74: 8,  # [coop_k_closeup_head]
        75: 8,  # [coop_k_closeup_hand]
        76: 2,  # [coop_g_closeup_head]
        77: 2,  # [coop_g_closeup_hand]
        78: 1,  # [coop_b_closeup_head]
        79: 1,  # [coop_b_closeup_hand]
        80: 0,  # [coop_v_closeup]
        81: 0,  # [coop_d_closeup_head]
        82: 0,  # [coop_d_closeup_hand]
        84: 8,  # [coop_k_near]
        85: 8,  # [coop_k_behind]
        86: 2,  # [coop_g_near]
        87: 2,  # [coop_g_behind]
        88: 1,  # [coop_b_near]
        89: 1,  # [coop_b_behind]
        90: 0,  # [coop_v_near]
        91: 0,  # [coop_v_behind]
        92: 0,  # [coop_d_near]
        93: 0,  # [coop_d_behind]
        95: 0,  # [coop_front_near]
        96: 0,  # [coop_front_behind]
        98: 0,  # [coop_all_near]
        99: 0,  # [coop_all_far]
        100:0   # [coop_all_behind] 
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

STROBE_VALUES = (4, 8, 16, 32, 104, 108, 116)

def reverse_dict(d):
    return {v: k for k, v in d.iteritems()}

def dict_merge(dicts):
    merged = {}
    for d in dicts:
        merged.update(d)

    return merged

# The spacing of notes, in ticks, for a subdivision.
# Over 100 becomes a tuplet.
def strobe_value(velocity):
    if velocity < 100:
        return 480 // (velocity // 4)
    else:
        return 320 // ((velocity - 100) // 4)

# Adds flare/blackout fast alternating underneath a strobe note duration.
# Same rules of fading are applied.
def apply_strobe_notes(MIDIdata):
    notes = [note for note in MIDIdata.notes if isinstance(note, MIDINote)]
    strobe_notes = [note for note in notes if note.note is STROBE]

    strobe_events = (LIGHTING[14], LIGHTING[17]) # Fast flare and blackout
    strobe_pos = 0

    for i in range(len(strobe_notes)):
        note = strobe_notes[i]
        to_add = []
        if note.status == MIDI_ON and note.velocity in STROBE_VALUES:
            spacing = strobe_value(note.velocity) // 2
            to_add.append((note.apos, strobe_events[0]))

            if (i+1) >= len(strobe_notes):
                vg_error("Invalid STROBE note.")
                return

            current_pos = note.apos + spacing
            end_pos = strobe_notes[i+1].apos
            strobe_pos = 1

            while current_pos < end_pos:
                to_add.append((current_pos, strobe_events[strobe_pos]))
                strobe_pos ^= 1
                current_pos = current_pos + spacing

        elif note.status == MIDI_OFF:
            full_pos = notes.index(note)
            if (full_pos+1) < len(notes) and notes[full_pos+1].apos != note.apos:
                to_add.append((note.apos, strobe_events[strobe_pos]))

        for element in to_add:
            add_text_event(MIDIdata, element[0], element[1], "text")

# Index for where in the notes by time structure the random note is.
# Random note should still be in that indexed list.
# There should be no random notes before.
def add_random_event(MIDIdata, notes_by_time, index):
    CAMERA_INV = reverse_dict(CAMERA)

    currents = notes_by_time[index]
    for i in range(len(currents)):
        if isinstance(currents[i], MIDINote):
            break

    rnote = currents.pop(i)

    min_level = MAX_LEVEL
    if len(currents) > 0:
        min_level = min([CAMERA_LEVELS[CAMERA_INV[n]] for n in currents])

    blacklist = currents
    if index > 0:
        blacklist += notes_by_time[index-1]
    if index < len(notes_by_time) - 1:
        blacklist += [isinstance(n, str) for n in notes_by_time[index+1]]

    valids = []
    for note in CAMERA:
        if CAMERA[note] in blacklist:
            continue
        if CAMERA_LEVELS[note] > 0 and min_level == 0:
            continue
        if CAMERA_LEVELS[note] >= min_level and min_level > 0:
            continue
        valids.append(note)

    random_event = random.choice(valids)
    notes_by_time[index].append(random_event)
    add_text_event(MIDIdata, rnote.apos, CAMERA[random_event], "text")

# Venue should already be generated before calling.
def apply_random_notes(MIDIdata):
    valid_notes = []
    for note in MIDIdata.notes:
        if isinstance(note, MIDIEvent) and note.text in CAMERA.values():
            valid_notes.append(note)
        elif isinstance(note, MIDINote) and note.note == RANDOM and note.status == MIDI_ON:
            valid_notes.append(note)

    # Creates a 2 dimensional array. Each list represents an apos
    # and contains all the events in that apos.
    notes_by_time = []
    for i in range(len(valid_notes)):
        note = valid_notes[i]

        if i <= 0:
            if isinstance(note, MIDINote):
                notes_by_time.append([note])
            elif isinstance(note, MIDIEvent):
                notes_by_time.append([note.text])
        else:
            prev = valid_notes[i-1]
            if note.apos == prev.apos:
                if isinstance(note, MIDINote):
                    notes_by_time[-1].append(note)
                elif isinstance(note, MIDIEvent):
                    notes_by_time[-1].append(note.text)
            else:
                if isinstance(note, MIDINote):
                    notes_by_time.append([note])
                elif isinstance(note, MIDIEvent):
                    notes_by_time.append([note.text])
    
    for i in range(len(notes_by_time)):
        if any([isinstance(n, MIDINote) for n in notes_by_time[i]]):
            add_random_event(MIDIdata, notes_by_time, i)

# mapping: Dictionary of notes->events that will be generated.
# map_range: Dictionary of notes-> containing all the valid notes to 
#            look at. This may be different from "mapping" to account for
#            start and end times even for notes that might not be mapped.
# event_on_off: If true, add event at the end of note to "fade" it.
def section_generate(MIDIdata, mapping, map_range, event_on_off):
    if len(MIDIdata.notes) <= 1: return
    to_add = []
    notes = [note for note in MIDIdata.notes if isinstance(note, MIDINote) and note.note in map_range]
    if len(notes) <= 1: return

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
        add_text_event(MIDIdata, element[0], mapping[element[1]], "text")
    
# Does everything.
def generate_venue():
    cam_item = get_reaper_item("camera")

    if cam_item is None:
        vg_error("Could not find a \"CAMERA\" track.")
        return 1

    data = get_midi_data(cam_item)

    remove_events(data)
    cam_range = dict_merge((DIRECTED, DIRECTED_FREEBIES, CAMERA))
    section_generate(data, DIRECTED, cam_range, False)
    section_generate(data, DIRECTED_FREEBIES, cam_range, True)
    section_generate(data, CAMERA, cam_range, False)
    apply_random_notes(data)
    write_midi_data(cam_item, data)

    light_item = get_reaper_item("lighting")

    if light_item is None:
        vg_error("Could not find a \"LIGHTING\" track.")
        return 1

    data = get_midi_data(light_item)

    remove_events(data)
    light_range = dict_merge((LIGHTS_SINGLE, LIGHTING, {8: "strobe"}))
    section_generate(data, LIGHTS_SINGLE, light_range, False)
    section_generate(data, LIGHTING, light_range, True)
    section_generate(data, POSTPROCS, POSTPROCS, True)
    apply_strobe_notes(data)
    write_midi_data(light_item, data)

# Takes a list of event NAMES (not note numbers)
def filter_venue_events(VENUEdata, event_filter):
    ven_events_readd = []
    for note in VENUEdata.notes:
        if isinstance(note, MIDINote):
            ven_events_readd.append(note)
        elif isinstance(note, MIDIEvent):
            if note.text not in event_filter:
                ven_events_readd.append(note)

    VENUEdata.notes = ven_events_readd

def copy_camera_to_venue():
    cam_item = get_reaper_item("camera")
    if cam_item is None: 
        vg_error("Could not find the \"CAMERA\" track.")
        return 

    venue_item = get_reaper_item("venue")
    if venue_item is None: 
        vg_error("Could not find the \"VENUE\" track.")
        return

    cam_events = CAMERA.values() + DIRECTED.values() + DIRECTED_FREEBIES.values()

    venue_data = get_midi_data(venue_item)

    existing_events = False
    for note in venue_data.notes:
        if isinstance(note, MIDIEvent) and note.text in cam_events:
            existing_events = True
            break

    if existing_events:
        r = vg_verify("CAMERA events exist in \"VENUE\". Replace with new generated events?")
        if r != YES:
            return

    filter_venue_events(venue_data, cam_events)

    cam_data = get_midi_data(cam_item)

    for note in cam_data.notes:
        if isinstance(note, MIDIEvent):
            add_text_event(venue_data, note.apos, note.text, "text")

    write_midi_data(venue_item, venue_data)

def copy_lights_to_venue():
    light_item = get_reaper_item("lighting")
    if light_item is None:
        vg_error("Could not find the \"LIGHTING\" track.")
        return

    venue_item = get_reaper_item("venue")
    if venue_item is None: 
        vg_error("Could not find the \"VENUE\" track.")
        return

    light_events = LIGHTING.values() + LIGHTS_SINGLE.values() + POSTPROCS.values()

    venue_data = get_midi_data(venue_item)

    existing_events = False
    for note in venue_data.notes:
        if isinstance(note, MIDIEvent) and note.text in light_events:
            existing_events = True
            break

    if existing_events:
        r = vg_verify("Light events exist in \"VENUE\". Replace with new generated events?")
        if r != YES:
            return

    filter_venue_events(venue_data, light_events)

    light_data = get_midi_data(light_item)

    for note in light_data.notes:
        if isinstance(note, MIDIEvent):
            add_text_event(venue_data, note.apos, note.text, "text")

    write_midi_data(venue_item, venue_data)


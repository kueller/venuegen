# Functions for event->note mapping.

from vgreaper import *
from vgmidi import (
        MIDI_ON, MIDI_OFF, MIDIEvent, MIDINote, add_note, remove_notes, remove_events
)

from vgprocess import (
        DIRECTED, DIRECTED_FREEBIES, CAMERA, LIGHTS_SINGLE, LIGHTING, POSTPROCS, 
        dict_merge, reverse_dict
)

SINGLE_LEN = 480 // (32 // 4) # 32nd note

def verify_overwrite(MIDIdata, name):
    r = YES
    existing_notes = False
    for note in MIDIdata.notes:
        if isinstance(note, MIDINote):
            existing_events = True
            break

    if existing_events:
        r = vg_verify("Notes found in \"%s\" track. Delete and replace with pulled venue?" % name)
    return r

# Grab notes from a map_range that only need the MIDI_ON (no fades)
# Note: map_range is an inverted dictionary from vgprocess.
#       It should translate event names->note numbers.
def pull_single_instance(data_src, data_dst, map_range):
    for note in data_src.notes:
        if isinstance(note, MIDIEvent) and note.text in map_range:
            pitch = map_range[note.text]
            add_note(data_dst, note.apos, MIDI_ON, pitch, 64)
            add_note(data_dst, note.apos + SINGLE_LEN, MIDI_OFF, pitch, 0)

# Map range should not contain overlapping notes
# Do not mix post-procs and lighting, only one effect can be on at a time.
def pull_faded_instance(data_src, data_dst, map_range):
    valid_notes = []
    for note in data_src.notes:
        if isinstance(note, MIDIEvent) and note.text in map_range:
            valid_notes.append(note)

    if len(valid_notes) == 0: return

    pitch = map_range[valid_notes[0].text]
    add_note(data_dst, valid_notes[0].apos, MIDI_ON, pitch, 64)

    event_active = True
    for i in range(1, len(valid_notes)):
        note = valid_notes[i]
        pitch = map_range[note.text]

        if valid_notes[i].text == valid_notes[i-1].text and event_active:
            add_note(data_dst, note.apos, MIDI_OFF, pitch, 0)
            event_active = False
        elif valid_notes[i].text == valid_notes[i-1].text and not event_active:
            add_note(data_dst, note.apos, MIDI_ON, pitch, 64)
            event_active = True
            if i == len(valid_notes) - 1:
                add_note(data_dst, note.apos + SINGLE_LEN, MIDI_OFF, pitch, 0)
        elif valid_notes[i].text != valid_notes[i-1].text and event_active:
            last_pitch = map_range[valid_notes[i-1].text]
            add_note(data_dst, note.apos, MIDI_OFF, last_pitch, 0)
            add_note(data_dst, note.apos, MIDI_ON, pitch, 64)
            if i == len(valid_notes) - 1:
                add_note(data_dst, note.apos + SINGLE_LEN, MIDI_OFF, pitch, 0)
        elif valid_notes[i].text != valid_notes[i-1].text and not event_active:
            add_note(data_dst, note.apos, MIDI_ON, pitch, 64)
            event_active = True
            if i == len(valid_notes) - 1:
                add_note(data_dst, note.apos + SINGLE_LEN, MIDI_OFF, pitch, 0)

def pull_camera_from_venue():
    cam_item = get_reaper_item("camera")
    if cam_item is None: 
        vg_error("Could not find the \"CAMERA\" track.")
        return 

    venue_item = get_reaper_item("venue")
    if venue_item is None: 
        vg_error("Could not find the \"VENUE\" track.")
        return

    single_cam_range = reverse_dict(dict_merge((CAMERA, DIRECTED)))

    cam_data = get_midi_data(cam_item)
    venue_data = get_midi_data(venue_item)

    if verify_overwrite(cam_data, "CAMERA") != YES:
        return

    remove_events(cam_data)
    remove_notes(cam_data)

    pull_single_instance(venue_data, cam_data, single_cam_range)

    # Since all directed cuts work independent of each other
    # in regards to fades it's best to process them all individually.
    for cut, note in reverse_dict(DIRECTED_FREEBIES).iteritems():
        pull_faded_instance(venue_data, cam_data, { cut: note })

    write_midi_data(cam_item, cam_data)

def pull_lighting_from_venue():
    light_item = get_reaper_item("lighting")
    if light_item is None:
        vg_error("Could not find the \"LIGHTING\" track.")
        return

    venue_item = get_reaper_item("venue")
    if venue_item is None: 
        vg_error("Could not find the \"VENUE\" track.")
        return

    single_light_range = reverse_dict(LIGHTS_SINGLE)
    faded_lights_range = reverse_dict(LIGHTING)
    faded_procs_range = reverse_dict(POSTPROCS)

    light_data = get_midi_data(light_item)
    venue_data = get_midi_data(venue_item)

    if verify_overwrite(light_data, "LIGHTING") != YES:
        return

    remove_events(light_data)
    remove_notes(light_data)

    pull_single_instance(venue_data, light_data, single_light_range)
    pull_faded_instance(venue_data, light_data, faded_lights_range)
    pull_faded_instance(venue_data, light_data, faded_procs_range)

    write_midi_data(light_item, light_data)
    

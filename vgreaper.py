# All interactions with the REAPER API.

from reaper_python import *
from vgmidi import MIDINote, MIDIEvent, MIDITrackData

MAXLEN = 1048567            # Max string length, stolen from CAT.
YES = 6                     # Return values from RPR_MB
NO = 7

# Pop-up error message.
def vg_error(message):
    RPR_MB(message, "venuegen", 0)

# Logs to the REAPER console. Should only be used for debugging.
def vg_log(message):
    RPR_ShowConsoleMsg(message)
    RPR_ShowConsoleMsg('\n')

# 6 = yes, 7 = no
def vg_verify(message):
    return RPR_MB(message, "venuegen", 4)

def get_reaper_item(title):
    # Iterate over all tracks and pull the track name and MediaTrack item
    tracks = {}
    for i in range(RPR_CountTracks(0)):
        t = RPR_GetTrack(0, i)

        try:
            t_name = RPR_GetSetMediaTrackInfo_String(t, "P_NAME", "", 0)[3]
        except UnicodeDecodeError:
            vg_error("One of your track names has special characters" \
                    "not allowed by Reaper. Make sure your track names" \
                    "use only basic characters and try again.")
            return None

        # Empty item check.
        if len(t_name) > 0:
            tracks[t_name.lower().strip()] = t

    if title not in tracks:
        return None

    icount = RPR_CountTrackMediaItems(tracks[title])
    if icount == 0: return None

    # Iterate over all items and find ones that are in the proper track.
    matched_items = []
    for i in range(RPR_CountMediaItems(0)):
        m = RPR_GetMediaItem(0, i)
        if RPR_GetMediaItem_Track(m) == tracks[title]:
            matched_items.append(m)

    if len(matched_items) == 0: return None

    # Media item found is the one we want. Ignore dupes.
    return matched_items[0]

def get_midi_data(item):
    notes_array = []
    notes_pos = 0

    start_midi = 0
    end_midi = 0

    # Grab the full MIDI track text. 
    chunk = RPR_GetSetItemState(item, "", MAXLEN)[2].strip()
    vars_array = chunk.split('\n')

    # Create MIDINote or MIDIEvent objects based off the relevant
    # entries in the "chunk". 
    # MIDI notes are in the form
    #     E [relative position )] [status] [note number] [velocity]
    #     (relative position is in decimal, the rest are in hex)
    # MIDI events are in the form
    #     <X [relative position] [status]
    #     [encoded text]
    #     (relative pos in decimal, status in hex. Encoded text is 
    #     a two byte header and the event text in base64)
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

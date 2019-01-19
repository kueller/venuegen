# MIDI note and event classes and functions that deal with them.

import base64

MIDI_ON = 0x90
MIDI_OFF = 0x80

# rpos: Number of ticks from the previous MIDI note/event (relative position).
# apos: Number of ticks from the start of the track (absolute position).
# status: Either MIDI_ON or MIDI_OFF.
# note: The number value of the MIDI note [0-127].
# velocity: Value of the velocity [0-127]
class MIDINote:

    def __init__(self, rpos, apos, status, note, velocity):
        self.rpos = rpos
        self.apos = apos
        self.status = status
        self.note = note
        self.velocity = velocity

    def __repr__(self):
        return "E %d %x %x %x" % (self.rpos, self.status, self.note, self.velocity)

# encText: Encoded text in base64 with MIDI event header.
# text: Plain text without the header (what the event would say)
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
        
# chunk: The entire text of the MIDI data from the REAPER API.
# midi_start: The line where the MIDI notes/events begin.
# midi_end: The line where they end.
# notes: A list of either MIDINote of MIDIEvent objects.
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

# Rewrites the rpos values of a MIDI notes array based on the apos values.
# venuegen works in apos values, but the MIDI standard (and what will 
# be written) uses rpos. This should be called after changes to the 
# MIDI notes/events array.
# This function is internal.
def recalculate_positions(MIDIdata):
    if len(MIDIdata.notes) < 2: return

    MIDIdata.notes[0].rpos = MIDIdata.notes[0].apos

    for i in range(1, len(MIDIdata.notes)):
        note = MIDIdata.notes[i]
        prev = MIDIdata.notes[i-1]

        # Ignore the note on/note off events
        if note.status != 0xb0 and prev.status != 0xb0:
            note.rpos = note.apos - prev.apos

# Adds the header and encodes MIDI event text to base64.
def encode_text_event(text, header):
    hx = header + text.encode("hex")
    return base64.encodestring(hx.decode("hex")).strip()

# Inserts a text event at apos to a MIDI array.
# etype: "text" for TEXT EVENT or "name" for TRACK NAME.
def add_text_event(MIDIdata, apos, text, etype):
    if etype == "text":
        e = MIDIEvent(0, apos, 0, encode_text_event(text, "ff01"))
    elif etype == "name":
        e = MIDIEvent(0, apos, 0, encode_text_event(text, "ff03"))
 
    for i in range(len(MIDIdata.notes)):
        if MIDIdata.notes[i].apos > apos:
            break

    if i == 0: e.rpos = apos
    MIDIdata.notes.insert(i, e)
    recalculate_positions(MIDIdata)

# Adds MIDI note at position apos.
def add_note(MIDIdata, apos, status, pitch, velocity):
    if status not in (MIDI_ON, MIDI_OFF): return
    n = MIDINote(0, apos, status, pitch, velocity)

    i = 0
    for i in range(len(MIDIdata.notes)):
        if MIDIdata.notes[i].apos > apos:
            break

    if i == 0: n.rpos = apos
    MIDIdata.notes.insert(i, n)
    recalculate_positions(MIDIdata)

# These two functions remove *all* the notes/events in a track.
def remove_notes(MIDIdata):
    new_notes = []

    for note in MIDIdata.notes:
        if isinstance(note, MIDIEvent):
            new_notes.append(note)

    MIDIdata.notes = new_notes
    recalculate_positions(MIDIdata)

def remove_events(MIDIdata):
    new_notes = []

    for note in MIDIdata.notes:
        if isinstance(note, MIDINote):
            new_notes.append(note)

    MIDIdata.notes = new_notes
    recalculate_positions(MIDIdata)


# venuegen.py

Generate events for your VENUE track from standard MIDI notes.

## Usage

### Setup

Create two tracks in your Reaper project: CAMERA and LIGHTING. Add MIDI items to those tracks as you would any other and import the respective note names provided. You do not need to place a track name.

Place the script **venuegen.py** into a convenient location, such as the folder where you put the other scripts for CAT. Load it into Reaper from the actions menu under **ReaScript: New/Load...**

### Usage

Place MIDI notes accordingly when you want the events to appear. For single shot events such as `[next]` and all standard camera cuts, you only need to care where the note begins. For events that can transition, such as all post-processes, use an extended tube to signal the start of the effect and when it should start fading to the next. If you don't want it to fade, connect the end of the tube to the next note.

When all your notes are placed, run **venuegen.py** from the actions menu. You can run it as many times as you need as it updates. Copy the events from LIGHTING and CAMERA into VENUE, and remember to mute your venuegen tracks before exporting.

Don't worry, better documentation (with images) will come soon.

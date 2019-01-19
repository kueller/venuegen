# venuegen

VENUEGEN is a tool to make venue authoring for Rock Band a little easier. Instead of manually placing events, you can enter notes on a piano roll and this script will map the notes to the proper text events for you. No more digging through a mess of text events in the VENUE track or misspelling names.

Please note venuegen is an *advanced tool*. If you know nothing about venue authoring it is recommended you familiarize yourself with the general process in the official [RBN Docs](http://docs.c3universe.com/rbndocs/index.php?title=RBN2_Camera_And_Lights).

## Setup

In order for venuegen to work you will need to have ReaScript enabled and the latest [Python 2.x](https://www.python.org/downloads/) installed. The process is the same as setting up [CAT](http://customscreators.com/index.php?/topic/10662-c3-automation-tools/) (which you should be using anyways). CAT has a good setup guide in its documentation.

Download venuegen from this GitHub page and keep the folder wherever you'd like (maybe in the same place you would put CAT). 

![REAPER Track Setup](https://i.imgur.com/ldgT6Rw.png)

Now in your Reaper template or current project create two new tracks called CAMERA and LIGHTING (**Ex. 1**). Add MIDI items to those tracks as you woud any other (Insert>New MIDI Item) and add the note names from CAMERA.txt and LIGHTING.txt respectively. You only need the names here. Unlike other tracks in the template you do not need a TRACK NAME event. The script would remove it anyways.

**NOTE:** It is recommended you mute the CAMERA and LIGHTING tracks. The notes in these tracks cannot be exported to Magma or it will generate errors. Since venuegen will still work even if those tracks are muted, there is no reason to ever unmute them.

Now in the Actions menu (Actions>Show Actions List...) using the **ReaScript: New/Load...** button, add the file **venuegen.py** from the venuegen folder you extracted (**Ex. 2**)

![Action Menu](https://i.imgur.com/yt5al6S.png)

## Basic Usage

### Interface

![venuegen GUI](https://i.imgur.com/xvTT7Wt.png)

Running venuegen from the actions menu will bring up the GUI shown in **Ex. 3**. The commands are straightforward with the primary function being the actual note to event mapping that is done by "Generate!". For this to have any effect notes will have to be placed in the CAMERA and LIGHTING tracks. This general process is introduced in the following sections.

**NOTE:** Unlike CAT, venuegen will not close automatically after finishing a function, and relies on you manually closing the window. This is because workflow will likely lead you to use "Generate!" and the copy functions in succession.

### CAMERA

Placing standard camera cuts in the piano roll (avoiding ones with an asterisk for now) then open venuegen and run "Generate!" will result in the corresponding events automatically placed. You can also stack notes to create stacked camera cut events. **Ex. 4.1** and **4.2** show the CAMERA track before and after running venuegen.

![CAMERA track before](https://i.imgur.com/tbkFRg5.png)

![CAMERA track after](https://i.imgur.com/8d4y6Tj.png)

Most directed cuts will have unpredictable start and end times due to pre and post roll (see the docs for more info). However, the directed cuts **All LT**, **Drums LT**, **Bass CLS**, **Gtr CLS**, **Drums KD**, and **Crowd** can have predictable start and end times so long as you add two of the same cut in a row.

To make this easier, in venuegen those cuts will generate two events: one at the start of the note and one at the end (**Ex. 5**). The placement of the end event does not matter so long as it is before the next camera cut.

![Directed Gtr CLS with two events](https://i.imgur.com/3ZKktjM.png)

### LIGHTING

In the LIGHTING track, the notes **first**, **prev**, **next**, **BONUSFX**, and **BONUSFX Opt** will generate an event only at the start of the note, the same way most camera cuts work. An example of using **first** and **next** is below in **Ex. 6**.

![next events generating single events](https://i.imgur.com/NZ8NlhA.png)

For all other lighting notes, the space between the notes will determine the transition time between the effects. If there is no space between the two notes, an event will be placed only at the start of the note as before. If there *is* space between two notes, an event will be added at the end of the first note and the time in between will be the transition. See the examples below.

![Two events with no space](https://i.imgur.com/t3yqKig.png)

**Example 7.1:** The **Desat Posterize** event will switch immediately to the **Film Contrast Red** event since there is no space in between the notes.

![Two events with space](https://i.imgur.com/ALX6Xrh.png)

**Example 7.2:** The **Bright** note has space before **Film Contrast Green**, so an extra event is added at the end of **Bright** to cause a cross-fade transition of the two effects for the duration of the open space.

## Advanced Features

### Autostrobe

At the bottom of the LIGHTING track notes is a STROBE note. This function works similar to the **Strobe Slow** and **Strobe Fast** in-game lighting effects, but with more control. 

The STROBE note should be the duration of the strobe effect you would like to have. The velocity will determine the frequency of the strobe. Velocities of 4, 8, 16, and 32 will result in strobe frequencies of quarter, 8th, 16th, and 32nd notes respectively. You can also do triplet spacings by adding 100 to the velocities. Velocities of 104, 108, and 116 will result in strobe frequencies of quarter triplet, 8th triplet, and 16th triplet. 

**NOTE:** Strobe "frequency" refers to how fast the lights will "flash". Each flash requires two events to turn the lights on, then off. This is similar behavior to the included strobe lighting effects.

After generating, the autostrobe note will generate alternating events of **Flare Fast** and **Blackout Fast**. 

**NOTE:** The strobe events are placed in relation to the start of the STROBE note. They do not inherently sync to a grid. You can verify all this in **Ex. 8** below for velocity 8 and 16.

![Example of two STROBE notes](https://i.imgur.com/9sOkNOs.png)

### RANDOM

![Example of RANDOM](https://i.imgur.com/kq8G2Ap.png)

The CAMERA track gives the option of a RANDOM note. By itself, the random note will choose a random cut from the set of standard camera cuts (*not directed cuts*). If RANDOM is stacked with existing cuts though, it will choose a cut of lower *precedence*. The official docs have a rough order on which cuts have higher precendence. Below is a full list of the behaviors of the RANDOM note.

* RANDOM will choose a random standard camera cut lower than the lowest precedence shot it is stacked with. If the RANDOM note is alone precedence is not a factor.
* The random generated event will be different from the previous and next camera cuts. If there are stacked cuts preceding and following the cut it will be different from all of them. Do not stack every single event to see what happens.
* RANDOM does check other RANDOM notes. It is possible to have an entire track of RANDOM notes and be guaranteed a sequence of camera cuts where no cuts repeat twice in a row.
* Directed cuts are not taken into account, due to their unpredictable nature. They are treated as the highest precedence.
* RANDOM will generate a new random event each time. If you like the result it gives you, change that to a static note.

### Reverse

If you have an old venue and would like to edit it using venuegen, you can use the "Pull [] from VENUE" options in the venuegen GUI. If you have the CAMERA and LIGHTING tracks properly setup these functions will do the "reverse" and populate those tracks with the appropriate MIDI notes. 

The result should be notes that will generate the same events as in the VENUE. The automatic note generation is sufficient but not perfect yet, and this will be improved upon over time.

![Existing venue](https://i.imgur.com/K9HUA0u.png)

**Example 10.1:** The venue opening of [STAND PROUD](http://customscreators.com/index.php?/page/index.html/_/stand-proud-r20907) as it was originally authored in the VENUE track using only events.

![After venuegen reverse](https://i.imgur.com/uofWBJm.png)

**Example 10.2:** The same section, now in LIGHTING track after running venuegen in reverse. 

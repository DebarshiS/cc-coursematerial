# Info on Recording the Videos

## What we record
* Theory modules; 
  * when there are exercises inside: just mention the exercise and the learning goal, but then continue
* For exercises: intro to exercise (short) and discussion of solution code (together in one video, separate with marker)

## VM Settings

For console demos change these settings:
* Click on Ubuntu `Settings` (top right), then `System Settings...` - `Appearance`- `Behavior`- `Show menus for a window`: select `in the window's title bar`
* Use the default terminal profile (defines colors as using system theme)
* Set color prompt: Edit `~/.bashrc`, uncomment the line that sets `force_color_prompt`. This turns the command prompt green so it is easy to see what is command and what is output.

## Recording parameters / settings in Camtasia

General parameters
* Slides are recorded in 4x3 format; **recording dimension is 1280 X 960 or higher; recommended: 1440 x 1080 **
* Code demos should be recorded in 16x9 format. **recording dimension is 1600 X 900 or higher like (1920 x 1080)**
* Windows: Taskbar --> properties --> autohide task bar (hide task bar in full screen recordings)

Settings within VM for recording
* We want to record terminal command and output in the default color settings.
* If for some reason we want to change to white background, it can be done this way:
  * Terminal window: `$ export CF_COLOR=false`  (no color output from CF)
  * Create profile 'black on white' to use for recording command line demos
   * `Edit - Profiles... - New`
    * Enter name e.g. black-on-white
   * Tab Colors: Uncheck `use colors from system theme`, then select from buil-in schemes 'Black on white'.
   * Close
 * Select the black on white profile: `Terminal - Change Profile`
  

## How to record and where
* For 'slides recordings' we go into the studio (WDF18 F4) so that our face / upper body can show in the video. (see M2 videos)
* Start with header slide of chapter
* For demos we can add the word 'DEMO' as overlay in the production of the video

## Video editing and production 
* If there is a 'system audio' track, click on it and lock it so it will not be part of the produced audio.
* Cut out stuff you do not want (all editing)
* Check audio quality and see if you need noise reduction and/or volume leveling
* When you want to put 'table of contents' markers in the video, add a marker at the right place in the video (editing view) by hitting `M`.
* To generate video: Use `File - Produce and Share` in Camtasia
  * Select `Custom production settings`, `MP4 - Smart Player`, 
  * `Controller` tab: make sure `produce with controller` is checked, 
  * `Size`: Both `Embed size` as well as `Video size` have to be set to the recording dimension (1440x1080)
  * `Video settings`: set `video quality` to 75%
  * `Next` ... `Finish`



# Technical Reference

## Engineering and Control

### Routing

A fundamental aspect of any TV studio is the ability to route signals. Routing allows for flexible control over which video sources are sent to which destinations without physically reconnecting cables. This is essential in a live production environment where multiple sources may be switched or displayed simultaneously for operators and for the different shows and their requirements.

The most common requirements for routing would be for multiviewers, vision engineering monitoring and changing which sources are available to the vision mixer.

=== "Multiviewers"

    * Multiple sources on a single screen
    * Operator can change what they see in front of them
    * Under monitor displays (UMDs) change reflecting the routed source

=== "Vision Engineering"

    * GPIs from RCPs connected to a control panel
    * Touchdowns from each RCP change what appears on the Vision Eng monitor instantly

=== "Vision Mixer Sources"

    * Show dependent routing of different sources
    * Button labels change automatically
    * Don't need to do routing within the vision mixer itself

The router in the TV studio can handle a large number of inputs and outputs. It is currently set to be 80x120 (in the format of INPUTSxOUTPUTS). This is a non-standard configuration but as the router works on a card/backplane (modular) system, the full capacity of the router (128x128) hasn't been reached. This means that we can change and expand the system to allow for varying sizes and types of IO. The router currently has 3G SDI cards for first 64 inputs and outputs, and HD-SDI cards for the rest. This means the studio is limited to HD-SDI as that is the highest format available everywhere. Having such a large number of inputs and outputs can make managing the routing quite difficult, so we rely on a...

### Broadcast Control System



#### Categories

#### Routemaster

Combination of all the routers

#### Salvos

Running pre-saved configutations

## Vision Mixer

### Key Links

Manuals:

## Record/Replay, VT Playback and EVS

In the TV Studio, we have an EVS XT3 server with a machine running IP Director. The XT3 server is an 8-channel record/replay system where there are 8 channels available to either record or replay. The default configuration is six record channels and two replay channels (6x2). Having two replay channels is useful as we have two controllers (LSM) which can control each output.

``` mermaid
flowchart LR
    RouterOutputs["Router Outputs"] -->|Input 1| EVS["EVS Server"]
    RouterOutputs -->|Input 2| EVS
    RouterOutputs -->|Input 3| EVS
    RouterOutputs -->|Input 4| EVS
    RouterOutputs -->|Input 5| EVS
    RouterOutputs -->|Input 6| EVS
    
    EVS -->|"Output 1 (Red)"| RouterInputs["Router Inputs"]
    EVS -->|"Output 2 (Blue)"| RouterInputs

    classDef box fill:#f9f,stroke:#333,stroke-width:2px;
    class EVS box;

    linkStyle default interpolate basis;
```

The EVS server records continuously on its record channels, sharing the remaining disk space equally; similar to how a CCTV system works. The saving of and addition of clips reduces the available record time.

All the record channels are routable from the Cerebrum control system, meaning any six sources can be recorded. Usually, this would be the main program output, a clean program output (this is the main program output without any downstream keys such as graphics), the three studio cameras and the studio PTX camera.

|                       |         6x2 ProRes         |   4x4 ProRes    | 6x2 DNxHD  | 4x4 DNxHD  |
| :-------------------- | :------------------------: | :-------------: | :--------: | :--------: |
| Record Channels       |             6              |        4        |     6      |     4      |
| Playback Channels     |             2              |        4        |     2      |     4      |
| Video Codec           |      ProRes 422 (SQ)       | ProRes 422 (SQ) | DNxHD 120  | DNxHD 120  |
| Audio Codec           |         PCM 48kHz          |    PCM 48kHz    | PCM 48kHz  | PCM 48kHz  |
| Video Wrapper         |            MOV             |       MOV       | MOV or MXF | MOV or MXF |
| Audio Record Input    | MADI from Calrec Brio desk |      MADI       |    MADI    |    MADI    |
| Audio Playback Output |  MADI to Calrec Brio desk  |      MADI       |    MADI    |    MADI    |


## Graphics with CasparCG

### Fill/Key Channels

A critical property of graphics channels is that they overlay only the necessary content on top of sources. In a baseband studio environment, if you were to simply overlay a graphic signal of a lower third, for example, on top of your program output, you would just see that lower third signal with which has the content of the lower third and the rest of the picture would be black. This is not the desired outcome. Therefore, graphics systems such as CasparCG can utilise the use of fill and key signals to allow the correct transparency to be processed in the appropriate areas.

``` mermaid
graph LR
    subgraph GFX_PC [GFX PC]
        GFX1[Channel 1]
        GFX2[Channel 2]
    end
    
    GFX1 -->|Fill| Vision_Mixer
    GFX1 -->|Key| Vision_Mixer
    GFX2 -->|Fill| Vision_Mixer
    GFX2 -->|Key| Vision_Mixer
    
    Vision_Mixer["Vision Mixer (via Router)"]

```

The vision mixer takes the fill and key signals and, through the use of a linear key, overlays the fill by using the information of the key signal to only show the appropriate part of the signal. Where the fill would be your standard colour signal, the key is a black to white signal. The vision mixer will not show any of the fill signal where the key is black. It will show 100% of the key signal where the key is white. If the key is grey (e.g. 50% gray), the overlayed fill signal will be translucent. This is done on a pixel-by-pixel basis and affects only the transparency of the fill signal.

Looking at one of the channels from the CasparCG configuration file, we can see how the channels are setup to be the appropriate format with the appropriate properties depending on the required outputs:

``` xml title="Channel 1 of casparcgconfig.xml"
<channel>
    <video-mode>1080i5000</video-mode> <!-- (1) -->
    <consumers>
        <decklink> <!--(2)-->
            <device>1</device>
            <key-device>2</key-device>
            <embedded-audio>true</embedded-audio>
            <latency>normal</latency>
            <keyer>external</keyer> <!-- (3) -->
            <key-only>false</key-only>
            <buffer-depth>10</buffer-depth>
            <custom-allocator>true</custom-allocator>
        </decklink>
        <ndi> <!-- (4) -->
            <name>GFX Ch.1</name>
            <allow-fields>false</allow-fields>
        </ndi>
    </consumers>
</channel>
```

1. The video format is declared to match the format used in the studio. It is in the format of `Vertical pixel count` `progressive/interlaced` `frame rate (x100 so that non integer frame rates don't use decimals in the declaration)`.
2. The main output to be used for the channel is a Decklink device. This is a Blackmagic Design PCIe card that sits inside the PC that outputs the channel over **SDI** connections.
3. The keyer will be external i.e. another device will do the processing for the key: the vision mixer. Therefore a **fill and a key signal will be output** from this consumer.
4. Here we also declare one of the consumers to be an NDI Output. This makes it available to view over the network.

## Sound

## Comms

One of the most vital parts of a studio and to keep a production running is the comms system. This allows people to communicate with each other across positions and rooms, avoiding the need to constantly traverse rooms to talk to operators and instruct them.

The TV studio uses an RTS ODIN talkback system as it's matrix. The matrix is reponsible for connecting all the panels and other signals together to ensure that the right person is heard at the right time. This can often be an incredibly complex configuration of different types of keys (the buttons on a keypanel that a user presses down) that can do a variety of things. But it can be built up by thinking first and foremost of the requirements and reviewing the feasibility of them. Once that has been considered the configuration of the comms system can begin.

### Physical Equipment and IO Options

The ODIN sits in the machine room and keypanels and are at each operator's position. The ODIN offers both phyisical and network ports, AIO (Analogue Input Output) and OMNEO (this is Dante with essentially a control layer on top) respectively. We have a 32-channel license which allows 32 ports to be confirgured. It's important to note that it is not just operators' panels that need to be configured as ports, it is also signals between talent that need to be carefully considered, specifically clean feeds and pre-hears, as summarised in the IFB section. The sound mixer can deliver aux outputs to the comms system over Dante for 

### Configuration

To configure all the aspects of how the comms system works, the following softwares are used.

#### IPEdit

IP port configuration and management

#### AZEdit

General port configuration

#### NEO

A new product from RTS.

### Panels

#### Talk Keys



#### Listen Keys



### IFBs

#### Configuration of IFBs

## Rundown Creator

Rundown Creator 



## Teleprompting, Rundowns and Scripts

### Rundown Creator

Rundown creator is a web-based rundown software that allows for the creation of rundowns and scripts for multiple shows. It works on the premise that a show is split into items based on the content or topic, similar to scenes in a film. Each item can have a script written for that item. The inclusion of different types of brackets in a script can change how the script is formatted on the teleprompter.

### Autoscript WinPlus-IP

It's important to note that the communication is one-way. Changes made in WinPlus-IP will not be reflected in Rundown Creator.

## Lighting

## Vision Engineering

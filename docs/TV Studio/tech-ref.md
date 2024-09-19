# Technical Reference

## Record/Replay, VT Playback and EVS

In the TV Studio, we have an EVS XT3 server with a machine running IP Director. The XT3 server is an 8-channel record/replay system where there are 8 channels available to either record or replay. The default configuration is six record channels and two replay channels (6x2). Having two replay channels is useful as we have two controllers (LSM) which can control each output.

The EVS records continuously on its record channels, sharing the remaining disk space equally; similar to how a CCTV system works. The addition of clips reduces the available record time.

All the record channels are routable from the Cerebrum control system, meaning any six sources can be recorded. Usually, this would be the main program output and the three studio cameras.

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

## Rundown Creator

## Vision Mixer

### Key Links

## Sound

## Comms

## Engineering and Control

## Autocue

## Lighting

## Vision Engineering

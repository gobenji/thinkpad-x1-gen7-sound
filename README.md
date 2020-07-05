# Description
Patches to improve the behavior of the audio system on the Lenovo Thinkpad X1
Carbon 7th gen. These should also be applicable to the X1 Yoga 4th gen.

Improvements compared to the mainline driver:
* max sound output level is raised
  See [this
  analysis](https://gist.github.com/hamidzr/dd81e429dc86f4327ded7a2030e7d7d9#gistcomment-3214171)
* independent control of output level on the two sets of speakers (front/back
  aka. tweeters/woofers)

Issues:
* There is some slight "pop" in headphones when content volume transitions
  to/from 0. This is especially easy to notice with voice content where there
  are pauses of silence. For example, I can hear it when listening to the
  first 15s of [this video](https://youtu.be/DmtpQZVzm1A)

  Also present on mainline.

# How to use
I've tested the patches under Debian Unstable with a self-compiled kernel,
patched alsa ucm profile and the rest (steps 2, 3, 4) of [these
instructions](https://gist.github.com/hamidzr/dd81e429dc86f4327ded7a2030e7d7d9#gistcomment-3204561).

Both the kernel driver (snd_hda_codec_realtek) and the alsa ucm profile must
be patched. On Debian, the ucm file to patch is found under
`/usr/share/alsa/ucm2/sof-hda-dsp/`

Note that the ucm patch is over alsa-ucm-conf commit 38e5906cd1b1
("sof-hda-dsp: fix the device order (Hdmi devices)"). At the moment
(alsa-ucm-conf git head ffe0cab5cfce ("sof-hda-dsp: use
sof-hda-dsp/Hdmi.conf")), newer versions do not work for me (with or without
the changes in this repository).

If you try the patches, please send me a mail to let me know of your results.
You can also open an issue here or post a comment in the above gist which has
become a forum for audio issues with the X1 Carbon 7th gen.

# Userspace alternative
Instead of patching the kernel, it is possible to use the `hda-verb` utility
(available from the "alsa-tools" package on Debian) to achieve a similar
effect. This can be done temporarily by running:
```
hda-verb /dev/snd/hwC0D0 0x17 SET_CONNECT_SEL 1
```

To make the effect persistent, two changes must be done:
1. The fixup must be applied each time the device is initialized, ie. at boot
   and after resume from S3 suspend AFAIK. A sample systemd service file to do
   so has been posted
   [here](https://gist.github.com/hamidzr/dd81e429dc86f4327ded7a2030e7d7d9#gistcomment-3345062).
2. In order to have effective volume control, pulseaudio must use the "Master"
   volume slider. To do so, the relevant ucm profile must be changed according
   to the patch found
   [here](https://gist.github.com/hamidzr/dd81e429dc86f4327ded7a2030e7d7d9#gistcomment-3335517).
   The patch is slightly different than the one contained in this repository
   because there is no renamed control to key off of.

# How to check that the fix has been applied correctly
To check that the kernel changes or hda-verb command are effective, run
```
root@f3:~# hda-verb /dev/snd/hwC0D0 0x17 GET_CONNECT_SEL 0
nid = 0x17, verb = 0xf01, param = 0x0
value = 0x1
```
Critically, "value" should be "0x1".

To check that the ucm profile changes are effective, start alsamixer on the X1
audio device in one terminal, `alsamixer -c sofhdadsp`. At the same time, run
`pavucontrol`. In the "Output Devices" tab, locate the "Cannon Point-LP High
Definition Audio Controller Speaker + Headphones" section, select the "Speaker"
port and adjust the volume to different values within 0-100% while looking at
alsamixer. In alsamixer, you should see the level of the "Master" mixer
changing. Change the port to "Headphones" and repeat the same test.

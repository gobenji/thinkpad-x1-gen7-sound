# Description
Patches to improve the behavior of the audio system on the Lenovo Thinkpad X1
Carbon 7th gen. These should also be applicable to the X1 Yoga 4th gen.

Improvements compared to the mainline driver:
* max sound output level is raised
  See [this
  analysis](https://gist.github.com/hamidzr/dd81e429dc86f4327ded7a2030e7d7d9#gistcomment-3214171)

Remaining issues:
* There is a slight "pop" in headphones when content volume transitions
  to/from 0. This is especially easy to notice with voice content where there
  are pauses of silence. For example, I can hear it when listening to the
  first 4s of [this video](https://youtu.be/2ZrWHtvSog4)

  Also present on mainline and in Windows.

I've tested the patches in this repository under Debian Unstable with a
self-compiled kernel and the rest (steps 2, 3, 4) of
[these
instructions](https://gist.github.com/hamidzr/dd81e429dc86f4327ded7a2030e7d7d9#gistcomment-3204561).

If you try the patches, please send me a mail to let me know of your results.
You can also open an issue here or post a comment in the above gist which has
become a forum for audio issues with the X1 Carbon 7th gen.

# How to enable the fixup in the patch
In order for the changes in this patch to be effective, they have to be
explicitly enabled using a module parameter. That parameter depends on which
driver model is in use: the new SOF driver architecture or the legacy mode.

Determine which driver architecture is in use:
* SOF
```
$ lspci -v
[...] Audio device: Intel Corporation Cannon Point-LP High Definition Audio Controller (rev 11) (prog-if 80)
[...]
        Kernel driver in use: sof-audio-pci
$ cat /proc/asound/cards
 0 [sofhdadsp      ]: sof-hda-dsp - sof-hda-dsp
                      LENOVO-20QDCTO1WW-ThinkPadX1Carbon7th
```

In this case, you need to specify the following module parameter:
```
snd_sof_intel_hda_common.hda_model=alc285-tpx1-dual-speakers
```

The hda_model module parameter was added by commit b8d3ad51dfec ("ASoC:
snd-sof-intel-hda-common - add hda_model parameter and pass it to HDA codec
driver", v5.8-rc1). If you want to try the patch over a kernel tree that
doesn't contain that commit, you must cherry-pick it first.

* legacy
```
$ lspci -v
[...] Audio device: Intel Corporation Cannon Point-LP High Definition Audio Controller (rev 11) (prog-if 80)
        [...]
        Kernel driver in use: snd_hda_intel
$ cat /proc/asound/cards
 0 [PCH            ]: HDA-Intel - HDA Intel PCH
                      HDA Intel PCH at 0xfeb70000 irq 30
```

In this case, you need to specify the following module parameter:
```
snd_hda_intel.model=alc285-tpx1-dual-speakers
```

Usually the sound modules are loaded during boot. The parameter can be
specified in different ways, I use a modprobe configuration file, ex:
```
$ cat /etc/modprobe.d/snd_sof.conf
options snd_sof_intel_hda_common hda_model=alc285-tpx1-dual-speakers
```

# How to check that the fix has been applied correctly
In order to check that the process of applying the patch, recompiling the
kernel, installing it, configuring the module parameter and booting the
correct kernel worked as expected, you can perform the following checks:

Add the following option to the kernel command line when booting:
```
snd_hda_codec.dyndbg=+p
```
and look for a message which indicates that the driver picked the expected
fixup ("alc285-tpx1-dual-speakers"):

```
# cat /proc/cmdline
[...] snd_hda_codec.dyndbg=+p
# journalctl -k -o short-monotonic -g "picked fixup"
[...]
[   38.082015] vsid kernel: snd_hda_codec_realtek hdaudioC0D0: ALC285: picked fixup alc285-tpx1-dual-speakers (model specified)
```

Run
```
$ cat /sys/class/sound/hwC0D0/modelname
alc285-tpx1-dual-speakers
```

Run
```
# hda-verb /dev/snd/hwC0D0 0x17 GET_CONNECT_SEL 0
nid = 0x17, verb = 0xf01, param = 0x0
value = 0x1
```
Critically, "value" should be "0x1".

Start `alsamixer` and adjust the level of the Headphone mixer. You should see
the level being mirrored by the Speaker mixer and vice-versa. This is the most
important difference with this new version of the patch compared to v2
submitted upstream.

# PCB Scanner

This is a proof of concept: use an Anet A8 3D printer to scan
a PCB and create a very big image.

## Getting started

The main script is ``anet_scan.py``:

```
$ python3 -m pip install -r requirements.txt
$ python anet_scan.py <serial device path> <width in mm> <height in mm>
 ...
```

I advice to move manually the printer's head and position it so that the microscope
is at the lower left. The scan is done one columns at times, from the left to the right.

the resulting images are in the ``shoots/`` directory.

```
$ v4l2-ctl -d /dev/video0 --list-formats-ext
ioctl: VIDIOC_ENUM_FMT
        Type: Video Capture

        [0]: 'YUYV' (YUYV 4:2:2)
                Size: Discrete 640x480
                        Interval: Discrete 0.033s (30.000 fps)
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 160x120
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 176x144
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 352x288
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 320x240
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 1280x1024
                        Interval: Discrete 0.200s (5.000 fps)
                Size: Discrete 1600x1200
                        Interval: Discrete 0.200s (5.000 fps)
                Size: Discrete 640x480
                        Interval: Discrete 0.033s (30.000 fps)
                        Interval: Discrete 0.033s (30.000 fps)
```

```
$ ./anet_scan.py michelin_back \
    --video /dev/video0 \
    --printer /dev/ttyACM0 \
    --size 100x90 \
    --resolution 1600x1200 \
    --steps 15x12
```

## Microscope holder

There is a ``FreeCAD`` design file named ``microscope_holder.fcstd`` for the microscope
holder.

![](holder.png)

The microscope used is [this](https://www.aliexpress.com/item/High-Quality-2-0-MP-HD-Android-phones-500X-USB-digital-microscope-electron-microscope-enlarge-for/32697275807.html)
but anyone would work as well.

## Stitching images

This is the hardest part: you could use [Hugin](http://hugin.sourceforge.net/)
but my brain is uncapable of using this program.

The only reliable way I found is using [Imagej](ImageJ.net) via [Fiji](https://imagej.net/software/fiji/):
it has a stitching plugin that works pretty good.

https://forum.image.sc/t/is-there-a-way-to-run-fijis-stitching-from-a-script/11846/2
https://github.com/fmi-faim/imagej-scripts/blob/d9ffd7c9895f43d06749ba16633d70f716af5079/Stitch_ND_File_MIPs_With_STG_Info.groovy#L336-L382

### Setup

To improve the final result you need a constant light source (but remember that
the silkscreen is pretty reflective) and the PCB must be levelled.

I have not investigated extensively but you should measure the actual size in
millimeters of the view field and set the ``--steps`` parameters to be something
sensible (I used 50% overlap both in x and y).

This is important In the stitching process since the algorithm rely on that value.

#!/usr/bin/env bash
WSI_FILE='tests/CMU-1-JP2K-33005.svs'

docker run --rm -it -v $PWD:/data stevennhart/dicom_wsi

mkdir /data/tests/dicom_wsi
wget -O dicom_wsi/tests/CMU-1-JP2K-33005.svs http://openslide.cs.cmu.edu/download/openslide-testdata/Aperio/CMU-1-JP2K-33005.svs


############################################################################
# dicom_wsi
# Sparse
cd /dicom_wsi/dicom_wsi
time python3 cli.py -y yaml/base.yaml

#real	10m22.956s
#user	24m2.570s
#sys	2m30.750s

#-rw-r--r-- 1 root root 40381694 Jul 21 16:03 output.0-1.dcm
#-rw-r--r-- 1 root root 38814548 Jul 21 16:03 output.0-2.dcm
#-rw-r--r-- 1 root root   198434 Jul 21 16:04 output.0-3.dcm
#-rw-r--r-- 1 root root 41159894 Jul 21 16:00 output.1-0.dcm
#-rw-r--r-- 1 root root 11400090 Jul 21 15:59 output.2-0.dcm
#-rw-r--r-- 1 root root  2960996 Jul 21 15:58 output.3-0.dcm
#-rw-r--r-- 1 root root   758390 Jul 21 15:57 output.4-0.dcm
#-rw-r--r-- 1 root root   217884 Jul 21 15:56 output.5-0.dcm
#-rw-r--r-- 1 root root    68920 Jul 21 15:55 output.6-0.dcm

time python3 cli.py -y yaml/base.yaml

#real	11m24.203s
#user	29m3.130s
#sys	3m18.600s

#ll output-full.*
#-rw-r--r-- 1 root root  7545834 Jul 21 18:32 output-full.0-1.dcm
#-rw-r--r-- 1 root root 13499820 Jul 21 18:34 output-full.0-10.dcm
#-rw-r--r-- 1 root root 14668970 Jul 21 18:34 output-full.0-11.dcm
#-rw-r--r-- 1 root root   637894 Jul 21 18:34 output-full.0-12.dcm
#-rw-r--r-- 1 root root 19292156 Jul 21 18:32 output-full.0-2.dcm
#-rw-r--r-- 1 root root 16638596 Jul 21 18:32 output-full.0-3.dcm
#-rw-r--r-- 1 root root 16302772 Jul 21 18:33 output-full.0-4.dcm
#-rw-r--r-- 1 root root 16967452 Jul 21 18:33 output-full.0-5.dcm
#-rw-r--r-- 1 root root  6823428 Jul 21 18:33 output-full.0-6.dcm
#-rw-r--r-- 1 root root  4243950 Jul 21 18:33 output-full.0-7.dcm
#-rw-r--r-- 1 root root 18131540 Jul 21 18:33 output-full.0-8.dcm
#-rw-r--r-- 1 root root 19668180 Jul 21 18:34 output-full.0-9.dcm
#-rw-r--r-- 1 root root 19249022 Jul 21 18:30 output-full.1-1.dcm
#-rw-r--r-- 1 root root 14828314 Jul 21 18:30 output-full.1-2.dcm
#-rw-r--r-- 1 root root   156710 Jul 21 18:30 output-full.1-3.dcm
#-rw-r--r-- 1 root root 13974302 Jul 21 18:29 output-full.2-0.dcm
#-rw-r--r-- 1 root root  3510192 Jul 21 18:28 output-full.3-0.dcm
#-rw-r--r-- 1 root root   873234 Jul 21 18:27 output-full.4-0.dcm
#-rw-r--r-- 1 root root   236712 Jul 21 18:26 output-full.5-0.dcm
#-rw-r--r-- 1 root root    80436 Jul 21 18:25 output-full.6-0.dcm
############################################################################
# wsi2dcm

mkdir /data/tests/wsi2dcm

time wsi2dcm /data/tests/CMU-1-JP2K-33005.svs \
    --outFolder /data/tests/wsi2dcm \
    --batch 500 \
    --levels 6 \
    --sparse  \
    --jsonFile /data/dicom_wsi/yaml/google.json \
    --seriesDescription ''


#real	4m5.475s
#user	7m50.060s
#sys	2m11.020s

# ll /data/tests/wsi2dcm
#-rw-r--r--  1 root root  3682132 Jul 21 14:20 level-0-frames-0-500.dcm
#-rw-r--r--  1 root root 10950806 Jul 21 14:20 level-0-frames-1000-1500.dcm
#-rw-r--r--  1 root root 12777662 Jul 21 14:20 level-0-frames-1500-2000.dcm
#-rw-r--r--  1 root root  9814868 Jul 21 14:21 level-0-frames-2000-2500.dcm
#-rw-r--r--  1 root root 11842370 Jul 21 14:21 level-0-frames-2500-3000.dcm
#-rw-r--r--  1 root root  9870956 Jul 21 14:21 level-0-frames-3000-3500.dcm
#-rw-r--r--  1 root root 11024994 Jul 21 14:21 level-0-frames-3500-4000.dcm
#-rw-r--r--  1 root root 11658012 Jul 21 14:21 level-0-frames-4000-4500.dcm
#-rw-r--r--  1 root root 11075960 Jul 21 14:21 level-0-frames-4500-5000.dcm
#-rw-r--r--  1 root root  9339888 Jul 21 14:20 level-0-frames-500-1000.dcm
#-rw-r--r--  1 root root  6601434 Jul 21 14:21 level-0-frames-5000-5500.dcm
#-rw-r--r--  1 root root  3936334 Jul 21 14:21 level-0-frames-5500-6000.dcm
#-rw-r--r--  1 root root   545556 Jul 21 14:21 level-0-frames-6000-6072.dcm
#-rw-r--r--  1 root root 12135834 Jul 21 14:22 level-1-frames-0-500.dcm
#-rw-r--r--  1 root root 10957788 Jul 21 14:23 level-1-frames-1000-1500.dcm
#-rw-r--r--  1 root root   130290 Jul 21 14:23 level-1-frames-1500-1518.dcm
#-rw-r--r--  1 root root 14307314 Jul 21 14:22 level-1-frames-500-1000.dcm
#-rw-r--r--  1 root root 11045220 Jul 21 14:24 level-2-frames-0-391.dcm
#-rw-r--r--  1 root root  2562998 Jul 21 14:24 level-3-frames-0-108.dcm
#-rw-r--r--  1 root root   738322 Jul 21 14:24 level-4-frames-0-30.dcm
#-rw-r--r--  1 root root   183400 Jul 21 14:24 level-5-frames-0-9.dcm

# Non-Sparse
mkdir /data/tests/wsi2dcm_full
time wsi2dcm /data/tests/CMU-1-JP2K-33005.svs \
    --outFolder /data/tests/wsi2dcm_full \
    --batch 500 \
    --levels 6 \
    --jsonFile /data/dicom_wsi/yaml/google.json \
    --seriesDescription ''
#real	4m5.875s
#user	7m45.450s
#sys	2m17.700s

#ll /data/tests/wsi2dcm_full
#total 160656
#drwxr-xr-x 23 root root      782 Jul 21 18:21 ./
#drwxr-xr-x 14 root root      476 Jul 21 18:22 ../
#-rw-r--r--  1 root root  3638154 Jul 21 18:17 level-0-frames-0-500.dcm
#-rw-r--r--  1 root root 10906828 Jul 21 18:18 level-0-frames-1000-1500.dcm
#-rw-r--r--  1 root root 12733684 Jul 21 18:18 level-0-frames-1500-2000.dcm
#-rw-r--r--  1 root root  9770890 Jul 21 18:18 level-0-frames-2000-2500.dcm
#-rw-r--r--  1 root root 11798392 Jul 21 18:18 level-0-frames-2500-3000.dcm
#-rw-r--r--  1 root root  9826978 Jul 21 18:18 level-0-frames-3000-3500.dcm
#-rw-r--r--  1 root root 10981016 Jul 21 18:18 level-0-frames-3500-4000.dcm
#-rw-r--r--  1 root root 11614034 Jul 21 18:18 level-0-frames-4000-4500.dcm
#-rw-r--r--  1 root root 11031982 Jul 21 18:19 level-0-frames-4500-5000.dcm
#-rw-r--r--  1 root root  9295910 Jul 21 18:17 level-0-frames-500-1000.dcm
#-rw-r--r--  1 root root  6557456 Jul 21 18:19 level-0-frames-5000-5500.dcm
#-rw-r--r--  1 root root  3892356 Jul 21 18:19 level-0-frames-5500-6000.dcm
#-rw-r--r--  1 root root   539242 Jul 21 18:19 level-0-frames-6000-6072.dcm
#-rw-r--r--  1 root root 12091856 Jul 21 18:19 level-1-frames-0-500.dcm
#-rw-r--r--  1 root root 10913810 Jul 21 18:20 level-1-frames-1000-1500.dcm
#-rw-r--r--  1 root root   128728 Jul 21 18:20 level-1-frames-1500-1518.dcm
#-rw-r--r--  1 root root 14263336 Jul 21 18:20 level-1-frames-500-1000.dcm
#-rw-r--r--  1 root root 11010830 Jul 21 18:21 level-2-frames-0-391.dcm
#-rw-r--r--  1 root root  2553512 Jul 21 18:21 level-3-frames-0-108.dcm
#-rw-r--r--  1 root root   735700 Jul 21 18:21 level-4-frames-0-30.dcm
#-rw-r--r--  1 root root   182626 Jul 21 18:21 level-5-frames-0-9.dcm

############################################################################
# Orthanc

ORTHANC=/OrthancWSI-0.7/Applications/Build
OPENSLIDE_SO=/usr/lib/x86_64-linux-gnu/libopenslide.so

# Does not support sparse
mkdir /data/tests/orthanc
time ${ORTHANC}/OrthancWSIDicomizer \
    --openslide $OPENSLIDE_SO \
    --tile-width 500 \
    --tile-height 500 \
    --compression jpeg \
    --folder /data/tests/orthanc \
    --dataset /data/dicom_wsi/yaml/orthanc.json \
    --levels 6 \
    /data/tests/CMU-1-JP2K-33005.svs

# real	2m22.826s
# user	3m11.340s
# sys	0m13.340s

# ll /data/tests/orthanc
# total 228200
#drwxr-xr-x 28 root root      952 Jul 21 15:32 ./
#drwxr-xr-x 12 root root      408 Jul 21 15:32 ../
#-rw-r--r--  1 root root 10627664 Jul 21 15:30 wsi-000000.dcm
#-rw-r--r--  1 root root 10635642 Jul 21 15:30 wsi-000001.dcm
#-rw-r--r--  1 root root 10692802 Jul 21 15:30 wsi-000002.dcm
#-rw-r--r--  1 root root 10539846 Jul 21 15:30 wsi-000003.dcm
#-rw-r--r--  1 root root 10583316 Jul 21 15:30 wsi-000004.dcm
#-rw-r--r--  1 root root 10592238 Jul 21 15:30 wsi-000005.dcm
#-rw-r--r--  1 root root 10588276 Jul 21 15:30 wsi-000006.dcm
#-rw-r--r--  1 root root 10590780 Jul 21 15:30 wsi-000007.dcm
#-rw-r--r--  1 root root 10551470 Jul 21 15:30 wsi-000008.dcm
#-rw-r--r--  1 root root 10542238 Jul 21 15:31 wsi-000009.dcm
#-rw-r--r--  1 root root 10643190 Jul 21 15:31 wsi-000010.dcm
#-rw-r--r--  1 root root 10538202 Jul 21 15:31 wsi-000011.dcm
#-rw-r--r--  1 root root 10529330 Jul 21 15:31 wsi-000012.dcm
#-rw-r--r--  1 root root 10577544 Jul 21 15:31 wsi-000013.dcm
#-rw-r--r--  1 root root 10662052 Jul 21 15:31 wsi-000014.dcm
#-rw-r--r--  1 root root 10535622 Jul 21 15:31 wsi-000015.dcm
#-rw-r--r--  1 root root 10676706 Jul 21 15:31 wsi-000016.dcm
#-rw-r--r--  1 root root 10533190 Jul 21 15:31 wsi-000017.dcm
#-rw-r--r--  1 root root 10550288 Jul 21 15:31 wsi-000018.dcm
#-rw-r--r--  1 root root 10651652 Jul 21 15:31 wsi-000019.dcm
#-rw-r--r--  1 root root  8691920 Jul 21 15:32 wsi-000020.dcm
#-rw-r--r--  1 root root  2078562 Jul 21 15:32 wsi-000021.dcm
#-rw-r--r--  1 root root  5426992 Jul 21 15:32 wsi-000022.dcm
#-rw-r--r--  1 root root  4149192 Jul 21 15:32 wsi-000023.dcm
#-rw-r--r--  1 root root  1119634 Jul 21 15:32 wsi-000024.dcm
#-rw-r--r--  1 root root   318368 Jul 21 15:32 wsi-000025.dcm

#############################################################
# Validate

# dciodvfy /data/tests/wsi2dcm_full/level-5-frames-0-9.dcm
#Error - Number of values of DimensionIndexValues does not match number of items in DimensionIndexSequence for frame 1 got 1 - expected 2
#Error - Number of items in Per-frame Functional Groups Sequence does not match Number of Frames - have 1 items - but 9 frames
#Error - Value invalid for this VR - (0x0002,0x0012) UI Implementation Class UID  UI [0] = <1.2.276.0.7230010.3.0.> - Empty component
#Error - Dicom dataset contains invalid data values for Value Representations
#VLWholeSlideMicroscopyImage
#Error - Missing attribute Type 2 Required Element=<PositionReferenceIndicator> Module=<FrameOfReference>
#Error - Missing attribute Type 1 Required Element=<ConceptNameCodeSequence> Module=<AcquisitionContext>
#Error - Missing attribute Type 1C Conditional Element=<NumericValue> Module=<AcquisitionContext>
#Error - Missing attribute Type 1C Conditional Element=<Date> Module=<AcquisitionContext>
#Error - Missing attribute Type 1C Conditional Element=<Time> Module=<AcquisitionContext>
#Error - Missing attribute Type 1C Conditional Element=<PersonName> Module=<AcquisitionContext>
#Error - Missing attribute Type 1C Conditional Element=<TextValue> Module=<AcquisitionContext>
#Error - Missing attribute Type 1C Conditional Element=<ConceptCodeSequence> Module=<AcquisitionContext>
#Error - Missing attribute Type 1C Conditional Element=<SliceThickness> Module=<PixelMeasuresMacro>
#Error - Missing attribute Type 1 Required Element=<WholeSlideMicroscopyImageFrameTypeSequence> Module=<WholeSlideMicroscopyImageFrameTypeMacro>
#Error - Missing attribute Type 1C Conditional Element=<CodeValue> Module=<BasicCodeSequenceMacro>
#Error - Missing attribute Type 1 Required Element=<CodeMeaning> Module=<BasicCodeSequenceMacro>
#Error - Missing attribute Type 1C Conditional Element=<LongCodeValue> Module=<BasicCodeSequenceMacro>
#Error - Missing attribute Type 1C Conditional Element=<URNCodeValue> Module=<BasicCodeSequenceMacro>
#Error - Missing attribute Type 1C Conditional Element=<LocalNamespaceEntityID> Module=<HL7v2HierarchicDesignatorMacro>
#Error - Missing attribute Type 1C Conditional Element=<UniversalEntityID> Module=<HL7v2HierarchicDesignatorMacro>
#Error - Missing attribute Type 1 Required Element=<SpecimenPreparationStepContentItemSequence> Module=<SpecimenMacro>
#Error - Missing attribute Type 1C Conditional Element=<TotalPixelMatrixFocalPlanes> Module=<WholeSlideMicroscopyImage>
#Error - Missing attribute Type 1C Conditional Element=<NumberOfOpticalPaths> Module=<OpticalPath>
#Error - Missing attribute Type 1C Conditional Element=<ICCProfile> Module=<OpticalPath>
#Warning - Attribute is not present in standard DICOM IOD - (0x0028,0x0009) AT Frame Increment Pointer
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x072a) DS X Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x073a) DS Y Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x074a) DS Z Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021e) SL Column Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021f) SL Row Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021a) SQ Plane Position (Slide) Sequence

#dciodvfy /data/tests/orthanc/wsi-000025.dcm
#VLWholeSlideMicroscopyImage
#Error - Missing attribute Type 1 Required Element=<WholeSlideMicroscopyImageFrameTypeSequence> Module=<WholeSlideMicroscopyImageFrameTypeMacro>
#Error - Missing attribute Type 1 Required Element=<ContainerIdentifier> Module=<SpecimenMacro>
#Error - Missing attribute Type 1C Conditional Element=<TotalPixelMatrixFocalPlanes> Module=<WholeSlideMicroscopyImage>
#Error - Missing attribute Type 1C Conditional Element=<NumberOfOpticalPaths> Module=<OpticalPath>
#Warning - Coding Scheme Designator is deprecated - attribute <CodingSchemeDesignator> = <SRT>
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x072a) DS X Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x073a) DS Y Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x074a) DS Z Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021e) SL Column Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021f) SL Row Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021a) SQ Plane Position (Slide) Sequence
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x072a) DS X Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x073a) DS Y Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x074a) DS Z Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021e) SL Column Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021f) SL Row Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021a) SQ Plane Position (Slide) Sequence
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x072a) DS X Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x073a) DS Y Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x074a) DS Z Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021e) SL Column Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021f) SL Row Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021a) SQ Plane Position (Slide) Sequence
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x072a) DS X Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x073a) DS Y Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x074a) DS Z Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021e) SL Column Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021f) SL Row Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021a) SQ Plane Position (Slide) Sequence
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x072a) DS X Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x073a) DS Y Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x074a) DS Z Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021e) SL Column Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021f) SL Row Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021a) SQ Plane Position (Slide) Sequence
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x072a) DS X Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x073a) DS Y Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x074a) DS Z Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021e) SL Column Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021f) SL Row Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021a) SQ Plane Position (Slide) Sequence
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x072a) DS X Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x073a) DS Y Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x074a) DS Z Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021e) SL Column Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021f) SL Row Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021a) SQ Plane Position (Slide) Sequence
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x072a) DS X Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x073a) DS Y Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x074a) DS Z Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021e) SL Column Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021f) SL Row Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021a) SQ Plane Position (Slide) Sequence
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x072a) DS X Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x073a) DS Y Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x074a) DS Z Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021e) SL Column Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021f) SL Row Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021a) SQ Plane Position (Slide) Sequence
#Warning - Dicom dataset contains attributes not present in standard DICOM IOD - this is a Standard Extended SOP Class


#dciodvfy /data/tests/dicom_wsi/output-full.6-0.dcm
#VLWholeSlideMicroscopyImage
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x072a) DS X Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x073a) DS Y Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x074a) DS Z Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021e) SL Column Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021f) SL Row Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021a) SQ Plane Position (Slide) Sequence
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x072a) DS X Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x073a) DS Y Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x074a) DS Z Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021e) SL Column Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021f) SL Row Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021a) SQ Plane Position (Slide) Sequence
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x072a) DS X Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x073a) DS Y Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x074a) DS Z Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021e) SL Column Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021f) SL Row Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021a) SQ Plane Position (Slide) Sequence
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x072a) DS X Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x073a) DS Y Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0040,0x074a) DS Z Offset in Slide Coordinate System
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021e) SL Column Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021f) SL Row Position In Total Image Pixel Matrix
#Warning - Attribute is not present in standard DICOM IOD - (0x0048,0x021a) SQ Plane Position (Slide) Sequence
#Warning - Dicom dataset contains attributes not present in standard DICOM IOD - this is a Standard Extended SOP Class



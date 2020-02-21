WSI_FILE='/data/DICOM/CMU-1-JP2K-33005.svs'
WSI_TO_DICOM=/home/m087494/wsi-to-dicom-converter-1.0/build/

${WSI_TO_DICOM}/wsi2dcm \
    --input $WSI_FILE \
    --outFolder wsi2dcm \
    --batch 500 \
    --levels 6 \
    --sparse --jsonFile wsi2dcm/google.json  \
    --seriesDescription ''

# real    0m52.445s
# user    10m16.430s
# sys     0m4.419s

# ll wsi2dcm/
# total 161372
# drwxrwxr-x 2 m087494 m087494     4096 Feb 17 13:29 ./
# drwxrwxr-x 9 m087494 m087494     4096 Feb 17 16:31 ../
# -rw-rw-r-- 1 m087494 m087494     4432 Feb 17 13:28 google.json
# -rw-rw-r-- 1 m087494 m087494  3682150 Feb 17 13:29 level-0-frames-0-500.dcm
# -rw-rw-r-- 1 m087494 m087494 10950824 Feb 17 13:29 level-0-frames-1000-1500.dcm
# -rw-rw-r-- 1 m087494 m087494 12777680 Feb 17 13:29 level-0-frames-1500-2000.dcm
# -rw-rw-r-- 1 m087494 m087494  9814886 Feb 17 13:29 level-0-frames-2000-2500.dcm
# -rw-rw-r-- 1 m087494 m087494 11842388 Feb 17 13:29 level-0-frames-2500-3000.dcm
# -rw-rw-r-- 1 m087494 m087494  9870974 Feb 17 13:29 level-0-frames-3000-3500.dcm
# -rw-rw-r-- 1 m087494 m087494 11025012 Feb 17 13:29 level-0-frames-3500-4000.dcm
# -rw-rw-r-- 1 m087494 m087494 11658030 Feb 17 13:29 level-0-frames-4000-4500.dcm
# -rw-rw-r-- 1 m087494 m087494 11075978 Feb 17 13:29 level-0-frames-4500-5000.dcm
# -rw-rw-r-- 1 m087494 m087494  6601452 Feb 17 13:29 level-0-frames-5000-5500.dcm
# -rw-rw-r-- 1 m087494 m087494  9339906 Feb 17 13:29 level-0-frames-500-1000.dcm
# -rw-rw-r-- 1 m087494 m087494  3936352 Feb 17 13:29 level-0-frames-5500-6000.dcm
# -rw-rw-r-- 1 m087494 m087494   545574 Feb 17 13:29 level-0-frames-6000-6072.dcm
# -rw-rw-r-- 1 m087494 m087494 12135852 Feb 17 13:29 level-1-frames-0-500.dcm
# -rw-rw-r-- 1 m087494 m087494 10957806 Feb 17 13:29 level-1-frames-1000-1500.dcm
# -rw-rw-r-- 1 m087494 m087494   130308 Feb 17 13:29 level-1-frames-1500-1518.dcm
# -rw-rw-r-- 1 m087494 m087494 14307332 Feb 17 13:29 level-1-frames-500-1000.dcm
# -rw-rw-r-- 1 m087494 m087494 11045236 Feb 17 13:29 level-2-frames-0-391.dcm
# -rw-rw-r-- 1 m087494 m087494  2563014 Feb 17 13:29 level-3-frames-0-108.dcm
# -rw-rw-r-- 1 m087494 m087494   738338 Feb 17 13:29 level-4-frames-0-30.dcm
# -rw-rw-r-- 1 m087494 m087494   183416 Feb 17 13:29 level-5-frames-0-9.dcm


ORTHANC=/data/DICOM//OrthancWSI-0.6/Applications/Build
OPENSLIDE_SO=Anaconda/Openslide/lib/libopenslide.so
${ORTHANC}/OrthancWSIDicomizer \
    --openslide $OPENSLIDE_SO \
    --tile-width 500 \
    --tile-height 500 \
    --compression jpeg \
    --folder orthanc/ \
    --dataset orthanc/config.json \
    --levels 6 \
    CMU-1-JP2K-33005.svs

# real    0m29.681s
# user    2m55.895s
# sys     0m0.612s

# ll orthanc/
# total 164364
# drwxrwxr-x 2 m087494 m087494     4096 Feb 17 16:41 ./
# drwxrwxr-x 9 m087494 m087494     4096 Feb 17 16:31 ../
# -rw-rw-r-- 1 m087494 m087494     1132 Feb 17 16:41 config.json
# -rw-rw-r-- 1 m087494 m087494 10604128 Feb 17 16:41 wsi-000000.dcm
# -rw-rw-r-- 1 m087494 m087494 10654900 Feb 17 16:41 wsi-000001.dcm
# -rw-rw-r-- 1 m087494 m087494 10546418 Feb 17 16:41 wsi-000002.dcm
# -rw-rw-r-- 1 m087494 m087494 10547130 Feb 17 16:41 wsi-000003.dcm
# -rw-rw-r-- 1 m087494 m087494 10609930 Feb 17 16:41 wsi-000004.dcm
# -rw-rw-r-- 1 m087494 m087494 10606290 Feb 17 16:41 wsi-000005.dcm
# -rw-rw-r-- 1 m087494 m087494 10545648 Feb 17 16:41 wsi-000006.dcm
# -rw-rw-r-- 1 m087494 m087494 10568834 Feb 17 16:41 wsi-000007.dcm
# -rw-rw-r-- 1 m087494 m087494 10595070 Feb 17 16:41 wsi-000008.dcm
# -rw-rw-r-- 1 m087494 m087494 10551932 Feb 17 16:41 wsi-000009.dcm
# -rw-rw-r-- 1 m087494 m087494 10600434 Feb 17 16:41 wsi-000010.dcm
# -rw-rw-r-- 1 m087494 m087494 10547460 Feb 17 16:41 wsi-000011.dcm
# -rw-rw-r-- 1 m087494 m087494 10546466 Feb 17 16:41 wsi-000012.dcm
# -rw-rw-r-- 1 m087494 m087494 10611284 Feb 17 16:41 wsi-000013.dcm
# -rw-rw-r-- 1 m087494 m087494 10555520 Feb 17 16:41 wsi-000014.dcm
# -rw-rw-r-- 1 m087494 m087494  8757172 Feb 17 16:41 wsi-000015.dcm
# -rw-rw-r-- 1 m087494 m087494   207562 Feb 17 16:41 wsi-000016.dcm
# -rw-rw-r-- 1 m087494 m087494   608460 Feb 17 16:41 wsi-000017.dcm


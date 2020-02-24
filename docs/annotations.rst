Annotations
-----------

THIS NEEDS TESTED!!!!!!!!!!!!!!!!!

Given an XML file of annotations, extract the data into the appropriate DICOM element.

|Annotation|

.. |Annotation| image:: docs/images/annotation.jpg
    :width: 500



Establish DisplayedArea
+++++++++++++++++++++++

.. code-block:: python

    dsDisplayedArea = Dataset()
    dsDisplayedArea.PresentationSizeMode = 'TRUE SIZE'
    ds.DisplayedAreaSelectionSequence = Sequence([dsDisplayedArea])


Determine what type of annotation element is needed:

1. Bounding Box

.. code-block:: python

    GraphicAnnotation = 6 #TODO: costumize your annotation, need validation
    ds.GraphicAnnotationSequence = [Dataset(), Dataset()]
    ds.GraphicAnnotationSequence[0].ReferencedImageSequence = [Dataset()]

    # Graphics on the first referenced image
    ds.GraphicAnnotationSequence[0].ReferencedImageSequence[0].TextObjectSequence = [Dataset()]
    obj_seq1 = ds.GraphicAnnotationSequence[0].ReferencedImageSequence[0].TextObjectSequence
    obj_seq1[0].BoundingBoxTopLeftHandCorner = [50, 50]  # top left coordinates of bounding box
    obj_seq1[0].BoundingBoxBottomRightHandCorner = [100, 100]  # bottom right coordinates of bounding box
    obj_seq1[0].BoundingBoxAnnotationUnits = 'PIXEL'  # unit of coordinates
    obj_seq1[0].BoundingBoxHorizontalJustification = 'LEFT'
    obj_seq1[0].UnformattedTextValue = 'Tumor'  # Annotation Label text
    obj_seq1[0].GraphicGroupID = 1  # Annotation Label ID: 1

2. Points

.. code-block:: python

    ds.GraphicAnnotationSequence[1].ReferencedImageSequence = [Dataset()]
    ds.GraphicAnnotationSequence[1].ReferencedImageSequence[0].GraphicObjectSequence = [Dataset(), Dataset()]
    obj_seq2 = ds.GraphicAnnotationSequence[1].ReferencedImageSequence[0].GraphicObjectSequence
    obj_seq2[0].GraphicType = "POINT"
    obj_seq2[0].NumberofGraphicPoints = 4  # how many points where saved in this domain, validate data is complete
    obj_seq2[0].GraphicData = [120, 60, 135, 75, 80, 125, 89, 139]   # x,y coordinates of points [x0, y0, x1, y1 ....]
    obj_seq2[0].GraphicAnnotationUnits = 'PIXEL'  # unit of coordinates
    obj_seq2[0].GraphicGroupID = 2  # Annotation Label ID: 2

2. Polygon

.. code-block:: python

    ds.GraphicAnnotationSequence[2].ReferencedImageSequence = [Dataset()]
    ds.GraphicAnnotationSequence[2].ReferencedImageSequence[0].GraphicObjectSequence = [Dataset(), Dataset()]
    obj_seq3 = ds.GraphicAnnotationSequence[1].ReferencedImageSequence[0].GraphicObjectSequence
    obj_seq3[1].GraphicType = "POLYLINE"  # add polyline
    obj_seq3[1].NumberofGraphicPoints = 4 # how many points where saved in this domain
    obj_seq3[1].GraphicData = [150, 80, 160, 80, 180, 120, 130, 120]
    obj_seq3[1].GraphicAnnotationUnits = 'PIXEL'  # unit of coordinates
    obj_seq3[1].GraphicGroupID = 3  # Annotation Label ID: 2



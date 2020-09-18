from pydicom.dataset import Dataset
from pydicom.sequence import Sequence
import xml.etree.ElementTree as ET


def add_Ellipse(coord, id, text):
    # ellipse
    GraphicObjectSequence = Dataset()
    GraphicObjectSequence.GraphicType = "ELLIPSE"
    GraphicObjectSequence.NumberofGraphicPoints = len(coord) / 2  # how many points where saved in this domain
    GraphicObjectSequence.GraphicData = coord
    GraphicObjectSequence.GraphicAnnotationUnits = 'PIXEL'  # unit of coordinates
    GraphicObjectSequence.GraphicGroupID = id  # Annotation Label ID: 2
    GraphicObjectSequence.UnformattedTextValue = text  # Text="Necrosis"
    return GraphicObjectSequence


def add_Area(coord, id, text):
    # Area
    GraphicObjectSequence = Dataset()
    GraphicObjectSequence.GraphicType = "POLYLINE"  # add polyline
    GraphicObjectSequence.NumberofGraphicPoints = len(coord) / 2  # how many points where saved in this domain
    GraphicObjectSequence.GraphicData = coord
    GraphicObjectSequence.GraphicAnnotationUnits = 'PIXEL'  # unit of coordinates
    GraphicObjectSequence.GraphicGroupID = id  # Annotation Label ID: 2
    GraphicObjectSequence.UnformattedTextValue = text  # Text="Necrosis"
    return GraphicObjectSequence


def add_Rectangle(coord, id, text):
    # Rectangle: Graphics on the first referenced image
    GraphicObjectSequence = Dataset()
    GraphicObjectSequence.GraphicType = "RECTANGLE"
    GraphicObjectSequence.BoundingBoxTopLeftHandCorner = [coord[6], coord[7]]
    GraphicObjectSequence.BoundingBoxBottomRightHandCorner = [coord[2], coord[3]]  # bottom right coordinates of bounding box [max_x, min_y]
    GraphicObjectSequence.BoundingBoxAnnotationUnits = 'PIXEL'  # unit of coordinates
    GraphicObjectSequence.BoundingBoxHorizontalJustification = 'LEFT'
    GraphicObjectSequence.UnformattedTextValue = text  # Text="Necrosis"
    GraphicObjectSequence.GraphicGroupID = id  # Id="2"
    return GraphicObjectSequence


def add_Point(coord, id, text):
    # Points
    GraphicObjectSequence = Dataset()
    GraphicObjectSequence.GraphicType = "POINT"
    GraphicObjectSequence.NumberofGraphicPoints = len(
        coord) / 2  # how many points where saved in this domain, validate data is complete
    GraphicObjectSequence.GraphicData = coord  # x,y coordinates of points [x0, y0, x1, y1 ....]
    GraphicObjectSequence.GraphicAnnotationUnits = 'PIXEL'  # unit of coordinates
    GraphicObjectSequence.GraphicGroupID = id  # Id="1" Type="0" Text="null"
    GraphicObjectSequence.UnformattedTextValue = text
    return GraphicObjectSequence


def add_annotations(ds, cfg, instance):
    """ all values are hard coded to ensure they are present in the final file """
    file_ann = cfg.get('General').get('Annotations')

    # create element tree object
    tree = ET.parse(file_ann)

    # get root element
    root = tree.getroot()
    # root = ET.fromstring(Regions_data_as_string)

    # initialize
    dsDisplayedArea = Dataset()
    dsDisplayedArea.PresentationSizeMode = 'TRUE SIZE'
    ds.DisplayedAreaSelectionSequence = Sequence([dsDisplayedArea])
    ds.GraphicAnnotationSequence = Sequence([Dataset()])
    ds.GraphicAnnotationSequence[0].ReferencedImageSequence = Sequence([Dataset()])

    list_gos = []
    # iterate news items
    for Region in root.iter('Region'):
        id = Region.get('Id')
        type = Region.get('Type')
        text = Region.get('Text')
        geo_shape = Region.get('GeoShape')
        zoom = Region.get('Zoom')
        selected = Region.get('Selected')
        image_loc = Region.get('ImageLocation')
        image_focus = Region.get('ImageFocus')
        length = Region.get('Length')
        area = Region.get('Area')
        len_microns = Region.get('LengthMicrons')
        area_microns = Region.get('AreaMicrons')
        neg_roa = Region.get('NegativeROA')
        input_reg = Region.get('InputRegionId')
        anal = Region.get('Analyze')
        displayid = Region.get('DisplayId')
        # print(id,type,geo_shape)
        vertex = []
        for Vertex in Region.iter('Vertex'):
            x = Vertex.get('X')
            y = Vertex.get('Y')
            '''Recalculating the coordinates '''
            x = float(float(x) / (2 ** instance))
            x = round(x, 2)
            y = float(float(y) / (2 ** instance))
            y = round(y, 2)
            vertex.append(float(x))
            vertex.append(float(y))

        if geo_shape == "Points":
            gos = add_Point(vertex, int(id),  text + '_' + geo_shape + '_' + zoom+'_'+type)
            # ds.GraphicAnnotationSequence[0].ReferencedImageSequence[0].GraphicObjectSequence.append(gos)
            list_gos.append(gos)
            del gos

        if geo_shape == "Rectangle":
            gos = add_Rectangle(vertex, int(id),  text + '_' + geo_shape + '_' + zoom+'_'+type)
            # ds.GraphicAnnotationSequence[0].ReferencedImageSequence[0].GraphicObjectSequence.append(gos)
            list_gos.append(gos)
            del gos

        if geo_shape == "Ellipse":
            gos = add_Ellipse(vertex, int(id),  text + '_' + geo_shape + '_' + zoom+'_'+type)
            # ds.GraphicAnnotationSequence[0].ReferencedImageSequence[0].GraphicObjectSequence.append(gos)
            list_gos.append(gos)
            del gos

        if geo_shape == "Area" or geo_shape == "Polygon":
            gos = add_Area(vertex, int(id),  text + '_' + geo_shape + '_' + zoom+'_'+type)
            # ds.GraphicAnnotationSequence[0].ReferencedImageSequence[0].GraphicObjectSequence.append(gos)
            list_gos.append(gos)
            del gos

    ds.GraphicAnnotationSequence[0].ReferencedImageSequence[0].GraphicObjectSequence = Sequence(list_gos)
    del list_gos

    return ds

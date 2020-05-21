.. highlight:: python

=====
TL;DR
=====

To use dicom-wsi in a project::

    from yaml import load, BaseLoader
    from dicom_wsi import create_dicom
    from parse_wsi import get_wsi

    # Define your YAML file
    my_yaml = '/path/to/yaml'
    # Load your YAML file
    cfg = load(open(my_yaml), Loader=BaseLoader)
    # Read the WSI, updating the config with information contained in the slide
    cfg, wsi = get_wsi(cfg)
    # Create DICOM files
    create_dicom(cfg)

That's it!

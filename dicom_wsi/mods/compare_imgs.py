from PIL import Image
import pyvips
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error
import pydicom
import numpy as np
from os.path import basename as bn

svs_file = '../tests/CMU-1.svs'
dcm_file = 'svs_jp2.0-1.dcm'
compression = 'jp2'
x, y = 24001, 2501
tile_size = 500
array_number = 378

ds = pydicom.dcmread(dcm_file)
dcm_img = ds.pixel_array[array_number]

wsi = pyvips.Image.new_from_file(svs_file)
resize_level = 1
img = wsi.resize(resize_level)

format_to_dtype = {
    'uchar': np.uint8,
    'char': np.int8,
    'ushort': np.uint16,
    'short': np.int16,
    'uint': np.uint32,
    'int': np.int32,
    'float': np.float32,
    'double': np.float64,
    'complex': np.complex64,
    'dpcomplex': np.complex128,
}

np_3d = np.ndarray(buffer=img.write_to_memory(),
    dtype=format_to_dtype[img.format],
    shape=[img.height, img.width, img.bands])
np_3d = np_3d[:, :, :3]

raw_img = np_3d[x:x+tile_size, y:y+tile_size, :]

mse_result = mean_squared_error(raw_img, dcm_img)
ssim_result = ssim(dcm_img, raw_img, multichannel=True)
Image.fromarray(dcm_img).save(f"OUT/{compression}_{bn(svs_file.split('.')[2])}_{x}-{y}-{array_number}.dcm.png")
Image.fromarray(raw_img).save(f"OUT/{compression}_{bn(svs_file.split('.')[2])}_{x}-{y}-{array_number}.raw.png")
print(f'mse_result: {mse_result:.4f}, ssim_result:{ssim_result:.4f}')

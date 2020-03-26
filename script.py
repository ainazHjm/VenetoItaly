import h5py as h5
import numpy as np
import argparse
import os
from PIL import Image

Image.MAX_IMAGE_PIXELS = 1e10

def get_args():
    parser = argparse.ArgumentParser(description="Joining Data")
    parser.add_argument("--dataset_path", type=str, help="path to the h5 dataset")
    return parser.parse_args()

def get_flags():
    _slope, _DEM = False, False
    img_names = os.listdir('images/')
    if not ('slope.tif' in img_names or 'DEM.tif' in img_names):
        raise ValueError('There are no DEM or slope maps in the images folder!')
    if 'slope.tif' in img_names:
        _slope = True
    if 'DEM.tif' in img_names:
        _DEM = True
    return _slope, _DEM

def normalize(np_img, _slope, data_indices):
    if _slope:
        np_img[np_img<0]=0
        np_img[np_img>180]=0
    mean = np.mean(np_img[data_indices])
    std = np.std(np_img[data_indices])
    np_img = (np_img-mean)/std
    padded = np.pad(
        np_img,
        ((0, 0), (0, 250)),
        mode='reflect'
    )
    return padded

def join():
    args = get_args()
    _slope, _DEM = get_flags()
    f = h5.File(args.dataset_path, 'a')
    data_indices = f['Veneto/data'][2, 64:-64, 64:-314] >= 0
    if _slope:
        f['Veneto/data'][0] = np.pad(
            normalize(np.array(Image.open('images/slope.tif')), _slope, data_indices),
            ((64, 64), (64, 64)),
            mode='reflect'
        )
    if _DEM:
        f['Veneto/data'][-1] = np.pad(
            normalize(np.array(Image.open('images/DEM.tif')), _slope, data_indices),
            ((64, 64), (64, 64)),
            mode='reflect'
        )
    f.close()
    print('The new images are added to the dataset.')

if __name__=='__main__':
    join()

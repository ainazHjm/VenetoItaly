import hdf5 as h5
import numpy as np
import argparse
import os
from PIL import Image

def get_args():
    parser = argparse.ArgumentParser(description="Joining Data")
    parser.add_argument("--dataset_path", type=str, help="path to the h5 dataset")
    parser.add_argument("--save_to", type=str, help="path to save the new h5 dataset")
    return parser.parse_args()

def get_flags():
    _slope, _DEM = False, False
    img_names = os.listdir('images/')
    if not ('slope' in img_names or 'DEM' in img_names):
        raise ValueError('There are no DEM or slope maps in the images folder!')
    if 'slope' in img_names:
        _slope = True
    if 'DEM' in img_names:
        _DEM = True
    return _slope, _DEM

def normalize(np_img):
    mean = np.mean(np_img)
    std = np.std(np_img)
    np_img = (np_img - mean)/std
    return np_img

def join():
    args = get_args()
    _slope, _DEM = get_flags()
    
    f = h5.File(args.dataset_path, 'r')
    (n, h, w) = f['Veneto/data'].shape
    newf = h5.File(args.save_to, 'w')
    newf.create_dataset('Veneto/data', (n+_slope+_DEM, h, w), dtype='f', compression='lzf')
    newf.create_dataset(
        'Veneto/gt',
        (1, f['Veneto/gt'].shape[1], f['Veneto/gt'].shape[2])
        dtype='f',
        compression='lzf'
    )
    
    if _slope:
        newf['Veneto/data'][0] = normalize(np.array(Image.open('images/slope.tif')))
        newf['Veneto/data'][1:1+n] = f['Veneto/data'][:]
    if _DEM:
        newf['Veneto/data'][-1] = normalize(np.array(Image.open('images/DEM.tif')))
        newf['Veneto/data'][-1-n:-1] = f['Veneto/data'][:]
    
    newf['Veneto/gt'][:] = f['Veneto/gt'][:]

    f.close()
    newf.close()
    print('The new dataset is created in %s.' %args.save_to)

if __name__=='__main__':
    join()
import h5py as h5
import numpy as np
import argparse
import os
from PIL import Image

Image.MAX_IMAGE_PIXELS = 1e10

def get_args():
    parser = argparse.ArgumentParser(description="Joining Data")
    parser.add_argument("--dataset_path", type=str, help="path to the h5 dataset")
    # parser.add_argument("--save_to", type=str, help="path to save the new h5 dataset")
    return parser.parse_args()

def get_flags():
    _slope, _DEM = False, False
    img_names = os.listdir('images/')
    # import ipdb; ipdb.set_trace()
    if not ('slope.tif' in img_names or 'DEM.tif' in img_names):
        raise ValueError('There are no DEM or slope maps in the images folder!')
    if 'slope.tif' in img_names:
        _slope = True
    if 'DEM.tif' in img_names:
        _DEM = True
    return _slope, _DEM

def normalize(np_img, _slope):
    if _slope:
        np_img[np_img<0]=0
        np_img[np_img>180]=0
    mean = np.mean(np_img)
    std = np.std(np_img)
    np_img = (np_img - mean)/std
    return np_img

def join():
    args = get_args()
    _slope, _DEM = get_flags()
    
    f = h5.File(args.dataset_path, 'a')
    # (n, h, w) = f['Veneto/data'].shape
    # newf = h5.File(args.save_to, 'w')
    # newf.create_dataset('Veneto/data', (n+_slope+_DEM, h, w), dtype='f', compression='lzf')
    # newf.create_dataset(
    #     'Veneto/gt',
    #     (1, f['Veneto/gt'].shape[1], f['Veneto/gt'].shape[2]),
    #     dtype='f',
    #     compression='lzf'
    # )
    # import ipdb; ipdb.set_trace() 
    if _slope:
        f['Veneto/data'][0] = np.pad(normalize(np.array(Image.open('images/slope.tif')), _slope), ((64, 64), (64, 64+250)), mode='reflect')
        # f['Veneto/data'][1:1+n] = f['Veneto/data'][:]
        # f.close()
        # ipdb.set_trace()
    if _DEM:
        f['Veneto/data'][-1] = np.pad(normalize(np.array(Image.open('images/DEM.tif')), _slope), ((64, 64), (64, 64+250)), mode='reflect')
        # if not _slope:
        #     f['Veneto/data'][-1-n:-1] = f['Veneto/data'][:]
        # ipdb.set_trace()
        # f.close()
    
    # f['Veneto/gt'][:] = f['Veneto/gt'][:]

    f.close()
    # newf.close()
    print('The new images are added to the dataset.')

if __name__=='__main__':
    join()

import numpy as np
import argparse
import os
import h5py
import json
from PIL import Image
from utils import args
from time import ctime

Image.MAX_IMAGE_PIXELS = 1e10

def get_args():
    parser = argparse.ArgumentParser(description="Data Preparation")
    parser.add_argument("--data_dir", action="append", type=str, help="path to each region's data")
    parser.add_argument("--save_to", type=str, default="../image_data/", help="path to write the new dataset")
    parser.add_argument("--feature_num", type=int, default=94, help="number of total features/inputs")
    parser.add_argument('--shape', action='append', type=args.shape, help="the shape of each region")
    parser.add_argument("--data_format", type=str, default=".tif", help="format of the images to read from")
    parser.add_argument("--pad", type=int, default=64, help="size of padding to each dimension")
    return parser.parse_args()

def normalize(np_img, f = 'slope'):
    if f == 'slope':
        np_img[np_img < 0] = 0
        np_img[np_img > 180] = 0
        print('slope values smaller than zero and bigger than 180 are ignored.')
    mean = np.mean(np_img)
    std = np.std(np_img)
    print('mean, std before normalizing: %f, %f' %(mean, std))
    np_img = (np_img - mean)/std
    print('after: %f, %f' %(np.mean(np_img), np.std(np_img)))
    return np_img

def zero_one(np_img):
    ones = np_img!=0
    np_img[ones]=1
    return np_img

def initialize(f, key):
    (n, h, w) = f[key]['data'].shape
    zero = np.zeros((h, w))
    for i in range(n):
        f[key]['data'][i] = zero
        print('%s -> %d/%d' %(ctime(), i+1, n), end='\r')
    return f

def process_data():
    '''
    only use 10% of the one patches for test and 10% of the one batches for validation
    so, we don't create separate partitions for train and test in the final dataset but only save the indices.
    '''
    args = get_args()
    g = open('data_dict.json', 'r')
    data_dict = json.load(g)
    g.close()
    f = h5py.File(args.save_to, 'a')
    
    for data_path in args.data_dir:
        name = data_path.split('/')[-2]
        for n, h, w in args.shape:
            if n == name and not name in f.keys():
                f.create_dataset(
                    name+'/data',
                    (args.feature_num, h+args.pad*2, w+args.pad*2),
                    dtype='f',
                    compression='lzf'
                )
                f.create_dataset(name+'/gt', (1, h, w), dtype='f', compression='lzf')
                print('created data and gt in %s' %name)
                break
        f = initialize(f, name)

    for data_path in args.data_dir:
        name = data_path.split('/')[-2]
        images = os.listdir(data_path)
        for img in images:
            if args.data_format in img and not '.xml' in img and not 'gt' in img:
                t = np.array(Image.open(data_path+img))
                n_ = img.split('.')[0]
                if int(data_dict[n_]) == 0:
                    print('normalizing slope ...')
                    t = normalize(t, 'slope')
                elif int(data_dict[n_]) == args.feature_num-1:
                    print('normalizing DEM')
                    t = normalize(t, 'DEM')
                print(data_dict[n_])
                t = np.pad(t, ((0, 0), (0, 250)), mode='reflect')
                f[name+'/data'][int(data_dict[n_])] = np.pad(
                    t,
                    ((args.pad, args.pad), (args.pad, args.pad)),
                    'reflect'
                )
        gt = np.array(Image.open(data_path+'gt'+args.data_format))
        f[name+'/gt'][0] = np.pad(gt, ((0, 0), (0, 250)), mode='reflect')

    f.close()

process_data()

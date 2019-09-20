import h5py
import argparse
import numpy as np
import resource
import gc
from utils.args import int_array
from utils.masks import mask_helper
from time import ctime

def get_args():
    parser = argparse.ArgumentParser(description='finding local features')
    parser.add_argument('--data_path', type=str, default='/tmp/Veneto_data.h5')
    parser.add_argument('--dist', type=int_array, help='input the distances (>0) that you want to look by , .')
    parser.add_argument('--pix_res', type=int, default=10)
    parser.add_argument('--region', type=str, default='Veneto')
    parser.add_argument('--save_to', type=str, default='/home/ainaz/Projects/Landslides/image_data/n_feature_data.h5')
    parser.add_argument('--pad', type=int, default=64)
    parser.add_argument('--features', type=int_array, default=[0,2,3,5,6,8,11,12,15,19,20,25,35,45,46,47,51,70,78,86,91,92])
    return parser.parse_args()

def create_mask(args, dist, efficiency=True):
    print('creating the mask')
    if efficiency:
        mask = mask_helper()[str(dist)]
    else:
        radius = dist//args.pix_res
        Y, X = np.ogrid[:(2*radius+1), :(2*radius+1)]
        center = (radius, radius)
        distance = np.sqrt((Y-center[1])**2 + (X-center[0])**2)
        mask = np.logical_and(distance <= radius, distance >= radius-1)
        if mask[radius, radius]:
            mask[radius, radius] = False
        print(mask)
    return mask

def find_max_idx(dem, mask):
    print('finding the indices for maximum elevation')
    gc.collect()
    # import ipdb; ipdb.set_trace()
    (h, w) = dem.shape
    mask_center = (mask.shape[0]//2, mask.shape[1]//2)
    mask_indices = mask.nonzero()
    n_dem = np.zeros((len(mask_indices[0]), h, w))
    for i in range(len(mask_indices[0])):
        row, col = mask_indices[0][i]-mask_center[0], mask_indices[1][i]-mask_center[1]
        # import ipdb; ipdb.set_trace()
        if col >=0:
            n_dem[i, :, :] = np.pad(dem[row:, col:], ((0, row), (0, col)), mode='constant') if row>=0 else np.pad(dem[:row, col:], ((-1*row, 0), (0, col)), mode='constant')
        else:
            n_dem[i, :, :] = np.pad(dem[row:, :col], ((0, row), (-1*col, 0)), mode='constant') if row>=0 else np.pad(dem[:row, :col], ((-1*row, 0), (-1*col, 0)), mode='constant')
    n_dem = n_dem.reshape(len(mask_indices[0]), -1)
    gc.collect()
    # import ipdb; ipdb.set_trace()
    return np.argmax(n_dem, axis=0) # a 1d array

def get_max_val(max_indices, mask, feature):
    print('finding the maximum values corresponding to indices')
    (h, w) = feature.shape
    mask_indices = mask.nonzero()
    mask_center = (mask.shape[0]//2, mask.shape[1]//2)
    n_feature = np.zeros((len(mask_indices[0]), h, w))
    for i in range(len(mask_indices[0])):
        r, c = mask_indices[0][i]-mask_center[0], mask_indices[1][i]-mask_center[1]
        if c >=0:
            n_feature[i, :, :] = np.pad(feature[r:, c:], ((0, r), (0, c)), mode='constant') if r>=0 else np.pad(feature[:r, c:], ((-1*r, 0), (0, c)), mode='constant')
        else:
            n_feature[i, :, :] = np.pad(feature[r:, :c], ((0, r), (-1*c, 0)), mode='constant') if r>=0 else np.pad(feature[:r, :c], ((-1*r, 0), (-1*c, 0)), mode='constant')
    n_feature = n_feature.reshape(len(mask_indices[0]), -1)
    max_features = n_feature[max_indices, np.arange(h*w)]
    return max_features.reshape(h, w)

def write_file(args, f, radius, new_f, radius_num):
    (n, _, _) = f[args.region]['data'].shape
    dem = f[args.region]['data'][-1, :, :] # load_the elevation map
    mask = create_mask(args, radius)
    import ipdb; ipdb.set_trace() 
    max_idx = find_max_idx(dem, mask) # returns a 1d array showing which channel is the max value
    gc.collect()
    print('-- memory usage after finding the index: %d (KB)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

    for i, feature_num in enumerate(args.features):
        new_f[args.region]['data/dist{}'.format(str(radius_num))][i, :, :] = get_max_val(
            max_idx,
            mask,
            f[args.region]['data'][feature_num, :, :]
        )
        print('[%s]: writing feature %d to the new dataset' %(ctime(), feature_num))
        print('-- memory usage: %d (KB)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return new_f

def initialize(args, newf, f):
    n = f[args.region]['data'].shape[0]
    for feature_idx in range(n-1): # dist 0
        newf[args.region]['data/dist0'][feature_idx, :, :] = f[args.region]['data'][
            feature_idx,
            :,
            :
        ]
        print('[%s]: writing feature %d' %(ctime(), feature_idx))
    print('-- memory usage: %d (KB)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print(args.features)
    for i, dist in enumerate(args.dist):
        newf = write_file(args, f, dist, newf, i+1)
    print('-- memory usage: %d (KB)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    newf[args.region]['gt'][:] = f[args.region]['gt'][:]
    print('[%s]: writing gt' %ctime())
    return newf

def create_dataset(args, f):
    (_, h_data, w_data) = f[args.region]['data'].shape
    (_, h_gt, w_gt) = f[args.region]['gt'].shape
    n = f[args.region]['data'].shape[0]
    # total_features = (len(args.dist)+1)*(n-1)
    print('[%s]: total number of features: %d, data shape= (%d, %d)' %(ctime(), n-1+len(args.features)*len(args.dist), h_data, w_data))
    newf = h5py.File(args.save_to, 'a')

    # instead of having data and gt as group names, use dist{} for each feature group
    newf.create_dataset(args.region+'/data/dist0', shape=(n-1, h_data, w_data),  dtype='f', compression='gzip')
    for i in range(len(args.dist)):
        newf.create_dataset(
            args.region+'/data/dist{}'.format(str(i+1)),
            shape=(len(args.features), h_data, w_data),
            dtype='f',
            compression='gzip'
        )
    newf.create_dataset(args.region+'/gt', shape=(1, h_gt, w_gt),  dtype='f', compression='gzip')
    print('[%s]: the new dataset is created' %(ctime()))
    print('-- memory usage: %d (KB)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    
    newf = initialize(args, newf, f)
    newf.close()
    print('[%s]: new dataset has been created, initialized and saved.' %(ctime()))

def helper(args):
    f = h5py.File(args.data_path, 'r')
    create_dataset(args, f)
    f.close()

def main():
    args = get_args()
    helper(args)
    
if __name__=='__main__':
    main()
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print('memory usage: %d (KB)' % mem)

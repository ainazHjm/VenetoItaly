import h5py
import argparse
import numpy as np

def get_args():
    parser = argparse.ArgumentParser(description='utilities')
    parser.add_argument('--data_path', type=str)
    parser.add_argument('--patch_size', type=int, default=500)
    parser.add_argument('--pruning_size', type=int, default=64)
    parser.add_argument('--region', type=str, default='Veneto')
    parser.add_argument('--write_ones', type=bool, default=False)
    parser.add_argument('--save_to', type=str)
    return parser.parse_args()

def find_one_patches(args):
    f = h5py.File(args.data_path, 'r')
    gt = f['{}/gt'.format(args.region)][0, :, :]
    ws = args.patch_size
    (h, w) = gt.shape
    ones_indices, zeros_indices = [], []
    ignore = 0
    for row in range(h//ws):
        for col in range(w//ws):
            patch = gt[row*ws:(row+1)*ws, col*ws:(col+1)*ws]
            area = np.sum(patch>=0)
            ones = np.sum(patch>0)

            if area == 0:
                ignore += 1
            
            if ones > 0:
                ones_indices.append([row, col, ones/area])
                print('patch at (%d, %d) has %.4f ones' %(row, col, ones/area))
            elif ones == 0 and area > 0:
                zeros_indices.append([row, col, np.sum(patch==0)/area])
    print('%.4f of the patches contain landslides' %(len(ones_indices)/(h//ws*w//ws-ignore)))
    print('ignore = %d' %ignore)
    ones_indices = np.array(ones_indices)
    zeros_indices = np.array(zeros_indices)
    if args.write_ones:
        np.save(args.save_to+'{}_one_indices.npy'.format(args.region), ones_indices)
        np.save(args.save_to+'{}_zero_indices.npy'.format(args.region), zeros_indices)
    return ones_indices, zeros_indices

def partition(args, ones, zeros):
    n_idx = ones.shape[0] + zeros.shape[0]
    np.random.shuffle(ones)
    np.random.shuffle(zeros)
    test = np.concatenate((ones[0:n_idx//20], zeros[0:n_idx//20]), axis=0)
    print(test.shape)
    validation = ones[n_idx//20:3*(n_idx//20)]
    print(validation.shape)
    np.save(args.save_to+'{}_test_indices.npy'.format(args.region), test)
    np.save(args.save_to+'{}_validation_indices.npy'.format(args.region), validation)

def main():
    args = get_args()
    ones, zeros = find_one_patches(args)
    partition(args, ones, zeros)

if __name__=='__main__':
    main()
import numpy as np

def mask_100(): #12 True
    m = np.zeros((21, 21), dtype=bool)
    m[10,0]=True; m[0,10]=True; m[-1,10]=True; m[10,-1]=True
    m[2,4]=True; m[2,16]=True; m[18,16]=True; m[18,4]=True
    m[6,1]=True; m[6,19]=True; m[14,19]=True; m[14,1]=True
    return m

def mask_300(): #16 True
    m = np.zeros((61,61), dtype=bool)
    m[30,0]=True; m[0,30]=True; m[-1,30]=True; m[30,-1]=True
    m[5,14]=True; m[5,46]=True; m[55,46]=True; m[55,14]=True
    m[13,7]=True; m[13,53]=True; m[47,53]=True; m[47,7]=True
    m[21,3]=True; m[21,57]=True; m[39,57]=True; m[39,3]=True
    return m

def mask_helper():
    masks = {
        '30': np.array(
            [
                [False, False, False,  True, False, False, False],
                [False,  True, False, False, False,  True, False],
                [False, False, False, False, False, False, False],
                [ True, False, False, False, False, False,  True],
                [False, False, False, False, False, False, False],
                [False,  True, False, False, False,  True, False],
                [False, False, False,  True, False, False, False]
            ]
        ),
        '100': mask_100(),
        '300': mask_300()
    }
    return masks
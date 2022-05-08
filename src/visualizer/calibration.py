import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
import cupy as cp
from cupyx.scipy.ndimage import shift
import cupy as cp
from skimage.io import imread
from skimage.io.collection import alphanumeric_key
from dask import delayed
from glob import glob
from skimage import io
import dask
import dask.array as da

@dask.delayed
# Read RAW files and return Dask Array
def lazy_imread_raw(raw_file, width=960, height=600, px_size='uint8'):
    #Parse data from the raw which contains padding if sensor array size is not 
    #divisible by 512. Sector aligned 
    raw_img = np.fromfile(raw_file, dtype= px_size)
    if px_size == 'uint16':
        raw_size = raw_img.shape[0]-((raw_img.shape[0]-(width*height))*16/8)
    else:
        raw_size= raw_img.shape[0]-((raw_img.shape[0]-(width*height)))
    raw_img = raw_img[0:int(raw_size)] 
    raw_reshape =np.reshape(raw_img,(1,height,width))
    return raw_reshape

def lazy_dask_stack(main_folder,num_cams=25, px_depth='uint16', height=600, width =960):
    folder_names = sorted(glob(main_folder + '/CAM*/'), key=alphanumeric_key)
    offset = np.floor(num_cams/2).astype(np.uint8)
    da_stack=[]
    
    for folder_name in folder_names[12-offset:offset+13]:
        file_extension = folder_name + '/' + '*.raw'
        file_names = sorted(glob(file_extension),key=alphanumeric_key)
        sample =np.fromfile(file_names[0],dtype=px_depth)
        if px_depth == 'uint16':
            raw_size = sample.shape[0]-((sample.shape[0]-(width*height))*16/8)
        else:
            raw_size= sample.shape[0]-((sample.shape[0]-(width*height)))
        sample = sample[0:int(raw_size)] 
        raw_reshape =np.reshape(sample,(1,height,width))
        delayed(lazy_imread_raw)
        lazy_arrays = [lazy_imread_raw(fn,width,height,px_depth) for fn in file_names]
        dask_arrays = [da.from_delayed(delayed_reader, shape=raw_reshape.shape,dtype=raw_reshape.dtype) for delayed_reader in lazy_arrays]
        # stack = da.concatenate(dask_arrays, axis=1)
        da_stack.append(dask_arrays)
    stack = da.concatenate(da_stack,axis=1)
    return stack 

def load_dataset(main_folder,num_cams=25,px_depth='uint16',width=808,height=608):
    folder_names = sorted(glob(main_folder + '/CAM*/'), key=alphanumeric_key)
    offset = np.floor(num_cams/2).astype(np.uint8)
    raw_M25_volume = [dask_raw_ds(fd,px_depth,width=width, height=height) for fd in folder_names[12-offset:offset+13]]
    stack = da.concatenate(raw_M25_volume, axis=1)
    return stack

# Read RAW files and return Dask Array
def imread_raw(raw_file, width=808, height=608, px_size='uint16'):
    raw_img = np.fromfile(raw_file, dtype= px_size)
    #Parse data from the raw which contains padding if sensor array size is not 
    #divisible by 512. Sector aligned 
    if px_size == 'uint16':
        raw_size = raw_img.shape[0]-((raw_img.shape[0]-(width*height))*16/8)
    else:
        raw_size= raw_img.shape[0]-((raw_img.shape[0]-(width*height)))
    raw_img = raw_img[0:int(raw_size)] 
    raw_reshape =np.reshape(raw_img,(1,height,width))
    return da.from_array(raw_reshape)

def dask_raw_ds(folder_name,px_depth,width=808,height=608):
    file_extension = folder_name + '/' + '*.raw'
    file_names = sorted(glob(file_extension),key=alphanumeric_key)
    raw_ds = [ imread_raw(fn,width=width,height=height,px_size= px_depth) for fn in file_names]
    # dask_raw_ds = da.stack(raw_ds,axis=1)
    return raw_ds

def save_zarr(folder_name,entered_name,stack)
    filename = entered_name + '.zarr'
    filepath_save = os.path.join(main_folder,filename)
    zarr.save(filepath_save,stack)

def 


## https://forum.image.sc/t/mask-and-crop-with-napari/54008/2

def create_box(data):
    
    #TODO : make sure this works for differnt size arrays
    """Create integer box

    Parameters
    ----------
    data : (N, 2) array
        Points around which the box is created.

    Returns
    -------
    box : (2, 2) array
        Integrer extrema of the box.
    """
    t,c,h,w = data.shape
    
    min_val = data.min(axis=0)
    max_val = data.max(axis=0)
    tl = np.array([min_val[0], min_val[1]])
    br = np.array([max_val[0], max_val[1]])
    box = np.round(np.array([tl, br])).astype(int)
    return box

def create_box_ndarray(crop_region):
    
    # Assuming data comes from napari as (4,4) shape given time and channel
    # t,c,h,w = crop_region.shape
    # box = calibration.create_box(d)
    # print(box)
    
    min = crop_region[0:4,2:4].min(axis=0)
    max =  crop_region[0:4,2:4].max(axis=0)

    tl = np.array((crop_region[0,0],crop_region[0,1],min[0],min[1]))
    br = np.array((crop_region[0,0],crop_region[0,1],max[0],max[1]))
    box  = np.round(np.array([tl,br])).astype(int)
    return box 

def crop(image, rectangle):
    """Create integer box

    Parameters
    ----------
    image : (N, M) array
        2D image.
    rectangle : (4, 2) array or (2, 2) array
        Rectangle for cropping.

    Returns
    -------
    cropped_image : (U, V) array
        Cropped 2D image.
    """
    min_val, max_val = create_box(rectangle)
    return image[min_val[0]: max_val[0], min_val[1]: max_val[1]]

def shift_stack(stack,coordinates, cuda_device_id = 0):
   # Generate our own shifted datset
    with cp.cuda.Device(cuda_device_id):
        stack_output = []
        for i in range(len(coordinates)):
            cp_stack = cp.array(stack[i])
            shift_stack_cam= shift(cp_stack,coordinates[i])
            stack_output.append(cp.asnumpy(shift_stack_cam))
            cp_stack = None
    stack_output = np.array(stack_output)
    return stack_output

# All the 6 methods for comparison in a list
methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

def find_offsets(stack, template,methods='cv.TM_CCOEFF'):
    #TODO: CV Match template only takes uint8 or float32. Need to implement check before this?
    coord =[]
    w,h = template.shape  
    for i in range(stack.shape[0]):
        method = eval(methods) # This method parses expression and runs ()
        # Apply template Matching
        # Slide through image and compare template patches.
        # Comparison of best matches is foudn as global minn in SQDIFF or max in CCORR or CCOEF.
        res = cv.matchTemplate(stack[i],template,method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
            
        bottom_right = (top_left[0] + w, top_left[1] + h)
        coord.append(((top_left[1],top_left[0]),(bottom_right[1],bottom_right[0])))
        
    return coord


def registration(img_stack,ref_index):
    t,c,h,w =img_stack.shape
    stack_max_projection= np.array([ da.max(img_stack[:,i,:,:],axis=0) for i in range(img_stack.shape[1])])
    offset = np.array([phase_cross_correlation(stack_max_projection[ref_index], stack_max_projection[i]) for i in range(stack_max_projection.shape[0])],dtype=object)
    offset = offset[0:c,0]
    offset_coords = np.stack(offset[0:,],axis=0)
    return offset_coords

# def align_projections(img_stack,offsets):
#     stack_max_projection= np.array([ da.max(img_stack[:,i,:,:],axis=0) for i in range(img_stack.shape[1])])
#     shifted= np.zeros_like(stack_max_projection)
#     for i in range(img_stack.shape[1]):
#         x_offset,y_offset = offsets[i]
#         M = np.float32([
#         [1, 0, y_offset],
#         [0, 1, x_offset]
#         ])
#         stack_max_projection= np.float32(stack_max_projection)
#         # print(M)
#         shifted[i] = cv.warpAffine(stack_max_projection[i],M,(stack_max_projection[i].shape[1],stack_max_projection[i].shape[0]))
#     return shifted

# def align_stack(img_stack,offsets):
#     shifted= np.zeros_like(img_stack)
#     print(img_stack.shape)
#     width = img_stack.shape[3] 
#     height = img_stack.shape[2]
#     img_stack= np.float32(img_stack)
#     for i in range(img_stack.shape[1] ):
#         x_offset,y_offset = offsets[i,0]
#         M = np.float32([
#         [1, 0, y_offset],
#         [0, 1, x_offset]
#         ])
        
#         for j in range(img_stack.shape[0]):
#             shifted[j,i] = cv.warpAffine(img_stack[j,i],M,(width,height))
    
#     return shifted

def cp_mip(np_image_stack):
        # Generate our own shifted datset
    with cp.cuda.Device(0):
        t,c,h,w  = np_image_stack.shape
        np_mip =[]
        for i in range(c):
            cp_stack = cp.array(np_image_stack[:,i,:,:])
            cp_mip = cp.max(cp_stack, axis=0)
            np_mip.append(cp.asnumpy(cp_mip))
            cp_mip = None
            cp_stack=None
        np_mip = np.array(np_mip)
        np_mip = np.expand_dims(np_mip,axis=0)
    return np_mip

def cp_align(np_image_stack, offsets):
    from cupyx.scipy.ndimage import shift
    t,c,h,w = np_image_stack.shape
    shift_stack_cam = cp.zeros((c,h,w))
    shift_stack_output = []
    columns = cp.zeros((offsets.shape[0],1))
    shift_stack_coord = cp.hstack((columns,offsets))
    
    for i in range(c):
        cam_stack = cp.array(np_image_stack[:,i,:,:])
        shift_stack_cam= shift(cam_stack,shift_stack_coord[i])
        shift_stack_output.append(cp.asnumpy(shift_stack_cam))
        # TODO: Check  this is proper way of transfering from GPU to CPU
        shift_stack_cam = None
        cam_stack = None
        # print("post")
    shift_stack_coord = None
    aligned_stack = np.array(shift_stack_output)
    return np.moveaxis(aligned_stack,0,1)
    # return shift_stack_output

def cuda_mem_info(device_id =0):
    with cp.cuda.Device(device_id):
        mempool = cp.get_default_memory_pool()
        pinned_mempool = cp.get_default_pinned_memory_pool()

        print(mempool.used_bytes())              # 
        print(mempool.total_bytes())             #
        print(pinned_mempool.n_free_blocks())    #

def cuda_clear(device_id=0):
    with cp.cuda.Device(device_id):
        mempool = cp.get_default_memory_pool()
        pinned_mempool = cp.get_default_pinned_memory_pool()
        mempool.free_all_blocks()
        pinned_mempool.free_all_blocks()
        print(mempool.used_bytes())              # 
        print(mempool.total_bytes())             #
        print(pinned_mempool.n_free_blocks())    #
# import napari
import numpy as np

# Borrowing from
# https://forum.image.sc/t/mask-and-crop-with-napari/54008/2
def create_box(data):
    """Create integer box

    Parameters
    ----------
    data : (N, 2) array
        Points around which the box is created.

    Returns
    -------
    box : (2, 2) array
        Integer extrema of the box.
    """
    min_val = data.min(axis=0)
    max_val = data.max(axis=0)
    tl = np.array([min_val[0], min_val[1]])
    br = np.array([max_val[0], max_val[1]])
    box = np.round(np.array([tl, br])).astype(int)
    return box

def crop(image, rectangle):
    """Create integer box

    Parameters
    ----------
    image : (N, M) array
        2D image.
    rectangle :(4,2) or (2, 2) array
        Rectangle for cropping.

    Returns
    -------
    cropped_image : (U, V) array
        Cropped 2D image.
    """
    min_val, max_val =create_box(rectangle)
    return image[min_val[0]: max_val[0], min_val[1]: max_val[1]]

def create_skeleton_box(coord_a,coord_b,side,width='100'):
    """
    
    Refresh on vector calc
    https://stackoverflow.com/questions/7469959/given-2-points-how-do-i-draw-a-line-at-a-right-angle-to-the-line-formed-by-the-t/7470098#7470098
    The matrix representation of 2D transformation:
    x' = xcos(t) - ysin(t)
    y' = xsin(t)  - ycost(t)

    so if t =90 deg then 
    x'=-y
    y'= x

    then normals to line segment would be:
    (-dy,dx)(dy,-dx)

    """
    width = 100
    skeleton_norm = np.empty((2,), dtype=np.float32)

    perp_line = [-(coord_b[1]-coord_a[1]), coord_b[0]-coord_a[0]]
    # Take the magnitude to get the length of the vector 
    norm = np.sqrt(perp_line[0]*perp_line[0]+perp_line[1]*perp_line[1])

    skeleton_norm[0] = (perp_line[0] / norm) * (width / 2)
    skeleton_norm[1] = (perp_line[1] / norm) * (width / 2)

    ##Box origin is 'lower' instead of upper
    bot_l = coord_a + skeleton_norm
    top_l = coord_b + skeleton_norm
    top_r = coord_b - skeleton_norm # 
    bot_r = coord_a - skeleton_norm # 

    if side == 'L':
        bbox_rect_left = np.array(
            [coord_a, coord_b, top_l, bot_l]
        )
        return bbox_rect_left
    elif side == 'R':
        bbox_rect_right = np.array(
            [coord_a, coord_b, top_r, bot_r]
        )
        return bbox_rect_right
    elif side == 'LR':
        bbox_rect_left =[coord_a, coord_b, top_l, bot_l]
        bbox_rect_right =[coord_a, coord_b, top_r, bot_r]
        return np.array([bbox_rect_left, bbox_rect_right])
    else: 
        bbox_rect = np.array(
            [bot_l, top_l, top_r, bot_r]
        )
        return bbox_rect

#Borrwing from WormPose
# https://github.com/iteal/wormpose/blob/main/wormpose/pose/centerline.py
from scipy.interpolate import interp1d
def interpolate_skeleton(skeleton: np.ndarray, new_dims: int) -> np.ndarray:
    """
    Interpolates a worm skeleton to have a different number of points
    """
    new_pos_dim = []
    for dim in range(skeleton.shape[1]):
        y = skeleton[:, dim]
        x = np.arange(y.size)
        if np.any(np.isnan(y)):
            new_pos_dim.append([np.nan] * (new_dims + 1))
        else:
            # Interpolate the data using a cubic spline to "new_length" samples
            new_length = new_dims + 1
            new_x = np.linspace(x.min(), x.max(), new_length)
            new_y = interp1d(x, y, kind="cubic")(new_x)
            new_pos_dim.append(new_y)
    new_pos = np.vstack(new_pos_dim).T
    return new_pos


def create_skeleton_circles(coord_a,coord_b,side='center',radius=100,offset=0):
    """_summary_

    Args:
        coord_a (_type_): _description_
        coord_b (_type_): _description_
        side (str, optional): _description_. Defaults to 'center'.
        radius (int, optional): _description_. Defaults to 100.
        offset (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_
    """
    skeleton_norm = np.empty((2,), dtype=np.float32)
    offset_coord =np.empty((2,),dtype=np.float32)

    perp_line = [-(coord_b[1]-coord_a[1]), coord_b[0]-coord_a[0]]/2

    # Take the magnitude to get the length of the vector 
    norm = np.sqrt(perp_line[0]*perp_line[0]+perp_line[1]*perp_line[1])

    #Bounding box coordinates for circle
    skeleton_norm[0] = (perp_line[0] / norm) * radius
    skeleton_norm[1] = (perp_line[1] / norm) * radius

    if side == 'L':
        bbox_rect_left = np.array(
            [coord_a, coord_b, top_l, bot_l]
        )
        return bbox_rect_left
    elif side == 'R':
        bbox_rect_right = np.array(
            [coord_a, coord_b, top_r, bot_r]
        )
        return bbox_rect_right
    elif side == 'LR':
        bbox_rect_left =[coord_a+c_off, coord_b+c_off, top_l, bot_l]
        bbox_rect_right =[coord_a-c_off, coord_b-c_off, top_r, bot_r]
        return np.array([bbox_rect_left, bbox_rect_right])
    elif side =='center':
        bbox_rect = np.array(
            [bot_l, top_l, top_r, bot_r]
        )
        return bbox_rect

def create_skeleton_box(coord_a,coord_b,side='center',width=100,offset=0):
    """
    
    Refresh on vector calc
    https://stackoverflow.com/questions/7469959/given-2-points-how-do-i-draw-a-line-at-a-right-angle-to-the-line-formed-by-the-t/7470098#7470098
    The matrix representation of 2D transformation:
    x' = xcos(t) - ysin(t)
    y' = xsin(t)  - ycost(t)

    so if t =90 deg then 
    x'=-y
    y'= x

    then normals to line segment would be:
    (-dy,dx)(dy,-dx)

    """
    skeleton_norm = np.empty((2,), dtype=np.float32)
    offset_norm =np.empty((2,),dtype=np.float32)

    perp_line = [-(coord_b[1]-coord_a[1]), coord_b[0]-coord_a[0]]
    # Take the magnitude to get the length of the vector 
    norm = np.sqrt(perp_line[0]*perp_line[0]+perp_line[1]*perp_line[1])

    skeleton_norm[0] = (perp_line[0] / norm) * (width+offset)
    skeleton_norm[1] = (perp_line[1] / norm) * (width+offset)

    offset_norm[0]= (perp_line[0] / norm) * (offset)
    offset_norm[1]= (perp_line[1] / norm) * (offset)

    # Coordinates of the boxes
    bot_l = coord_a + skeleton_norm
    top_l = coord_b + skeleton_norm
    top_r = coord_b - skeleton_norm
    bot_r = coord_a - skeleton_norm

    #Offsets for coordinate of box
    offset_a_L = coord_a +  offset_norm
    offset_b_L = coord_b + offset_norm
    offset_a_R = coord_a -  offset_norm
    offset_b_R = coord_b - offset_norm


    if side == 'L':
        bbox_rect_left = np.array(
            [offset_a_L, offset_b_L, top_l, bot_l]
        )
        return bbox_rect_left
    elif side == 'R':
        bbox_rect_right = np.array(
            [offset_a_R, offset_b_R, top_r, bot_r]
        )
        return bbox_rect_right
    elif side == 'LR':
        bbox_rect_left =[offset_a_L, offset_b_L, top_l, bot_l]
        bbox_rect_right =[offset_a_R, offset_b_R, top_r, bot_r]
        return np.array([bbox_rect_left, bbox_rect_right])
    elif side =='center':
        bbox_rect = np.array(
            [bot_l, top_l, top_r, bot_r]
        )
        return bbox_rect
        
from scipy.interpolate import interp1d

def interpolate_skeleton(skeleton: np.ndarray, new_dims: int) -> np.ndarray:
    """
    Interpolates a worm skeleton to have a different number of points
    """
    new_pos_dim = []
    for dim in range(skeleton.shape[1]):
        y = skeleton[:, dim]
        x = np.arange(y.size)
        if np.any(np.isnan(y)):
            new_pos_dim.append([np.nan] * (new_dims + 1))
        else:
            # Interpolate the data using a cubic spline to "new_length" samples
            new_length = new_dims + 1
            new_x = np.linspace(x.min(), x.max(), new_length)
            new_y = interp1d(x, y, kind="cubic")(new_x)
            new_pos_dim.append(new_y)
    new_pos = np.vstack(new_pos_dim).T
    return new_pos
    
def skeletons_to_angles(skeletons: np.ndarray, theta_dims: int) -> np.ndarray:
    new_skeletons = []
    for frame in range(skeletons.shape[0]):
        skeleton = skeletons[frame]
        new_skeletons.append(interpolate_skeleton(skeleton, theta_dims))
    new_skeletons = np.array(new_skeletons, skeletons.dtype)

    skel_x = new_skeletons[:, :, 0]
    skel_y = new_skeletons[:, :, 1]
    d_x = np.diff(skel_x, axis=1)
    d_y = np.diff(skel_y, axis=1)
    # calculate tangent angles.  atan2 uses angles from -pi to pi
    angles = np.arctan2(d_y, d_x)
    return angles.astype(np.float32)

def skeleton_to_angle(skeleton: np.ndarray, theta_dims: int):
    new_skeleton = interpolate_skeleton(skeleton, theta_dims)
    skel_x = new_skeleton[:, 1]
    skel_y = new_skeleton[:, 2]
    d_x = np.diff(skel_x)
    d_y = np.diff(skel_y)
    # calculate tangent angles.  atan2 uses angles from -pi to pi
    angles = np.arctan2(d_y, d_x)
    angles=np.degrees(angles)
    return angles.astype(np.float32)
    
def angle_distance(theta_a: np.ndarray, theta_b: np.ndarray) -> float:
    """
    Angle distance that takes into account the periodicity of angles
    """
    diff = np.abs(np.arctan2(np.sin(theta_a - theta_b), np.cos(theta_a - theta_b)))
    return diff.mean()

def skeleton_bends(skeleton: np.ndarray, theta_dims: int):
    new_skeleton = interpolate_skeleton(skeleton, theta_dims)
    skel_x = new_skeleton[:, 1]
    skel_y = new_skeleton[:, 2]
    bends =[]
    for i in range(2,len(skel_x)-1):
        a = [skel_x[i-1]-skel_x[i], skel_y[i-1]-skel_y[i]]
        b = [skel_x[i+1]-skel_x[i], skel_y[i+1]-skel_y[i]]
        angle= np.arcsin(np.cross(a,b)/np.mag(a)/np.mag(b))*180/np.pi
        bends.appends(angle)
    return bends

"""
Crop out the tilted ROIs generated to measure the ventral and dorsal sides

# https://stackoverflow.com/questions/11627362/how-to-straighten-a-rotated-rectangle-area-of-an-image-using-opencv-in-python/48553593#48553593

    @Parameters:
    rect (y,x) = coordinates of corners of ROI
    src (y,x) =image in 8 bit or float 32
"""

def getSubImage(src, rect):
    """_summary_

    Args:
        src (y,x): uint8 or float 32 image 
        rect (y,x): coordinates of 4 corners of ROI


    Returns:
        _type_: _description_
    """
    import cv2 
    
    rect = np.int0(rect)
    rect = rect[:,[1,0]]
    rect = cv2.minAreaRect(rect)

    # Get center, size, and angle from rect
    center, size, theta = rect
    # Convert to int 
    center, size = tuple(map(int, center)), tuple(map(int, size))
    # Get rotation matrix for rectangle
    M = cv2.getRotationMatrix2D( center, theta, 1)
    # Perform rotation on src image
    dst = cv2.warpAffine(src.astype(np.float32), M, src.shape[:2])
    out = cv2.getRectSubPix(dst, size, center)
    return out

def create_circular_mask(h, w, center=None, radius=None):
    """_summary_

    Args:
        h (_type_): _description_
        w (_type_): _description_
        center (_type_, optional): _description_.
        radius (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    if center is None: # use the middle of the image
        center = (int(w/2), int(h/2))
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    return mask
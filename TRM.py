import numpy as np
import functions as fn

def TRM_single_point(img, point, step_size = 15, weights=np.array([[-1-1j, 0-1j, 1-1j],[-1, 0, 1],[-1+1j,0+1j,1+1j]]), scale=False, return_points = False):
    weights = weights.reshape(1, -1)[0]
    weights = np.delete(weights, 4)
    h, w = img.shape
    # step_size = 15
    dx, dy = np.gradient(img)
    magnitude = np.sqrt(dx**2 + dy**2)
    mean = np.average(magnitude)
    std = np.std(magnitude)
    thresh = mean + 2 * std

    near_points = fn.find_8_neighbors(point, step_size=step_size, max_size=h)
    mem_link_state = np.ones(8)
    for i, near_point in enumerate(near_points):
        # print(point, near_point)
        max_value = fn.max_intensity_along_line(magnitude, point, near_point)
        if max_value>=thresh:
            mem_link_state[i] = 0

    THI = np.sum(mem_link_state * weights)
    return THI
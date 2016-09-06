import numpy as np
nBin=16
kernel_sum=0.0

def get_pdf(img, box):
    global nBin, kernel_sum
    kernel_sum = 0.0
    pdf = np.zeros((3, nBin), np.float32)
    bin_width = (np.round(256./float(nBin)))
    center = (box['height']/2,box['width']/2)
    max_r = max(center)
    for i in range(box['height']):
        for j in range(box['width']):
            # print box['y']+i, box['x']+j
            pixel_val = img[box['y']+i][box['x']+j]
            # print pixel_val
            bin_val = (pixel_val[0], pixel_val[1], pixel_val[2])/bin_width
            # print bin_val
            r2 = np.float64(np.abs(i-center[0])**2+np.abs(j-center[1])**2)
            kernel = max(0.0, (1.0 - r2/(max_r**2)))
            # kernel = 1.0
            pdf[0][bin_val[0]] += kernel
            pdf[1][bin_val[1]] += kernel
            pdf[2][bin_val[2]] += kernel
            kernel_sum += kernel

    pdf /= kernel_sum
    return pdf


def get_weight(img, target_model, target_candidate, box):
    global nBin
    weight = np.ones((box['height'], box['width']), np.float32)
    bin_width = np.round(256./float(nBin))

    for i in range(box['height']):
        for j in range(box['width']):
            pixel_val = img[box['y']+i][box['x']+j]
            bin_val = (pixel_val[0], pixel_val[1], pixel_val[2])/bin_width
            for k in range(3):
                if target_candidate[k][bin_val[k]] == 0.0:
                        target_candidate[k][bin_val[k]] = 0.00000000001
                weight[i][j] *= (np.sqrt(target_model[k][bin_val[k]]/target_candidate[k][bin_val[k]]))
    return weight, sum(sum(weight))

def box_to_array(next_box):
    b=[]
    b.append(next_box['x'])
    b.append(next_box['y'])
    b.append(next_box['width'])
    b.append(next_box['height'])
    return np.array(b, np.uint16)


import numpy as np
cimport numpy as np
cimport cython

DTYPE = np.uint8
DLTYPE = np.uint16
DFTYPE = np.float32
# "ctypedef" assigns a corresponding compile-time type to DTYPE_t. For
# every type in the numpy module there's a corresponding compile-time
# type with a _t-suffix.
ctypedef np.uint8_t DTYPE_t
ctypedef np.uint16_t DLTYPE_t
ctypedef np.float32_t DFTYPE_t

def get_pdf(np.ndarray[DTYPE_t, ndim=3] img, np.ndarray[DLTYPE_t, ndim=1] box, int nBin):
    cdef DFTYPE_t kernel_sum=0.
    cdef np.ndarray[DFTYPE_t, ndim=2] pdf = np.zeros((3, nBin), DFTYPE)
    cdef DFTYPE_t bin_width = (np.round(256./np.float32(nBin)))
    cdef np.ndarray[DTYPE_t, ndim=1]  center = np.array([box[3]/2, box[2]/2], DTYPE)
    cdef DTYPE_t max_r = center.max()
    cdef np.ndarray[DTYPE_t, ndim=1] bin_val
    cdef np.ndarray[DTYPE_t, ndim=1] pixel_val
    cdef DFTYPE_t r2, kernel
    cdef int i,j
    for i in range(box[3]):
        for j in range(box[2]):
            # print box[1]+i, box[0]+j
            pixel_val = img[box[1]+i][box[0]+j]
            # print pixel_val
            bin_val = np.uint8(pixel_val/ bin_width)
            # print bin_val
            r2 = np.abs(i-center[0])**2+np.abs(j-center[1])**2
            kernel = max(0.0, (1.0 - r2/(max_r**2)))
            pdf[0, bin_val[0]] += kernel
            pdf[1, bin_val[1]] += kernel
            pdf[2, bin_val[2]] += kernel
            kernel_sum += kernel

    pdf /= kernel_sum
    return pdf


def get_weight(np.ndarray[DTYPE_t, ndim=3] img, np.ndarray[DFTYPE_t, ndim=2] target_model,  np.ndarray[DFTYPE_t, ndim=2] target_candidate, np.ndarray[DLTYPE_t, ndim=1] box, int nBin):
    cdef np.ndarray[DFTYPE_t, ndim=2] weight = np.ones((box[3], box[2]), DFTYPE)
    cdef DFTYPE_t bin_width = np.round(256./float(nBin))
    cdef np.ndarray[DTYPE_t, ndim=1] bin_val
    cdef np.ndarray[DTYPE_t, ndim=1] pixel_val
    cdef int i,j,k
    for i in range(box[3]):
        for j in range(box[2]):
            pixel_val = img[box[1]+i, box[0]+j]
            bin_val = np.uint8(np.divide(pixel_val, bin_width))
            for k in range(3):
                if target_candidate[k, bin_val[k]] == 0.0:
                        target_candidate[k, bin_val[k]] = 0.00000000001
                weight[i, j] *= (np.sqrt(target_model[k, bin_val[k]]/target_candidate[k, bin_val[k]]))
    return weight, weight.sum()


def get_pdf_and_weight2(np.ndarray[DTYPE_t, ndim=3] img, np.ndarray[DFTYPE_t, ndim=2] target_model, np.ndarray[DLTYPE_t, ndim=1] box, int nBin):
    cdef DFTYPE_t kernel_sum=0
    cdef np.ndarray[DFTYPE_t, ndim=2] target_candidate = np.zeros((3, nBin), DFTYPE)
    cdef DTYPE_t bin_width = (np.round(256./float(nBin)))
    cdef np.ndarray[DFTYPE_t, ndim=1]  center = np.array([box[3]/2, box[2]/2], DFTYPE)
    cdef int max_r = max(center)
    cdef np.ndarray[DTYPE_t, ndim=1] bin_val
    cdef np.ndarray[DTYPE_t, ndim=1] pixel_val
    cdef DFTYPE_t r2, kernel
    cdef np.ndarray[DFTYPE_t, ndim=2] weight = np.ones((box[3], box[2]), np.float32)
    cdef int i,j,k

    for i in range(box[3]):
        for j in range(box[2]):
            pixel_val = img[box[1]+i, box[0]+j]
            bin_val = pixel_val/bin_width
            r2 = float(np.abs(i-center[0])**2+np.abs(j-center[1])**2)
            kernel = max(0.0, (1.0 - r2/(max_r**2)))
            target_candidate[0, bin_val[0]] += kernel
            target_candidate[1, bin_val[1]] += kernel
            target_candidate[2, bin_val[2]] += kernel
            kernel_sum += kernel

    target_candidate = np.divide(target_candidate, kernel_sum)

    for i in range(box[3]):
        for j in range(box[2]):
            pixel_val = img[box[1]+i, box[0]+j]
            bin_val = pixel_val/bin_width
            for k in range(3):
                if target_candidate[k, bin_val[k]] == 0.0:
                        target_candidate[k, bin_val[k]] = 0.00000000001
                weight[i, j] *= (np.sqrt(target_model[k, bin_val[k]]/target_candidate[k, bin_val[k]]))
    return target_candidate,weight, weight.sum()

def get_pdf_and_weight(np.ndarray[DTYPE_t, ndim=3] img, np.ndarray[DFTYPE_t, ndim=2] target_model, np.ndarray[DLTYPE_t, ndim=1] box, int nBin):
    cdef DFTYPE_t kernel_sum=0
    cdef np.ndarray[DFTYPE_t, ndim=2] target_candidate = np.zeros((3, nBin), DFTYPE)
    cdef DTYPE_t bin_width = (np.round(256./float(nBin)))
    cdef np.ndarray[DFTYPE_t, ndim=1]  center = np.array([box[3]/2, box[2]/2], DFTYPE)
    cdef int max_r = max(center)
    cdef np.ndarray[DTYPE_t, ndim=1] bin_val
    cdef np.ndarray[DTYPE_t, ndim=1] pixel_val
    cdef DFTYPE_t r2, kernel=1
    cdef np.ndarray[DFTYPE_t, ndim=2] weight = np.ones((box[3], box[2]), np.float32)
    cdef int i,j,k

    for i in range(box[3]):
        for j in range(box[2]):
            pixel_val = img[box[1]+i, box[0]+j]
            bin_val = pixel_val/bin_width
            target_candidate[0, bin_val[0]] += kernel
            target_candidate[1, bin_val[1]] += kernel
            target_candidate[2, bin_val[2]] += kernel
            kernel_sum += kernel

    target_candidate = np.divide(target_candidate, kernel_sum)

    for i in range(box[3]):
        for j in range(box[2]):
            pixel_val = img[box[1]+i, box[0]+j]
            bin_val = pixel_val/bin_width
            for k in range(3):
                if target_candidate[k, bin_val[k]] == 0.0:
                        target_candidate[k, bin_val[k]] = 0.00000000001
                weight[i, j] *= (np.sqrt(target_model[k, bin_val[k]]/target_candidate[k, bin_val[k]]))
    return target_candidate, weight, weight.sum()


def calc_bhattacharya(np.ndarray[DFTYPE_t, ndim = 2] target_model, np.ndarray[DFTYPE_t, ndim = 2] target_candidate):
    cdef DFTYPE_t p_bar = np.sqrt(np.multiply(target_candidate, target_model)).sum()
    return np.sqrt(1 - p_bar)

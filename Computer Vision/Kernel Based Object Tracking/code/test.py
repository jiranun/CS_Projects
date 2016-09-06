import timeit
import pickle
import numpy as np
import kotutilities
import oldfunctions
nBin = 16

img = np.load('img.pkl')
target_candidate=np.load('targetcandidate.pkl')
target_model=np.load('targetmodel.pkl')
box=pickle.load(open('box.pkl', 'rb'))
b={}
b['x']=box[0]
b['y']=box[1]
b['width']=box[2]
b['height']=box[3]

box = np.array(box, np.uint16)
# m = np.random.rand(50,50)
n=1000
# timer = timeit.Timer(stmt='oldfunctions.box_to_array2(b)', setup='from __main__ import oldfunctions, b')
# print "Python 1       (ms): %g" % (timer.timeit(n)*1000/n)
#
# timer = timeit.Timer(stmt='oldfunctions.box_to_array2(b)', setup='from __main__ import oldfunctions, b')
# print "Python 2       (ms): %g" % (timer.timeit(n)*1000/n)

# # ** changed .timeit(1) to .timeit(1000) for each one **
# timer = timeit.Timer(stmt='oldfunctions.get_pdf(img, b)', setup='from __main__ import oldfunctions, img, b')
# print "Python PDF       (ms): %g" % (timer.timeit(n)*1000/n)
#
# timer = timeit.Timer(stmt='kotutilities.get_pdf(img, box, nBin)', setup='from __main__ import kotutilities, img, box, nBin')
# print "Cython PDF       (ms): %g" % (timer.timeit(n)*1000/n)
#
# timer = timeit.Timer(stmt='oldfunctions.get_weight(img, target_model, target_candidate, b)', setup='from __main__ import oldfunctions, img, target_model, target_candidate, b')
# print "Python WEIGHT       (ms): %g" % (timer.timeit(n)*1000/n)
#
# timer = timeit.Timer(stmt='kotutilities.get_weight(img,target_model, target_candidate, box, nBin)', setup='from __main__ import kotutilities, img,target_model, target_candidate, box, nBin')
# print "Cython WEIGHT       (ms): %g" % (timer.timeit(n)*1000/n)
#
# timer = timeit.Timer(stmt='kotutilities.get_pdf_and_weight(img, target_model, box, nBin)', setup='from __main__ import kotutilities, img,target_model, box, nBin')
# print "Cython PDF&WEIGHT 1      (ms): %g" % (timer.timeit(n)*1000/n)
#
# timer = timeit.Timer(stmt='kotutilities.get_pdf_and_weight2(img, target_model, box, nBin)', setup='from __main__ import kotutilities, img,target_model, box, nBin')
# print "Cython PDF&WEIGHT 2      (ms): %g" % (timer.timeit(n)*1000/n)

timer = timeit.Timer(stmt='kotutilities.calc_bhattacharya(target_model, target_candidate)', setup='from __main__ import kotutilities, target_model, target_candidate')
print "Cython BachCoef     (ms): %g" % (timer.timeit(n)*1000/n)
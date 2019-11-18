import numpy as np
from scipy.misc import imread, imresize
import tensorflow as tf
import matplotlib.pyplot as plt


def vignetting(I, a):
    r = radius(I)
    s = poly(a, r)

    J = np.zeros(I.shape, np.float32)
    J[:, :, 0] = s * I[:, :, 0]
    J[:, :, 1] = s * I[:, :, 1]
    J[:, :, 2] = s * I[:, :, 2]
    return J


def poly(a, r):
    s = a[0] * np.ones_like(r)
    for deg in range(1, len(a)):
        s += a[deg] * (r ** deg)
    return s


def radius(I):
    W, H = (I.shape[1], I.shape[0])
    wc = W / 2
    hc = H / 2

    xv, yv = np.meshgrid(np.arange(W) - wc, np.arange(H) - hc)
    r = np.sqrt(xv ** 2 + yv ** 2) / np.sqrt(wc ** 2 + hc ** 2)
    return r


# image to W*H by 4 matrix
def I2X(I):
    W, H = (I.shape[1], I.shape[0])
    r = radius(I)

    X = np.zeros((W * H, 4), dtype=np.float32)
    X[:, 0] = np.ravel(I[:, :, 0])
    X[:, 1] = np.ravel(I[:, :, 1])
    X[:, 2] = np.ravel(I[:, :, 2])
    X[:, 3] = np.ravel(r)
    return X


def est(Xt, Dt, Xv, Dv, theta0, lam, learning_rate=0.0005, niter=100):
    theta = [tf.Variable(t) for t in theta0]

    x = tf.placeholder(tf.float32)
    d = tf.placeholder(tf.float32)

    st = poly(theta, Xt[:, 3])
    sv = poly(theta, Xv[:, 3])

    losst = (st * x[:, 0] - d[:, 0]) ** 2 + \
            (st * x[:, 1] - d[:, 1]) ** 2 + \
            (st * x[:, 2] - d[:, 2]) ** 2

    lossv = (sv * x[:, 0] - d[:, 0]) ** 2 + \
            (sv * x[:, 1] - d[:, 1]) ** 2 + \
            (sv * x[:, 2] - d[:, 2]) ** 2

    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    train = optimizer.minimize(losst + (lam) * tf.reduce_sum([t ** 2 for t in theta]))
    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)

    for t in range(niter):
        sess.run(train, {x: Xt, d: Dt})
        v_loss = sess.run(lossv, {x: Xv, d: Dv})
        print
        t, v_loss.sum(), sess.run([theta])[0]
        # print '.',
    return sess.run(lossv, {x: Xv, d: Dv}).mean(), sess.run(losst, {x: Xt, d: Dt}).mean(), sess.run([theta])[0]


def devignetting(I, a):
    # compute vignetting factor on complete grid
    r = radius((I))
    s = poly(a, r)

    J = np.zeros(I.shape, np.float32)
    J[:, :, 0] = I[:, :, 0] / s
    J[:, :, 1] = I[:, :, 1] / s
    J[:, :, 2] = I[:, :, 2] / s
    return J


X = np.concatenate((I2X(imread('cat_01.jpg')),
                    I2X(imread('cat_02.jpg')),
                    I2X(imread('cat_03.jpg'))), 0)

D = np.concatenate((I2X(imread('cat_01_vignetted.jpg')),
                    I2X(imread('cat_02_vignetted.jpg')),
                    I2X(imread('cat_03_vignetted.jpg'))), 0)

# randomly suffling the dataset
perm = np.random.permutation(X.shape[0])
perm = perm[1:100]
X = X[perm, :]
D = D[perm, :]
n = X.shape[0]
K = 5
nrange = range(1, 20)

chunk_length = int(n / K)

lossv = np.zeros((K, len(nrange)), dtype=np.float32)
losst = np.zeros((K, len(nrange)), dtype=np.float32)
for ni in range(len(nrange)):

    theta0 = np.zeros(nrange[ni], dtype=np.float32)

    for k in range(K):
        start = k * chunk_length
        stop = (k + 1) * chunk_length

        Xv = X[start:stop, :]
        Dv = D[start:stop, :]

        Xt = X[np.concatenate((np.arange(0, start), np.arange(stop + 1, n))), :]
        Dt = D[np.concatenate((np.arange(0, start), np.arange(stop + 1, n))), :]

        lossv[k, ni], losst[k, ni], thetan = est(Xt, Dt, Xv, Dv, theta0, 0, 0.000000001)

        print
        ni, k, lossv[k, ni], losst[k, ni], thetan
        np.save('lossv', lossv)
        np.save('losst', losst)

plt.subplot(1, 2, 1)
plt.plot(np.mean(lossv, 0))
plt.subplot(1, 2, 2)
plt.plot(np.mean(losst, 0))
plt.show()

'''
theta0 = np.zeros(20,dtype=np.float32)
_,_ , thetan = est(X, D, X, D, theta0, 0, 0.000000001,niter=1000)

X = np.concatenate((I2X(vignetting(imread('cat_01.jpg'), thetan)),
                    I2X(vignetting(imread('cat_02.jpg'), thetan)),
                    I2X(vignetting(imread('cat_03.jpg'), thetan))), 0)

D = np.concatenate((I2X(imread('cat_01_vignetted.jpg')),
                    I2X(imread('cat_02_vignetted.jpg')),
                    I2X(imread('cat_03_vignetted.jpg'))), 0)

standard_deviation = np.sqrt(np.sum((X[:, :-1] - D[:, :-1]) ** 2) / (D.shape[0] - 1))
print standard_deviation

plt.subplot(1, 2, 1)
plt.imshow(np.uint8(devignetting(imread('cat_05_vignetted.jpg'), thetan)))
plt.subplot(1, 2, 2)
plt.imshow(np.uint8(imread('cat_05_vignetted.jpg')))
plt.show()
'''

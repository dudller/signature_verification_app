import numpy as np
import cv2
import pandas as pd
from sklearn.svm import LinearSVC
from skimage.feature import hog
from joblib import dump, load


N_OF_TRAIN_HOGS_1 = 30
N_OF_TRAIN_HOGS_2 = 20


def preprocess(img_list=[]):

    if isinstance(img_list, list):
        output = []
        for img in img_list:
            img_grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_resized = cv2.resize(
                img_grayscale, (700, 350), interpolation=cv2.INTER_AREA)
            _, otsu = cv2.threshold(
                img_resized, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            dft = cv2.dft(np.float32(otsu), flags=cv2.DFT_COMPLEX_OUTPUT)
            dft_shift = np.fft.fftshift(dft)
            magnitude_spectrum = 20 * \
                np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))
            fft_hog = hog(magnitude_spectrum, orientations=8, pixels_per_cell=(8, 8),
                          cells_per_block=(2, 2), multichannel=False, block_norm='L2-Hys', feature_vector=True)

            output.append(fft_hog)
        return output
    else:
        img_grayscale = cv2.cvtColor(img_list, cv2.COLOR_BGR2GRAY)
        img_resized = cv2.resize(
            img_grayscale, (700, 350), interpolation=cv2.INTER_AREA)
        _, otsu = cv2.threshold(
            img_resized, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        dft = cv2.dft(np.float32(otsu), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        magnitude_spectrum = 20 * \
            np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))
        fft_hog = hog(magnitude_spectrum, orientations=8, pixels_per_cell=(8, 8),
                      cells_per_block=(2, 2), multichannel=False, block_norm='L2-Hys', feature_vector=True)
        return fft_hog


def check_signature(img, username):
    descriptor = preprocess(img)
    path = "users/{}.joblib".format(username)
    model = load(path)
    pred = model.predict(descriptor.reshape(1, -1))
    result = pred > 0.5
    return bool(result)


def make_new_model(img_list, username):
    train_hogs = np.load('training/training_features.npz',
                         allow_pickle=True)['arr_0']
    try:
        print(username)
        path = "users/{}.joblib".format(username)
        y_ok = np.ones(len(img_list))
        y_no_ok1 = np.zeros(N_OF_TRAIN_HOGS_1)
        y_no_ok2 = np.zeros(N_OF_TRAIN_HOGS_2)
        y = np.concatenate((y_no_ok1, y_ok, y_no_ok2))
        positives = np.array(preprocess(img_list))
        x = np.concatenate((train_hogs[0:N_OF_TRAIN_HOGS_1], positives,
                            train_hogs[N_OF_TRAIN_HOGS_1:N_OF_TRAIN_HOGS_1+N_OF_TRAIN_HOGS_2]))

        svm = LinearSVC(penalty='l2', loss='squared_hinge',
                        C=1.1, class_weight='balanced')
        model = svm.fit(x, y)
        dump(model, path)
        return True
    except Exception as e:
        print(e.__class__)
        print(e)
        return False

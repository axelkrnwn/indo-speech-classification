from scipy.signal import butter, lfilter, resample
import librosa
import noisereduce as nr
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA

def f_high(y,sr):
    b,a = butter(10, 2000/(sr/2), btype='highpass')
    yf = lfilter(b,a,y)
    return yf

def preprocess(audio, sample_rate):
    audio = nr.reduce_noise(y=audio, sr=sample_rate, stationary=True, prop_decrease=0.9)
    audio = librosa.resample(audio, orig_sr=sample_rate, target_sr=22050)
    return audio

def resampling(cepstral_coefficients):
    length_cc = [len(cc) for cc in cepstral_coefficients]
    return [resample(x, num=int(max(length_cc))) for x in cepstral_coefficients]

def normalize(X):
    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)
    return X

def reduce_dimension(X):
    pca = PCA(n_components=100)
    X = pca.fit_transform(X)
    return X
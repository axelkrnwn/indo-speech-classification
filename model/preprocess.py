from scipy.signal import resample
import loader
import librosa
import noisereduce as nr
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA

def preprocess(audio, sample_rate):
    """
    Preprocesses an audio signal by trimming silence, reducing noise, and resampling.

    Parameters
    ----------
    audio : np.ndarray
        The input audio signal.
    sample_rate : int
        The sampling rate of the audio signal.

    Returns
    -------
    audio: np.ndarray
        The preprocessed audio signal.
    """
    audio =librosa.effects.trim(audio, top_db=10)[0]
    audio = nr.reduce_noise(y=audio, sr=sample_rate, stationary=True, prop_decrease=0.9)
    audio = librosa.resample(audio, orig_sr=sample_rate, target_sr=22050)
    return audio

def resampling(cepstral_coefficients):
    """
    Resamples a list of cepstral coefficient sequences to the same length.

    Parameters
    ----------
    cepstral_coefficients : list of np.ndarray
        A list of numpy arrays representing cepstral coefficient sequences of varying lengths.

    Returns
    -------
    list of np.ndarray
        A list of resampled cepstral coefficient sequences with uniform length.
    """
    length_cc = [len(cc) for cc in cepstral_coefficients]
    return [resample(x, num=3560) for x in cepstral_coefficients]

def normalize(X):
    """
    Normalizes the feature matrix using Min-Max scaling.

    Parameters
    ----------
    X : np.ndarray
        The input feature matrix.

    Returns
    -------
    X: np.ndarray
        The normalized feature matrix.
    """
    try:
        scaler = loader.load_model('scaler')
    except:
        scaler = MinMaxScaler() 
    
    if len(X) == 1:
        X = scaler.transform(X)
    else:
        print(X.shape)
        X = scaler.fit_transform(X)
        loader.save_model(scaler, 'scaler')
    return X

def reduce_dimension(X):
    """
    Reduces the dimensionality of the feature matrix using Principal Component Analysis (PCA).

    Parameters
    ----------
    X : np.ndarray
        The input feature matrix.

    Returns
    -------
    X: np.ndarray
        The transformed feature matrix with reduced dimensions.
    """
    try:
        pca = loader.load_model('pca')
    except:
        pca = PCA(n_components=150)
    
    if min(X.shape) == 1:
        X = pca.transform(X)
    else:
        X = pca.fit_transform(X)
        loader.save_model(pca, 'pca')
    return X
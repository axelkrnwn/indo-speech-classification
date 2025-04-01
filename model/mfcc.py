import numpy as np
from scipy.signal import get_window
import scipy.fftpack as fft

def framing(audio, sample_rate, hop_size, fft_size):
    """
    Splits an audio signal into overlapping frames for further processing.

    This function pads the audio signal using a reflection mode, then segments
    it into frames of a specified size with a given hop size.

    Parameters
    ----------
    audio: np.ndarray
        The input audio signal as a 1D NumPy array.

    sample_rate: int
        The audio signal sampling rate.

    hop_size: float
        The hop size between frames in milliseconds.

    fft_size: int
        The size of each frame in samples.

    Returns
    -------
    audio_frame: np.ndarray
        A numpy array contains framed segment of the input audio.
    """
    
    audio = np.pad(audio, int(fft_size / 2), mode='reflect')
    
    frame_len = np.round(sample_rate * (hop_size / 1000)).astype(int)
    frame_num = int((len(audio) - fft_size) / frame_len)
    audio_frame = np.zeros((frame_num, fft_size))

    for i in range(frame_num):
        audio_frame[i] = audio[i * frame_len: i * frame_len + fft_size]
    
    return audio_frame


def fast_fourier_transform(audio_window_T, fft_size):
    """
    Performs fast fourier transform to the audio window in order to transform the audio to frequency domain.

    This function initializes a numpy complex array using fortran order so that the elements of the array are stored column by column in memory then process each column using fast fourier transform.

    Parameters
    ----------
    audio_window_T: np.ndarray
        The transposed numpy array of audio window.

    fft_size: int
        The size of each frame in samples.
    
    Returns
    -------
    fft_res: np.ndarray
        A complex numpy array contains audio in frequency domain.
    """
    fft_res = np.empty(((fft_size // 2) + 1, audio_window_T.shape[1]), dtype=np.complex64, order='F')

    for i in range(fft_res.shape[1]):
        fft_res[:, i] = fft.fft(audio_window_T[:, i],axis=0)[:fft_res.shape[0]]

    return fft_res

def freq_to_mel(freq):
    """
    Convert frequency to mel.

    Parameters
    ----------
    freq: Any
        The audio frequency value(s).

    Returns
    -------
    Any
        The mel value(s) for each frequency.
    """
    return 2595 * np.log10(1 + freq / 700)

def mel_to_freq(mel):
    """
    Convert mel to frequency.

    Parameters
    ----------
    freq: Any
        The audio mel value(s).

    Returns
    -------
    Any
        The frequency value(s) for each mel.
    """
    return 700 * (10**(mel / 2595) - 1)

def get_filter_points(fmin, fmax, filter_num, sample_rate, fft_size):
    """
    Creates a array of filter points in the audio from fmin to fmax using mel of the frequencies.

    Parameters
    ----------
    fmin: int
        The minimum value of frequency.

    fmax: int
        The maximum value of frequency.

    filter_num: int
        The number of filter points.

    sample_rate: int
        The audio signal sampling rate.

    fft_size: int
        The size of each frame in samples.

    Returns
    -------
    tuple of np.ndarray
        - A numpy array contains computed filter bank points in FFT bin indices.
        - A numpy array contains frequency valueS.
    """
    fmin_mel = freq_to_mel(fmin)
    fmax_mel = freq_to_mel(fmax)

    mels = np.linspace(fmin_mel, fmax_mel, filter_num + 2)
    freqs = mel_to_freq(mels)

    return ((fft_size + 1) / sample_rate * freqs).astype(int),freqs

def get_filters(filter_points, fft_size):
    """
    Generates a set of triangular filter bank filters based on given filter points.

    Parameters
    ----------
    filter_points : np.ndarray
        A sequence of frequency bin indices that define the filter boundaries.
    
    fft_size : int
        The size of the FFT, which determines the frequency resolution.

    Returns
    -------
    np.ndarray
        A numpy array where each row corresponds to a triangular filter 
        applied across the FFT bins.
    """
    filters = np.zeros((len(filter_points) - 2, int(fft_size / 2) + 1))

    for i in range(len(filter_points) - 2):
        filters[i, filter_points[i]:filter_points[i+1]] = np.linspace(0, 1,filter_points[i+1] - filter_points[i])
        filters[i, filter_points[i+1]:filter_points[i+2]] = np.linspace(1, 0,filter_points[i+2] - filter_points[i+1])

    return filters

def mel_filterbank_log(power_audio, fmin, fmax, filter_num, sample_rate, fft_size):
    """
    Computes the logarithmic Mel-filterbank energies.

    This function applies a Mel-filterbank to the power spectrum of an audio signal,
    normalizes the filters, and computes the log power of the filtered signal.
    It is a crucial step in extracting Mel-Frequency Cepstral Coefficients (MFCCs).

    Parameters
    ----------
    power_audio : np.ndarray
        The power spectrum of the audio signal.
    
    fmin: int
        The minimum value of frequency.

    fmax: int
        The maximum value of frequency.

    filter_num: int
        The number of filter points.

    sample_rate: int
        The audio signal sampling rate.

    fft_size: int
        The size of each frame in samples.

    Returns
    -------
    np.ndarray
        A numpy array containing the log Mel-filterbank energies.
    """
    filter_points, freqs = get_filter_points(fmin, fmax , filter_num, sample_rate, fft_size)
    filters = get_filters(filter_points, fft_size)
    enorm = 2 / (freqs[2:2+filter_num] - freqs[:filter_num])
    enorm = enorm[:, np.newaxis]
    filters *= enorm
    audio_filtered = np.dot(filters, power_audio)
    audio_filtered = np.where(audio_filtered == 0, np.finfo(float).eps, audio_filtered)  
    audio_log = 10 * np.log10(audio_filtered)
    return audio_log

def windowing(audio_frames, fft_size):
    """
    Creates an audio window for each frames using hann windowing.

    Parameters
    ----------
    audio_frames: np.ndarray
        A numpy array contains framed segment of the input audio.

    fft_size: int
        The size of each frame in samples.

    Returns
    -------
    audio_window: np.ndarray
        A numpy ndarray contains audio frames after windowing process.
    """
    window = get_window('hann', fft_size, fftbins=True)
    audio_window = audio_frames * window
    return audio_window
    
def dct(dct_filter_num, filter_len):
    """
    Computes the Discrete Cosine Transform (DCT) basis functions.

    Parameters
    ----------
    dct_filter_num : int
        The number of DCT basis filters to generate.

    filter_len : int
        The length of each DCT basis filter.

    Returns
    -------
    np.ndarray
        A numpy array containing the computed DCT basis functions.
    """
    basis = np.empty((dct_filter_num, filter_len))

    basis[0, :] = 1 / np.sqrt(filter_len)

    samples = np.arange(1,2*filter_len, 2) * np.pi / (filter_len * 2)

    for i in range(1,dct_filter_num):
        basis[i, :] = np.cos(i * samples) * np.sqrt(2 / filter_len)

    return basis

def mfcc(audio, sample_rate, fft_size, hop_size, dct_filter_num):
    """
    The overall MFCC Process from pre-emphasis to DCT.
    
    Parameters
    ----------
    audio: np.ndarray
        The input audio.

    sample_rate: int
        The audio signal sampling rate.

    fft_size: int
        The size of each frame in samples.
    
    hop_size: float
        The hop size between frames in milliseconds.
    
    dct_filter_num : int
        The number of DCT basis filters to generate.

    Returns
    -------
    cc: np.ndarray
        A 2D NumPy array where each column represents an MFCC feature vector.
    """
    
    audio = audio / np.max(np.abs(audio))
    audio_frames = framing(audio, sample_rate, hop_size, fft_size)
    audio_window = windowing(audio_frames, fft_size)
    audio_fft = fast_fourier_transform(audio_window.T, fft_size)
    power_audio = np.square(np.abs(audio_fft))
    fmin = 0
    fmax = sample_rate / 2
    filter_num = 10
    audio_log = mel_filterbank_log(power_audio, fmin, fmax, filter_num, sample_rate, fft_size) 
    dct_filters = dct(dct_filter_num, filter_num)
    cc = np.dot(dct_filters, audio_log)
    return cc

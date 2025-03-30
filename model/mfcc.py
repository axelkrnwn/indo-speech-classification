import numpy as np
from scipy.signal import get_window
import scipy.fftpack as fft

def framing(audio, sample_rate, hop_size, fft_size):
    
    audio = np.pad(audio, int(fft_size / 2), mode='reflect')
    
    frame_len = np.round(sample_rate * (hop_size / 1000)).astype(int)
    frame_num = int((len(audio) - fft_size) / frame_len)
    audio_frame = np.zeros((frame_num, fft_size))

    for i in range(frame_num):
        audio_frame[i] = audio[i * frame_len: i * frame_len + fft_size]
    
    return audio_frame


def fast_fourier_transform(audio_window_T, fft_size):
    fft_res = np.empty(((fft_size // 2) + 1, audio_window_T.shape[1]), dtype=np.complex64, order='F')

    for i in range(fft_res.shape[1]):
        fft_res[:, i] = fft.fft(audio_window_T[:, i],axis=0)[:fft_res.shape[0]]

    return fft_res

def freq_to_mel(freq):
    return 2595 * np.log10(1 + freq / 700)

def mel_to_freq(mel):
    return 700 * (10**(mel / 2595) - 1)

def get_filter_points(fmin, fmax, filter_num, sample_rate, fft_size):
    fmin_mel = freq_to_mel(fmin)
    fmax_mel = freq_to_mel(fmax)

    mels = np.linspace(fmin_mel, fmax_mel, filter_num + 2)
    freqs = mel_to_freq(mels)

    return ((fft_size + 1) / sample_rate * freqs).astype(int),freqs

def get_filters(filter_points, fft_size):
    filters = np.zeros((len(filter_points) - 2, int(fft_size / 2) + 1))

    for i in range(len(filter_points) - 2):
        filters[i, filter_points[i]:filter_points[i+1]] = np.linspace(0, 1,filter_points[i+1] - filter_points[i])
        filters[i, filter_points[i+1]:filter_points[i+2]] = np.linspace(1, 0,filter_points[i+2] - filter_points[i+1])

    return filters

def mel_filterbank_log(power_audio, fmin, fmax, filter_num, sample_rate, fft_size):
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
    window = get_window('hann', fft_size, fftbins=True)
    audio_window = audio_frames * window
    return audio_window
    
def dct(dct_filter_num, filter_len):
    basis = np.empty((dct_filter_num, filter_len))

    basis[0, :] = 1 / np.sqrt(filter_len)

    samples = np.arange(1,2*filter_len, 2) * np.pi / (filter_len * 2)

    for i in range(1,dct_filter_num):
        basis[i, :] = np.cos(i * samples) * np.sqrt(2 / filter_len)

    return basis

def mfcc(audio, sample_rate, fft_size, hop_size, dct_filter_num):
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

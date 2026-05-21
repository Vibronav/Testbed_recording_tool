import matplotlib.pyplot as plt
from scipy.io import wavfile

def show_spectrogram(recording_path):
    try:
        sample_rate, data = wavfile.read(recording_path)
            
        plt.figure(figsize=(10, 4))
        plt.specgram(data, Fs=sample_rate, NFFT=1024, noverlap=512, cmap='viridis')
        plt.title(f'Spectrogram of {recording_path.name}')
        plt.xlabel('Time [s]')
        plt.ylabel('Frequency [Hz]')
        plt.colorbar(label='Intensity [dB]')
        plt.tight_layout()
        plt.show()
    except ImportError:
        print("To view the spectrogram, please install matplotlib and scipy.")
        print("pip install matplotlib scipy")

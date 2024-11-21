import numpy as np
import torch
import torch.nn as nn
import scipy.io.wavfile as wav

# 오디오 로드
sample_rate, waveform = wav.read("./music/noise_short.wav")  # WAV 파일 로드
waveform = waveform.astype(np.float32) / 32768.0  # 정규화 (16-bit PCM 기준)
waveform = torch.from_numpy(waveform).unsqueeze(0)  # PyTorch 텐서 변환 (채널 추가)

# 멜 스펙트로그램 변환 (직접 구현)
class MelSpectrogram:
    def __init__(self, sample_rate, n_mels, n_fft, hop_length):
        self.sample_rate = sample_rate
        self.n_mels = n_mels
        self.n_fft = n_fft
        self.hop_length = hop_length

    def __call__(self, waveform):
        # Short-Time Fourier Transform (STFT)
        stft = torch.stft(waveform, n_fft=self.n_fft, hop_length=self.hop_length, return_complex=True)
        spectrogram = torch.abs(stft) ** 2  # Power spectrogram
        # Mel filter bank 적용
        mel_filter = torch.randn(self.n_mels, self.n_fft // 2 + 1)  # 간단히 임의의 필터 생성 (예시)
        mel_spectrogram = torch.matmul(mel_filter, spectrogram)
        return mel_spectrogram

# 멜 스펙트로그램 생성
mel_transform = MelSpectrogram(sample_rate=sample_rate, n_mels=128, n_fft=1024, hop_length=512)
mel_spec = mel_transform(waveform)

# 간단한 CNN 모델
class AudioEmbeddingModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.flatten = nn.Flatten()

    def forward(self, x):
        x = self.conv1(x)
        x = self.pool(x)
        x = self.flatten(x)
        return x

# CNN 모델로 임베딩 추출
model = AudioEmbeddingModel()
mel_spec = mel_spec.unsqueeze(0).unsqueeze(0)  # (배치, 채널, 높이, 너비)
embedding = model(mel_spec)

print("Mel spectrogram shape:", mel_spec.shape)
print("Embedding shape:", embedding.shape)

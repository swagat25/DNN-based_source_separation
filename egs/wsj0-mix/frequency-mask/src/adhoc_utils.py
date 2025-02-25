import torch
import torch.nn as nn
import torch.nn.functional as F

from utils.utils_audio import build_window
from algorithm.frequency_mask import compute_ideal_binary_mask, compute_ideal_ratio_mask, compute_phase_sensitive_mask

class FrequencyMasking(nn.Module):
    def __init__(self, fft_size, hop_size=None, window_fn='hann', domain='time'):
        super().__init__()
        
        if hop_size is None:
            hop_size = fft_size // 2
        
        self.fft_size, self.hop_size = fft_size, hop_size
        window = build_window(fft_size, window_fn=window_fn)
        self.window = nn.Parameter(window, requires_grad=False)

        assert domain in ['time'], "domain is expected time."

        self.domain = domain

    def forward(self, mixture, sources):
        T = mixture.size(-1)

        mixture, sources = self.stft(mixture), self.stft(sources)
        mask = self.compute_mask(sources)
        output = mask * mixture
        output = self.istft(output)

        T_pad = output.size(-1)
        output = F.pad(output, (0, T - T_pad))

        return output
    
    def compute_mask(self, input):
        raise NotImplementedError("Implement compute_mask().")
    
    def stft(self, input):
        fft_size, hop_size = self.fft_size, self.hop_size
        window = self.window

        n_dims = input.dim()

        if n_dims > 2:
            channels = input.size()[:-1]
            input = input.view(-1, input.size(-1))
        
        output = torch.stft(input, fft_size, hop_length=hop_size, window=window, return_complex=True)

        if n_dims > 2:
            output = output.view(*channels, *output.size()[-2:])

        return output

    def istft(self, input):
        fft_size, hop_size = self.fft_size, self.hop_size
        window = self.window

        n_dims = input.dim()

        if n_dims > 2:
            channels = input.size()[:-2]
            input = input.view(-1, *input.size()[-2:])
        
        output = torch.istft(input, fft_size, hop_length=hop_size, window=window, return_complex=False)

        if n_dims > 2:
            output = output.view(*channels, output.size(-1))

        return output

class IdealBinaryMasking(FrequencyMasking):
    def __init__(self, fft_size, hop_size=None, window_fn='hann', domain='time'):
        super().__init__(fft_size, hop_size=hop_size, window_fn=window_fn, domain=domain)
    
    def compute_mask(self, input):
        mask = compute_ideal_binary_mask(input)
        return mask

class IdealRatioMasking(FrequencyMasking):
    def __init__(self, fft_size, hop_size=None, window_fn='hann', domain='time'):
        super().__init__(fft_size, hop_size=hop_size, window_fn=window_fn, domain=domain)
    
    def compute_mask(self, input):
        mask = compute_ideal_ratio_mask(input)
        return mask

class PhaseSensitiveMasking(FrequencyMasking):
    def __init__(self, fft_size, hop_size=None, window_fn='hann', domain='time'):
        super().__init__(fft_size, hop_size=hop_size, window_fn=window_fn, domain=domain)
    
    def compute_mask(self, input):
        mask = compute_phase_sensitive_mask(input)
        return mask
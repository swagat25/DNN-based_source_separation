#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import numpy as np
import pyaudio
import torch
import torchaudio

from models.dprnn_tasnet import DPRNNTasNet

parser = argparse.ArgumentParser(description="Demonstration of Conv-TasNet")

parser.add_argument('--sample_rate', '-sr', type=int, default=16000, help='Sampling rate')
parser.add_argument('--num_chunk', type=int, default=256, help='Number of chunks')
parser.add_argument('--duration', type=int, default=10, help='Duration [sec]')
parser.add_argument('--model_path', type=str, default='./best.pth', help='Path for model')
parser.add_argument('--save_dir', type=str, default='./results', help='Directory to save estimation.')

FORMAT = pyaudio.paInt16
NUM_CHANNEL = 1
DEVICE_INDEX = 0

def main(args):
    process_offline(args.sample_rate, args.num_chunk, duration=args.duration, model_path=args.model_path, save_dir=args.save_dir)

def process_offline(sample_rate, num_chunk, duration=5, model_path=None, save_dir="results"):
    num_loop = int(duration * sample_rate / num_chunk)
    sequence = []
    
    P = pyaudio.PyAudio()
    
    # Record
    stream = P.open(format=FORMAT, channels=NUM_CHANNEL, rate=sample_rate, input_device_index=DEVICE_INDEX, frames_per_buffer=num_chunk, input=True, output=False)
    
    for i in range(num_loop):
        input = stream.read(num_chunk)
        sequence.append(input)
        time = int(i * num_chunk / sample_rate)
        show_progress_bar(time, duration)
    
    show_progress_bar(duration, duration)
    print()
    
    stream.stop_stream()
    stream.close()
    P.terminate()
    
    print("Stop recording")
    
    # Save
    signal = b"".join(sequence)
    signal = np.frombuffer(signal, dtype=np.int16)
    signal = signal / 32768

    save_path = os.path.join(save_dir, "mixture.wav")
    mixture = torch.Tensor(signal).float()
    torchaudio.save(save_path, mixture.unsqueeze(dim=0), sample_rate=sample_rate)

    # Separate by DNN
    os.makedirs(save_dir, exist_ok=True)
    
    model = load_model(model_path)
    model.eval()

    print("Start separation...")
    
    with torch.no_grad():
        mixture = torch.Tensor(signal).float()
        mixture = mixture.unsqueeze(dim=0).unsqueeze(dim=0)
        estimated_sources = model(mixture)
        estimated_sources = estimated_sources.squeeze(dim=0).detach().cpu()
    
    print("Finished separation...")
    
    for idx, estimated_source in enumerate(estimated_sources):
        save_path = os.path.join(save_dir, "estimated-{}.wav".format(idx))
        torchaudio.save(save_path, estimated_source.unsqueeze(dim=0), sample_rate=sample_rate)
    
def show_progress_bar(time, duration):
    rest = duration-time
    progress_bar = ">"*time + "-"*rest
    print("\rNow recording...", progress_bar, "{:2d}[sec]".format(rest), end="")

    
def load_model(model_path):
    package = torch.load(model_path, map_location=lambda storage, loc: storage)
    
    model = DPRNNTasNet.build_model(model_path)
    model.load_state_dict(package['state_dict'])
    
    print("# Parameters: {}".format(model.num_parameters))

    return model
    

if __name__ == '__main__':
    args = parser.parse_args()

    print(args)
    main(args)



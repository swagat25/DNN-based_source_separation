#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse

import torch
import torch.nn as nn

from utils.utils import set_seed
from adhoc_dataset import SpectrogramTestDataset, TestDataLoader
from adhoc_driver import AdhocTester
from models.d3net import D3Net, ParallelD3Net
from criterion.distance import MeanSquaredError

parser = argparse.ArgumentParser(description="Evaluation of D3Net")

parser.add_argument('--musdb18_root', type=str, default=None, help='Path to MUSDB18')
parser.add_argument('--sample_rate', '-sr', type=int, default=44100, help='Sampling rate')
parser.add_argument('--patch_size', type=int, default=256, help='Patch size')
parser.add_argument('--fft_size', type=int, default=4096, help='FFT length')
parser.add_argument('--hop_size', type=int, default=1024, help='Hop length')
parser.add_argument('--window_fn', type=str, default='hann', help='Window function')
parser.add_argument('--sources', type=str, default="[bass,drums,other,vocals]", help='Source names')
parser.add_argument('--criterion', type=str, default='mse', choices=['mse'], help='Criterion')
parser.add_argument('--model_dir', type=str, default=None, help='Directory which includes drums/<model_choice>.pth, ..., vocals/<model_choice>.pth')
parser.add_argument('--estimates_dir', type=str, default=None, help='Estimated sources output directory')
parser.add_argument('--json_dir', type=str, default=None, help='Json directory')
parser.add_argument('--model_choice', type=str, default='last', choices=['best', 'last'], help='Model choice. Default: last')
parser.add_argument('--estimate_all', type=int, default=1, help='Estimates all songs. GPU is required if use_cuda=1.')
parser.add_argument('--evaluate_all', type=int, default=1, help='Evaluates all estimations. GPU is NOT required.')
parser.add_argument('--use_norbert', type=int, default=0, help='Use norbert.wiener for multichannel wiener filetering. 0: Not use norbert, 1: Use norbert (you have to install norbert)')
parser.add_argument('--use_cuda', type=int, default=1, help='0: Not use cuda, 1: Use cuda')
parser.add_argument('--seed', type=int, default=42, help='Random seed')

def main(args):
    set_seed(args.seed)
    
    args.sources = args.sources.replace('[', '').replace(']', '').split(',')

    test_dataset = SpectrogramTestDataset(args.musdb18_root, fft_size=args.fft_size, hop_size=args.hop_size, window_fn=args.window_fn, sample_rate=args.sample_rate, patch_size=args.patch_size, sources=args.sources, target=args.sources)
    print("Test dataset includes {} samples.".format(len(test_dataset)))
    
    loader = TestDataLoader(test_dataset, batch_size=1, shuffle=False)
    
    modules = {}
    for source in args.sources:
        model_path = os.path.join(args.model_dir, source, "{}.pth".format(args.model_choice))
        modules[source] = D3Net.build_model(model_path)
    
    model = ParallelD3Net(modules)
    
    print(model)
    print("# Parameters: {}".format(model.num_parameters))
    
    if args.use_cuda:
        if torch.cuda.is_available():
            model.cuda()
            model = nn.DataParallel(model)
            print("Use CUDA")
        else:
            raise ValueError("Cannot use CUDA.")
    else:
        print("Does NOT use CUDA")
    
    # Criterion
    if args.criterion == 'mse':
        criterion = MeanSquaredError(dim=(1,2,3))
        args.save_normalized = False
    else:
        raise ValueError("Not support criterion {}".format(args.criterion))
    
    tester = AdhocTester(model, loader, criterion, args)
    tester.run()
    
if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
    main(args)

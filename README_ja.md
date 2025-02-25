# DNNによる音源分離
DNNによる音源分離（PyTorch実装）

## 新しい情報
- v0.7.0
  - モデルの追加（`MMDenseLSTM`，`X-UMX`，`HRNet`，`SepFormer`）．
  - 学習済みモデルの追加．

## モデル
| モデル | 参考文献 | 実装 |
| :---: | :---: | :---: |
| WaveNet | [WaveNet: A Generative Model for Raw Audio](https://arxiv.org/abs/1609.03499) | ✔ |
| Wave-U-Net | [Wave-U-Net: A Multi-Scale Neural Network for End-to-End Audio Source Separation](https://arxiv.org/abs/1806.03185) |  |
| Deep clustering | [Single-Channel Multi-Speaker Separation using Deep Clustering](https://arxiv.org/abs/1607.02173) |  |
| Chimera++ | [Alternative Objective Functions for Deep Clustering](https://www.merl.com/publications/docs/TR2018-005.pdf) |  |
| DANet | [Deep Attractor Network for Single-microphone Apeaker Aeparation](https://arxiv.org/abs/1611.08930) | ✔ |
| ADANet | [Speaker-independent Speech Separation with Deep Attractor Network](https://arxiv.org/abs/1707.03634) |  |
| TasNet | [TasNet: Time-domain Audio Separation Network for Real-time, Single-channel Speech Separation](https://arxiv.org/abs/1711.00541) | ✔ |
| Conv-TasNet | [Conv-TasNet: Surpassing Ideal Time-Frequency Magnitude Masking for Speech Separation](https://arxiv.org/abs/1809.07454) | ✔ |
| DPRNN-TasNet | [Dual-path RNN: Efficient Long Sequence Modeling for Time-domain Single-channel Speech Separation](https://arxiv.org/abs/1910.06379) | ✔ |
| Gated DPRNN-TasNet | [Voice Separation with an Unknown Number of Multiple Speakers](https://arxiv.org/abs/2003.01531) |  |
| FurcaNet | [FurcaNet: An End-to-End Deep Gated Convolutional, Long Short-term Memory, Deep Neural Networks for Single Channel Speech Separation](https://arxiv.org/abs/1902.00651) |  |
| FurcaNeXt | [FurcaNeXt: End-to-End Monaural Speech Separation with Dynamic Gated Dilated Temporal Convolutional Networks](https://arxiv.org/abs/1902.04891) |
| DeepCASA | [Divide and Conquer: A Deep Casa Approach to Talker-independent Monaural Speaker Separation](https://arxiv.org/abs/1904.11148) |  |
| Conditioned-U-Net | [Conditioned-U-Net: Introducing a Control Mechanism in the U-Net for multiple source separations](https://arxiv.org/abs/1907.01277) | ✔ |
| MMDenseNet | [Multi-scale Multi-band DenseNets for Audio Source Separation](https://arxiv.org/abs/1706.09588) | ✔ |
| MMDenseLSTM | [MMDenseLSTM: An Efficient Combination of Convolutional and Recurrent Neural Networks for Audio Source Separation](https://arxiv.org/abs/1805.02410) | ✔ |
| Open-Unmix (UMX) | [Open-Unmix - A Reference Implementation for Music Source Separation](https://hal.inria.fr/hal-02293689/document) | ✔ |
| Wavesplit | [Wavesplit: End-to-End Speech Separation by Speaker Clustering](https://arxiv.org/abs/2002.08933) |  |
| Dual-Path Transformer Network (DPTNet) | [Dual-Path Transformer Network: Direct Context-Aware Modeling for End-to-End Monaural Speech Separation](https://arxiv.org/abs/2007.13975) | ✔ |
| CrossNet-Open-Unmix (X-UMX) | [All for One and One for All: Improving Music Separation by Bridging Networks](https://arxiv.org/abs/2010.04228) | ✔ |
| D3Net | [D3Net: Densely connected multidilated DenseNet for music source separation](https://arxiv.org/abs/2010.01733) | ✔ |
| LaSAFT | [LaSAFT: Latent Source Attentive Frequency Transformation for Conditioned Source Separation](https://arxiv.org/abs/2010.11631) |  |
| SepFormer | [Attention is All You Need in Speech Separation](https://arxiv.org/abs/2010.13154) | ✔ |
| GALR | [Effective Low-Cost Time-Domain Audio Separation Using Globally Attentive Locally Reccurent networks](https://arxiv.org/abs/2101.05014) | ✔ |
| HRNet | [Vocal Melody Extraction via HRNet-Based Singing Voice Separation and Encoder-Decoder-Based F0 Estimation](https://www.mdpi.com/2079-9292/10/3/298) | ✔ |
| MRX | [The Cocktail Fork Problem: Three-Stem Audio Separation for Real-World Soundtracks](https://arxiv.org/abs/2110.09958) |  |

## モジュール
| モジュール | 参考文献 | 実装 |
| :---: | :---: | :---: |
| Depthwise-separable convolution |  | ✔ |
| Gated Linear Units (GLU) |  | ✔ |
| Feature-wise Linear Modulation (FiLM) | [FiLM: Visual Reasoning with a General Conditioning Layer](https://arxiv.org/abs/1709.07871) | ✔ |
| Point-wise Convolutional Modulation (PoCM) | [LaSAFT: Latent Source Attentive Frequency Transformation for Conditioned Source Separation](https://arxiv.org/abs/2010.11631) | ✔ |

## 学習に関する手法
| 手法 | 参考文献 | 実装 |
| :---: | :---: | :---: |
| Pemutation invariant training (PIT) | [Multi-talker Speech Separation with Utterance-level Permutation Invariant Training of Deep Recurrent Neural Networks](https://arxiv.org/abs/1703.06284) | ✔ |
| One-and-rest PIT | [Recursive Speech Separation for Unknown Number of Speakers](https://arxiv.org/abs/1904.03065) | ✔ |
| Probabilistic PIT | [Probabilistic Permutation Invariant Training for Speech Separation](https://arxiv.org/abs/1908.01768) |  |
| Sinkhorn PIT | [Towards Listening to 10 People Simultaneously: An Efficient Permutation Invariant Training of Audio Source Separation Using Sinkhorn's Algorithm](https://arxiv.org/abs/2010.11871) | ✔ |
| Combination Loss | [All for One and One for All: Improving Music Separation by Bridging Networks](https://arxiv.org/abs/2010.04228) | ✔ |

## 実行例
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tky823/DNN-based_source_separation/blob/main/egs/tutorials/conv-tasnet/train_librispeech.ipynb)

[Conv-TasNet](https://arxiv.org/abs/1809.07454)によるLibriSpeechデータセットを用いた音源分離の例

`<REPOSITORY_ROOT>/egs/tutorials/`で他のチュートリアルも確認可能．

### 0. データセットの準備
```sh
cd <REPOSITORY_ROOT>/egs/tutorials/common/
. ./prepare_librispeech.sh --dataset_root <DATASET_DIR> --n_sources <#SPEAKERS>
```

### 1. 学習
```sh
cd <REPOSITORY_ROOT>/egs/tutorials/conv-tasnet/
. ./train.sh --exp_dir <OUTPUT_DIR>
```

学習を途中から再開したい場合，
```sh
. ./train.sh --exp_dir <OUTPUT_DIR> --continue_from <MODEL_PATH>
```

### 2. 評価
```sh
cd <REPOSITORY_ROOT>/egs/tutorials/conv-tasnet/
. ./test.sh --exp_dir <OUTPUT_DIR>
```

### 3. デモンストレーション
```sh
cd <REPOSITORY_ROOT>/egs/tutorials/conv-tasnet/
. ./demo.sh
```

## 楽音分離の例
- MMDenseLSTM: `egs/tutorials/mm-dense-lstm/separate_music_ja.ipynb`を見るか， [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tky823/DNN-based_source_separation/blob/main/egs/tutorials/mm-dense-lstm/separate_music_ja.ipynb)にとんでください．
- Conv-TasNet: `egs/tutorials/conv-tasnet/separate_music_ja.ipynb`を見るか， [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tky823/DNN-based_source_separation/blob/main/egs/tutorials/conv-tasnet/separate_music_ja.ipynb)にとんでください．
- UMX: `egs/tutorials/umx/separate_music_ja.ipynb`を見るか， [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tky823/DNN-based_source_separation/blob/main/egs/tutorials/umx/separate_music_ja.ipynb)にとんでください．
- X-UMX: `egs/tutorials/x-umx/separate_music_ja.ipynb`を見るか， [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tky823/DNN-based_source_separation/blob/main/egs/tutorials/x-umx/separate_music_ja.ipynb)にとんでください．
- D3Net: `egs/tutorials/d3net/separate_music_ja.ipynb`を見るか， [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tky823/DNN-based_source_separation/blob/main/egs/tutorials/d3net/separate_music_ja.ipynb)にとんでください．

## 学習済みモデル
事前学習済みモデルを次のようにダウンロードすることができます．
```py
from models.conv_tasnet import ConvTasNet

model = ConvTasNet.build_from_pretrained(task="musdb18", sample_rate=44100, target='vocals')
```

| モデル | データセット | ダウンロードの例 |
|:---:|:---:|:---:|
| LSTM-TasNet | WSJ0-2mix | `model = LSTMTasNet.build_from_pretrained(task="wsj0-mix", sample_rate=8000, n_sources=2)` |
| Conv-TasNet | WSJ0-2mix | `model = ConvTasNet.build_from_pretrained(task="wsj0-mix", sample_rate=8000, n_sources=2)` |
| Conv-TasNet | WSJ0-3mix | `model = ConvTasNet.build_from_pretrained(task="wsj0-mix", sample_rate=8000, n_sources=3)` |
| Conv-TasNet | MUSDB18 | `model = ConvTasNet.build_from_pretrained(task="musdb18", sample_rate=44100)` |
| Conv-TasNet | WHAM | `model = ConvTasNet.build_from_pretrained(task="wham/separate-noisy", sample_rate=8000)` |
| Conv-TasNet | WHAM | `model = ConvTasNet.build_from_pretrained(task="wham/enhance-single", sample_rate=8000)` |
| Conv-TasNet | WHAM | `model = ConvTasNet.build_from_pretrained(task="wham/enhance-both", sample_rate=8000)` |
| Conv-TasNet | LibriSpeech | `model = ConvTasNet.build_from_pretrained(task="librispeech", sample_rate=16000, n_sources=2)` |
| DPRNN-TasNet | WSJ0-2mix | `model = DPRNNTasNet.build_from_pretrained(task="wsj0-mix", sample_rate=8000, n_sources=2)` |
| DPRNN-TasNet | WSJ0-3mix | `model = DPRNNTasNet.build_from_pretrained(task="wsj0-mix", sample_rate=8000, n_sources=3)` |
| DPRNN-TasNet | LibriSpeech | `model = DPRNNTasNet.build_from_pretrained(task="librispeech", sample_rate=16000, n_sources=2)` |
| MMDenseLSTM | MUSDB18 | `model = MMDenseLSTM.build_from_pretrained(task="musdb18", sample_rate=44100, target="vocals")` |
| Open-Unmix | MUSDB18 | `model = OpenUnmix.build_from_pretrained(task="musdb18", sample_rate=44100, target="vocals")` |
| Open-Unmix | MUSDB18-HQ | `model = OpenUnmix.build_from_pretrained(task="musdb18hq", sample_rate=44100, target="vocals")` |
| DPTNet | WSJ0-2mix | `model = DPTNet.build_from_pretrained(task="wsj0-mix", sample_rate=8000, n_sources=2)` |
| CrossNet-Open-Unmix | MUSDB18 | `model = CrossNetOpenUnmix.build_from_pretrained(task="musdb18", sample_rate=44100)` |
| D3Net | MUSDB18 | `model = D3Net.build_from_pretrained(task="musdb18", sample_rate=44100, target="vocals")` |

`egs/tutorials/hub/pretrained.ipynb`を見るか， [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tky823/DNN-based_source_separation/blob/main/egs/tutorials/hub/pretrained.ipynb)にとんでください．
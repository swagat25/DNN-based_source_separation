#!/bin/bash

exp_dir="./exp"
continue_from=""
tag=""

n_sources=2

wav_root="../../../dataset/LibriSpeech"
train_json_path="../../../dataset/LibriSpeech/train-clean-100/train-100-${n_sources}mix.json"
valid_json_path="../../../dataset/LibriSpeech/dev-clean/valid-${n_sources}mix.json"

sample_rate=16000

# Encoder & decoder
enc_basis='trainable' # choose from ['trainable','Fourier', 'trainableFourier', 'trainableFourierTrainablePhase']
dec_basis='trainable' # choose from ['trainable','Fourier', 'trainableFourier', 'trainableFourierTrainablePhase', 'pinv']
enc_nonlinear='' # enc_nonlinear is activated if enc_basis='trainable' and dec_basis!='pinv'
window_fn='' # window_fn is activated if enc_basis or dec_basis in ['Fourier', 'trainableFourier', 'trainableFourierTrainablePhase']
enc_onesided=0 # enc_onesided is activated if enc_basis or dec_basis in ['Fourier', 'trainableFourier', 'trainableFourierTrainablePhase']
enc_return_complex=0 # enc_return_complex is activated if enc_basis or dec_basis in ['Fourier', 'trainableFourier', 'trainableFourierTrainablePhase']

N=64
L=16 # L corresponds to the window length (samples) in this script.

# Separator
F=64
H=128
K=100
P=50
B=3
causal=0
sep_norm=1
mask_nonlinear='sigmoid'

# Criterion
criterion='sisdr'

# Optimizer
optimizer='adam'
lr=1e-3
weight_decay=0
max_norm=0

batch_size=4
epochs=100

use_cuda=1
overwrite=0
seed=111

. ./path.sh
. parse_options.sh || exit 1

prefix=""

if [ ${enc_basis} = 'trainable' -a -n "${enc_nonlinear}" -a ${dec_basis} != 'pinv' ]; then
    prefix="${preffix}enc-${enc_nonlinear}_"
fi

if [ ${enc_basis} = 'Fourier' -o ${enc_basis} = 'trainableFourier' -o ${enc_basis} = 'trainableFourierTrainablePhase' -o ${dec_basis} = 'Fourier' -o ${dec_basis} = 'trainableFourier' -o ${dec_basis} = 'trainableFourierTrainablePhase' ]; then
    prefix="${preffix}${window_fn}-window_enc-onesided${enc_onesided}_enc-complex${enc_return_complex}/"
fi

if [ -z "${tag}" ]; then
    save_dir="${exp_dir}/${n_sources}mix/${enc_basis}-${dec_basis}/${criterion}/N${N}_L${L}_F${F}_H${H}_K${K}_P${P}_B${B}/${prefix}causal${causal}_norm${sep_norm}_mask-${mask_nonlinear}/b${batch_size}_e${epochs}_${optimizer}-lr${lr}-decay${weight_decay}_clip${max_norm}/seed${seed}"
else
    save_dir="${exp_dir}/${tag}"
fi

model_dir="${save_dir}/model"
loss_dir="${save_dir}/loss"
sample_dir="${save_dir}/sample"
log_dir="${save_dir}/log"

if [ ! -e "${log_dir}" ]; then
    mkdir -p "${log_dir}"
fi

time_stamp=`date "+%Y%m%d-%H%M%S"`

export CUDA_VISIBLE_DEVICES="0"

train.py \
--wav_root ${wav_root} \
--train_json_path ${train_json_path} \
--valid_json_path ${valid_json_path} \
--sample_rate ${sample_rate} \
--enc_basis ${enc_basis} \
--dec_basis ${dec_basis} \
--enc_nonlinear "${enc_nonlinear}" \
--window_fn "${window_fn}" \
--enc_onesided "${enc_onesided}" \
--enc_return_complex "${enc_return_complex}" \
-N ${N} \
-L ${L} \
-F ${F} \
-H ${H} \
-K ${K} \
-P ${P} \
-B ${B} \
--causal ${causal} \
--sep_norm ${sep_norm} \
--mask_nonlinear ${mask_nonlinear} \
--n_sources ${n_sources} \
--criterion ${criterion} \
--optimizer ${optimizer} \
--lr ${lr} \
--weight_decay ${weight_decay} \
--max_norm ${max_norm} \
--batch_size ${batch_size} \
--epochs ${epochs} \
--model_dir "${model_dir}" \
--loss_dir "${loss_dir}" \
--sample_dir "${sample_dir}" \
--continue_from "${continue_from}" \
--use_cuda ${use_cuda} \
--overwrite ${overwrite} \
--seed ${seed} | tee "${log_dir}/train_${time_stamp}.log"

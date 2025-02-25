#!/bin/bash

exp_dir="./exp"
continue_from=""
tag=""

n_sources=2
sr_k=8 # sr_k=8 means sampling rate is 8kHz. Choose from 8kHz or 16kHz.
sample_rate=${sr_k}000
duration=4
valid_duration=10
max_or_min='min'

train_wav_root="../../../dataset/wsj0-mix/${n_sources}speakers/wav${sr_k}k/${max_or_min}/tr"
valid_wav_root="../../../dataset/wsj0-mix/${n_sources}speakers/wav${sr_k}k/${max_or_min}/cv"

train_list_path="../../../dataset/wsj0-mix/${n_sources}speakers/mix_${n_sources}_spk_${max_or_min}_tr_mix"
valid_list_path="../../../dataset/wsj0-mix/${n_sources}speakers/mix_${n_sources}_spk_${max_or_min}_cv_mix"

# Encoder & decoder
enc_basis='trainableGated' # choose from ['trainable', 'trainableGated']
dec_basis='trainable' # choose from ['trainable']
enc_nonlinear='' # enc_nonlinear is activated if enc_basis='trainable'

N=500
L=40

# Separator
H=500
X=2
R=2 # R x X is actual number of layers in LSTM.
causal=0
mask_nonlinear='sigmoid'

# Criterion
criterion='sisdr'

# Optimizer
optimizer='adam'
lr=1e-3
weight_decay=0
max_norm=5

batch_size_train=128
batch_size_finetune=128
epochs_train=50
epochs_finetune=50

use_cuda=1
overwrite=0
seed_train=111
seed_finetune=111
gpu_id="0"

. ./path.sh
. parse_options.sh || exit 1

prefix=""

if [ ${enc_basis} = 'trainable' -a -n "${enc_nonlinear}" -a ${dec_basis} != 'pinv' ]; then
    prefix="${preffix}enc-${enc_nonlinear}_"
fi

if [ -z "${tag}" ]; then
    save_dir="${exp_dir}/${n_sources}mix/sr${sr_k}k_${max_or_min}/${duration}sec/${enc_basis}-${dec_basis}/${criterion}/N${N}_L${L}_H${H}_X${X}_R${R}/${prefix}causal${causal}_mask-${mask_nonlinear}/b${batch_size_train}_e${epochs_train}_${optimizer}-lr${lr}-decay${weight_decay}_clip${max_norm}/seed${seed_train}"
else
    save_dir="${exp_dir}/${tag}"
fi
save_dir="${save_dir}/finetune/b${batch_size_finetune}_e${epochs_finetune}/seed${seed_finetune}"

model_dir="${save_dir}/model"
loss_dir="${save_dir}/loss"
sample_dir="${save_dir}/sample"
log_dir="${save_dir}/log"

if [ ! -e "${log_dir}" ]; then
    mkdir -p "${log_dir}"
fi

time_stamp=`date "+%Y%m%d-%H%M%S"`

export CUDA_VISIBLE_DEVICES="${gpu_id}"

finetune.py \
--train_wav_root ${train_wav_root} \
--valid_wav_root ${valid_wav_root} \
--train_list_path ${train_list_path} \
--valid_list_path ${valid_list_path} \
--sample_rate ${sample_rate} \
--duration ${duration} \
--valid_duration ${valid_duration} \
--enc_basis ${enc_basis} \
--dec_basis ${dec_basis} \
--enc_nonlinear "${enc_nonlinear}" \
-N ${N} \
-L ${L} \
-H ${H} \
-X ${X} \
-R ${R} \
--causal ${causal} \
--mask_nonlinear ${mask_nonlinear} \
--n_sources ${n_sources} \
--criterion ${criterion} \
--optimizer ${optimizer} \
--lr ${lr} \
--weight_decay ${weight_decay} \
--max_norm ${max_norm} \
--batch_size ${batch_size_finetune} \
--epochs ${epochs_finetune} \
--model_dir "${model_dir}" \
--loss_dir "${loss_dir}" \
--sample_dir "${sample_dir}" \
--continue_from "${continue_from}" \
--use_cuda ${use_cuda} \
--overwrite ${overwrite} \
--seed ${seed_finetune} | tee "${log_dir}/finetune_${time_stamp}.log"

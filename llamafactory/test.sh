set -x 
source /root/.profile

# git拉取数据
git clone ssh://git@code.baichuan-inc.com:2224/mllm_align/llamafactory.git
cd llamafactory
# 激活python训练环境
source /root/miniconda3/bin/activate mmtrain 
python3 -m pip install six
python3 -m pip install ks3sdk
python3 -m pip install cairosvg
which is python
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

# pip install -e .

# 2. 配置训练集
data_json_dir=/global_data/mllm/liulijun/data/medical/json
data_set_path=/global_data/mllm/liulijun/data/medical/dataset_info.json
yaml_path=examples/train_full/qwen2_5vl_full_sft.yaml 

cp ${data_json_dir}/* ./data/
cp ${data_set_path} ./data/

yaml_config='''
### model
model_name_or_path: /mnt/bc_fs/code/mllm/mmsft_data/source/pretrain/Qwen2.5-VL-7B-Instruct
image_max_pixels: 262144
video_max_pixels: 16384
trust_remote_code: true
# attn_implementation: flash_attention_2

### method
stage: sft
do_train: true
finetuning_type: full
freeze_vision_tower: true  # choices: [true, false]
freeze_multi_modal_projector: true  # choices: [true, false]
train_mm_proj_only: false  # choices: [true, false]
deepspeed: examples/deepspeed/ds_z3_offload_config.json  # choices: [ds_z0_config.json, ds_z2_config.json, ds_z3_config.json]

### dataset
dataset: medical_ocr_1
template: qwen2_vl
cutoff_len: 16000
max_samples: 100000
overwrite_cache: true
preprocessing_num_workers: 80
packing: true


### output
output_dir: saves/qwen2_5_vl-7b/full/sft
logging_steps: 10
save_steps: 500
save_strategy: epoch
plot_loss: true
overwrite_output_dir: true

### train
flash_attn: fa2
per_device_train_batch_size: 1
gradient_accumulation_steps: 1
gradient_checkpointing: true
learning_rate: 1.0e-7
num_train_epochs: 3.0
lr_scheduler_type: cosine
warmup_ratio: 0.1
bf16: true
ddp_timeout: 180000000

### eval
# val_size: 0.1
# per_device_eval_batch_size: 1
# eval_strategy: steps
# eval_steps: 500
'''
echo "$yaml_config" > ${yaml_path}
/bin/bash train.sh ${yaml_path}
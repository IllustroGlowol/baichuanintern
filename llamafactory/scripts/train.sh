# #!/bin/bash
export NCCL_DEBUG=WARN
export NCCL_SOCKET_IFNAME=eth0
export NCCL_IB_DISABLE=0
export NCCL_IB_HCA=mlx5_bond_0,mlx5_bond_1,mlx5_bond_2,mlx5_bond_3
export NCCL_IB_HCA=mlx5_bond_1,mlx5_bond_2,mlx5_bond_3,mlx5_bond_4,mlx5_bond _5,mlx5_bond_6,mlx5_bond_7,mlx5_bond_8
export NCCL_IB_GID_INDEX=3

pretrain="examples/train_full/qwen2_5vl_full_sft.yaml"
# 解析长格式命令行参数
extra_arguments=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --yaml_path) yaml_path="$2"; shift 2;;
        *) extra_arguments="$extra_arguments $1"; shift 1;;
    esac
done

# 启动Python环境
cd "$(dirname "$0")" && cd ..
echo "workspace_dir=$PWD"

echo "python=$(which python)"

# FORCE_TORCHRUN=1 llamafactory-cli train ${pretrain}
#     # --nproc_per_node=2 \
#     # --nnodes=$WORLD_SIZE \
#     # --node_rank=$RANK \
#     # --master_addr=$MASTER_ADDR \
#     # --master_port=$MASTER_PORT \
#     # NNODES=$WORLD_SIZE \
#     # NODE_RANK=$RANK \
#     # MASTER_ADDR=$MASTER_ADDR \
#     # MASTER_PORT=$MASTER_PORT \
#     # llamafactory-cli train ${pretrain}

torchrun --nproc_per_node=8 --nnodes=$WORLD_SIZE --node_rank=$RANK --master_addr=$MASTER_ADDR --master_port=$MASTER_PORT src/train.py ${pretrain}
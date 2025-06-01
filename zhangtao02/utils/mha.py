import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_head):
        super(MultiHeadAttention, self).__init__()
        self.d_model = d_model
        self.n_head = n_head
        self.d_head = self.d_model // self.n_head
        self.w_q = nn.Linear(self.d_model, self.d_model)
        self.w_k = nn.Linear(self.d_model, self.d_model)
        self.w_v = nn.Linear(self.d_model, self.d_model)
        self.w_o = nn.Linear(self.d_model, self.d_model)
        self.softmax = nn.Softmax(dim=-1)
    
    def forward(self, x, mask=None):
        q, k, v = self.w_q(x), self.w_k(x), self.w_v(x)     # step1
        q, k, v = self.split(q), self.split(k), self.split(v)   # step2
        if mask is not None:
            mask = mask.unsqueeze(1)
        sa_output, attn_weights = self.attention(q, k, v, mask=mask)    # step3
        concat_tensor = self.concat(sa_output)      # step4
        mha_output = self.w_o(concat_tensor)        # step5
        return mha_output

    def split(self, tensor):
        bsz, seq_len, d_model = tensor.size()
        split_tensor = tensor.view(bsz, seq_len, self.n_head, self.d_head).transpose(1, 2)
        return split_tensor

    def attention(self, q, k, v, mask=None):
        k_t = k.transpose(-1, -2)       # step1
        d_k = q.size(-1)        # step2
        scores = torch.matmul(q, k_t) / math.sqrt(d_k)      # step3
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)        # step4
        attn_weight = self.softmax(scores)          # step5
        sa_output = torch.matmul(attn_weight, v)
        return sa_output, attn_weight
    
    def concat(self, sa_output):
        bsz, n_head, seq_len, d_head = sa_output.size()
        concat_tensor = sa_output.transpose(1, 2).contiguous().view(bsz, seq_len, self.d_model)
        return concat_tensor


MHA = MultiHeadAttention(8, 2)
inputs = torch.ones([2, 3, 8])
res = MHA(inputs)
print(res)
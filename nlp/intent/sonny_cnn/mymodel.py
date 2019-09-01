import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


class CNN_Text(nn.Module):
    
    def __init__(self, embed_num, class_num, ):
        super(CNN_Text, self).__init__()
        
        V = embed_num
        D = 100 #args.embed_dim
        C = class_num
        Ci = 1
        Co = 20 #args.kernel_num
        Ks = [1,2,3]

        self.embed = nn.Embedding(V, D)

        self.convs1 = nn.ModuleList([nn.Conv2d(Ci, Co, (K, D), padding=(2,0)) for K in Ks])

        self.dropout = nn.Dropout(0.2)
        self.fc1 = nn.Linear(len(Ks)*Co, C)

    def forward(self, x):
        x = self.embed(x)  # (N, W, D)
        
        x = x.unsqueeze(1)  # (N, Ci, W, D)

        x = [F.relu(conv(x)).squeeze(3) for conv in self.convs1]  # [(N, Co, W), ...]*len(Ks)

        x = [F.max_pool1d(i, i.size(2)).squeeze(2) for i in x]  # [(N, Co), ...]*len(Ks)
        
        x = torch.cat(x, 1)

        x = self.dropout(x)  # (N, len(Ks)*Co)
        logit = self.fc1(x)  # (N, C)
        return logit

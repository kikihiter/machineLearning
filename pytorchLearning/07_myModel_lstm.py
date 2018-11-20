#!user/bin/env python
# kiki 2018/11/01
# python 07_myModel_lstm.py

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
import random
import torch.nn.init as init
# import hyperparams
# torch.manual_seed(hyperparams.seed_num)
# random.seed(hyperparams.seed_num)

class  LSTM(nn.Module):
    
    def __init__(self, args):
        super(LSTM, self).__init__()
        self.args = args
        # print(args)

        self.hidden_dim = args.lstm_hidden_dim
        self.num_layers = args.lstm_num_layers
        V = args.embed_num
        D = args.embed_dim
        C = args.class_num
        if args.max_norm is not None:
            print("max_norm = {} ".format(args.max_norm))
            self.embed = nn.Embedding(V, D, max_norm=args.max_norm, scale_grad_by_freq=True)
        else:
            print("max_norm = {} |||||".format(args.max_norm))
            self.embed = nn.Embedding(V, D, scale_grad_by_freq=True)
        # word embedding
        if args.word_Embedding:
            pretrained_weight = np.array(args.pretrained_weight)
            self.embed.weight.data.copy_(torch.from_numpy(pretrained_weight))
        # lstm
        self.lstm = nn.LSTM(D, self.hidden_dim, dropout=args.dropout, num_layers=self.num_layers)

        if args.init_weight:
            print("Initing W .......")
            # n = self.lstm.input_size * self.lstm
            init.xavier_normal(self.lstm.all_weights[0][0], gain=np.sqrt(args.init_weight_value))
            init.xavier_normal(self.lstm.all_weights[0][1], gain=np.sqrt(args.init_weight_value))

        # linear
        self.hidden2label = nn.Linear(self.hidden_dim, C)
        # hidden
        self.hidden = self.init_hidden(self.num_layers, args.batch_size)
        # dropout
        self.dropout = nn.Dropout(args.dropout)
        self.dropout_embed = nn.Dropout(args.dropout_embed)

    def init_hidden(self, num_layers, batch_size):
        # the first is the hidden h
        # the second is the cell  c
        # return (Variable(torch.zeros(1, batch_size, self.hidden_dim)),
        #          Variable(torch.zeros(1, batch_size, self.hidden_dim)))
        if self.args.cuda is True:
            return (Variable(torch.zeros(1 * num_layers, batch_size, self.hidden_dim)).cuda(),
                    Variable(torch.zeros(1 * num_layers, batch_size, self.hidden_dim)).cuda())
        else:
            return (Variable(torch.zeros(1 * num_layers, batch_size, self.hidden_dim)),
                    Variable(torch.zeros(1 * num_layers, batch_size, self.hidden_dim)))

    def forward(self, x):
        embed = self.embed(x)
        embed = self.dropout_embed(embed)
        x = embed.view(len(x), embed.size(1), -1)
        # lstm
        lstm_out, self.hidden = self.lstm(x, self.hidden)
        lstm_out = torch.transpose(lstm_out, 0, 1)
        lstm_out = torch.transpose(lstm_out, 1, 2)
        # pooling
        lstm_out = F.tanh(lstm_out)
        lstm_out = F.max_pool1d(lstm_out, lstm_out.size(2)).squeeze(2)
        lstm_out = F.tanh(lstm_out)
        # linear
        logit = self.hidden2label(lstm_out)
        return logit
import torch.nn as nn


class MyLSTM(nn.Module):
    def __init__(self, n_inputs, n_hidden, n_layers,dropout=0.2):
        super().__init__()
        self.n_hidden = n_hidden

        self.lstm = nn.LSTM(
            input_size=n_inputs,
            hidden_size=n_hidden,
            num_layers=n_layers,
            dropout=dropout,
            batch_first=True
        )

        self.fc1 = nn.Linear(self.n_hidden, 1)

    def forward(self, x):
        _, (h_t, _) = self.lstm(x)

        x = self.fc1(h_t[-1])
        return x

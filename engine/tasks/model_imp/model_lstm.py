import numpy as np
import pandas as pd
import torch
from tasks.model_imp.my_lstm import MyLSTM
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import r2_score
import time


class LSTM:

    def __init__(self, n_hidden=256, n_layers=3, normalize=True, epochs=200, lr=0.0001, batch_size=64):
        start=time.time()
        if n_layers>3:
            n_layers=3
        elif n_layers<=0:
            n_layers=1
        if n_hidden>256:
            n_hidden=256
        elif n_hidden<=0:
            n_hidden=32
        self.t_e=[]
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.n_hidden=n_hidden
        self.n_layers=n_layers
        self.lr=lr
        self.model = None
        self.criterion = nn.MSELoss()
        self.normalize = normalize
        self.input_scaler = StandardScaler()
        self.label_scaler = MinMaxScaler()
        self.epochs = epochs
        self.optimizer = None
        self.batch_size = batch_size
        self._estimator_type = "Regressor"
        end=time.time()
        self.t_e.append({'init time':(end-start)})

    def predict(self, x):
        start=time.time()
        if (self.normalize):
            x = self.input_scaler.transform(x)
        testloader = self.create_loader(x, x)
        self.model.eval()
        prediction = []
        with torch.no_grad():
            for inputs, _ in testloader:
                inputs = inputs.to(self.device)
                logps = self.model.forward(inputs).cpu().data.numpy()
                prediction += (logps.tolist())

        if (self.normalize):
            prediction = self.label_scaler.inverse_transform(prediction)
        else:
            prediction = np.asarray(prediction)
        self.model.train()
        end = time.time()
        self.t_e.append({'prediction time': (end - start)})
        print(self.t_e)
        return prediction

    def score(self, x, y):
        start = time.time()

        if (self.normalize):
            x = self.input_scaler.transform(x)
            y = self.label_scaler.transform(x)
        testloader = self.create_loader(x, y)
        self.model.eval()
        prediction = []
        labelss = []
        with torch.no_grad():
            for inputs, labels in testloader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                logps = self.model.forward(inputs).cpu().data.numpy()
                prediction += (logps.tolist())
                labelss += labels.tolist()

        self.model.train()
        r2=r2_score(y_true=labelss, y_pred=prediction)
        end = time.time()
        self.t_e.append({'score time': (end - start)})
        print(self.t_e)
        return r2

    def fit(self, x, y):
        start=time.time()
        self.model=MyLSTM(n_inputs=len(x.columns),n_hidden=self.n_hidden,n_layers=self.n_layers)
        self.optimizer = optim.Adam(self.model.parameters(), self.lr)

        if (self.normalize):
            x = self.input_scaler.fit_transform(x)
            y = self.label_scaler.fit_transform(y.values.reshape(-1, 1))
        X_train, X_val, y_train, y_val = train_test_split(x, y, test_size=0.2, shuffle=False)
        trainloader = self.create_loader(X_train, y_train)
        validationloader = self.create_loader(X_val, y_val)
        min_validation_loss = np.Infinity
        training_losses, validation_losses = [], []
        steps, running_loss, test_loss = 0, 0, 0
        self.model.to(self.device)
        validate_every = 50

        for e in range(self.epochs):

            # training
            for inputs, labels in trainloader:
                steps += 1
                inputs, labels = inputs.to(self.device), labels.to(self.device)

                self.optimizer.zero_grad()
                logps = self.model.forward(inputs)
                loss = self.criterion(logps, labels)
                loss.backward()
                self.optimizer.step()
                running_loss += loss.item()

                # validating
                if steps % validate_every == 0:
                    validation_loss = 0
                    self.model.eval()
                    with torch.no_grad():
                        for inputs, labels in validationloader:
                            inputs, labels = inputs.to(self.device), labels.to(self.device)
                            logps = self.model.forward(inputs)
                            v_loss = self.criterion(logps, labels)
                            validation_loss += v_loss.item()

                    self.model.train()

                    avg_validation_loss = validation_loss / len(validationloader)

                    print(f"Epoch {e + 1}/{self.epochs},  "
                          f"Training loss: {running_loss / validate_every:.5f},  "
                          f"Validation loss: {avg_validation_loss:.5f},  ")

                    training_losses.append(running_loss / validate_every)
                    validation_losses.append(avg_validation_loss)

                    # Saving better model
                    if avg_validation_loss < min_validation_loss:
                        print(f"Saving better model")
                        min_validation_loss = avg_validation_loss
                        torch.save(self.model.state_dict(), 'lstm_model_dict.pt')

                    running_loss = 0
        # loading best model
        self.model.load_state_dict(torch.load('lstm_model_dict.pt'))
        end = time.time()
        self.t_e.append({f'fit time with {self.epochs} epochs': (end - start)})
        print(self.t_e)

    def create_loader(self, x, y, shuffle=False):
        x_t = self.tensorfy(x)
        y_t = self.tensorfy(y, is_label=True)
        sets = self.createSet(x_t, y_t)
        loader = torch.utils.data.DataLoader(sets, batch_size=self.batch_size, shuffle=shuffle)
        return loader

    def tensorfy(self, x, is_label=False):
        tx = self.isDataFrame(x)
        tx = Variable(torch.Tensor(tx.to_numpy()))
        if (not is_label and len(tx.shape)<=2):
            tx = torch.reshape(tx, (tx.shape[0], 1, tx.shape[1]))
        return tx   

    def isDataFrame(self, var):
        if (isinstance(var, pd.DataFrame)):
            return var
        return pd.DataFrame(var)

    def createSet(self, x, y):
        # CA
        x = x.type(torch.FloatTensor)
        y = y.type(torch.FloatTensor)
        train_data = [[i, j] for i, j in zip(x, y)]
        return train_data

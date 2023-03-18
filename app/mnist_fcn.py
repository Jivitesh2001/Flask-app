# MNIST
# DataLoader, Transformation
# Multilayer Neural Net, activation function
# Loss and Optimizer
# Training Loop (batch training)
# Model evaluation
# GPU Support

import torch 
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

#device config
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Hyper parameters
input_size = 784 # 28x28
hidden_size = 100
num_classes = 10
num_epochs = 10
batch_size = 100
learning_rate = 0.001

transform = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.1307,),(0.3081))])# global mean and global std dev of MNIST dataset



# examples = iter(train_loader)
# # samples,labels = examples.next()
# print(samples.shape,labels.shape)

# for i in range(6):
#     plt.subplot(2,3,i+1)
#     plt.imshow(samples[i][0],cmap='gray')
#plt.show()

class NeuralNet(nn.Module):
    def __init__(self,input_size,hidden_size,num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size,hidden_size)
        self.relu = nn.ReLU()
        self.l2 = nn.Linear(hidden_size,num_classes)
        self.dropout = nn.Dropout(p=0.12)
    
    def forward(self,X):
        out = self.l1(X)
        out = self.relu(out)
        out = self.l2(out)
        return self.dropout(out)

model = NeuralNet(input_size,hidden_size,num_classes).to(device)

# Loss and Optimizer

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(),lr = learning_rate)


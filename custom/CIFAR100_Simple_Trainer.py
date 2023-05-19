import torch
import os
import torchvision
import torchvision.transforms as  transforms

import torch.nn as nn 
import torch.nn.functional as F
import torch.optim as optim

import matplotlib.pyplot as plt
import numpy as np 

from models.networks import SimpleCNN
from datasets.cifar100_load import cifar100_mean_std


transform = transforms.Compose(
    [transforms.ToTensor(),
    transforms.Normalize(mean=(cifar100_mean_std()[1],cifar100_mean_std()[2],cifar100_mean_std()[3]), std=(cifar100_mean_std()[4],cifar100_mean_std()[5],cifar100_mean_std()[6]))])

batch_size = 4

trainset = torchvision.datasets.CIFAR100(root='./data', train=True, 
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                            shuffle=True, num_workers=2)



device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device}")


model = SimpleCNN(3,100)
model.to(device)


criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)


for epoch in range(10):  # loop over the dataset multiple times

    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data[0].to(device), data[1].to(device)

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 2000 == 1999:    # print every 2000 mini-batches
            print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
            running_loss = 0.0

print('Finished Training')


if not os.path.exists('./saved_models'):
    os.makedirs('./saved_models')
path = './saved_models/cifar100_simple.pth'
torch.save(model.state_dict(), path)

print('Model Saved')








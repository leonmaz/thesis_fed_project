import torch
import torchvision
import torchvision.transforms as  transforms

import torch.nn as nn 
import torch.nn.functional as F
import torch.optim as optim

import matplotlib.pyplot as plt
import numpy as np 
import os 

from models.networks import ResNet, BasicBlock
from datasets.cifar10_load import cifar10_mean_std

path = './saved_models/cifar100_resnet.pth'
if not os.path.exists(path):
    print("Model is not created, run file 'CIFAR10_ResNet_Trainer.py' first")
    exit()

model = ResNet(3, 18, BasicBlock, 100)
model.load_state_dict(torch.load(path))


transform = transforms.Compose(
    [transforms.ToTensor(),
    transforms.Normalize(mean=(cifar10_mean_std()[1],cifar10_mean_std()[2],cifar10_mean_std()[3]), std=(cifar10_mean_std()[4],cifar10_mean_std()[5],cifar10_mean_std()[6]))])

batch_size = 4

testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                        download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                            shuffle=False, num_workers=2)


correct = 0
total = 0

for data in testloader:
    inputs, labels = data
    # calculate outputs by running images through the network
    outputs = model(inputs)
    # the class with the highest energy is what we choose as prediction
    _, predicted = torch.max(outputs.data, 1)
    total += labels.size(0)
    correct += (predicted == labels).sum().item()

print(f'Accuracy of the network on the 10000 test images: {100 * correct // total} %')

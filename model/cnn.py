import torch


class Model(torch.nn.Module):
    def __init__(self, class_num):
        super(Model, self).__init__()
        self.conv1 = torch.nn.Conv2d(in_channels=3, out_channels=128, kernel_size=(5,5))
        self.conv2 = torch.nn.Conv2d(in_channels=128, out_channels=64, kernel_size=(3,3))
        self.conv3 = torch.nn.Conv2d(in_channels=64, out_channels=32, kernel_size=(3,3))
        self.max_pool1 = torch.nn.MaxPool2d(kernel_size=(2,2),stride=(2,2))
        self.max_pool2 = torch.nn.MaxPool2d(kernel_size=(2,2),stride=(2,2))
        self.max_pool3 = torch.nn.MaxPool2d(kernel_size=(2,2),stride=(2,2))
        self.relu1 = torch.nn.ReLU()
        self.relu2 = torch.nn.ReLU()
        self.relu3 = torch.nn.ReLU()
        self.relu4 = torch.nn.ReLU()
        self.linear1 = torch.nn.Linear(in_features=128, out_features=64)
        self.linear2 = torch.nn.Linear(in_features=64, out_features=class_num)
        self.logSoftmax = torch.nn.LogSoftmax(dim=1)

    def forward(self, x):
        x =  self.conv1(x)
        x = self.relu1(x)
        x = self.max_pool1(x)
        
        x =  self.conv2(x)
        x = self.relu2(x)
        x = self.max_pool2(x)
        
        x =  self.conv3(x)
        x = self.relu3(x)
        x = self.max_pool1(x)

        x = torch.nn.Flatten(x, 1)
        x = self.linear1(x)
        x = self.relu4()
        x = self.linear2(x)
        output = self.logSoftmax(x)

        return output
    
import torch
import torch.nn as nn

class SELayer(nn.Module):
    def __init__(self, channel, reduction=5):
        super(SELayer, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channel, channel // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(channel // reduction, channel, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y.expand_as(x)

class Residual_Block(nn.Module):
    def __init__(self, i_channel, o_channel, stride=1, downsample=None):
        super(Residual_Block, self).__init__()

        self.conv1 = nn.Conv2d(in_channels=i_channel, out_channels=o_channel, kernel_size=3, stride=stride, padding=1,
                               bias=False)

        self.bn1 = nn.BatchNorm2d(o_channel)

        self.relu = nn.ReLU(inplace=True)

        self.conv2 = nn.Conv2d(in_channels=o_channel, out_channels=o_channel, kernel_size=3, stride=1, padding=1,
                               bias=False)

        self.bn2 = nn.BatchNorm2d(o_channel)

        self.downsample = downsample

    def forward(self, x):
        residual = x

        out = self.conv1(x)

        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)

        out = self.bn2(out)

        if self.downsample:
            residual = self.downsample(x)

        out += residual
        out = self.relu(out)
        return out


##############################################################
# ResNet
class ResNet(nn.Module):
    def __init__(self, block, layers, num_classes=1):
        super(ResNet, self).__init__()
        self.in_channels = 16
        self.conv = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, stride=1, padding=1, bias=False)
        self.SElayer = SELayer(16)
        self.bn = nn.BatchNorm2d(16)
        self.relu = nn.ReLU(inplace=True)
        self.layer1 = self.make_layer(block, 16, layers[0])
        self.layer2 = self.make_layer(block, 32, layers[0], 2)
        self.layer3 = self.make_layer(block, 64, layers[1], 2)
        self.layer4 = self.make_layer(block, 96, layers[2], 2)   #add0
        self.layer5 = self.make_layer(block, 128, layers[3], 2)  #add1
        #self.layer6 = self.make_layer(block, 512, layers[3], 2)  # add2
        self.avg_pool = nn.AvgPool2d((2,2))
        #self.fc = nn.Linear(64, num_classes)
        self.fc = nn.Sequential(
            nn.Linear(128, 1),
            nn.Sigmoid()
        )

    def make_layer(self, block, out_channels, blocks, stride=1):  # blocks=layers,the number of residual block
        downsample = None

        if (stride != 1) or (self.in_channels != out_channels):
            downsample = nn.Sequential(
                #nn.Conv2d(self.in_channels, out_channels, kernel_size=1, stride=1, padding=0, bias=False),
                nn.Conv2d(self.in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False),
                nn.BatchNorm2d(out_channels)
            )
        layers = []
        layers.append(block(self.in_channels, out_channels, stride, downsample))
        self.in_channels = out_channels

        for i in range(1, blocks):
            layers.append(block(out_channels, out_channels))
        return nn.Sequential(*layers)  # add all of the residual block

    def forward(self, x):
        out = self.conv(x)
        out = self.SElayer(out)
        #print(out.shape)
        out = self.bn(out)
        #print(out.shape)
        #out = SELayer(out)
        out = self.relu(out)
        #print(out.shape)
        out = self.layer1(out)
        #print(out.shape)
        out = self.layer2(out)
        #print(out.shape)
        out = self.layer3(out)
        #print(out.shape)
        out = self.layer4(out)     #add0
        #print(out.shape)
        out = self.layer5(out)     #add1
        #out = self.layer6(out)     #add2
        #print(out.shape)
        out = self.avg_pool(out)
        #print(out.shape)
        out = out.view(out.size(0), -1)
        out = self.fc(out)


        return out


#model = ResNet(Residual_Block, [3, 3, 3, 3])
#x = torch.rand(2,1,39,31)
#f = model(x)
#print(f)
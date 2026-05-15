import torch.nn as nn
import torch.nn.functional as F

class ResBlock(nn.Module):
    def __init__(self, channels):
        super(ResBlock, self).__init__()
        # Keep kernel=3, padding=1 to maintain 19x19 size
        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(channels)

    def forward(self, x):
        identity = x  # Save the input for the skip connection

        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))

        out += identity  # Add the original input back (the skip)
        return F.relu(out)


class GoPolicyResNet(nn.Module):
    def __init__(self, num_blocks=20):
        super(GoPolicyResNet, self).__init__()

        # Initial Layer: Converts 4 input planes to 128 feature maps
        self.start = nn.Sequential(
            nn.Conv2d(4, 128, kernel_size=3, padding=1),  # 4 planes: B, W, Lib, Ko
            nn.BatchNorm2d(128),
            nn.ReLU()
        )

        # Stack of Residual Blocks
        self.res_blocks = nn.Sequential(*[ResBlock(128) for _ in range(num_blocks)])

        # Output Layer: Global Average Pooling + Linear
        self.policy_head = nn.Sequential(
            nn.Conv2d(128, 2, kernel_size=1),  # Reduce depth to 2 channels
            nn.BatchNorm2d(2),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(2 * 19 * 19, 361)  # Map to 361 coordinates
        )

    def forward(self, x):
        x = self.start(x)
        for block in self.res_blocks:
            x = block(x)
        return self.policy_head(x)
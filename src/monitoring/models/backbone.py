# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Backbone modules.
"""
import torch.nn.functional as F
from torch import nn

import models.vgg_ as models

class BackboneBase_VGG(nn.Module):
    def __init__(self, backbone: nn.Module, num_channels: int, return_interm_layers: bool):
        super().__init__()
        features = list(backbone.features.children())
        if return_interm_layers:
            self.body1 = nn.Sequential(*features[:13])
            self.body2 = nn.Sequential(*features[13:23])
            self.body3 = nn.Sequential(*features[23:33])
            self.body4 = nn.Sequential(*features[33:43])
        else:
            self.body = nn.Sequential(*features[:44])  # 16x down-sample
        self.num_channels = num_channels
        self.return_interm_layers = return_interm_layers

    def forward(self, tensor_list):
        out = []

        if self.return_interm_layers:
            xs = tensor_list
            for _, layer in enumerate([self.body1, self.body2, self.body3, self.body4]):
                xs = layer(xs)
                out.append(xs)

        else:
            xs = self.body(tensor_list)
            out.append(xs)
        return out


class Backbone_VGG(BackboneBase_VGG):
    """ResNet backbone with frozen BatchNorm."""
    def __init__(self, return_interm_layers: bool):
        backbone = models.vgg16_bn(pretrained=True)
        num_channels = 256
        super().__init__(backbone, num_channels, return_interm_layers)


def build_backbone():
    return Backbone_VGG(True)

if __name__ == '__main__':
    Backbone_VGG(True)
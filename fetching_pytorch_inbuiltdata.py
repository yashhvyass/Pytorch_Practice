# -*- coding: utf-8 -*-
"""Fetching_Pytorch_inbuiltdata.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17leAxM1kwN-nm6L6UNIsiSL9Vw_kAlfh
"""

import torch
import torchvision

## split = select subset of data or all the data, given that images are in PIL format and we can obtain a transformed version using custom transform function.
## tyes of targets => attributes - 40 facial aatributes of a person in an image, identity - person id for an image, landmarks - disctionary of extracte facial points
image_path = './'
celeba_dataset = torchvision.datasets.CelebA(
    image_path, split='train', target_type='atrr', download=True
)

"""You may encounter an error due to bad zip file or simply the file may not be downaloadable."""

mnist_data = torchvision.datasets.MNIST(image_path, 'train', download=True)
assert isinstance(mnist_data, torch.utils.data.Dataset)
example = next(iter(mnist_data))
print(example)

"""Example id of the form PIL.image and target

Visualize 10 examples
"""

import matplotlib.pyplot as plt
from itertools import islice

fig = plt.figure(figsize=(12, 5))

for i, (image, label) in islice(enumerate(mnist_data), 10):
  ax = fig.add_subplot(2, 5, i+1)
  ax.set_xticks([])
  ax.set_yticks([])
  ax.imshow(image, cmap='gray_r')
  ax.set_title(f'{label}', size=15)

plt.show()

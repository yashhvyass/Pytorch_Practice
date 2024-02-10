# -*- coding: utf-8 -*-
"""Dataset_and_DataLoader.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PtW5CW-xhLqUapqbNuDfjGBgmP97y-4V
"""

import torch

"""# Creating a Pytorch DataLoader from existing tensor



*   If the data already exist in the form of tensor object, a python list or numpy array we can easily create a dataloader using torch.utils.data.DataLoader() class.
*   Returns object of DataLoader class which we can use to iterate through the individual elements in the input dataset.
"""

from torch.utils.data import DataLoader
t = torch.arange(6, dtype=torch.float32) ### creates a 1D tensor with specified stepsize.
data_loader = DataLoader(t)

for i in data_loader:
  print(i)

"""## How to create batches from this dataset?



*   include an argument batch_size.
"""

t = torch.arange(0, 10, 2, dtype=torch.float32)
data_loader = DataLoader(t)

data_loader = DataLoader(t, batch_size=3, drop_last=False)  ### drop_last = used to drop last non-full batch.

for i, batch in enumerate(data_loader):
  print(f'Batch {i}: {batch}')

"""# Combining two Tensors into a Joint Dataset

*   Often we will have data in two ot more possible tensors. for eg -> we could have tensors of features and labels. In such cases, we need to build a dataset that combines these tensors, which will allow us to retrieve the elements of these tensors in tuples.
"""

from torch.utils.data import Dataset

torch.manual_seed(42)
x = torch.rand([4, 3], dtype=torch.float32)  ## create a tensor with size [4,3]
y = torch.arange(4)

print(x)
print(y)

class JointDataset(Dataset):
  def __init__(self, x, y):  ## init = here inital logic happens, such as reading existing arrays, loading a file, filtering data etc.
    self.x=x
    self.y=y

  def __len__(self):
    return len(self.x)

  def __getitem__(self, idx): ## getitem = returns corresponding sample to the given index.
    return self.x[idx], self.y[idx]

joint_dataset = JointDataset(x, y)

for i in joint_dataset: ## joint dataset is a tuple
  print(f'x: {i[0]}, y:, {i[1]}')

"""*   We can also simple utilize TensorDataset class, (if the second dataset is a labelled dataset in the form of tensors)

JointDataset(x, y) <-- use directly this then.

# Shuffle, batch and Repeat

*   It is important to shuffle the data.
"""

torch.manual_seed(42)
data_loader = DataLoader(dataset=joint_dataset, batch_size=2, shuffle=True)

for i, batch in enumerate(data_loader):
  print(f'batch {i}:', 'x:', batch[0],'\n y:', batch[1])

"""*   The rows are shuffled without losing the one-one correspondence between the entries in x and y.

* We also need to iterate over the dataset for multiple epochs while shuffling the data. Here the elements in the batch will also be shuffled. Let' see how we can do that.   
"""

for epoch in range(2):
  print(f'Epoch {epoch+1}')
  for i, batch in enumerate(data_loader, 1):
    print(f'batch {i}:', 'x:', batch[0], '\n y:', batch[1])

"""# Creating a dataset from files on our local storage disk

Generate a list of image files.
"""

import pathlib

img_dirpath = pathlib.Path('sample_data/cat_dog_images')

file_list = sorted([str(path) for path in img_dirpath.glob('*.jpg')])
print(file_list)

"""Visualize these images using matplotlib.

Data shape is also called aspect ratio in computer vision. We will find that they have different aspect ratios and later we have to convert them to consistent shapes (aspect ratios).
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
fig = plt.figure(figsize=(12, 5))

for i, file in enumerate(file_list):
  img = Image.open(file) ## open image
  print('Image shape:', np.array(img).shape) ## image shape
  ax = fig.add_subplot(2, 3, i+1) ## how many axes (rows, columns)
  ax.set_xticks([])
  ax.set_yticks([])
  ax.imshow(img) ## visualize image
  ax.set_title(os.path.basename(file), size=15)  ## usage of os to get basename.

plt.tight_layout()
plt.show()

"""Assign labels from the filenames."""

labels = [1 if 'dog' in os.path.basename(file) else 0 for file in file_list]
print(labels)

"""Now we have list of filenames (or path of each image) and a list of their labels."""

class ImageDataset(Dataset):
  def __init__(self, file_list, labels):
    self.file_list = file_list
    self.labels = labels

  def __len__(self):
    return len(self.labels)

  def __getitem__(self, index):
    file = self.file_list[index]
    label = self.labels[index]
    return file, label

image_dataset = ImageDataset(file_list, labels)

for file, label in image_dataset:
  print(file, label)

"""Apply Transformations"""

import torchvision.transforms as transforms
img_height, img_width = 80, 120
transform = transforms.Compose([transforms.ToTensor(),
                                transforms.Resize((img_height, img_width))
                                ])

"""Now upate the image dataset with the transforms we defined."""

class ImageDataset(Dataset):
  def __init__(self, file_list, labels, transform=None):
    self.file_list = file_list
    self.labels = labels
    self.transform = transform

  def __len__(self):
    return len(self.labels)

  def __getitem__(self, index):  ## loading of the raw content(images and labels), decoding images into tensors and resizing the images.
    img = Image.open(self.file_list[index])
    if self.transform is not None:
      img = self.transform(img)
    label = self.labels[index]
    return img, label

image_dataset = ImageDataset(file_list, labels, transform)

fig = plt.figure(figsize=(12, 5))
for i, example in enumerate(image_dataset):
  ax = fig.add_subplot(2, 3, i+1)
  ax.set_xticks([])
  ax.set_yticks([])
  ax.imshow(example[0].numpy().transpose((1,2,0)))
  ax.set_title(f'{example[1]}', size=15)

plt.tight_layout()
plt.show()

"""# Fetching data from Torchvision Library"""


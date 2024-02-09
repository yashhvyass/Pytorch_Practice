{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyMxWDdjMbO+Auu8+mgGn3uQ",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/yashhvyass/Pytorch_Practice/blob/main/LogisticRegression_Pytorch.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 2,
      "metadata": {
        "id": "6RRlgxgMVOWq"
      },
      "outputs": [],
      "source": [
        "import torch\n",
        "import torch.nn as nn\n",
        "import numpy as np\n",
        "from sklearn import datasets\n",
        "import matplotlib.pyplot as plt\n",
        "from sklearn.preprocessing import StandardScaler\n",
        "from sklearn.model_selection import train_test_split"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "bc = datasets.load_breast_cancer()\n",
        "X, y = bc.data, bc.target"
      ],
      "metadata": {
        "id": "Fh1rjfR5VwDP"
      },
      "execution_count": 3,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "n_samples, n_features = X.shape"
      ],
      "metadata": {
        "id": "jbF-EIxeWSor"
      },
      "execution_count": 6,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)"
      ],
      "metadata": {
        "id": "0JyHGxv4WaTY"
      },
      "execution_count": 8,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "## Scaling\n",
        "sc = StandardScaler()\n",
        "X_train = sc.fit_transform(X_train)\n",
        "X_test = sc.transform(X_test)"
      ],
      "metadata": {
        "id": "V5r8huoWY-5L"
      },
      "execution_count": 9,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Convert to tensors\n",
        "X_train = torch.from_numpy(X_train.astype(np.float32))\n",
        "X_test = torch.from_numpy(X_test.astype(np.float32))\n",
        "y_train = torch.from_numpy(y_train.astype(np.float32))\n",
        "y_test = torch.from_numpy(y_test.astype(np.float32))"
      ],
      "metadata": {
        "id": "ns951UG0ZmC_"
      },
      "execution_count": 10,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "print(y_train.shape, y_test.shape)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "eiVJiQtiZ-MJ",
        "outputId": "efd7c2b7-aaa5-40ee-d07e-d3d23c72812c"
      },
      "execution_count": 11,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "torch.Size([455]) torch.Size([114])\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "## To reshape the values we will use view().\n",
        "y_train = y_train.view(y_train.shape[0], 1)\n",
        "y_test = y_test.view(y_test.shape[0], 1)"
      ],
      "metadata": {
        "id": "lNic7f4baNKW"
      },
      "execution_count": 12,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "class LogisticRegression(nn.Module):\n",
        "  def __init__(self, n_input_features):\n",
        "    super(LogisticRegression, self).__init__()\n",
        "\n",
        "    self.linear = nn.Linear(n_input_features, 1)\n",
        "\n",
        "  def forward(self, x):\n",
        "    y_predicted = torch.sigmoid(self.linear(x))\n",
        "    return y_predicted\n",
        "\n",
        "model = LogisticRegression(n_features)"
      ],
      "metadata": {
        "id": "OYSo8ZAcaeqF"
      },
      "execution_count": 15,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Loss\n",
        "learning_rate=0.01\n",
        "criterion = nn.BCELoss()\n",
        "# Optimizer\n",
        "optimizer = torch.optim.SGD(model.parameters(), lr = learning_rate)"
      ],
      "metadata": {
        "id": "KTHj03Bzbi4O"
      },
      "execution_count": 18,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Training Loop\n",
        "num_epochs = 100\n",
        "for epoch in range(num_epochs):\n",
        "  y_predicted = model(X_train)\n",
        "  loss = criterion(y_predicted, y_train)\n",
        "\n",
        "  loss.backward()\n",
        "\n",
        "  optimizer.step()\n",
        "\n",
        "  optimizer.zero_grad()\n",
        "\n",
        "  if (epoch+1)%10==0:\n",
        "    print(f'epoch: {epoch+1}, loss: {loss.item():.4f}')\n",
        "\n",
        "# For Evaluation\n",
        "with torch.no_grad():\n",
        "  y_predicted = model(X_test)\n",
        "  y_predicted_class = y_predicted.round()\n",
        "  acc = y_predicted_class.eq(y_test).sum() / float(y_test.shape[0])\n",
        "  print(f'Accuracy = {acc:.4f}')"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "b5rBLAyFcAbB",
        "outputId": "0f4d03b4-de39-4256-861d-a56753a9973c"
      },
      "execution_count": 23,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "epoch: 10, loss: 0.1947\n",
            "epoch: 20, loss: 0.1909\n",
            "epoch: 30, loss: 0.1874\n",
            "epoch: 40, loss: 0.1840\n",
            "epoch: 50, loss: 0.1809\n",
            "epoch: 60, loss: 0.1780\n",
            "epoch: 70, loss: 0.1752\n",
            "epoch: 80, loss: 0.1726\n",
            "epoch: 90, loss: 0.1701\n",
            "epoch: 100, loss: 0.1678\n",
            "Accuracy = 0.9649\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "VhwVcDYXfMoe"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}
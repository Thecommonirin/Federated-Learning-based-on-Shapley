# Data Valuation in Federated Learning

## Overview
This project implements data valuation algorithms, particularly focusing on Shapley values, within a federated learning context. It provides tools for evaluating the effectiveness and robustness of data contributions, as well as analyzing the marginal contribution of pre-shared and public datasets.

## Features
- **Shapley Value Calculation**: Implements methods for calculating Shapley values to quantify data contributions.
- **Data Effectiveness Evaluation**: Scripts to assess the impact of data on model accuracy.
- **Marginal Contribution Analysis**: Tools to evaluate the contribution of shared and public data.
- **Flexible Data Handling**: Supports various datasets (MNIST, USPS, CIFAR-10, STL-10, a9a) and data partitioning strategies.
- **Proxy Model Training**: Includes utilities for training proxy models (CNN, Logistic Regression) and DeepSets for utility function approximation.

## Project Structure

```
.
├── core/                     # Core utility functions and modules (dataloader, deepsets_training, proxy_models, shapley)
├── datasets/                 # Stores datasets used in the project
├── models/                   # Contains model architectures (e.g., ADDA, DeepSets, task networks)
├── outputs/                  # Stores all generated output files (e.g., accuracy lines, Shapley values)
├── utils/                    # Utility functions and helper scripts
├── scripts/                  # Auxiliary scripts for experimental settings and sampling utilities

├── main_evalRobust.py        # Main execution script for evaluating data robustness and calculating Shapley values
├── main_margiContrib.py      # Main execution script for evaluating marginal contributions
└── README.md                 # This file
```

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd DataValuation
    ```
2.  **Create a virtual environment (recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install dependencies**:
    ```bash
    pip install torch torchvision numpy scikit-learn pandas openpyxl
    ```
    *(Note: Specific versions of libraries might be required. Please refer to a `requirements.txt` if available or install compatible versions.)*

## Datasets

All datasets are expected to be placed in the `datasets/` directory.
- `MNIST`, `USPS`, `CIFAR-10`, `STL-10` are downloaded automatically using `torchvision` when `core/dataloader.py` is run.
- The `a9a` dataset can be downloaded from [LIBSVM](https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary.html#a9a) and should be placed manually in `datasets/`.

## Usage

The main entry points for running experiments are now in the root directory:

-   **`main_evalEffective.py`**: Used to obtain accuracy lines and corresponding effectiveness scores.
    Example: `python main_evalEffective.py --tgt mnist --n_owners 10 --data_size 50 --share 0.2 --epochs 50 --seed 123`

-   **`main_evalRobust.py`**: Used to calculate Shapley values.
    Example: `python main_evalRobust.py --tgt mnist --n_owners 10 --data_size 50 --adv-owners 1 --epsilon 0.1 --epochs 50 --seed 123`

-   **`main_margiContrib.py`**: Used to evaluate the marginal contribution of pre-shared data and public datasets.
    Example: `python main_margiContrib.py --src usps --tgt mnist --share 0.1 --epochs 50 --seed 123`

Please refer to the individual scripts for specific command-line arguments and their descriptions.

## Outputs

All generated output files, typically in `.xlsx` format, are stored in the `outputs/` directory. The structure within `outputs/` is organized by experiment type and dataset.
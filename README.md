# πFL: Private, atomic, incentive mechanism for federated learning based on blockchain

This repository combines two main projects focused on data valuation in the context of Federated Learning, with a strong emphasis on using Shapley values to create fair and robust incentive mechanisms.

The primary projects included are:

1.  **DataValuation**: An implementation of data valuation algorithms in a federated learning setting. It provides tools to evaluate the effectiveness and robustness of data contributions and is the basis for the **πFL** incentive mechanism.
2.  **DistributionalShapley**: An implementation of the paper "A Distributional Framework for Data Valuation," which offers a distributional approach to valuing data points.

---

## Core Components

### 1. DataValuation & πFL

This component focuses on quantifying the contribution of each client in a federated learning setup. It implements various methods for calculating Shapley values to assess data quality and impact on the model's performance.

Based on this, we propose **πFL**, a privacy-preserving and blockchain-based incentive mechanism. Clients are rewarded based on their data contributions, which are evaluated using Shapley value estimations.

📄 **πFL Paper**: [πFL: Private, atomic, incentive mechanism for federated learning based on blockchain](https://www.sciencedirect.com/science/article/pii/S2096720924000848)
*Published at BCRA 2024 (Oral)*

### 2. Distributional Shapley

This component provides the code for the paper "Distributional Shapley: A Distributional Framework for Data Valuation." It offers a more equitable measure of the value of data points that come from an underlying distribution, given a machine learning model and a performance metric.

📄 **Distributional Shapley Paper**: [A Distributional Framework for Data Valuation](https://arxiv.org/pdf/2002.12334.pdf)
*Published at ICML 2020*

---

## Key Features

- **Shapley Value Calculation**: Implements multiple methods for calculating Shapley values to quantify data contributions.
- **Distributional Shapley Framework**: Provides a distributional framework for a more equitable data valuation.
- **Data Effectiveness Evaluation**: Includes scripts to assess the impact of data on model accuracy.
- **Robustness & Contribution Analysis**: Offers tools to evaluate data robustness and the marginal contribution of different datasets.
- **πFL Incentive Mechanism**:
    - 🔐 Privacy-preserving computation.
    - ⚖️ Normalized scoring for fair rewards.
    - ⛓️ On-chain reward distribution via a smart contract.

---

## Repository Structure

The repository is organized into two main directories, each corresponding to one of the core projects:

-   `DataValuation/`: Contains the implementation of data valuation algorithms for federated learning and the πFL framework.
-   `DistributionalShapley/`: Contains the implementation of the Distributional Shapley paper.

Please refer to the `README.md` file within each directory for specific instructions on installation and usage.

---

## Citation

If you use this work, please cite the relevant papers:

```
@article{piFL2024,
  title={πFL: Private, atomic, incentive mechanism for federated learning based on blockchain},
  author={...},
  journal={Blockchain: Research and Applications},
  year={2024},
  publisher={Elsevier}
}

@inproceedings{ghorbani2020distributional,
  title={A Distributional Framework for Data Valuation},
  author={Ghorbani, Amirata and Kim, Michael P. and Zou, James},
  booktitle={International Conference on Machine Learning},
  year={2020}
}
```

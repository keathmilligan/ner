# Project Overview

Prepare data and train a Named Entity Recognition (NER) model to identify key information items in a text document including company names,
domain names, URLs, IP addresses and email addresses. It includes Jupyter notebooks for data generation,
model training, and inference, as well as Python scripts for various NER-related tasks.

Model is exported for use with the ONNX runtime.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Poetry (for dependency management)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/ner.git
   cd ner
   ```

2. **Install dependencies using Poetry:**
   ```bash
   poetry install
   ```

## Directory Structure

- `data/`: Contains data files and notebooks for data generation.
- `logs/`: Stores log files from model training and inference.
- `models/`: Contains trained models and ONNX exports.
  - `ner/`: NER-specific models.
  - `onnx/`: ONNX exports of the models.
- `ner/`: Python scripts for NER tasks.
  - `__init__.py`: Initializes the package.
  - `datagen.py`: Data generation scripts.
  - `ipgen.py`: IP address generation scripts.
  - `urlgen.py`: URL generation scripts.
- `sample_templates/`: Sample templates for various data types.
- `tmp_trainer/`: Temporary files and scripts used during training.

## Usage

### Data Generation

Combines raw data from Kaggle or sources or generated fake data with collections of contextual English sentences
and log messages to produce a NER-ready annotated dataset.

Run the `data.ipynb` Jupyter notebook to generate data for training.

Adjust the count parameters as needed.

The model with current parameters takes about 1.5hrs to train on a Macbook Pro M2 Max.

### Model Training

Run the `model.ipynb` Jupyter notebook to tokenize the dataset, train and test the NER model.

The model exported to ONNX format.

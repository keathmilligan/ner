# Project Overview

The `ner` project is a collection of tools and models for Named Entity Recognition (NER). It includes Jupyter notebooks for data generation, model training, and inference, as well as Python scripts for various NER-related tasks.

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
Run the `data.ipynb` Jupyter notebook to generate data for training.

### Model Training
Run the `model.ipynb` Jupyter notebook to train and test the NER model.

# Image Generation

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Image generation from a t-shirt dataset using neural networks

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         image_generation and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── image_generation   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes image_generation a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

## ***Project Objective***

The objective of this project is to design and train a Variational Autoencoder (VAE) capable of learning a latent representation of T-shirt images and generating new synthetic samples.

The model is trained on a custom dataset of T-shirt images and aims to:
- Learn compressed latent representations
- Reconstruct input images
- Generate new variations of T-shirts
- Analyze reconstruction quality using MSE

## ***Project Description***

This project implements a Convolutional Variational Autoencoder (VAE) using TensorFlow/Keras to model the distribution of T-shirt images.

Unlike a standard Autoencoder, the VAE:
- Learns a probabilistic latent space
- Regularizes latent representations using KL divergence
- Enables sampling and generation of new images

The dataset contains:
- 293 RGB images
- Resolution: 64×64 pixels
- Various T-shirt colors and designs

## ***Dataset Preprocessing***

Before training, all images undergo a preprocessing pipeline to ensure consistency.

*Preprocessing Steps*
1. Format Standardization
    - Supported formats: .jpg, .jpeg, .png, .avif
    - All images are converted to JPEG

2. RGB Conversion
    - All images are converted to RGB (3 channels)

3. Center Cropping
    - Images are cropped to a square shape based on the smallest dimension
    - This avoids distortion during resizing

4. Resizing
    - All images are resized to 64×64 pixels

5. Output Storage
    - Processed images are saved into a clean dataset directory

This ensures:
- Uniform image dimensions
- No aspect ratio distortion
- Clean input for CNN training

## ***Variational Autoencoder Architecture***

The model follows a Convolutional VAE structure:

**Encoder**
- Conv2D + ReLU
- MaxPooling layers
- Feature compression to latent variables
- Outputs:
    - z_mean
    - z_log_var

The encoder learns the parameters of a Gaussian distribution in latent space.

## ***Reparameterization Trick***

To allow backpropagation through stochastic sampling:

$$
z = \mu + \sigma \cdot \epsilon
$$

Where:

$$
\epsilon \sim \mathcal{N}(0,1)
$$

$$
\sigma = e^{0.5 \cdot \text{log\_var}}
$$

This enables gradient flow while sampling.

## ***Decoder***

- Dense layer to reshape latent vector
- Conv2D + UpSampling layers
- Final Sigmoid activation

The decoder reconstructs images back to 64×64×3 format.

## ***Loss Function***

The VAE optimizes a combined loss:

$$
\text{Loss} = \text{Reconstruction Loss} + \text{KL Divergence}
$$

1. Reconstruction Loss

Measured using Mean Squared Error (MSE) between input and reconstructed images.

2. KL Divergence

Regularizes the latent space toward a standard normal distribution.

## ***Evaluation Metric***

The model is evaluated using:
- Mean Squared Error (MSE) on test data
- Visual inspection of reconstructed and generated samples
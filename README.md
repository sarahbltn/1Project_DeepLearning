# Image Generation

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Image generation from a t-shirt dataset using neural networks

## Project Organization

```
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
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
    │
    ├── preprocessing.py              <- Scripts to preprocess the data
```

## **Project Objective**

The objective of this project is to design and train a Variational Autoencoder (VAE) capable of learning a latent representation of T-shirt images and generating new synthetic samples.

The model is trained on a custom dataset of T-shirt images and tries to:

- Learn compressed latent representations
- Reconstruct input images
- Generate new variations of T-shirts
- Analyze reconstruction quality using reconstruction metrics
- Explore and validate the learned latent space


## **Project Description**

This project implements a Convolutional Variational Autoencoder (VAE) using TensorFlow/Keras to model the distribution of T-shirt images.

Unlike a standard Autoencoder, the VAE:

- Learns a probabilistic latent space
- Regularizes latent representations using KL divergence
- Enables sampling and generation of new images
- Allows smooth transitions between samples through latent space interpolation

The project was developed through **three main experiments**, progressively improving dataset quality, model capacity, and training strategy.

### Experiment 1 Dataset
- 293 RGB images
- Resolution: 64×64 pixels
- Various T-shirt colors and designs

### Final Dataset
- 686 RGB images
- Resolution: 128×128 pixels
- Dataset cleaning performed to remove low-visibility samples
- Increased visual variability and detail

All experiments and implementations can be found in the **notebooks** directory.

## **Dataset Preprocessing**

Before training, all images were preprocessed to ensure consistency.

### *Preprocessing Steps*

1. **Format Standardization**
   - Supported formats: `.jpg`, `.jpeg`, `.png`, `.avif`
   - All images are converted to JPEG

2. **RGB Conversion**
   - All images are converted to RGB (3 channels)

3. **Center Cropping**
   - Images are cropped to a square shape based on the smallest dimension
   - Prevents distortion during resizing

4. **Resizing**
   - Images resized to **64×64** for Experiment 1
   - Images resized to **128×128** for Experiment 2

5. **Normalization**
   - Pixel values scaled to the range [0,1]

6. **Data Augmentation**
   - Small rotations
   - Horizontal and vertical shifts
   - Zoom variations
   - Horizontal flipping

   Data augmentation is applied during training using `ImageDataGenerator` to improve generalization and increase effective dataset variability.

7. **Output Storage**
   - Processed images stored in a clean dataset directory

This ensures:

- Uniform image dimensions
- No aspect ratio distortion
- Stable CNN training input
- Increased robustness to visual variations

---

## **Variational Autoencoder Architecture**

The model follows a Convolutional VAE structure composed of an encoder, a sampling layer, and a decoder.

### **Encoder**

- Conv2D + ReLU layers
- MaxPooling layers for spatial compression
- Feature extraction and dimensionality reduction
- Dense layer for feature integration

Outputs:

- `z_mean`
- `z_log_var`

The encoder learns the parameters of a Gaussian distribution representing each image in latent space.

Experiment 2 increases model capacity by:
- Using higher-resolution images
- Increasing latent dimensionality
- Allowing richer feature representations.


## **Reparameterization Trick**

To allow backpropagation through stochastic sampling:

$$
z = \mu + \sigma \cdot \epsilon
$$

Where:

$$
\epsilon \sim \mathcal{N}(0,1)
$$

$$
\sigma = e^{\frac{1}{2} \log \sigma^2}
$$

This enables gradient flow while sampling latent variables.

### β-VAE Extension (Experiment 2)

A scaling factor β is introduced:

$$
\text{Loss} = \text{Reconstruction Loss} + \beta \cdot \text{KL Divergence}
$$

The β parameter controls the balance between:

- reconstruction accuracy
- latent space regularization

This encourages a smoother and more structured latent representation.


## **Decoder**

The decoder performs the inverse operation of the encoder:

- Dense layer expands latent representation
- Reshape layer converts vectors into feature maps
- Conv2D + UpSampling layers progressively increase spatial resolution
- Final Sigmoid activation outputs normalized pixel values

The decoder reconstructs images back to their original dimensions:

- 64×64×3 (Experiment 1)
- 128×128×3 (Experiment 2)


## **Loss Function**

The VAE optimizes a combined loss:

$$
\text{Loss} =
\text{Reconstruction Loss}
+
\beta \cdot
\text{KL Divergence}
$$

### 1. Reconstruction Loss

Measured using **Mean Squared Error (MSE)** between input and reconstructed images.

This ensures reconstructed images remain visually similar to the originals.

### 2. KL Divergence

Regularizes the latent space toward a standard normal distribution, enabling meaningful sampling and image generation.


## **Evaluation Strategy**

The model is evaluated using:

- Mean Squared Error (MSE)
- Structural Similarity Index (SSIM)
- Visual comparison of reconstructed images
- Visualization of newly generated samples

Latent space interpolation verifies that transitions between encoded images are smooth, indicating that the model learned a continuous and meaningful latent representation.

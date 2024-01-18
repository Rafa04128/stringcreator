import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Load an image
image = cv2.imread('path/to/your/image.jpg')

# Resize image
resized_image = cv2.resize(image, (224, 224))  # Resize to 224x224 pixels



# Normalize pixel values to be between 0 and 1
normalized_image = resized_image / 255.0

# Convert to grayscale
gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)




# Create an image data generator for augmentation
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True
)

# Apply it to an image
augmented_images = datagen.flow(normalized_image)


import tensorflow as tf

# Assuming 'images' is a list of multiple images
images = np.array([normalized_image, ...])  # Convert list of images to a numpy array

# Create a dataset and batch it
dataset = tf.data.Dataset.from_tensor_slices(images)
batched_dataset = dataset.batch(32)  # Batch size of 32



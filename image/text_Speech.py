import cv2
import tensorflow as tf

def load_and_preprocess_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (224, 224))  # Resize to the desired input size of the model
    image = image / 255.0  # Normalize pixel values
    return image

# Assuming you have a list of image paths and corresponding texts
image_paths = ['path/to/image1.jpg', 'path/to/image2.jpg', ...]
text_descriptions = ['description for image1', 'description for image2', ...]

# Load and preprocess images
images = [load_and_preprocess_image(path) for path in image_paths]

# Assuming you are using TensorFlow
text_vectorization = tf.keras.layers.TextVectorization(max_tokens=10000, output_sequence_length=200)
text_vectorization.adapt(text_descriptions)

# Vectorize text descriptions
vectorized_texts = text_vectorization(text_descriptions)


# Convert to TensorFlow dataset
train_dataset = tf.data.Dataset.from_tensor_slices((images, vectorized_texts))

# Shuffle and batch the dataset
train_dataset = train_dataset.shuffle(buffer_size=1024).batch(32)

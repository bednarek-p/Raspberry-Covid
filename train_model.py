import matplotlib.pyplot as plt
import numpy as np
import argparse
import os

from imutils import paths
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.utils import to_categorical

# Initialize leatning rate, epochs and batch size
INITIAL_LEARNING_RATE = 1e-4
EPOCHS = 20
BATCH_SIZE = 32


def load_dataset():
    print("|*DEBUG*| IMAGES LOADING")
    image_paths = list(paths.list_images("./dataset/"))
    data_array = []
    label_list = []

    # Loop over all images
    for path_to_image in image_paths:
        # Extract class label from the path
        label = path_to_image.split(os.path.sep)[-2]

        # Load the input image and preprocess it
        image = load_img(path_to_image, target_size=(224, 224))
        image = img_to_array(image)
        image = preprocess_input(image)

        # Update data array and labels lists
        data_array.append(image)
        label_list.append(label)

    # Convert data and labels to NumPy arrays
    data_array = np.array(data_array, dtype="float32")
    label_list = np.array(label_list)

    # Labels encoding using labelBinarizer
    lb = LabelBinarizer()
    label_list = lb.fit_transform(label_list)
    label_list = to_categorical(label_list)

    # Split the data into training and testing sets.
    # 80% for training, 20% for testing
    (trainX, testX, trainY, testY) = train_test_split(
        data_array, label_list, test_size=0.20, stratify=label_list, random_state=42
    )

    # Augment training data set using ImageDataGenerator
    augmented_data = ImageDataGenerator(
        rotation_range=20,
        zoom_range=0.15,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.15,
        horizontal_flip=True,
        fill_mode="nearest",
    )

    return trainX, testX, trainY, testY, augmented_data, lb


def create_model():
    # Load the MobileNetV2 network, ensure the head layers are not included
    base_model = MobileNetV2(
        weights="imagenet", include_top=False, input_tensor=Input(shape=(224, 224, 3))
    )

    # Create the head of the model that will be placed on the top of base model
    head_model = base_model.output
    head_model = AveragePooling2D(pool_size=(7, 7))(head_model)
    head_model = Flatten(name="flatten")(head_model)
    head_model = Dense(128, activation="relu")(head_model)
    head_model = Dropout(0.5)(head_model)
    head_model = Dense(2, activation="softmax")(head_model)

    # Place created head model on top of the base model
    model = Model(inputs=base_model.input, outputs=head_model)

    # Loop over all layers in the base model and freeze them
    # (ensure they won't be updated on training process)
    for layer in base_model.layers:
        layer.trainable = False

    # Compile created model
    print("|*DEBUG*| MODEL COMPILING")
    optimizer = Adam(lr=INITIAL_LEARNING_RATE, decay=INITIAL_LEARNING_RATE / EPOCHS)
    model.compile(loss="binary_crossentropy", optimizer=optimizer, metrics=["accuracy"])
    return model


def train_model(trainX, testX, trainY, testY, augmented_data, model, lb):
    # Train model head
    print("|*DEBUG*| NETWORK HEAD TRAINING")
    model_head = model.fit(
        augmented_data.flow(trainX, trainY, batch_size=BATCH_SIZE),
        steps_per_epoch=len(trainX) // BATCH_SIZE,
        validation_data=(testX, testY),
        validation_steps=len(testX) // BATCH_SIZE,
        epochs=EPOCHS,
    )

    # Make predictions on testing set
    print("|*DEBUG*| NETWORK PREDICTIONS ON TESTING SET")
    predIdxs = model.predict(testX, batch_size=BATCH_SIZE)

    # Find label with largest predicted porbability for each image
    # in testing set
    predIdxs = np.argmax(predIdxs, axis=1)

    # Print classification report
    print(
        classification_report(testY.argmax(axis=1), predIdxs, target_names=lb.classes_)
    )
    # Save model to disc
    print("|*DEBUG*| MODEL SAVING")
    model.save("mask_detector.model", save_format="h5")
    return model_head


def plot_model_results(model_head):
    plt.style.use("ggplot")
    plt.figure()
    plt.plot(np.arange(0, EPOCHS), model_head.history["loss"], label="train_loss")
    plt.plot(np.arange(0, EPOCHS), model_head.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, EPOCHS), model_head.history["accuracy"], label="train_acc")
    plt.plot(np.arange(0, EPOCHS), model_head.history["val_accuracy"], label="val_acc")
    plt.title("Training Loss and Accuracy")
    plt.xlabel("Epoch X")
    plt.ylabel("Loss/Accuracy")
    plt.legend(loc="lower left")
    plt.savefig("./results.png")


def run_training():
    trainX, testX, trainY, testY, augmented_data, lb = load_dataset()
    model = create_model()
    head_model = train_model(trainX, testX, trainY, testY, augmented_data, model, lb)
    plot_model_results(head_model)


if __name__ == "__main__":
    run_training()

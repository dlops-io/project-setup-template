"""Trainer: Vertex AI runs `python -m trainer.task --epochs=3 --batch_size=16` in a prebuilt TensorFlow
image (container_uri in src/ml-workflow/components.py).

This skeleton trains a tiny model on made-up data, so the whole path works before you have your own:
train, save to $AIP_MODEL_DIR, upload to the Model Registry, deploy, predict. Replace load_data() and
build_model() with yours, and keep the export at the end.

The saved model answers {"features": [<NUM_FEATURES> numbers]} with {"prediction": [<number>]}.
src/model-deploy/cli.py --predict sends that.
"""

import argparse
import os

import numpy as np
import tensorflow as tf

NUM_FEATURES = 4


def load_data(num_rows=1000):
    """Made-up data: y = sum of the features, plus noise. Replace with yours, e.g. from GCS."""
    rng = np.random.default_rng(seed=42)
    x = rng.random((num_rows, NUM_FEATURES), dtype=np.float32)
    y = x.sum(axis=1, keepdims=True) + rng.normal(0, 0.01, (num_rows, 1)).astype(np.float32)
    return x, y


def build_model():
    model = tf.keras.Sequential(
        [
            tf.keras.Input(shape=(NUM_FEATURES,)),
            tf.keras.layers.Dense(8, activation="relu"),
            tf.keras.layers.Dense(1),
        ]
    )
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01), loss="mse")
    return model


def export(model, model_dir):
    """Saves a SavedModel for the prebuilt serving image. The argument name of serve() (`features`)
    is the key clients send in each prediction instance."""
    archive = tf.keras.export.ExportArchive()
    archive.track(model)

    def serve(features):
        return {"prediction": model(features, training=False)}

    archive.add_endpoint(
        name="serving_default",
        fn=serve,
        input_signature=[tf.TensorSpec([None, NUM_FEATURES], tf.float32, name="features")],
    )
    archive.write_out(model_dir)


def main():
    parser = argparse.ArgumentParser(description="Trainer")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=16)
    args = parser.parse_args()

    # Vertex AI sets AIP_MODEL_DIR to <base_output_dir>/model (a gs:// path; TensorFlow writes there
    # directly). Running it yourself, it saves next to you.
    model_dir = os.getenv("AIP_MODEL_DIR", "outputs/model")

    x, y = load_data()
    model = build_model()
    history = model.fit(x, y, epochs=args.epochs, batch_size=args.batch_size, validation_split=0.2)
    print("Final validation loss:", history.history["val_loss"][-1])

    export(model, model_dir)
    print("Saved the model to", model_dir)


if __name__ == "__main__":
    main()

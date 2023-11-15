import datetime
import os

import gradio as gr
import keras
import numpy as np
from PIL import Image

import database_operations
import digit_clipping_and_preprocessing

model = keras.models.load_model("mnist_model.h5")  # Egitilen modeli yukluyorum
images = os.getcwd() + "\\static\\"


def digit_recognition(image, is_image_saved):
    processed_image = digit_clipping_and_preprocessing.clipping_digit_from_image(image)
    processed_image = digit_clipping_and_preprocessing.add_frame_and_resize_image(
        processed_image
    )

    processed_image = processed_image.reshape(1, 28, 28, 1).astype("float32")
    processed_image = processed_image / 255

    prediction_1 = model.predict(processed_image).tolist()[0]
    prediction_2 = model.predict([processed_image])[0]
    predicted_digit, digit_correctness = str(np.argmax(prediction_2)), max(prediction_2)

    digit_correctness = "%" + str(round(digit_correctness * 100, 2))

    if is_image_saved == "Yes":
        fixed_name = "image"
        additional_name = datetime.datetime.now().strftime("%d%m%y_%H%M%S")
        image_name = "_".join([fixed_name, additional_name])

        image_data = Image.fromarray(image)
        image_data.save(images + image_name + ".png", format="png")

        image_path = image_name + ".png"

        data = image_path, predicted_digit, digit_correctness

        database_operations.add_database_record(data)

    database_operations.run_threading()

    return {str(i): prediction_1[i] for i in range(10)}


output_component = gr.outputs.Label(label="Prediction", type="auto", num_top_classes=2)
gr.Interface(
    fn=digit_recognition,
    inputs=["sketchpad", gr.inputs.Radio(["No", "Yes"])],
    outputs=output_component,
    allow_screenshot=False,
    allow_flagging=False,
    theme="compact",
    article="""# **Welcome to the Handwritten Digit Recognition Project.**
- Draw a Number in the White Area (between 0 - 9).
- You can see the result by clicking the Submit button. The 2 closest results are shown.
- To save the image to the Database, check the "Yes" box and press the Submit button again.
- Image, image digit prediction, and prediction accuracy information are kept in the database.
- In addition, the images that are correctly recognized in the database are marked with a checkbox and the success rate is calculated.""",
).launch(inbrowser=True, share=False)

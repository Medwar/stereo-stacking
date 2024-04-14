#First working version

import os
import cv2
import numpy as np

# Folder containing the source images
source_folder = r"F:\shift test\gibbs\align"
shift_values = (-2, 2, -1, 1)

for shift in shift_values:

    # Folder to save the resulting images
    result_folder = os.path.join(source_folder, "stereoshift", str(shift))
    # Create the result folder if it doesn't exist
    os.makedirs(result_folder, exist_ok=True)

    # Define the image extensions to include
    valid_extensions = ['.jpg', '.tif', '.tiff', '.jpeg', '.png', '.gif']  # Add more extensions if needed

    # Filter files based on extensions
    image_files = [os.path.join(source_folder, file) for file in os.listdir(source_folder) if
                   os.path.splitext(file)[1].lower() in valid_extensions]

    # Count the number of files in the source folder
    num_files = len(image_files)

    # Calculate the step
    percent = shift / 100
    image_width = cv2.imread(image_files[0]).shape[1]
    step = percent * image_width / (num_files - 1)

    print(f"num_files: {num_files}")
    print(f"step: {step}")

    # Find the index of the middle image
    middle_index = num_files // 2

    print(f"middle_index: {middle_index}")

    # Iterate through images in the folder, apply subpixel X shift to each of them, and save the results
    for idx, filename in enumerate(image_files):
        # Read the image
        image = cv2.imread(filename)

        # Calculate the shift for the current image
        shift_x = (idx - middle_index) * step

        # Apply subpixel translation using interpolation
        rows, cols = image.shape[:2]
        M = np.float32([[1, 0, shift_x], [0, 1, 0]])
        translated_image = cv2.warpAffine(image, M, (cols, rows), borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))

        # Save the resulting image with the same name in the result folder
        filename_s = os.path.basename(filename)
        result_image_path = os.path.join(result_folder, filename_s)
        cv2.imwrite(result_image_path, translated_image)

        print(f"Processed #{idx + 1}/{num_files}: {filename} with X shift: {shift_x}")

print("All images processed successfully.")

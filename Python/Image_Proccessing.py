import os
import cv2


def convert_images_to_grayscale(input_folder, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        # Skip non-files or non-image formats
        if not os.path.isfile(input_path) or not filename.lower().endswith(
            ("png", "jpg", "jpeg", "bmp", "tiff")
        ):
            continue

        try:
            # Read the image
            img = cv2.imread(input_path)

            # Check if the image is loaded properly
            if img is None:
                print(f"Could not read {filename}, skipping.")
                continue

            # Convert to grayscale
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            bla_img = cv2.bilateralFilter(gray_img, 11, 17, 17)

            # Save the grayscale image to the output folder
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, bla_img)
            print(f"Converted and saved: {output_path}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    # Define input and output folders
    input_folder = "E:\MV_Project\Picture"  # Replace with your input folder path
    output_folder = "E:\MV_Project\Picture1"  # Replace with your output folder path

    # Run the conversion
    convert_images_to_grayscale(input_folder, output_folder)

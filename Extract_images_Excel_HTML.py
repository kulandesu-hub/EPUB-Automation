import openpyxl
import os


def extract_images_from_excel(file_path, output_dir='D:\\alt-text_report\\Excel_images'):
    # Load the workbook
    wb = openpyxl.load_workbook(file_path)
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over all the worksheets in the workbook
    for sheet in wb.worksheets:
        # Access the _images attribute
        images = sheet._images
        
        for img in images:
            # Access the image data
            image_data = img._data()
            
            # Determine the file format based on the image data
            image_format = img.path.split('.')[-1]  # Assuming the format is in the file extension
            if image_format.lower() not in ['png', 'jpg', 'jpeg', 'bmp']:
                image_format = 'png'  # Default to PNG if unknown

            # Extract the cell coordinate where the image is anchored
            anchor = img.anchor
            if isinstance(anchor, str):
                cell_coordinate = anchor
            else:
                cell_coordinate = f"{openpyxl.utils.get_column_letter(anchor._from.col + 1)}{anchor._from.row + 1}"

            # Create a filename using the cell coordinate
            image_filename = f"image_{sheet.title}_{cell_coordinate}.{image_format}"
            
            # Replace invalid filename characters
            image_filename = image_filename.replace(':', '_')
            
            # Create the full path for the image file
            image_path = os.path.join(output_dir, image_filename)
            
            # Write the image data to a file
            with open(image_path, 'wb') as image_file:
                image_file.write(image_data)
            
            print(f"Saved {image_path}")

# Example usage
extract_images_from_excel(r'D:\alt-text_report\excel\excel.xlsx')


with open("D:\\alt-text_report\\Extract_images_finished.txt", "a", encoding="utf-8") as f:
    f.write("task completed")
print('Finished')

def _import_image(img):
    if not PILImage:
        raise ImportError('You must install Pillow to fetch image objects')

    if not isinstance(img, PILImage.Image):
        img = PILImage.open(img)
    
    # This is the part you have to add (Start)
    try:
        if (img.format.lower() == "wmf"):
            fp = BytesIO()
            img.save(fp, format="png")
            img = PILImage.open(fp)
    except:
        None
    # This is the part you have to add (End)

    return img
_import_image()

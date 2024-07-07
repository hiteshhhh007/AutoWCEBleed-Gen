import os
import shutil
import random

# Define paths
base_dir = 'WCEBleedGen'
categories = ['bleeding', 'non-bleeding']
bounding_box_dirs = ['TXT', 'XML', 'YOLO_TXT']

# Define the split ratio
train_ratio = 0.8

# Create train and test directories
for category in categories:
    os.makedirs(os.path.join(base_dir, 'train', category, 'Annotations'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'train', category, 'Images'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'test', category, 'Annotations'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'test', category, 'Images'), exist_ok=True)
    if category == 'bleeding':
        for bbox_dir in bounding_box_dirs:
            os.makedirs(os.path.join(base_dir, 'train', category, 'Bounding boxes', bbox_dir), exist_ok=True)
            os.makedirs(os.path.join(base_dir, 'test', category, 'Bounding boxes', bbox_dir), exist_ok=True)

# Function to split files and move annotations with images
def split_and_move_files(category, train_ratio, base_dir):
    image_dir = os.path.join(base_dir, category, 'Images')
    images = os.listdir(image_dir)
    random.shuffle(images)
    train_split = int(len(images) * train_ratio)
    train_images = images[:train_split]
    test_images = images[train_split:]

    def move_files(images, dataset_type):
        for image in images:
            image_name, ext = os.path.splitext(image)
            # Move image
            shutil.move(os.path.join(image_dir, image), os.path.join(base_dir, dataset_type, category, 'Images', image))
            # Move corresponding annotation
            ann_file = image_name + '.txt'  # Assuming annotations are in TXT format
            ann_path = os.path.join(base_dir, category, 'Annotations', ann_file)
            if os.path.exists(ann_path):
                shutil.move(ann_path, os.path.join(base_dir, dataset_type, category, 'Annotations', ann_file))
            # Move bounding boxes if category is 'bleeding'
            if category == 'bleeding':
                for bbox_dir in bounding_box_dirs:
                    bbox_file = image_name + '.txt'
                    bbox_path = os.path.join(base_dir, category, 'Bounding boxes', bbox_dir, bbox_file)
                    if os.path.exists(bbox_path):
                        shutil.move(bbox_path, os.path.join(base_dir, dataset_type, category, 'Bounding boxes', bbox_dir, bbox_file))

    move_files(train_images, 'train')
    move_files(test_images, 'test')

# Split files for each category
for category in categories:
    split_and_move_files(category, train_ratio, base_dir)

print("Dataset split into training and testing sets successfully.")

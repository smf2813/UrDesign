import faiss
import numpy as np
import torch
import os
from PIL import Image
from torchvision import transforms
import clip

# Avoid multiple OpenMP runtime libraries conflict
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, preprocess = clip.load("ViT-B/32", device=device)

# Function to convert images to CLIP vectors
def image_to_vector(image):
    image = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        vector = clip_model.encode_image(image)
    return vector.cpu().numpy().flatten()

# Create FAISS index
def create_faiss_index(vectors):
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    faiss.normalize_L2(vectors)
    index.add(vectors)
    return index

# Load all images from database folder and convert to vectors
def load_image_vectors(folder_path):
    product_vectors = []
    image_paths = []
    
    # Supported image extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']
    
    # Walk through directory
    for root, _, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_path = os.path.join(root, file)
                try:
                    image = Image.open(image_path).convert('RGB')
                    vector = image_to_vector(image)
                    product_vectors.append(vector)
                    image_paths.append(image_path)
                except Exception as e:
                    print(f"Error processing {image_path}: {e}")
    
    return np.array(product_vectors, dtype=np.float32), image_paths
'''
# Search similar images
def search_similar_images(query_vector, index, image_paths, top_k=5):
    query_vector = np.array([query_vector], dtype=np.float32)
    faiss.normalize_L2(query_vector)
    distances, indices = index.search(query_vector, top_k)
    return [(image_paths[i], distances[0][i]) for i in indices[0]]
'''

def search_similar_images(query_vector, index, image_paths, top_k=5):
    query_vector = np.array([query_vector], dtype=np.float32)
    faiss.normalize_L2(query_vector)
    distances, indices = index.search(query_vector, top_k)
    results = []
    for pos, i in enumerate(indices[0]):
        if i < len(image_paths):
            results.append((image_paths[i], distances[0][pos]))
        else:
            print(f"Warning: received index {i} which is out of bounds (max allowed is {len(image_paths)-1})")
    return results


# Configuration
database_folder = r"C:\Users\Aurora\Downloads\שולחנות עתיקים 500\שולחנות עתיקים 500"
query_image_path = r"C:\Users\Aurora\Downloads\שולחנות עתיקים 500\שולחנות עתיקים 500\image_90.jpg"


# Step 1: Load database images and create index
print("Loading database images...")
database_vectors, image_paths = load_image_vectors(database_folder)
print(f"Loaded {len(image_paths)} images")

print("Creating FAISS index...")
index = create_faiss_index(database_vectors)
print(f"FAISS index ntotal: {index.ntotal}")

# Step 2: Process query image
print("Processing query image...")
query_image = Image.open(query_image_path).convert('RGB')
query_vector = image_to_vector(query_image)

# Step 3: Search for similar images
top_k = 5
similar_images = search_similar_images(query_vector, index, image_paths, top_k)

# Display results
print(f"\nTop {top_k} similar images:")
for path, distance in similar_images:
    print(f"Image: {path}")
    print(f"Similarity Distance: {distance:.4f}\n")
    

# 🔎 FurnitureMatch – AI-Powered Visual Search for Furniture

**FurnitureMatch** is a visual search app where users upload a photo of a furniture item, and the system returns the top 5 most visually similar purchasable items scraped from Pinterest. It combines machine learning, computer vision, and fast similarity search to deliver accurate, aesthetic matches.

## 🛠 Tech Stack

- **Frontend**: React Native 
- **Backend**: Python FastAPI  
- **Database**: SQLite  
- **Image Processing**: OpenCV, YOLO  
- **Embedding Model**: CLIP  
- **Similarity Search**: FAISS  
- **Scraping Source**: Pinterest  

## 🚀 Features

- 📷 Upload a photo of any furniture item  
- 🧠 AI detects and isolates the furniture  
- 🧬 Generates image embeddings using CLIP  
- ⚡ Searches Pinterest product embeddings with FAISS  
- 🖼 Returns top 5 visually similar matches  


## 🔄 Workflow

1. **Scraping**: Collect furniture images from Pinterest using a custom scraper  
2. **Storage**: Save the images and metadata in SQLite  
3. **Preprocessing**: Use YOLO to detect and crop furniture  
4. **Embedding**: Generate feature vectors using CLIP  
5. **Indexing**: Store embeddings in a FAISS index for fast lookup  
6. **Search**: On user upload, embed the input and search FAISS for nearest neighbors  

## 📦 Installation

### Environment Setup

1. Install **Python 3.10** or newer.
2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install all dependencies:

```bash
pip install -r requirements.txt
```

### Download the YOLO model

The backend expects a file called `yolo11n.pt` in the `backend/` directory.
If it is missing, download the YOLOv8n model from the
[Ultralytics releases page](https://github.com/ultralytics/assets/releases),
rename it to `yolo11n.pt` and place it inside `backend/`.

### Starting the backend

Run the FastAPI server from the repository root:

```bash
uvicorn app.main:app --reload --app-dir backend
```

The API will be available at `http://127.0.0.1:8000`.

### Accessing the frontend

Open `frontend/index.html` in your browser. The page uploads images to the
`/match` endpoint of the running backend and displays the results.

## 🧪 Example


## 🛤 Future Enhancements







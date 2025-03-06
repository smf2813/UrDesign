Non-Profit Acadimic Project
For an academic project, you can build the app at **$0 cost** using open-source tools and free-tier services. Here's a revised plan with budget-friendly alternatives:

---

### **Phase 1: Backend Setup (Free Tools)**
1. **Backend Framework**
   - Use **Python Flask** or **FastAPI** (open-source) for APIs.
   - Host for free on **Heroku** (free dyno) or **PythonAnywhere** (free tier).  
   *Note: Heroku’s free tier sleeps after inactivity, but works for testing.*

2. **Image Processing**
   - Keep using **YOLO** (free, open-source) for object detection.
   - Use **OpenCV** (free) for cropping/resizing images.
   - Run FAISS locally on CPU (no GPU costs) for similarity search.

3. **Database**
   - Use **SQLite** (file-based, no server) or **Supabase** (free tier for PostgreSQL).
   - Store product metadata in a CSV/JSON file if the dataset is small (no database needed).

4. **Pinterest API**
   - Use the free tier of Pinterest’s API (limit requests to stay within quota).

---

### **Phase 2: Frontend (Zero Cost)**
5. **UI Framework**
   - Build with **React** or **Svelte** (open-source).
   - Host the frontend for free on **GitHub Pages**, **Vercel**, or **Netlify**.

6. **Image Upload**
   - Use **Cloudinary** (free tier: 25GB storage, 25k monthly transformations) to store user-uploaded images.  
   *Alternative:* Encode images as Base64 and process them in-memory (no storage).

---

### **Phase 3: AI/ML (Free Compute)**
7. **YOLO & FAISS**
   - Run inference on CPU (no GPU) using **ONNX Runtime** (optimized for low-resource environments).
   - Precompute embeddings for your furniture database offline to avoid real-time costs.

8. **Embedding Model**  
   Use a lightweight model like **MobileNet** (free, CPU-friendly) instead of heavy models like ResNet.

---

### **Phase 4: Deployment & Tools**
9. **Hosting**
   - Backend: Heroku (free) or **Railway.app** (free tier).
   - Frontend: Netlify/Vercel (free static hosting).
   - Database: **Supabase** (free tier) or **Neon.tech** (free Postgres).

10. **APIs & Auth**
    - Authentication: Use **Firebase Auth** (free tier) if needed.
    - Pinterest API: Stick to rate limits to avoid charges.

11. **Monitoring**  
    Use **Prometheus** + **Grafana** (open-source) for logging, or **Better Stack** (free tier).

---

### **Phase 5: Cost-Free Workflow**
1. **Code Repo**: GitHub (free).
2. **CI/CD**: GitHub Actions (free for public repos).
3. **Image Storage**: Cloudinary free tier.
4. **Compute**: Local CPU for YOLO/FAISS or free cloud tiers.
5. **Domain**: Use a free subdomain (e.g., `yourapp.netlify.app`).

---

### **Tools to Replace Paid Services**
| **Function**       | **Free Alternative**                          |
|---------------------|-----------------------------------------------|
| Image Hosting       | Cloudinary (25GB free)                        |
| Database            | Supabase / Neon.tech (Postgres free tier)     |
| Backend Hosting     | Heroku, Railway.app                           |
| Frontend Hosting    | Vercel, Netlify, GitHub Pages                 |
| Authentication      | Firebase Auth (free)                          |
| Monitoring          | Better Stack (free) / Prometheus              |
| CI/CD               | GitHub Actions                                |
| Email/SMS           | SendGrid (100 emails/day free)                |

---

### **Limitations to Accept**
- **Heroku**: Sleeps after 30 mins of inactivity (not ideal for 24/7 demo, but fine for academic use).
- **Cloudinary**: 25GB/month limit (delete test images regularly).
- **Pinterest API**: Rate limits (e.g., 100 requests/day).
- **CPU Inference**: Slower than GPU, but works for small-scale testing.

---

### **Step-by-Step Implementation**
1. **Backend**  
   - Deploy Flask API on Heroku.  
   - Use this template: [Flask on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python).

2. **Frontend**  
   - Create a React app with `create-react-app` and deploy to Netlify:  
     ```bash
     npm create vite@latest my-frontend -- --template react
     cd my-frontend
     npm install
     npm run build
     ```
   - Drag-and-drop the `dist` folder to Netlify.

3. **Database**  
   - Create a Supabase project, set up a `products` table with columns: `id`, `image_url`, `embedding`, `product_link`.

4. **Integrate YOLO/FAISS**  
   - Example code for CPU inference:  
     ```python
     from ultralytics import YOLO
     model = YOLO("yolov8n.pt")  # Lightweight YOLO model
     results = model.predict(uploaded_image)
     ```

5. **Connect to Pinterest API**  
   - Use the `pinterest-api` Python library:  
     ```python
     import requests
     response = requests.get(
       f"https://api.pinterest.com/v5/pins?query=chair",
       headers={"Authorization": "Bearer YOUR_TOKEN"}
     )
     ```

---

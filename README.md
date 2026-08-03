# 🎬 Movie Recommendation System

https://drive.google.com/file/d/1zp5m_rM3F6zJRyMRal1y7d964bwqgGap/view?usp=sharing

A Machine Learning-based **Movie Recommendation System** built using **Python, Scikit-learn, Pandas, and Streamlit**. The application recommends movies similar to the selected movie using **content-based filtering** and **cosine similarity**. Movie posters are fetched dynamically using the **OMDb API**, providing an interactive and visually appealing user experience.

---

## 📌 Features

- 🎥 Recommend similar movies based on selected movie
- 📊 Content-Based Recommendation System
- 🔍 Cosine Similarity for finding similar movies
- 🖼️ Fetches movie posters using the OMDb API
- ⚡ Interactive Streamlit web application
- 💻 Simple and user-friendly interface

---

## 🛠️ Technologies Used

- Python
- Pandas
- Scikit-learn
- Streamlit
- FastAPI
- Pickle
- OMDb API

---

## ⚙️ How It Works

1. Movie data is preprocessed.
2. Important features (genres, titles, release year, ratings, imdb ids, etc.) are combined into a single text field.
3. Text data is converted into vectors using vectorization techniques.
4. Cosine similarity is calculated between movie vectors.
5. When a user selects a movie, the system finds the most similar movies.
6. Movie posters are retrieved using the OMDb API and displayed alongside recommendations.

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/Abhishek98negi/Movie-Recommendation-System.git
```

```bash
cd Movie-Recommendation-System
```

### Create a virtual environment (Optional)

```bash
python -m venv .venv
```

Activate it

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 OMDb API Setup

1. Visit **https://www.omdbapi.com/apikey.aspx**
2. Generate your free API key.
3. Replace the API key in your project.

Example:

```python
API_KEY = "YOUR_API_KEY"
```

---

## ▶️ Run the Application

```bash
uvicorn backend.main:app --reload
```

```bash
streamlit run frontend/app.py
```

Open your browser and visit

```
http://localhost:8501
```

---


## 🧠 Machine Learning Concepts Used

- Content-Based Recommendation
- Feature Engineering
- Text Vectorization
- Cosine Similarity
- Data Preprocessing

---

## 📚 Dataset

This project uses the **Movie Lens Small Latest Dataset** for generating movie recommendations.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

## 👨‍💻 Author

**Abhishek Negi**

GitHub: https://github.com/Abhishek98negi

---

## ⭐ If you found this project useful, please give it a Star!

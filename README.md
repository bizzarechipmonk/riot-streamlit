Love it. Let’s make this feel like a legit internal product, not just “Jacob’s side script.” Here’s a clean, professional README you can drop straight into `README.md`.

---

# RIOT – Sales Enablement Streamlit App

RIOT (Rep Intelligence Opportunity Tool) is a Streamlit-based sales enablement application that delivers **vertical-, stage-, and competitor-specific guidance** to sales reps based on a Salesforce Opportunity ID.

The goal is to provide contextual coaching and resources in real time — helping reps advance deals more effectively.

---

## 🚀 What This App Does

When a rep enters an **Opportunity ID**, the app:

1. Looks up the opportunity in `opportunities.csv`
2. Extracts:

   * Sales Stage
   * Vertical
   * Competitor
3. Matches those attributes against `guidance.json`
4. Returns tailored:

   * Messaging guidance
   * Strategic recommendations
   * Relevant enablement resources

---

## 📂 Project Structure

```
riot-streamlit/
│
├── app.py                # Main Streamlit application
├── opportunities.csv     # Opportunity dataset (9k+ rows)
├── guidance.json         # Structured enablement guidance
├── requirements.txt      # Python dependencies
├── .gitignore
└── README.md
```

---

## 📊 Data Requirements

### `opportunities.csv`

Must contain at minimum:

| Column Name  | Description                |
| ------------ | -------------------------- |
| `Id`         | Salesforce Opportunity ID  |
| `StageName`  | Current sales stage        |
| `Vertical`   | Target industry / vertical |
| `Competitor` | Primary competitor         |

Additional fields can be included as needed.

---

### `guidance.json`

Structured by:

* Stage
* Vertical
* Competitor

Example structure:

```json
{
  "StageName": {
    "Vertical": {
      "Competitor": {
        "guidance": "...",
        "resources": ["..."]
      }
    }
  }
}
```

---

## 🛠 Installation & Local Development

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/riot-streamlit.git
cd riot-streamlit
```

### 2️⃣ Create Virtual Environment (Optional but Recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the App

```bash
streamlit run app.py
```

The app will launch at:

```
http://localhost:8501
```

---

## ☁ Deployment

This app is designed to be deployed via:

**Streamlit Community Cloud**

Deployment requires:

* GitHub repository connection
* `requirements.txt`
* `app.py` at repository root

---

## 🔐 Data Sensitivity

If `opportunities.csv` contains sensitive Salesforce data:

* The GitHub repository should be set to **Private**
* Alternatively, replace the CSV with a secure data source (database, API, S3, etc.)

---

## 📈 Future Enhancements (Roadmap Ideas)

* Authentication (restrict to internal users)
* Salesforce API integration (real-time data)
* LLM-powered dynamic guidance generation
* Resource filtering by deal size or region
* Analytics on most requested opportunity types

---

## 🧠 Purpose

RIOT exists to reduce friction in sales execution by delivering the right strategic insight at the right moment — directly within the workflow.

---

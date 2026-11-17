# NyayaSathi (न्याय साथी / ನ್ಯಾಯ ಸಾಥಿ)

**AI-Powered Multilingual Legal Guidance Assistant for India**  
*Built for FirstCommit '26 Hackathon*

---

## Overview

NyayaSathi makes Indian legal procedures and rights understandable for ordinary citizens. It uses Google's Gemini multimodal intelligence to analyze legal grievances across civil, criminal, consumer, tenancy, and cyber domains, providing:

- Relevant statutory citations (Bharatiya Nyaya Sanhita 2023, IPC, IT Act 2000, Consumer Protection Act 2019, etc.)
- Practical, sequential action plans
- Necessary evidence and documentation lists
- Contact details for official dispute resolution forums and free legal aid (NALSA/DLSA)

---

## Setup & Running

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Run the Application
```bash
streamlit run app.py
```

Access the interface in your browser at `http://localhost:8501`.

---

## Key Features

- **Conversational Legal Interface:** Natural-language interaction for everyday legal dilemmas.
- **Multilingual Understanding:** Supports queries in English, Hindi, and Kannada.
- **Verified Statutory Citations:** Direct mapping to enacted Indian legislation and statutory sections.
- **Emergency Directory:** Quick access to critical national helplines (1930, 112, 15100, 1915).

---

## Disclaimer

NyayaSathi provides educational and informational assistance. It does not provide formal legal representation or establish an advocate-client relationship. Citizens are encouraged to seek certified legal counsel for court proceedings.

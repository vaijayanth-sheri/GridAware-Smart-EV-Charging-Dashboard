# GridAware – Smart EV Charging Dashboard

**Developed by Vaijayanth Sheri | MIT License**

GridAware is a modern, intelligent web dashboard that empowers Electric Vehicle (EV) owners in Germany to make cost-optimal charging decisions using real-time electricity prices. By integrating the Awattar market API, GridAware delivers actionable, transparent insights, enabling users to maximize savings, efficiency, and confidence in their energy decisions.

This application is built with a focus on user control, data transparency, and professional-level accuracy.

---

### **Core Features**

*   **Live Market Prices:** On-demand fetching of hourly electricity prices from the Awattar Germany API. Data is never fetched automatically, giving the user full control.
*   **Data Visualization:** A clear, interactive bar chart displays the current and upcoming hourly prices (€/kWh), with full transparency on data source and update times.
*   **EV Charging Optimization:** A comprehensive configuration form allows users to specify their vehicle, battery state, charging preferences, and constraints.
*   **Smart Recommendation Engine:** Calculates the optimal charging start time to achieve the desired state of charge at the lowest possible cost, considering all user-defined parameters.
*   **Clear Results & Insights:** A detailed summary card, visual overlay on the price chart, and cost breakdown provide unambiguous, actionable recommendations.
*   **Persistent State:** Your EV configuration is saved within your browser session, so you don't have to re-enter it every time.
*   **Robust Error Handling:** The UI provides clear feedback for all states, including loading, successful fetches, API errors, or incomplete configurations.

---

### **Tech Stack**

*   **Backend:** Python 3.9+
*   **Frontend/UI:** Dash (v2.16+), Plotly (v5.22+), CSS3
*   **Data Processing:** Pandas
*   **API Communication:** Requests
*   **Data Source:** Awattar Germany API
*   **License:** MIT

---

### **How to Run Locally**

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/vaijayanth-sheri/GridAware-Smart-EV-Charging-Dashboard.git
    cd GridAware-Smart-EV-Charging-Dashboard
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    Make sure you have all the required packages by running:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application:**
    Execute the main application file:
    ```bash
    python app.py
    ```

5.  **Access the Dashboard:**
    Open your web browser and navigate to `http://127.0.0.1:8050`.

---

### **Project Structure**

The project is organized into a modular structure for clarity and maintainability:

### 📦 Dependencies
Main libraries used:

Dash: App framework\
Plotly: Interactive visualizations\
Pandas: Data processing

Requests: For API calls to Awattar

Awattar API: Free & open German electricity market data

### 🔐 Data Source
Awattar Germany API

Free to use, no API key required

Prices returned in EUR/MWh, converted to €/kWh inside the app

Data includes timestamps and granularity suitable for scheduling

## 💡 Roadmap (Upcoming Features)
Smart charging auto-scheduler (start/stop suggestions)

User account/profile memory (persistent configuration)

Solar panel output integration (based on system size & location)

CO₂ emission-aware charging decisions

Price alerts & notification system

👤 Author & Credits
Developed by vaijayanth Sheri as a prototype project focused on real-time energy intelligence and decision support systems.


Inspired by the goal of building accessible tools for the energy transition 🌍

### 📄 License
This project is open-sourced under the MIT License.

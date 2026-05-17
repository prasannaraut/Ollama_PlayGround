# Ollama Gemma 4 Web Search Chat Assistant

A modern, responsive, and robust Streamlit chat application powered by **Ollama (gemma4:e4b)** with an integrated **Web Search Tool**. This application retains chat history across active sessions and allows full configuration of runtime parameters via an interactive sidebar.

---

## 🚀 Features

* **gemma4:e4b Integration:** Seamless chat connectivity with Ollama running locally.
* **Live Web Search Tool:** Automatically triggers a live DuckDuckGo web search when queries demand real-time information or up-to-date data.
* **Active Session Memory:** Full context retention for consecutive follow-up questions.
* **Dynamic Configurations:** Configurable Ollama model names, API/Host URLs, and Temperature values directly from the UI.
* **Chat Reset:** Clear message buffers instantly with a dedicated "Reset Chat" action.

---

## 🛠️ Prerequisites

Before launching the application, ensure you have the following ready on your system:

1.  **Python 3.11 installed.
2.  **Ollama Desktop** installed and running locally.
3.  The desired model pulled down via your terminal:
    *(Note: If `gemma4:e4b` is not yet available on your Ollama server, you can type any valid model name directly into the application's sidebar input field at runtime).*

---

## 📦 Installation

1. **Clone or Download** the repository containing the `ai_assistant.py` script.
2. Navigate to the project directory and install the necessary dependencies using pip: `pip install streamlit ollama duckduckgo-search`
3. Run the application with command `streamlit run ai_assistant.py`
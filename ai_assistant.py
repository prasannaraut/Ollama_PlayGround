#ollama web_search api key == 694eecf2a5fa45168559b503e8c1ccc0.uYyBd4TLmDWdpzEMKS8VJZoG

import streamlit as st
import ollama
import json

st.set_page_config(
    page_title="Ollama Web Search Chat",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded"
)

def perform_web_search(query: str) -> str:
    """
    A tool function to perform live web searches.
    Uses duckduckgo-search to pull real-time internet data without needing a paid API key.
    """
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if not results:
                return "No search results found for the query."
            
            # Format the results for the LLM to read easily
            formatted_results = "\n\n".join(
                [f"Title: {r['title']}\nSnippet: {r['body']}\nLink: {r['href']}" for r in results]
            )
            return formatted_results
    except ImportError:
        return "Error: The 'duckduckgo-search' library is not installed. Please install it using `pip install duckduckgo-search` to enable web search."
    except Exception as e:
        return f"Web search failed due to an error: {str(e)}"

# This schema tells the Ollama model how and when it can use the web search capability.
OLLAMA_TOOLS = [{
    'type': 'function',
    'function': {
        'name': 'perform_web_search',
        'description': 'Search the internet for real-time, up-to-date information, news, or facts that you do not know.',
        'parameters': {
            'type': 'object',
            'properties': {
                'query': {
                    'type': 'string',
                    'description': 'The precise search query to look up on the web.'
                }
            },
            'required': ['query']
        }
    }
}]

with st.sidebar:
    st.title("⚙️ Settings")
    
    # Pre-populated inputs as requested
    api_key = st.text_input(
        "API Key", 
        value="694eecf2a5fa45168559b503e8c1ccc0.uYyBd4TLmDWdpzEMKS8VJZoG",
        help="Optional: If you are using a hosted Ollama instance that requires an authorization token."
    )
    
    ollama_model = st.text_input(
        "Ollama Model", 
        value="gemma4:e4b",
        help="The name of the Ollama model. Ensure you have pulled it via `ollama run <model_name>`."
    )
    
    base_url = st.text_input(
        "Ollama Base URL", 
        value="http://localhost:11434",
        help="The URL where your Ollama service is running."
    )
    
    temperature = st.slider(
        "Temperature", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.7, 
        step=0.1,
        help="Higher values make output more random, lower values make it more deterministic."
    )
    
    st.divider()
    
    # Button to clear the active session history
    if st.button("🗑️ Reset Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# This preserves the active session history across reruns
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🦙 Ollama Assistant")
st.caption(f"Powered by `{ollama_model}` with Web Search Capabilities")

# We skip rendering 'tool' role messages to keep the chat interface clean for the user.
for message in st.session_state.messages:
    if message["role"] != "tool":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# st.chat_input acts as both the text box and the submit button
if prompt := st.chat_input("Ask a question (e.g., 'What is AI?')..."):
    
    # 1. Display user message and append to session state
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Configure Ollama Client
    # Pass the API key in headers if the user modifies it for a secured remote server
    headers = {"Authorization": f"Bearer {api_key}"} if api_key and api_key != "sk-default-dummy-key" else {}
    client = ollama.Client(host=base_url, headers=headers)

    # 3. Generate Response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        try:
            with st.spinner("Thinking..."):
                # Initial call to Ollama (checking if it needs to use a tool)
                response = client.chat(
                    model=ollama_model,
                    messages=st.session_state.messages,
                    tools=OLLAMA_TOOLS,
                    options={"temperature": temperature}
                )
                
                assistant_message = response['message']
                
                if assistant_message.get('tool_calls'):
                    # Append the model's tool call request to the history
                    st.session_state.messages.append(assistant_message)
                    
                    for tool_call in assistant_message['tool_calls']:
                        if tool_call['function']['name'] == 'perform_web_search':
                            search_query = tool_call['function']['arguments']['query']
                            
                            # Show a temporary status indicator that we are searching the web
                            with st.status(f"🔍 Searching the web for: **{search_query}**"):
                                search_result = perform_web_search(search_query)
                                st.write("Search complete.")
                                
                            # Append the search results back to the history as a 'tool' message
                            st.session_state.messages.append({
                                'role': 'tool',
                                'content': search_result,
                                'name': 'perform_web_search'
                            })
                    
                    # Call Ollama again so it can read the web search results and formulate a final answer
                    with st.spinner("Reading search results..."):
                        final_response = client.chat(
                            model=ollama_model,
                            messages=st.session_state.messages,
                            options={"temperature": temperature}
                        )
                        
                        final_content = final_response['message']['content']
                        response_placeholder.markdown(final_content)
                        st.session_state.messages.append(final_response['message'])
                
                else:
                    final_content = assistant_message['content']
                    response_placeholder.markdown(final_content)
                    st.session_state.messages.append(assistant_message)
                    
        except ollama.ResponseError as e:
            st.error(f"Ollama Error: {str(e)}\n\nPlease check if Ollama is running and if the model '{ollama_model}' is downloaded.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
# OpenAI Chat Interface

This project provides a simple chat interface that interacts with the OpenAI API using Streamlit. Users can start a new chat, select an existing chat, and configure the GPT model parameters to generate responses from the model in a conversational context.

### Features

- Chat Management: Create new chats or select from existing ones.
- Model Configuration: Select from a list of GPT models and adjust parameters such as temperature and max tokens.
- Persistent Chat History: Chat histories are saved to a JSON file, allowing for persistence across sessions.
- Streamlit Interface: A user-friendly web interface built with Streamlit for easy interaction.

### Installation

Before you begin, ensure you have Python installed on your system. Then, follow these steps:

1. Clone the repository:

```
git clone https://github.com/fe-lipe-c/py_chat.git
cd py_chat
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Add your OpenAI API key the your .bashrc file:

```
export OPENAI_API_KEY="your-api-key"
```

### Usage

To run the chat interface, execute the following command in your terminal:

```
streamlit run chat_ui.py
```

This will start a local server and open the Streamlit web interface in your default web browser.

### Configuration

You can configure the following parameters from the Streamlit sidebar:

- Select a chat: Choose an existing chat or start a new one.
- Select a model: Choose the GPT model you want to use for generating responses.
- Temperature: Control the randomness of the model output.
- Max Tokens: Set the maximum length of the output message.

### Contributing

Contributions are welcome! Please feel free to submit a pull request or create an issue if you have any ideas, suggestions, or find any bugs.

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### References

- [Build a basic LLM chat app](https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps)
- [chatbot-ui](https://github.com/mckaywrigley/chatbot-ui)
- [chatgpt-streamlit](https://github.com/haiichuan/chatgpt-streamlit)



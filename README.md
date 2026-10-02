# Infinite Chat with Ollama - Qwen3:4B

An interactive terminal chat application that maintains persistent conversation context and history.

## Features

- ✅ **Persistent Memory**: Saves conversation history and context notes to files
- ✅ **Context Awareness**: Includes the last 2 messages in each API call for continuity
- ✅ **Resume Sessions**: Close and reopen the terminal—your conversation continues where you left off
- ✅ **Organized Notes**: Maintain a notes.txt file with conversation context
- ✅ **Streaming Responses**: Real-time response display from the AI
- ✅ **Session Management**: Clear, quit, or view notes with simple commands

## Requirements

```bash
pip install ollama
```

Ensure Ollama is running:
```bash
ollama serve
```

Ensure the model is available:
```bash
ollama run qwen3:4b
```

## Usage

```bash
python chat.py
```

### Commands

- **Type your message** → Chat with the AI
- **`quit`** → Exit and save the conversation
- **`clear`** → Reset all conversation history and context
- **`notes`** → View your current context notes

## File Structure

- **conversation_context.txt** - Human-readable notes and context
- **conversation_data.json** - Structured data (context, history, timestamp)

## How It Works

1. **On startup**: Loads previous context and conversation history
2. **During chat**: Includes last 2 messages + context with each API call
3. **On exit**: Automatically saves all context and history
4. **Resume**: Close terminal, reopen, and continue from where you left off

## Example Session

```
You: What's the capital of France?
AI: The capital of France is Paris...

[Close terminal and reopen later]

You: What about Germany?
AI: The capital of Germany is Berlin. [AI remembers Paris conversation]
```

## Notes

- The script keeps the last 10 messages in memory for API efficiency
- Context persists separately from chat history
- All data is automatically saved after each message
- Ctrl+C also saves and exits gracefully

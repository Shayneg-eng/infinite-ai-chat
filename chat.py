from ollama import chat
import os
import json
from datetime import datetime

NOTES_FILE = "conversation_context.txt"
DATA_FILE = "conversation_data.json"

def load_context():
    """Load previous context and conversation history from files"""
    context = ""
    history = []
    
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r') as f:
            context = f.read()
    
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                history = data.get('history', [])
                if context == "":  # Only use saved context if notes file doesn't exist
                    context = data.get('context', "")
        except:
            pass
    
    return context, history

def save_context(context, history):
    """Save context and conversation history to files"""
    # Save readable notes file
    with open(NOTES_FILE, 'w') as f:
        f.write(context)
    
    # Save structured data file
    data = {
        'context': context,
        'history': history,
        'last_updated': datetime.now().isoformat()
    }
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_last_two_messages(history):
    """Get the last 2 messages from history for context"""
    if len(history) == 0:
        return ""
    
    messages_text = "\n--- Last 2 Messages ---\n"
    start_idx = max(0, len(history) - 2)
    
    for msg in history[start_idx:]:
        messages_text += f"{msg['role'].upper()}: {msg['content']}\n"
    
    messages_text += "---\n"
    return messages_text

def build_system_context(context, history):
    """Build the system context including notes and last 2 messages"""
    system_msg = "You are a helpful AI assistant. "
    
    if context:
        system_msg += f"\n\nPrevious context and notes:\n{context}\n"
    
    if history:
        last_two = get_last_two_messages(history)
        system_msg += f"\n{last_two}"
    
    return system_msg

def main():
    print("=" * 60)
    print("INFINITE CHAT WITH OLLAMA - QWEN3:4B")
    print("=" * 60)
    
    # Load context and history
    context, history = load_context()
    
    if context:
        print("\n📝 LOADED CONTEXT:")
        print(context[:300] + ("..." if len(context) > 300 else ""))
    
    if history:
        print(f"\n💬 LOADED {len(history)} PREVIOUS MESSAGES")
        print("Last 2 messages:")
        for msg in history[-2:]:
            print(f"  {msg['role'].upper()}: {msg['content'][:60]}...")
    
    print("\n" + "=" * 60)
    print("Type 'quit' to exit | Type 'clear' to reset | Type 'notes' to view context")
    print("=" * 60 + "\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'quit':
                print("Saving conversation... Goodbye!")
                save_context(context, history)
                break
            
            if user_input.lower() == 'clear':
                context = ""
                history = []
                save_context(context, history)
                print("✓ Conversation cleared!")
                continue
            
            if user_input.lower() == 'notes':
                print("\n" + "=" * 40)
                print("CURRENT CONTEXT NOTES:")
                print("=" * 40)
                print(context if context else "(No notes yet)")
                print("=" * 40 + "\n")
                continue
            
            if not user_input:
                continue
            
            # Add user message to history
            history.append({'role': 'user', 'content': user_input})
            
            # Keep only last 10 messages in history (for API efficiency)
            if len(history) > 10:
                history = history[-10:]
            
            print("\n🤖 AI: ", end="", flush=True)
            
            # Build messages for API call
            messages = []
            
            # Add context if it exists
            if context:
                messages.append({'role': 'system', 'content': f"Context and notes:\n{context}"})
            
            # Add last 2 messages for continuity
            if len(history) > 1:
                messages.extend(history[-3:-1])  # Last 2 before current
            
            # Add current user message
            messages.append({'role': 'user', 'content': user_input})
            
            # Get response
            response = chat(
                model='qwen3:4b',
                messages=messages,
                stream=True
            )
            
            full_response = ""
            for chunk in response:
                content = chunk.get('message', {}).get('content', '')
                print(content, end="", flush=True)
                full_response += content
            
            print("\n")
            
            # Add AI response to history
            history.append({'role': 'assistant', 'content': full_response})
            
            # Save after each interaction
            save_context(context, history)
            
        except KeyboardInterrupt:
            print("\n\nSaving conversation... Goodbye!")
            save_context(context, history)
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Make sure Ollama is running with: ollama serve")
            print("And the model is available: ollama run qwen3:4b\n")

if __name__ == "__main__":
    main()

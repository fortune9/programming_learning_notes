# Ollama Tutorial

## Introduction

### What is Ollama?

Ollama is the easiest way to get up and running with large language models (LLMs) locally on your computer. It provides a simple command-line interface and API to run powerful open-source models like GPT-OSS, Gemma 4, DeepSeek-R1, Qwen3, and many others without needing extensive machine learning knowledge or cloud API keys.

### Main Use Cases

- **Local AI Development**: Run LLMs locally for development and testing without API costs
- **Privacy**: Keep your data on your machine - nothing is sent to external servers (when using local models)
- **AI Tool Integration**: Power AI assistants, coding tools, and applications with local or cloud models
- **Experimentation**: Easily try different models and compare their capabilities
- **API Development**: Build applications that integrate with LLMs using a simple REST API

### Prerequisites

- **Operating System**: macOS, Windows, or Linux
- **Hardware**:
  - Minimum 8GB RAM (16GB+ recommended)
  - For larger models, a GPU is beneficial but not required
- **Disk Space**: Several GB for models (varies by model size)

---

## Installation & Setup

### Installation

Visit [https://ollama.com/download](https://ollama.com/download) and download the installer for your operating system.

**macOS/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download and run the Windows installer from the website.

### Verify Installation

After installation, verify Ollama is working:

```bash
ollama --version
```

The Ollama service should start automatically. If not, run:

```bash
ollama serve
```

---

## Key Concepts

| Concept | Description | Example |
|---------|-------------|---------|
| **Model** | A pre-trained language model you can run locally | `gemma4`, `gpt-oss`, `qwen3` |
| **Prompt** | The input text you send to the model | `"Why is the sky blue?"` |
| **Run** | Execute a model interactively or with a single prompt | `ollama run gemma4` |
| **Pull** | Download a model from the Ollama library | `ollama pull gemma4` |
| **Modelfile** | Configuration file to customize or create models | Similar to Dockerfile |
| **Cloud Models** | Larger models that run on Ollama's servers | Models ending in `-cloud` |
| **Integration/Launch** | Configure external tools to use Ollama | `ollama launch claude` |

---

## Key CLI Commands

| Command | Purpose | Example | Notes |
|---------|---------|---------|-------|
| `ollama` | Launch interactive menu to select models/assistants | `ollama` | Use arrow keys to navigate |
| `ollama run <model>` | Run a model interactively | `ollama run gemma4` | Starts chat session |
| `ollama run <model> "<prompt>"` | Run model with single prompt | `ollama run gemma4 "Hello!"` | One-shot execution |
| `ollama pull <model>` | Download a model | `ollama pull gemma4` | Required before first use |
| `ollama ls` | List downloaded models | `ollama ls` | Shows local models only |
| `ollama rm <model>` | Delete a model | `ollama rm gemma4` | Frees up disk space |
| `ollama ps` | List currently running models | `ollama ps` | Shows active models |
| `ollama stop <model>` | Stop a running model | `ollama stop gemma4` | Frees up memory |
| `ollama launch` | Launch interactive integration menu | `ollama launch` | Select AI assistants/tools |
| `ollama launch <integration>` | Launch a specific AI tool | `ollama launch claude` | Auto-configures tool |
| `ollama signin` | Sign in to your Ollama account | `ollama signin` | Required for cloud models |
| `ollama signout` | Sign out of Ollama | `ollama signout` | |
| `ollama create -f <file>` | Create custom model from Modelfile | `ollama create -f Modelfile` | For advanced customization |
| `ollama serve` | Start the Ollama service | `ollama serve` | Usually auto-starts |

---

## Full Working Examples

### Example 1: First Time Setup and Chat

```bash
# Download a model (first time only)
ollama pull gemma4

# Start an interactive chat session
ollama run gemma4

# Now you can chat:
>>> What is the capital of France?
The capital of France is Paris.

>>> /bye
# Use /bye to exit the chat
```

### Example 2: One-Shot Commands

```bash
# Single question without interactive mode
ollama run gemma4 "Explain what Ollama is in one sentence"

# Analyze an image (for vision models)
ollama run gemma4 "What's in this image? /home/user/photo.png"
```

### Example 3: Launching AI Assistants

```bash
# Interactive menu - navigate with arrow keys
ollama

# Launch specific assistants
ollama launch openclaw      # Personal AI assistant
ollama launch claude        # Claude Code IDE integration
ollama launch codex         # Codex coding assistant

# Launch with specific model
ollama launch openclaw --model gemma4

# Just configure without launching
ollama launch vscode --config
```

### Example 4: Using Ollama Cloud

Cloud models provide access to larger, more powerful models without requiring local GPU resources.

```bash
# Sign in to Ollama (required for cloud)
ollama signin

# Run a large cloud model
ollama run gpt-oss:120b-cloud

# Check available cloud models at:
# https://ollama.com/search?c=cloud
```

### Example 5: API Usage

Ollama runs a local API server on `http://localhost:11434` that you can call from any programming language.

**Using curl:**
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "gemma4",
  "messages": [
    { "role": "user", "content": "Hello!" }
  ]
}'
```

**Using Python:**
```python
# First install: pip install ollama
import ollama

# Simple chat
response = ollama.chat(model='gemma4', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])
```

**Using JavaScript:**
```javascript
// First install: npm install ollama
import ollama from 'ollama'

const response = await ollama.chat({
  model: 'gemma4',
  messages: [{ role: 'user', content: 'Why is the sky blue?' }],
})
console.log(response.message.content)
```

### Example 6: Model Management

```bash
# List all downloaded models
ollama ls

# Check running models
ollama ps

# Download multiple models
ollama pull gemma4
ollama pull qwen3
ollama pull deepseek-r1

# Remove unused models to free space
ollama rm old-model

# Stop a running model to free memory
ollama stop gemma4
```

---

## Cloud Features

Ollama Cloud allows you to run larger models that may not fit on your local machine or require more computational power.

### Key Differences: Local vs Cloud

| Feature | Local | Cloud |
|---------|-------|-------|
| **Model Size** | Limited by your hardware | Access to 120B+ parameter models |
| **GPU Required** | Recommended for larger models | Not required |
| **Privacy** | Data stays on your machine | Data sent to Ollama servers |
| **Cost** | Free (uses your hardware) | Free tier + paid plans available |
| **Speed** | Depends on your hardware | Consistent fast performance |
| **Internet** | Not required | Required |

### Using Cloud Models

```bash
# 1. Sign in (one-time setup)
ollama signin

# 2. Run a cloud model (note the -cloud suffix)
ollama run gpt-oss:120b-cloud

# 3. For API access, create an API key at:
# https://ollama.com/settings/keys

# 4. Set your API key for programmatic access
export OLLAMA_API_KEY=your-api-key-here

# 5. Use the cloud API endpoint
curl https://ollama.com/api/chat -d '{
  "model": "gpt-oss:120b-cloud",
  "messages": [{"role": "user", "content": "Hello"}]
}' -H "Authorization: Bearer $OLLAMA_API_KEY"
```

### Cloud Pricing

- **Free**: Included with Ollama account
- **Pro ($20/month)**: 50x more cloud usage, run 3 models simultaneously
- **Max ($100/month)**: 5x more than Pro, run 10 models simultaneously

---

## Common Patterns & Best Practices

### 1. Start Small, Scale Up

```bash
# Start with smaller, faster models
ollama run gemma4

# Once comfortable, try larger models
ollama run gpt-oss:120b-cloud
```

### 2. Manage Disk Space

```bash
# Regularly check downloaded models
ollama ls

# Remove models you no longer use
ollama rm unused-model

# Only pull models when you need them
```

### 3. Stop Models to Free Memory

```bash
# Check what's running
ollama ps

# Stop models you're not using
ollama stop gemma4
```

### 4. Use the Right Model for the Task

- **Fast Q&A**: `gemma4` (smaller, faster)
- **Complex reasoning**: `gpt-oss:120b-cloud` (larger, slower)
- **Coding**: Specialized coding models like `deepseek-coder`
- **Vision tasks**: Models with vision support

### 5. API Integration Best Practices

```python
# Always handle errors when using the API
import ollama

try:
    response = ollama.chat(
        model='gemma4',
        messages=[{'role': 'user', 'content': 'Hello'}]
    )
    print(response['message']['content'])
except ollama.ResponseError as e:
    print(f'Error: {e.error}')
```

### 6. Model Selection Tips

```bash
# Browse available models
# Visit: https://ollama.com/search

# Check model details before downloading
# Model names usually indicate size:
# - gemma4:7b (7 billion parameters - smaller, faster)
# - gpt-oss:120b (120 billion parameters - larger, more capable)
```

### 7. Environment Variables

```bash
# Customize Ollama behavior
export OLLAMA_HOST=0.0.0.0:11434    # Listen on all interfaces
export OLLAMA_MODELS=/custom/path   # Custom model storage location

# View all environment variables
ollama serve --help
```

### 8. Common Pitfalls to Avoid

- **Don't download too many large models** - They consume significant disk space
- **Don't forget to sign in for cloud models** - Required for `-cloud` models
- **Don't assume local models are internet-free** - Some features may require connectivity
- **Check model compatibility** - Not all models support all features (e.g., vision)

---

## References & Further Reading

### Official Documentation
- **Main Documentation**: https://docs.ollama.com/
- **Quickstart Guide**: https://docs.ollama.com/quickstart
- **CLI Reference**: https://docs.ollama.com/cli
- **API Reference**: https://docs.ollama.com/api/introduction
- **Cloud Documentation**: https://docs.ollama.com/cloud
- **Complete Documentation Index**: https://docs.ollama.com/llms.txt

### Official Libraries
- **Python Library**: https://github.com/ollama/ollama-python
- **JavaScript Library**: https://github.com/ollama/ollama-js
- **Community Libraries** (20+): Available on the documentation site

### Model Resources
- **Browse Models**: https://ollama.com/search
- **Cloud Models**: https://ollama.com/search?c=cloud
- **Download Ollama**: https://ollama.com/download

### Community
- **Discord**: Join the Ollama Discord community for support
- **Reddit**: r/ollama for discussions and tips
- **GitHub**: https://github.com/ollama for issues and contributions

### Additional Resources
- **Model Customization**: Learn about Modelfiles for creating custom models
- **Integration Guides**: Documentation for Claude Code, VS Code, and other tools
- **API Examples**: More examples in Python, JavaScript, and other languages

---

## Quick Reference Card

```bash
# Essential Commands
ollama                                    # Interactive menu
ollama run <model>                        # Start chat with model
ollama pull <model>                       # Download model
ollama ls                                 # List models
ollama ps                                 # List running models
ollama signin                             # Sign in for cloud

# API Testing
curl http://localhost:11434/api/chat -d '{
  "model": "gemma4",
  "messages": [{"role": "user", "content": "Hi"}]
}'

# Launch Assistants
ollama launch                             # Interactive launch menu
ollama launch claude                      # Launch Claude Code
ollama launch openclaw                    # Launch OpenClaw

# Model Management
ollama stop <model>                       # Stop model
ollama rm <model>                         # Remove model
```

Happy learning with Ollama!

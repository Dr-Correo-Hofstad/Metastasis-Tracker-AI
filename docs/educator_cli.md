# Setup and Usage Guide: Metastasis-Tracker Educator AI

Welcome to the official documentation for the **Metastasis-Tracker Educator AI** CLI tool. This command-line interface acts as both a clinical tutor for medical staff and an architectural assistant for the Revolutionary Technology software team.

By reading the `docs/` directory of the Metastasis-Tracker-AI repository, the AI dynamically learns the specific fluid dynamics, WBE scaling algorithms, and biological behaviors of the marine variant species to provide highly contextual answers and documentation.

---

## 1. Prerequisites & Installation

Before running the CLI, ensure your environment has Python installed. Then, install the required packages:

```

Code output

```
File created successfully.

```bash
pip install typer rich google-genai

```

2\. API Key Configuration (The `export` Command)
------------------------------------------------

To power the AI, the tool relies on Google's Gemini models. The script requires a secure "key" to authenticate your terminal with Google's servers.

You must set this key as an **Environment Variable**.

### What does `export GEMINI_API_KEY="your_api_key_here"` actually do?

When you type this command into your terminal, you are creating a temporary system variable named `GEMINI_API_KEY`.

-   **Security:** Instead of pasting your secret API key directly into the Python code (where it could be accidentally uploaded to GitHub or stolen), you store it safely in your terminal's memory.

-   **Access:** When `educator_cli.py` runs, the `google-genai` library automatically searches your terminal's environment variables for this specific key to authorize the AI requests.

### How to set it up:

**For macOS / Linux (AlmaLinux/CentOS servers):**

Run this directly in your terminal before running the script:

Bash

```
export GEMINI_API_KEY="your_actual_api_key_string"

```

*(To make this permanent across reboots, add the line above to the bottom of your `~/.bashrc` or `~/.zshrc` file).*

**For Windows (Command Prompt):**

DOS

```
set GEMINI_API_KEY="your_actual_api_key_string"

```

**For Windows (PowerShell):**

PowerShell

```
$env:GEMINI_API_KEY="your_actual_api_key_string"

```

3\. Preparing the Knowledge Base
--------------------------------

The AI requires context to function correctly. Ensure your root directory looks like this:

Plaintext

```
Metastasis-Tracker-AI/
├── educator_cli.py
└── docs/
    ├── patient_anatomy.py
    ├── state_matrix.json
    ├── target_proteins.py
    └── ... (any other equations, scripts, or notes)

```

*Note: The AI will automatically read any `.py`, `.md`, `.txt`, or `.json` file placed in the `docs/` folder to build its internal knowledge base before answering a prompt.*

4\. Command Reference
---------------------

The CLI features three primary commands tailored for clinical oncology and software engineering.

### A. The `teach` Command

Use this to interactively question the AI about complex mathematical or biological concepts. Excellent for quick verifications or explaining mechanics to medical students.

**Syntax:**

Bash

```
python educator_cli.py teach "<your question>"

```

**Example:**

Bash

```
python educator_cli.py teach "Explain how Starling forces affect the variant species when it reaches a Generation 30 capillary bed."

```

### B. The `suggest` Command

Use this to generate high-level architectural feedback for the software engineering team. The AI will audit the files in `docs/` and propose optimizations for traversal efficiency, data recovery fail-safes, and payload transmission.

**Syntax:**

Bash

```
python educator_cli.py suggest

```

*Output:* Automatically generates a formatted Markdown file in `docs/suggestions/`.

### C. The `build-training` Command

Use this to draft formal, academic medical curriculum. It synthesizes your equations and physics models into a structured study guide complete with a diagnostic quiz.

**Syntax:**

Bash

```
python educator_cli.py build-training --topic "<Specific Topic>"

```

**Example:**

Bash

```
python educator_cli.py build-training --topic "pH-Driven Enzyme Activation and Vesicle Calcification"

```

*Output:* Automatically generates a clinical study guide in `docs/training/`.

"""

with open("Metastasis_Educator_AI_Guide.md", "w", encoding="utf-8") as f:

f.write(markdown_content)

print("File created successfully.")

```
Your Markdown file is ready
[file-tag: code-generated-file-0-1782172319591359188]

The guide provides a comprehensive breakdown of the CLI functionality and a clear, non-jargon explanation of how environment variables protect your Revolutionary Technology server environments by keeping hardcoded credentials out of the codebase. It also outlines exactly how to structure the `docs/` folder so the AI has the proper context regarding the variant species and fluid matrices before it attempts to generate curriculum or architectural suggestions.

```

*This project has been created as part of the 42 curriculum by alebaron.*

# Call Me Maybe: Introduction to Large Language Models (LLM)

## Description

**Call Me Maybe** is a learning project on "function calling" with Large Language Models (LLM). Rather than asking the model directly to generate an answer, this project trains the LLM to:

1. **Identify the appropriate function** to call from a predefined list
2. **Generate the correct parameters** for that function
3. **Return the result** in structured JSON format

### Use cases

- **Conversational AI assistants**: Allow chatbots to decide which APIs to call
- **Automation systems**: Transform instructions into precise actions
- **Tool integration**: Connect LLMs with external services (calculators, databases, etc.)

## Installation

```bash
# Clone the project
git clone https://github.com/alizealebaron/call_me_maybe.git
cd call_me_maybe

# Install dependencies
uv sync
# Or with the makefile
make install
```

### Makefile Commands

```bash
# Installs dependencies and creates an environment
make install

# Launches the program
make run

# Checks and returns strict norm errors
make lint-strict

# Checks and returns norm errors
make lint

# Cleans files created by python
make clean

# Launches a test environment
make debug
```

### Basic Execution

```bash
# Use default files
uv run python -m src
# Or with the makefile
make run

# Result: data/output/function_calling_results.json
cat data/output/function_calling_results.json
```

### Custom Execution

```bash
# With custom files
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/custom_results.json
```

### Example Files

**Input** (`data/input/function_calling_tests.json`) :
```json
[
  {
    "prompt": "What are Palkia's weaknesses ?"
  }
  ...
]
```

**Function Definitions** (`data/input/functions_definition.json`) :
```json
[
  {
    "name": "fn_find_weakness",
    "description": "Find Pokémon's type weaknesses",
    "parameters": {
      "pokemon": {
        "type": "string"
      }
    },
    "returns": {
      "type": "string"
    }
  }
  ...
]
```

**Output** (`data/output/function_calling_results.json`) :
```json
[
  {
    "prompt": "What are Palkia's weaknesses ?",
    "name": "fn_find_weakness",
    "parameters": {
      "pokemon": "Palkia",
    }
  }
  ...
]
```

## Code Architecture

### File Tree
```
call_me_maybe/
├── pyproject.toml            # Configuration file
├── Makefile                  # Command automation
├── README.md                 # Project explanations in English
├── README_EN.md              # Project explanations in English
└── src/
    ├── algorithm/          
    │   └── calling_llm.py    # Call to the LLM
    ├── models/
    │   ├── functionModel.py  # Function model
    │   └── promptModel.py    # Prompt models
    ├── parsing/            
    │   ├── parsing_args.py   # Parse passed arguments
    │   ├── parsing_json.py   # Retrieve JSON data
    │   └── parsing_name.py   # Retrieve name and output folder
    ├── utils/              
    │   └── error.py          # Error handling
    └── __main__.py           # Program entry point
```

## Algorithm Explanation: Constrained Decoding

### Fundamental Concept

Constrained decoding is a technique that forces the LLM to generate only from a predefined set of valid tokens. Instead of letting the model generate any token, we mask the logits (probability scores) of invalid tokens, making them impossible to select.

### Algorithm for Function Name Generation

```python
1. For each position in the function name:
   a. Retrieve the LLM logits
   b. Calculate valid tokens:
      - For each available function
      - If the function starts with the text generated so far
      - The next token of the name is valid
   c. Mask the logits:
      - All invalid tokens → -∞
      - All valid tokens → their original logit
   d. Select the best valid token (argmax)
   e. Add the token to the output
   f. Stop if a complete name is found
```

**Concrete example** :
```
Available functions: [fn_add_numbers, fn_greet, fn_reverse_string]

Initial generated prompt: "function name: "

Step 1 (First token):
  - Masked logits for tokens: ['f', 'g', 'r']
  - Best: 'f' (very likely for "fn_")
  - Output: "f"

Step 2 (Second token):
  - Masked logits to continue as "fn_"
  - Best: 'n'
  - Output: "fn"

... (continues until a complete name is detected)
```

### Algorithm for Parameter Generation

#### For numeric parameters

```python
1. Valid set = {'-', '0'-'9', '.', '\n'}
2. Loop until max_tokens or '\n' encountered:
   a. Masked logits for numeric characters
   b. Select the best valid token
   c. Validate numeric rules:
      - Maximum 1 decimal point
      - Maximum 1 minus, at the beginning only
   d. If invalid: reject this token
   e. If '\n' encountered: extract and convert to float
3. Return the validated float
```

#### For string parameters

```python
1. No logits masking (all tokens allowed)
2. Loop until max_tokens:
   a. Get the best token (normal argmax)
   b. Add to output
   c. Stop if:
      - Stop character encountered ('\n', multiple spaces, etc.)
      - Empty token
3. Clean and return the string
```

## Challenges Faced and Solutions

### Challenge 1: Model Hallucinations

**Problem** :
```
Input: "Call the function..."
Output: "call the function I imagine"
        (non-existent function)
```

**Implemented Solution** :
```python
# Mask all tokens except valid ones
logits_masked = np.full_like(logits, -np.inf)
for token_id in valid_tokens:
    logits_masked[token_id] = logits[token_id]
```

---

### Challenge 2: Infinite Token Generation

**Problem** :
```
Infinite loop if no clear stopping condition
Execution time becomes huge
```

**Implemented Solution** :
- Max tokens per phase (20 for function, 100 for string params)
- Detection of special stop characters
- Rejection of empty tokens

---

### Challenge 3: Misunderstood Tokenization

**Problem** :
```
LLM sometimes encodes "fn_add" as 1 token
But sometimes as 4 tokens: ['f', 'n', '_', 'add']
Inconsistency creates errors
```

**Implemented Solution** :
```python
# Flatten all tokens
token_seq = [t for sublist in encoding for t in sublist]
# Ensure consistency
```

## Resources

### Help with JSON Usage

- [Parse JSON data with Python](https://brightdata.fr/blog/savoir-faire/parse-json-data-with-python)
- [Using JSON with Python](https://www.docstring.fr/glossaire/json/)

## Understanding LLMs

- [What is an LLM?](https://www.cloudflare.com/learning/ai/what-is-large-language-model/)
- [Messages and special tokens](https://huggingface.co/learn/agents-course/unit1/messages-and-special-tokens)

### Other Call Me Maybe Projects

- [shadox254's project](https://github.com/shadox254/Call-Me-Maybe)
- [Sousampere's project](https://github.com/sousampere/42_call_me_maybe_v1.2)

### AI Usage in This Project

1. **Algorithm (calling_llm.py)**
   - Simplified explanation of the principle to implement
   - Generation of pseudo code to illustrate the explanation
   - Debugging infinite loops

2. **Checking Norm**
   - Correction of mypy errors found

3. **Documentation and Comments**
   - Generation of certain docstrings and class documentation
   - Correction of spelling errors and reformulation

# AgentLogger CLI

The AgentLogger CLI is a command-line tool that allows you to interact with the AgentLogger API directly from your terminal. It provides commands for analyzing code, fixing issues, explaining errors, and generating patches.

## Installation

### Using pip

```bash
pip install agent-logger-cli
```

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger

# Install the CLI
pip install -e cli/
```

## Configuration

Before using the CLI, you need to configure it with your API key:

```bash
agent-logger configure --api-key YOUR_API_KEY
```

By default, the CLI will connect to the AgentLogger API at `http://localhost:8000`. If you want to use a different API endpoint, you can specify it during configuration:

```bash
agent-logger configure --api-key YOUR_API_KEY --api-url https://api.yourdomain.com
```

Configuration settings are stored in `~/.agentlogger/config.json`.

## Commands

### analyze

Analyze a file for issues:

```bash
agent-logger analyze path/to/file.py
```

Options:
- `--language`: Specify the language of the file (default: auto-detect)
- `--output`: Output format (json, text, default: text)
- `--save`: Save the analysis to a file

Example:
```bash
agent-logger analyze buggy.py --output json --save analysis.json
```

### fix

Fix issues in a file:

```bash
agent-logger fix path/to/file.py
```

Options:
- `--language`: Specify the language of the file (default: auto-detect)
- `--analysis-id`: Use a specific analysis ID
- `--output`: Output format (json, text, default: text)
- `--save`: Save the fixed code to a file
- `--apply`: Apply the fixes to the original file

Example:
```bash
agent-logger fix buggy.py --apply
```

### explain

Get an explanation for an error message:

```bash
agent-logger explain "TypeError: cannot unpack non-iterable int object" --file path/to/file.py
```

Options:
- `--file`: File containing the code that generated the error
- `--language`: Specify the language of the file (default: auto-detect)
- `--level`: Explanation level (beginner, intermediate, advanced, default: intermediate)
- `--output`: Output format (json, text, default: text)

Example:
```bash
agent-logger explain "ZeroDivisionError: division by zero" --file divide.py --level beginner
```

### patch

Generate a patch for a file:

```bash
agent-logger patch path/to/file.py --issue "Division by zero error"
```

Options:
- `--issue`: Description of the issue to fix
- `--language`: Specify the language of the file (default: auto-detect)
- `--output`: Output format (json, text, default: text)
- `--save`: Save the patch to a file
- `--apply`: Apply the patch to the original file

Example:
```bash
agent-logger patch buggy.py --issue "Fix division by zero error" --apply
```

### github

Create a GitHub pull request with fixes:

```bash
agent-logger github path/to/file.py --issue "Fix division by zero error"
```

Options:
- `--issue`: Description of the issue to fix
- `--repo`: GitHub repository in the format `owner/repo`
- `--branch`: Branch name for the fix (default: `fix/agentlogger-{timestamp}`)
- `--title`: Pull request title
- `--description`: Pull request description

Example:
```bash
agent-logger github buggy.py --issue "Fix division by zero error" --repo yourusername/yourrepo
```

### version

Display the CLI version:

```bash
agent-logger version
```

### help

Display help information:

```bash
agent-logger help
```

Or for a specific command:

```bash
agent-logger help analyze
```

## Examples

### Analyze a Python File

```bash
agent-logger analyze buggy.py
```

Output:
```
Issues found in buggy.py:

1. ZeroDivisionError: Division by zero at line 4
   Code: result = divide(10, 0)
   Severity: Critical
   Description: The function 'divide' is called with a second argument of 0, which will cause a division by zero error.

2. Unused variable: 'result' is defined but never used
   Code: result = divide(10, 0)
   Severity: Warning
   Description: The variable 'result' is assigned a value but never used in the code.

Run 'agent-logger fix buggy.py' to generate fixes for these issues.
```

### Fix a Python File

```bash
agent-logger fix buggy.py --apply
```

Output:
```
Fixed code has been applied to buggy.py

Fixes applied:

1. Added check for zero divisor in divide function
   Before: def divide(a, b):
               return a / b
   After:  def divide(a, b):
               if b == 0:
                   return "Cannot divide by zero"
               return a / b

2. Used the result variable
   Before: result = divide(10, 0)
   After:  result = divide(10, 0)
           print(f"Result: {result}")

Original file has been backed up to buggy.py.bak
```

### Get an Explanation for an Error

```bash
agent-logger explain "ZeroDivisionError: division by zero" --file divide.py --level beginner
```

Output:
```
Explanation for ZeroDivisionError: division by zero (Beginner level)

What happened:
You tried to divide a number by zero, which is not allowed in mathematics.

Why it's a problem:
In mathematics, division by zero is undefined. When you try to divide any number by zero in Python, it raises a ZeroDivisionError.

In your code:
The error occurred at line 4: result = divide(10, 0)
You're calling the divide function with 10 and 0 as arguments. Inside the function, it tries to return a / b, which is 10 / 0, causing the error.

How to fix it:
Add a check in your divide function to handle the case when b is zero:

def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b

Or change the call to divide(10, 0) to use a non-zero value for the second argument:

result = divide(10, 5)
```

### Generate a Patch

```bash
agent-logger patch buggy.py --issue "Fix division by zero error" --save patch.diff
```

Output:
```
Patch has been saved to patch.diff

The patch fixes the division by zero error by adding a check in the divide function:

--- buggy.py
+++ buggy.py
@@ -1,4 +1,6 @@
 def divide(a, b):
+    if b == 0:
+        return "Cannot divide by zero"
     return a / b

 result = divide(10, 0)
```

## Exit Codes

The CLI uses the following exit codes:

- `0`: Success
- `1`: General error
- `2`: Configuration error
- `3`: API error
- `4`: File error
- `5`: Network error

## Environment Variables

The CLI supports the following environment variables:

- `AGENTLOGGER_API_KEY`: API key for authentication
- `AGENTLOGGER_API_URL`: URL of the AgentLogger API
- `AGENTLOGGER_OUTPUT`: Default output format (json, text)
- `AGENTLOGGER_GITHUB_TOKEN`: GitHub token for GitHub integration

Example:
```bash
export AGENTLOGGER_API_KEY=your-api-key
export AGENTLOGGER_API_URL=https://api.yourdomain.com
agent-logger analyze buggy.py
```

## Troubleshooting

### API Connection Issues

If you're having trouble connecting to the API, check your configuration:

```bash
cat ~/.agentlogger/config.json
```

You can reset your configuration:

```bash
agent-logger configure --reset
```

### Authentication Issues

If you're seeing authentication errors, make sure your API key is correct:

```bash
agent-logger configure --api-key YOUR_API_KEY
```

### File Issues

If the CLI can't read your file, check the file permissions:

```bash
chmod 644 path/to/file.py
```

## Conclusion

The AgentLogger CLI provides a convenient way to interact with the AgentLogger API from your terminal. It's designed to be easy to use and integrate into your development workflow.

For more information about the AgentLogger API, see the [API Documentation](../api/index.md). 
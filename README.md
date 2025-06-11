# SlidesGPT

SlidesGPT is a command-line tool that converts plain text into presentation slides using Google's Gemini AI. It generates well-structured markdown and converts it to PowerPoint presentations.

## Features

- Convert text to presentation slides using AI
- Automatic markdown generation
- PowerPoint (.pptx) output
- Support for custom PowerPoint templates
- Progress feedback and error handling

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Internet connection

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SlidesGPT.git
cd SlidesGPT
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Google Gemini API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

### Basic Usage

Generate slides from text input:
```bash
python -m src.cli generate --text "Your presentation content here" --output presentation.pptx
```

Generate slides from a text file:
```bash
python -m src.cli generate --input your_content.txt --output presentation.pptx
```

### Command Options

- `--text`, `-t`: Direct text input for the presentation
- `--input`, `-i`: Input file path containing the presentation content
- `--output`, `-o`: Output file path (will be saved as .pptx)

### Custom Templates

You can use a custom PowerPoint template by placing a `template.pptx` file in the project root directory. The generated presentation will use this template's styling.

## Example

```bash
# Generate a presentation about Python
python -m src.cli generate --text "Introduction to Python Programming. Python is a high-level programming language. It is known for its simplicity and readability. Python has a large standard library. It is widely used in web development, data science, and AI." --output python_intro.pptx
```

## Output

The program generates two files:
1. A markdown file (`.md`) with the structured content
2. A PowerPoint presentation (`.pptx`) converted from the markdown

## Error Handling

The program provides clear error messages for common issues:
- Missing API key
- Invalid input
- Conversion errors
- Missing required elements in the generated content

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
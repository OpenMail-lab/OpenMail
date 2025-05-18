#!/bin/bash
echo "🔹 Building OpenMail as an installable application..."

# Convert Python code into a standalone executable
pip install pyinstaller
pyinstaller --onefile --windowed --name "OpenMail-App" main.py

echo "✅ Build complete! Find your OpenMail executable inside 'dist/'"

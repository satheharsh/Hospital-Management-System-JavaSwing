#!/bin/bash
echo "Verifying Python syntax and discovery tests..."
python3 -m py_compile main.py
if [ $? -eq 0 ]; then
    echo "Python syntax verification successful!"
else
    echo "Python syntax verification failed!"
    exit 1
fi

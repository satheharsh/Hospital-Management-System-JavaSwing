#!/bin/bash
cd "$(dirname "$0")/.."
echo "Verifying Python syntax and running discovery tests..."
python3 -c "import glob, py_compile; [py_compile.compile(f, doraise=True) for f in glob.glob('./**/*.py', recursive=True)]"
if [ $? -eq 0 ]; then
    echo "Python syntax verification successful!"
else
    echo "Python syntax verification failed!"
    exit 1
fi

echo "Running unit tests..."
python3 -m unittest discover -s tests
if [ $? -eq 0 ]; then
    echo "All tests passed successfully!"
else
    echo "Tests failed!"
    exit 1
fi


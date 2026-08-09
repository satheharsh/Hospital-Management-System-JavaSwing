#!/bin/bash
echo "Building Hospital Management System using Maven..."
mvn clean compile
if [ $? -eq 0 ]; then
    echo "Compilation successful!"
else
    echo "Compilation failed!"
    exit 1
fi

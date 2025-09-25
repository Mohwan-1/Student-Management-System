#!/bin/bash

echo "Starting Student Management System..."
echo

if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Please run setup.py first."
    exit 1
fi

.venv/bin/python main.py

if [ $? -ne 0 ]; then
    echo
    echo "Program exited with an error."
    read -p "Press Enter to continue..."
fi
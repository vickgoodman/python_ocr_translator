#!/bin/zsh

source venv/bin/activate

# Try to login first
if instaloader --login=minte.motivata; then
    echo "Login successful"
else
    echo "Login failed, trying to load cookies..."
    instaloader --load-cookies brave
fi

python3 main.py

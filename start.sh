#!/bin/bash
# Memory-optimized startup script

# Set environment variables for memory optimization
export MPLBACKEND=Agg
export PYTHONUNBUFFERED=1

# Start the app
python app.py

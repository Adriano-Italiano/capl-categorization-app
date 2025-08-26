#!/bin/bash
gunicorn app:app --workers 1 --threads 2 --timeout 600 -b 0.0.0.0:$PORT

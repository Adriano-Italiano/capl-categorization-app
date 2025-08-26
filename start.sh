#!/bin/bash
exec gunicorn app:app --workers 1 --threads 2 --timeout 600 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT

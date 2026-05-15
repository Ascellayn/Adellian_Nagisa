#!/bin/bash

python3 -m uvicorn Nagisa:API --host 0.0.0.0 --port 7040 --log-level critical
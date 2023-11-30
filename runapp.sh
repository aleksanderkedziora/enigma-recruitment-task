#!/bin/sh

set -e

# Run backend server (you can run it from backend/run.sh, results will be the same)
cd backend
chmod -R 777 .
./run.sh

# ...
# can run other components, for example frontend app

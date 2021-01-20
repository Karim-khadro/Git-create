@echo off
set fn=%1

If "%1"=="" (
    echo "error"
)else (
    python CreateNewProject.py %fn%
)

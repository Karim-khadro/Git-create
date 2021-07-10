@echo off
set fn=%1

If "%1"=="" (
    echo "error"
)else (
    python F:\Projects\Git-create\CreateNewProject.py %fn%
)

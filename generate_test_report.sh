#!/bin/bash

echo "Starting Allure report generation..."

# If an Allure report already exists, copy history and data folders to new results folder.
if [ -d ".output/allure_report" ]; then
    cp -r .output/allure_report/history .output/allure_report/data .output/allure_results/
fi

# Generate Allure report.
allure generate .output/allure_results -o .output/allure_report --clean

# Echo the full path of the directory where the index.html file was created
echo "Report successfully generated at $(realpath .output/allure_report)"

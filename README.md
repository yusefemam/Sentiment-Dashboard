Author
Developed by Youssef - 2025

License
This project is licensed under the MIT License - see the LICENSE file for details. """

requirements_txt = """
fastapi uvicorn transformers jinja2 torch """

gitignore = """
pycache/ *.pyc .env """

Write all files
with open(f"{project_name}/backend/main.py", "w") as f: f.write(main_py)

with open(f"{project_name}/backend/index.html", "w") as f: f.write(index_html)

with open(f"{project_name}/LICENSE", "w") as f: f.write(license_text)

with open(f"{project_name}/README.md", "w") as f: f.write(readme_text)

with open(f"{project_name}/requirements.txt", "w") as f: f.write(requirements_txt)

with open(f"{project_name}/.gitignore", "w") as f: f.write(gitignore)

"Project structure and files created successfully."

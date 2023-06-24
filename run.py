import os

if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.realpath(__file__))
    app_dir = os.path.join(project_dir, "app")
    os.system(
        f"cd {app_dir} && uvicorn main:app --host=0.0.0.0 --port=1337 --workers=4"
    )

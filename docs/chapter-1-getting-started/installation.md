### Setting Up Your Environment with Poetry

To correctly set up your environment with Poetry inside the `backend/app` directory, follow these steps:

#### 1. Install Poetry

First, ensure Poetry is installed. If it's not already installed, you can do so by running the following command in your terminal:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

After installation, make sure to add Poetry to your system's PATH.

#### 2. Configure Poetry

Navigate to your project's root directory (`/home/sam/github/fastapi-your-data`) and then enter the `backend/app` directory. If you're using a custom setup or working within a specific part of your project, adjust paths accordingly.

```bash
cd /home/sam/github/fastapi-your-data/backend/app
```

Before proceeding, ensure you have a `pyproject.toml` file in the `app` directory. This file defines your project and its dependencies. If it's not present, you can create it by running:

```bash
poetry init
```

And follow the interactive prompts.

#### 3. Install Dependencies

```bash
poetry add pandas uvicorn fastapi pytest loguru pydantic-settings alembic pgvector
```

This command installs all necessary packages in a virtual environment managed by Poetry.

#### 4. Activate the Virtual Environment

To activate the Poetry-managed virtual environment, use the following command:

```bash
poetry shell
```

This command spawns a shell within the virtual environment, allowing you to run your project's Python scripts and manage dependencies.

#### 5. Running Your Application

Within the activated virtual environment and the correct directory, you can run your FastAPI application. For instance, to run the main application found in `backend/app/app/main.py`, execute:

```bash
uvicorn app.main:app --reload
```

This command starts the Uvicorn server with hot reload enabled, serving your FastAPI application.

#### 6. Deactivating the Virtual Environment

When you're done working in the virtual environment, you can exit by typing `exit` or pressing `Ctrl+D`.

### Additional Tips

- **Environment Variables**: Make sure to set up any required environment variables. You can manage them using `.env` files and load them in your application using libraries like `python-dotenv`.
- **Dependency Management**: Use `poetry add <package-name>` to add new dependencies and `poetry update` to update existing ones.
- **Testing and Linting**: Utilize Poetry to run tests and linters by adding custom scripts in the `pyproject.toml` file.

This guide should help you set up and manage your Python environment effectively using Poetry, enhancing your development workflow for the FastAPI project located in `/home/sam/github/fastapi-your-data/backend/app`.

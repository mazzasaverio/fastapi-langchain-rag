### Creating a Documentation with MkDocs

To create a living documentation for your project `fastapi-your-data` that acts as a theoretical guide, practical handbook, and technical diary, we will use MkDocs in combination with GitHub and Python. This guide covers setting up MkDocs, organizing documentation, configuring it with `mkdocs.yml`, writing documentation in Markdown, and deploying it using GitHub Actions.

#### Setting Up MkDocs

**Install MkDocs**: Ensure you have Python 3.6 or higher and pip installed. Install MkDocs with pip:

```bash
pip install mkdocs
```

**Initialize MkDocs Project**: In your project's root directory (`/home/sam/github/fastapi-your-data`), initialize MkDocs:

```bash
mkdocs new .
```

This creates a `mkdocs.yml` configuration file and a `docs` directory with an `index.md` file for your documentation.

#### Organizing Documentation Content

Create a structured documentation within the `docs` directory. Example structure:

```
docs/
    index.md
    getting-started/
        installation.md
    tutorials/
        mkdocs-setup-and-usage-guide.md
    changelog.md
```

#### Configuring Documentation in `mkdocs.yml`

Edit the `mkdocs.yml` file to define your documentation's structure and navigation. Example configuration:

```yaml
site_name: FastAPI Your Data Documentation
nav:
  - Home: index.md
  - Getting Started: getting-started/installation.md
  - Tutorials: tutorials/mkdocs-setup-and-usage-guide.md
  - Changelog: changelog.md
theme: readthedocs
```

#### Writing Documentation

Write your documentation content in Markdown format. Markdown files should be saved inside the `docs` directory according to the structure defined in `mkdocs.yml`.

Example content for `installation.md`:

````markdown
# Installation

## Requirements

- Python 3.6 or higher
- pip

## Installation Steps

To install the required packages, run:

```bash
pip install -r requirements.txt
```
````

````

#### Previewing Documentation Locally

Use MkDocs' built-in server to preview your documentation:
```bash
mkdocs serve
````

Visit `http://127.0.0.1:8080` in your browser to see your documentation.

#### Deploying Documentation

Build the static site with:

```bash
mkdocs build
```

The static site is generated in the `site` directory. Deploy this directory to any web server.

For GitHub Pages, you can automate deployment using GitHub Actions as described below.

#### Automating Deployment with GitHub Actions

**GitHub Actions Workflow**
In your project, create a workflow file under `.github/workflows/` (e.g., `deploy-docs.yml`) to define the steps for building and deploying your documentation to GitHub Pages.

**Generating a GitHub Token**

To perform actions such as deploying to GitHub Pages through GitHub Actions, you often need a GitHub token with the appropriate permissions. Here's how you can generate a `MY_GITHUB_TOKEN`:

**Access GitHub Token Settings**

- Log in to your GitHub account.
- Click on your profile picture in the top right corner and select **Settings**.
- On the left sidebar, click on **Developer settings**.
- Under Developer settings, click on **Personal access tokens**.
- Click on the **Generate new token** button.

**Configure Token Permissions**

- Give your token a descriptive name in the **Note** field.
- Set the expiration for your token as per your requirement. For continuous integration (CI) purposes, you might want to select a longer duration or no expiration.
- Select the scopes or permissions you want to grant this token. For deploying to GitHub Pages, you typically need:
  - `repo` - Full control of private repositories (includes `public_repo` for public repositories).
  - Additionally, you might need other permissions based on your specific requirements, but for deployment, `repo` is often sufficient.
- Scroll down and click **Generate token**.

After clicking **Generate token**, GitHub will display your new personal access token. **Make sure to copy your new personal access token now. You won’t be able to see it again!**

For use in GitHub Actions:

- Go to your repository on GitHub.
- Click on **Settings** > **Secrets** > **Actions**.
- Click on **New repository secret**.
- Name your secret `MY_GITHUB_TOKEN` (or another name if you prefer, but remember to reference the correct name in your workflow file).
- Paste your token into the **Value** field and click **Add secret**.```

If you named your secret something other than `MY_GITHUB_TOKEN`, make sure to reference it correctly in the `MY_GITHUB_TOKEN` field.

**Workflow Example**

Here's an example workflow that uses the `peaceiris/actions-gh-pages` action to deploy your MkDocs site to GitHub Pages:

```yaml
name: Deploy MkDocs Site

on:
  push:
    branches:
      - master

jobs:
  deploy-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.x"
      - name: Install dependencies
        run: |
          pip install mkdocs
      - name: Build MkDocs site
        run: mkdocs build
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.MY_GITHUB_TOKEN }}
          publish_dir: ./site
```

This workflow automatically builds and deploys your MkDocs site to GitHub Pages whenever changes are pushed to the master branch.

#### Conclusion

You've now set up MkDocs for your project, organized your documentation, written content in Markdown, previewed it locally, and deployed it using GitHub Actions. This setup allows you to maintain a comprehensive, up-to-date documentation for your project, facilitating both development and user guidance.

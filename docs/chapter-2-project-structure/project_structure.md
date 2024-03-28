## Project Structure and Microservice Design Patterns (FastAPI Your Data - Episode 1)

A well-organized project structure is paramount for any development endeavor. The ideal structure is one that maintains consistency, simplicity, and predictability throughout.

- A clear project structure should immediately convey the essence of the project to anyone reviewing it. If it fails to do so, it may be considered ambiguous.
- The necessity to navigate through packages to decipher the contents and purpose of modules indicates a lack of clarity in the structure.
- An arbitrary arrangement of files, both in terms of frequency and location, signifies a poorly organized project structure.
- When the naming and placement of a module do not intuitively suggest its functionality, the structure is deemed highly ineffective.

### Exploring Microservice Design Patterns

Our journey into the realm of software architecture focuses on strategies and principles designed to ease the transition from monolithic systems to a microservices architecture. This exploration is centered around breaking down a large application into smaller, more manageable segments, known as problem domains or use cases. A critical step in this process is the establishment of a unified gateway that consolidates these domains, thereby facilitating smoother interaction and integration. Additionally, we employ specialized modeling techniques tailored to each microservice, while also tackling essential aspects such as logging and configuration management within the application.

#### Objectives and Topics

The aim is to showcase the effectiveness and feasibility of applying these architectural patterns to a software sample. To accomplish this, we will explore several essential topics, including:

- Application of decomposition patterns
- Creation of a common gateway
- Centralization of logging mechanisms
- Consumption of REST APIs
- Application of domain modeling approaches
- Management of microservice configurations

#### Principles on Project Structure

There are numerous ways to structure a project, but the optimal structure is one that is consistent, straightforward, and devoid of surprises.

If a glance at the project structure doesn't convey what the project entails, then the structure might be unclear. If you need to open packages to decipher the modules within them, your structure is not clear. If the organization and location of files seem arbitrary, then your project structure is poor. If the module's location and name don't offer insight into its contents, then the structure is very poor. Although the project structure, where files are separated by type (e.g., api, crud, models, schemas) as presented by @tiangolo, is suitable for microservices or projects with limited scopes, it was not adaptable to our monolith with numerous domains and modules. A structure I found more scalable and evolvable draws inspiration from Netflix's Dispatch, with some minor adjustments.

### Applying the Decomposition Pattern

For instance, consider solving problems like:

- Identifying GitHub repositories that match your interests and where you'd like to contribute, based on a questionnaire that analyzes similarities with repository READMEs and other details.
- A module for finding companies, startups, or projects that align with your personality and characteristics.
- A note organization and interaction module.
- A module that guides you through decision-making questions based on books of interest.

Each microservice operates independently, having its server instance, management, logging mechanism, dependencies, container, and configuration file. Starting or shutting down one service does not affect the others, thanks to unique context roots and ports.

#### Sub-Applications in FastAPI

FastAPI provides an alternative design approach through the creation of sub-applications within a main application. The main application file (`main.py`) acts as a gateway, directing traffic to these sub-applications based on their context paths. This setup allows for the mounting of FastAPI instances for each sub-application, showcasing FastAPI's flexibility in microservice design.

Sub-applications, such as `sub_app_1`, `sub_app_2`, etc., are typical independent microservice applications mounted into the `main.py` component, the top-level application. Each sub-application has a `main.py` component which sets up its FastAPI instance, as demonstrated in the following code snippet:

```python
from fastapi import FastAPI
sub_app_1 = FastAPI()
sub_app_1.include_router(admin.router)
sub_app_1.include_router(management.router)
```

##

These sub-applications are typical FastAPI microservice applications containing all essential components such as routers, middleware, exception handlers, and all necessary packages to build REST API services. The only difference from standard applications is that their context paths or URLs are defined and managed by the top-level application that oversees them.

Optionally, we can run sub-applications independently from `main.py` using commands like `uvicorn main:sub_app_1 --port 8001` for `sub_app_1`, `uvicorn main:sub_app_2 --port 8082` for `sub_app_2`, and `uvicorn main:sub_app_3 --port 8003` for `sub_app_3`. The ability to run them independently despite being mounted illustrates why these mounted sub-applications are considered microservices.

### Mounting Submodules

All FastAPI decorators from each sub-application must be mounted in the `main.py` component of the top-level application to be accessible at runtime. The `mount()` function is called by the FastAPI decorator object of the top-level application, which incorporates all FastAPI instances of the sub-applications into the gateway application (`main.py`) and assigns each to its corresponding URL context.

```python
from fastapi import FastAPI
from application.sub_app_1 import main as sub_app_1_main

app = FastAPI()

app.mount("/sub_app_1", sub_app_1_main.app)
```

With this configuration, the mounted `/sub_app_1` URL will be used to access all the API services of the `sub_app_1` module app. These mounted paths are recognized once declared in `mount()`, as FastAPI automatically manages all these paths through the root_path specification.

Since all sub-applications in our system are independent microservices, let's now apply another design strategy to manage requests to these applications using only the main URL. We will use the main application as a gateway to our sub-applications.

### Creating a Common Gateway

It will be simpler to use the URL of the main application to manage requests and direct users to any sub-application. The main application can act as a pseudo-reverse proxy or an entry point for user requests, which will then redirect user requests to the desired sub-application. This approach is based on a design pattern known as API Gateway. Let's explore how we can implement this design to manage independent microservices mounted on the main application using a workaround.

### Implementing the Main Endpoint

There are various solutions for implementing this gateway endpoint. One option is to create a simple REST API service in the top-level application with an integer path parameter that identifies the microservice's ID parameter. If the ID parameter is invalid, the endpoint will return a JSON string instead of an error. Below is a straightforward implementation of this endpoint:

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/platform/{portal_id}")
def access_portal(portal_id: int):
    return {"message": "Welcome"}
```

The `access_portal` API endpoint is established as a GET path operation with `portal_id` as its path parameter. This parameter is crucial because it determines which sub-app microservice the user wishes to access.

### Evaluating the Microservice ID

The `portal_id` parameter is automatically retrieved and evaluated using a dependable function injected into the `APIRouter` instance where the API endpoint is defined.

```python
from fastapi import Request

def call_api_gateway(request: Request):
    portal_id = request.path_params["portal_id"]
    print(request.path_params)
    if portal_id == str(1):
        raise RedirectSubApp1PortalException()

class RedirectSubApp1PortalException(Exception):
    pass
```

### Evaluating the Microservice ID

This solution is a practical workaround to initiate a custom event, as FastAPI lacks built-in event handling aside from startup and shutdown event handlers. Once `call_api_gateway()` identifies `portal_id` as a valid microservice ID, it will raise custom exceptions. For instance, it will throw `RedirectStudentPortalException` if the user aims to access a specific microservice. However, first, we need to inject `call_api_gateway()` into the `APIRouter` instance managing the gateway endpoint through the `main.py` component of the top-level application.

```python
from fastapi import FastAPI, Depends, Request, Response
from gateway.api_router import call_api_gateway
from controller import platform
app = FastAPI()
app.include_router(platform.router, dependencies=[Depends(call_api_gateway)])
```

All raised exceptions require an exception handler to listen for the throws and execute necessary tasks to engage with the microservices.

## References and Inspirations

### Github

- [fastapi-alembic-sqlmodel-async](https://github.com/jonra1993/fastapi-alembic-sqlmodel-async): A project integrating FastAPI with Alembic and SQLModel for asynchronous database operations.
- [fastcrud](https://github.com/igorbenav/fastcrud): A library for simplifying CRUD operations in FastAPI.
- [agentkit](https://github.com/BCG-X-Official/agentkit): A toolkit for building intelligent agents.
- [fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices)

### Books

- [Building Python Microservices with FastAPI](https://amzn.to/3SZvdFk)

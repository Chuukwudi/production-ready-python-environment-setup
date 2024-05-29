# Production-ready Python Environment Setup
Video: https://www.youtube.com/watch?v=6OxqiEeCvMI
Outline
1. Why Docker?
2. Dockerize an App
3. Immediate file changes (Volumes)
4. Use IDE In Docker
5. Docker Compose
6. Add more services (Redis)
7. Debug Python code inside Docker


## 1. Why Docker?
- More than just a virtual env, isolated environment for all dependencies, multiple
services, easy deployment, same environment for collaborators, Python versions, etc...

## 2. Dockerise an app
Dockerfile

1. Add requirements.txt
2. Create the Dockerfile. Something like...
   ```Dockerfile
    FROM python:3.10-slim
    WORKDIR/code
    COPY ./requirements.txt ./
    RUN pip install --no-cache-dir -r requirements.txt
    COPY ./src ./src
    CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
   ```
   


- `docker build -t fastapi-image .`
- `docker run --name fastapi-container -p 80:80 -d -v ${pwd}:/code fastapi-image`

or use the docker-compose:
- `docker-compose up` to start
- `docker-compose down` to stop
- `docker-compose up --build` to rebuild for fresh modifications to the code
- add the `-d` flag to run in detached mode.
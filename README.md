- `docker build -t fastapi-image .`
- `docker run --name fastapi-container -p 80:80 -d -v ${pwd}:/code fastapi-image`

or use the docker-compose:
- `docker-compose up` to start
- `docker-compose down` to stop
- `docker-compose up --build` to rebuild for fresh modifications to the code
- add the `-d` flag to run in detached mode.
# DOT - The Decision Optimization Tool

## Description

The *Decision Optimization Tool (DOT)* is a **prototype** of a web application to guide users and teams through complex decision making processes.
The prototype utilizes the concepts of *Decision Quality* and *Structured Decision Making*.
The web application contains features for documented framing exercises (issue list, objectives, decision hierarchy, strategy table, etc.) and a graphical interface for the creation of Influence Diagrams and the visualization of a resulting Decision Trees.
Below is some information on how to run the web application locally on any machine using different technologies including a local database.


## Installation Instructions

The code is built on

- **TinkerPop** Graph database
- **FastAPI** - Python backend (>=3.10)
- **React** - JavaScript frontend (>=20.1.0)


and the used ports are

- port 8182: local database
- port 8000: API hosted
- port 3000: web application

### Command Line

```bash
git clone https://github.com/equinor/dot.git
```


#### Backend - API

Installation

```bash
pip install poetry==1.8.5
poetry --directory ./api install
```

Running the tests

```bash
poetry --directory ./api run pytest ./api
```

Start of local database

```bash
poetry run --directory ./api uvicorn api.main:app --reload
```

The API documentation can be found on: http://localhost:8000/docs#/default

#### Frontend - Web Application

Installation

```bash
npm install --prefix web
```

Start of web application

```bash
npm start --prefix web
```

### Docker

```bash
docker-compose up --build
```

The suffix ` -d` can be added to run the containers in detached mode.

### Codespace

Github codespace is set up for the project. Be aware the database is available only if running the codespace locally and not from vscode browser version.


### Docs

```bash
poetry --directory ./api install --with docs
cd docs
make html
```

In case of modifications of endpoints, the openapi spec files needs to be updated before building the documentation

```bash
uvicorn main:app --reload
curl -X GET "http://127.0.0.1:8000/openapi.json" -o docs/src/developers/apiopenapi.json
```


## Usage


The frontend application is available on port 3000 and the API documentation on port 8000. Once the local database is running, they respectively can be started from a browser at addresses
http://localhost:3000 and http://localhost:8000/docs#/default.


## Contributing

[Contribution guidelines for this project](./CONTRIBUTING.md)

## Documentation

## License

[Licence file](./LICENSE)


## Contact Information

## Acknowledgments

The project has been greatly influenced by the concepts and work shared by Reidar B. Bratvold (https://reidar-bratvold.com/) from the University in Stavanger.


__Reference:__

Making Good Decisions by Reidar B Bratvold and Steve H Begg. _Society of Petroleum Engineers_, vol. 207,  2010. ISBN 9781555632588.

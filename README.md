# DOT - The Decision Optimization Tool

## Description

The _Decision Optimization Tool (DOT)_ is a **prototype** of a web application to guide users and teams through complex decision making processes.
The prototype utilizes the concepts of _Decision Quality_ and _Structured Decision Making_.
The web application contains features for documented framing exercises (issue list, objectives, decision hierarchy, strategy table, etc.) and a graphical interface for the creation of Influence Diagrams and the visualization of a resulting Decision Trees.
Below is some information on how to run the web application locally on any machine using different technologies including a local database.

_This branch aims at providing the setup and information for a local installation on Windows. This is targeted toward students of DA/DQ course._

## Installation Instructions

The code is built on

-   **TinkerPop** Graph database
-   **FastAPI** - Python backend (>=3.10)
-   **React** - JavaScript frontend (>=20.1.0)

and the used ports are

-   port 8182: local database
-   port 8000: API hosted
-   port 3000: web application

### Dependency installation

You need to install:

- git
- Java (>8)
- node
- python
- pip

### Environment

You have to setup the environment variable JAVA_HOME and update the paths. If java is installed in 
`$JAVADIR` you should defined as the variable JAVA_HOME, as, for example

```
JAVA_HOME = C:\Program Files\Java\jre1.8.0_461
```

Together with the dot package installed in `$DODIR`, PATHS are then

```
$JAVADIR$\bin
$DOTDIR$\db_server\bin
$DOTDIR$\db_console\bin
```

Make sure that python, pip, node and npm are in the paths. For example:

```
C:\Users\<user_name>\AppData\Roaming\npm
C:\Program Files\nodejs
C:\Python313
C:\Python313\Scripts
```

You may have to create an inbound rules for the port 8182. 

> Window Defender Firewall -> Inbound Rules -> New Rule...

### DOT package

```bash
git clone https://github.com/equinor/dot.git
```

#### Backend - API

Installation

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install --upgrade pip
pip install poetry==1.8.5
poetry --directory .\api install
```

Notice you may prefer having poetry available outside your virtual environment and

```bash
pip install --upgrade pip
pip install poetry==1.8.5
python -m venv .venv
.\.venv\Scripts\activate
poetry --directory .\api install
```

_Remark:_ 

In this installation, the graphviz package has not been installed. This means neither the ongoing connection to pyagrum nor the uml diagrams would be available.

Running the tests

```bash
poetry --directory .\api run pytest .\api
```

#### Backend - Database

Start the server

```bash
cd db_server
start bin\gremlin-server.bat conf\gremlin-dot.yaml
```

Start of local database

```bash
poetry --directory .\api run uvicorn api.main:app --reload
```

The API documentation can be found on: http://localhost:8000/docs#/default

#### Frontend - Web Application

Installation

```bash
cd web
npm install
```

Start of web application

```bash
cd web
npm start
```

## Other installation methods

### Installation through Docker

```bash
docker-compose -f .\docker-compose.dev.yaml up --build
```

The suffix ` -d` can be added to run the containers in detached mode.

### Installation in Codespace

Github codespace is set up for the project. Be aware the database is available only if running the codespace locally and not from vscode browser version.

## Documentation

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

**Reference:**

Making Good Decisions by Reidar B Bratvold and Steve H Begg. _Society of Petroleum Engineers_, vol. 207, 2010. ISBN 9781555632588.



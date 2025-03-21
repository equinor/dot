from dependencies import create_app, create_versions

app = create_app()
versions = create_versions(app)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the DOT api"}

import yaml
import httpx
import uvicorn
from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import StreamingResponse
import importlib.util
import sys
from pathlib import Path

app = FastAPI()

# Load configuration
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

MOONRAKER_URL = config["moonraker"]["url"]
PROXY_HOST = config["proxy"]["host"]
PROXY_PORT = config["proxy"]["port"]

async def load_and_execute_rule(rule_path: str, file_path: Path):
    """Load and execute a preprocessing rule on the uploaded file."""
    try:
        spec = importlib.util.spec_from_file_location("rule", rule_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules["rule"] = module
            spec.loader.exec_module(module)
            if hasattr(module, "process"):
                await module.process(file_path)
    except Exception as e:
        print(f"Error executing rule {rule_path}: {str(e)}")

@app.api_route("/{path:path}", methods=["POST"])
async def proxy_post(request: Request, path: str):
    """Handle POST requests, with special handling for file uploads."""
    content_type = request.headers.get("content-type", "")
    
    # Check if this is a file upload request
    if "multipart/form-data" in content_type and "upload" in path:
        # Handle file upload with preprocessing
        form = await request.form()
        for field_name, field_value in form.items():
            if isinstance(field_value, UploadFile):
                # Save the uploaded file temporarily
                temp_path = Path(f"/tmp/{field_value.filename}")
                with open(temp_path, "wb") as temp_file:
                    content = await field_value.read()
                    temp_file.write(content)

                # Execute preprocessing rules
                for rule in config["preprocessing_rules"]:
                    if rule["enabled"]:
                        await load_and_execute_rule(rule["script"], temp_path)

                # Upload processed file to Moonraker
                async with httpx.AsyncClient() as client:
                    files = {field_name: (field_value.filename, open(temp_path, "rb"), field_value.content_type)}
                    response = await client.post(f"{MOONRAKER_URL}/{path}", files=files)
                    temp_path.unlink()  # Clean up temporary file
                    return StreamingResponse(
                        content=response.iter_bytes(),
                        status_code=response.status_code,
                        headers=dict(response.headers)
                    )

    # For non-file-upload requests, pass through directly
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{MOONRAKER_URL}/{path}",
            content=await request.body(),
            headers=request.headers
        )
        return StreamingResponse(
            content=response.iter_bytes(),
            status_code=response.status_code,
            headers=dict(response.headers)
        )

@app.api_route("/{path:path}", methods=["GET", "PUT", "DELETE", "PATCH"])
async def proxy_request(request: Request, path: str):
    """Handle all other HTTP methods by passing through to Moonraker."""
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=f"{MOONRAKER_URL}/{path}",
            content=await request.body(),
            headers=request.headers
        )
        return StreamingResponse(
            content=response.iter_bytes(),
            status_code=response.status_code,
            headers=dict(response.headers)
        )

if __name__ == "__main__":
    uvicorn.run(app, host=PROXY_HOST, port=PROXY_PORT)

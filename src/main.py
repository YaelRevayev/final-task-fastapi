from fastapi_server import app
import uvicorn
from configs import config


def main():
    uvicorn.run(app, host="0.0.0.0", port=config.HTTP_PORT)


if __name__ == "__main__":
    main()

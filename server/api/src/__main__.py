import logging

import uvicorn

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run("src.app:app", host="0.0.0.0", port=5285)

# Setup

1. Install dependencies.
    ```bash
    uv sync
    ```

2. Install pre-commit to automatically lint and format via ruff before commit
    ```bash
    uv run pre-commit install
    ```

3. Generate ES256 private key
    ```bash
    openssl ecparam -name prime256v1 -genkey -noout -out src/auth/certs/private_key.pem
    ```

4. Generate ES256 public key
    ```bash
    openssl ec -in src/auth/certs/private_key.pem -pubout -out src/auth/certs/public_key.pem
    ```

# Launch

### Docker

* Development mode (fast-refresh)
    ```bash
    docker compose watch
    ```

* Production mode
    ```bash
    docker compose up --build -d
    ```

### Pure python

* Development mode (fast-refresh)
    ```bash
    uv run fastapi dev
    ```

* Production mode
    ```bash
    uv run --no-dev fastapi run
    ```
# Setup
1. Create virtual environment.
```bash
python -m venv .venv 
```

2. Activate it.
* On Windows:
```bash
.venv\Scripts\activate
```

* On MacOS/Linux:
```bash
source .venv/bin/activate
```

3. Install requirements.
```bash
pip install -r .\requirements.txt
```

```bash
pre-commit install
```

# Launch
## Docker
### Development mode (fast-refresh)
```bash
docker compose watch
```

### Production mode
```bash
docker compose up --build -d
```

## Default
#### Development mode (fast-refresh)
```bash
fastapi dev
```

#### Production mode
```bash
fastapi run
```

## Instructions
Generate ES256 private key
```bash
openssl ecparam -name prime256v1 -genkey -noout -out src/auth/certs/private_key.pem
```

Generate ES256 public key
```bash
openssl ec -in src/auth/certs/private_key.pem -pubout -out src/auth/certs/public_key.pem
```

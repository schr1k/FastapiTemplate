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
source venv/bin/activate
```

3. Install requirements.
```bash
pip install -r .\requirements.txt
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
uvicorn main:app --reload
```

#### Production mode
```bash
uvicorn main:app
```

## Instructions
Generate ES256 private key
```bash
openssl ecparam -name prime256v1 -genkey -noout -out certs/private_key.pem
```

Generate ES256 public key
```bash
openssl ec -in private_key.pem -pubout -out certs/public_key.pem
```

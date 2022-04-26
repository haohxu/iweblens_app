## 1. install environment and 2.Write Web-Service

- `python -m venv ./server`
- `cd ./server` or `cd ./client` for client test
- `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- `.\Scripts\Activate.ps1`
- after work remember to `Set-ExecutionPolicy Restricted`

### create requirements.txt file
- `python -m pip freeze > requirements.txt`

### test by using iWebLens_client.py
- `python iWebLens_client.py inputfolder/ http://118.138.43.2:5000/api/object_detection 16`

## 3. Dockerize
- dockerfile

## 4. Docker hub

## 5. Build
- `Docker build -t ezra20/iWebLens_app:1.0`
- `Docker login`
- `Docker push ezra20/iWebLens_app:1.0`
- `docker run -d -p 5000:5000 --name my-flask-app flask-app`

## 6. OCI
- install Docker K8s
- Open 6443
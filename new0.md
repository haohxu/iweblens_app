# local

## 1. install environment and 2.Write Web-Service

- `python -m venv ./server`
- `cd ./server` or `cd ./client` for client test
- `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- `.\Scripts\Activate.ps1`
- after work remember to `Set-ExecutionPolicy Restricted`

### create requirements.txt file
- `python -m pip freeze > requirements.txt`



## 3. Dockerize
- dockerfile

## 4. Docker hub


# 5. Docker and dockerfile

```
docker build -t haoxucode/iweblens_app:1.0 .
docker login
docker run -p 5000:5000 haoxucode/iweblens_app:1.0
docker push haoxucode/iweblens_app:1.0

```

local to local
python iWebLens_client.py inputfolder/ http://192.168.20.2:5000/api/object_detection


# !!!!!!! for only test !!!!!

# local-client POST request
python iWebLens_client.py inputfolder/ http://168.138.13.227:31000/api/object_detection

# cloud-client POST request
python3 git-repos/iweblens_app/client/iWebLens_client.py git-repos/iweblens_app/client/inputfolder/ http://168.138.13.227:31000/api/object_detection 
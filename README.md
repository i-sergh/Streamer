# DESCRIPRION 
A little handmade client-server video-stream app.
It grabs screenshot from client side and send it to the server.
From the server all, who enters to the root path, would see the clients image 

it works only with one client yet

# Usage
## SERVER
To start server you just need to run a compose file 
```bash
sudo docker-compose -f dev-docker-compose.yaml up
```

## CLIENT 

1. <p>Create virtual environment and install all dependencies in `/client` folder</p>
venv creation

```bash
python -m venv venv
```

windows env activation

```bash
venv\Scripts\activate
```

linux env activation
```bash
source venv/bin/activate
```

dependencies installation

```bash
python -m pip install -r client/requirements.txt
```



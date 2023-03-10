# Gunicorn Flask encryption API with NGINX reverse proxy

Provides endpoints for encrypting and decrypting using AES in CBC mode with PBKDF2 key derivation

## Requirements

* x86-64
* Linux
* Docker
* k8s

## Creating resources
The shell script "up.sh" is responsible for building the local Docker image and creating resources
```
sh up.sh
```

## Destroying resources
The shell script "down.sh" frees up allocated resources

```
sh down.sh
```

## Endpoints


### Encrypt (raw body: text), (bearer token) -> ciphertext

POST http://localhost:5001/encrypt

### Decrypt (raw body: ciphertext), (bearer token) -> text


POST http://localhost:5001/decrypt

### Create User (json body: {username, password}) -> text


POST http://localhost:5001/users

### List All Users -> JSON


GET http://localhost:5001/users

### Login (json body: {username, password}) -> Token


POST http://localhost:5001/login



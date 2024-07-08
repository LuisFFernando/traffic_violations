#!/bin/bash

# Genera un secreto aleatorio para JWT
JWT_SECRET=$(openssl rand -base64 32)

export JWT_SECRET

exec "$@"

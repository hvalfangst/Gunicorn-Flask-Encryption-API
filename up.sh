#!/bin/sh

echo -e "\n\n"


# Build image from Dockerfile - exit script on failure
echo "Building image [encryption-service] from local Dockerfile"
  if ! docker build -t hardokkerdocker/hvalfangst:encryption-service . ; then
      echo
      echo "[Error building image 'encryption-service' - Exiting script]"
      exit 1
  fi
echo

echo -e "\n\n"

# Prompt user for encryption key
read -p "Enter desired encryption key: " encryption_key

echo -e "\n\n"

# Base64 encode the encryption key
encoded_key=$(echo -n "$encryption_key" | base64 | tr -d '\n')

# Use 'sed' to overwrite value of the field "encryption_key" contained in yaml file "secrets"
sed -i "s|^\(.*encryption_key: \)\(.*\)|\1$encoded_key|" k8s/secrets.yaml

# Create our initial resources
kubectl apply -f k8s/secrets.yaml > /dev/null 2>&1
kubectl apply -f k8s/nginx.yaml > /dev/null 2>&1
kubectl apply -f k8s/manifest.yaml > /dev/null 2>&1


echo "Creating resources defined in manifest.yaml"

./misc/progress_bar.sh 0.25

echo -e "\n\n"

echo "Preparing pods..."
./misc/progress_bar.sh 0.25

echo -e "\n\n"

# List pods
kubectl get pods
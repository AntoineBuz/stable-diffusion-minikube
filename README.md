# Stable Diffusion app, deployed with Minikube

![Static Badge](https://img.shields.io/badge/Minikube-blue)
![Static Badge](https://img.shields.io/badge/HuggingFace-yellow)
![Static Badge](https://img.shields.io/badge/gradio-orange)
![Static Badge](https://img.shields.io/badge/GPU-%23009900)
![Static Badge](https://img.shields.io/badge/port-7860-green)

**This project aims at giving resources to deploy containerized ML apps with Kubernetes.**

Main difficulty is handling gpu usage while running apps in containers.

This is supposed to run on an Ubuntu22.04 distro (dedicated cuda Docker image) but running it on another distribution can be made possible by changing the base image according to your environment. See [Nvidia on Docker Hub](https://hub.docker.com/r/nvidia/cuda/tags) for this purpose and edit `./Dockerfile` accordingly. 

## Index

1. [Image Setup](#image-setup)
   1. [Prerequisites](#prerequisites)
   2. [Image build](#image-build)
   3. [Container run](#container-run)
   4. [Access the app](#access)
2. [K8S deployement](#k8s-deployement)
    1. [Start your cluster](#start-cluster)
    2. [Load your image](#load-your-image)
    3. [Launch a deployement](#launch-a-deployement)

## Image setup 

### Prerequisites

- **Docker installed** : See basic [installation documentation](https://docs.docker.com/engine/install/) if needed.
- **Cuda drivers installed** for your Nvidia GPU.
- **Cuda container toolkit installed** : See nvidia container toolkit [documentation](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.14.4/install-guide.html)
- **Have a K8S cluster (we use Minikube here)**

### Image build

```bash
git clone git@github.com:AntoineBuz/stable-diffusion-minikube.git
cd ./stable-diffusion-minikube
docker build -t sd . # Let's call it sd (you can name it as you want)
```

This **may take some time** to download every needed packages (nvidia/cuda image, ML libs, model...). The whole image is **about 20GB**.

### Container run

Setup Nvidia Container Toolkit (required to use GPUs from containers)

```bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```
Run the container with gpu enabled

```bash
docker run -d --gpus all -p 7860:7860 sd
```

### Access

Access the app within your favorite browser on [127.0.0.1:7860](http://127.0.0.1:7860)

## K8S deployement

### Start Cluster
*This part is deeply inspired from [minikube documentation](https://minikube.sigs.k8s.io/docs/tutorials/nvidia/)*

#### Configure Docker

```bash
sudo nvidia-ctk runtime configure --runtime=docker && sudo systemctl restart docker
```

#### Start minikube

```bash
minikube start --driver docker --container-runtime docker --gpus all
```

#### Enable nvidia plugins

```bash
minikube addons enable nvidia-device-plugin
minikube addons enable nvidia-gpu-device-plugin
```

#### Check for GPU 

The following command should at least return info about gpu allocatability

```bash
$kubectl describe nodes | grep nvidia

>
...
Allocatable:
  cpu:                24
  ephemeral-storage:  1917499848Ki
  hugepages-1Gi:      0
  hugepages-2Mi:      0
  memory:             32589244Ki
  nvidia.com/gpu:     1 # Good news, our GPU is detected in our node
  pods:               110
...
```

### Load your image

This step aims at loading the image into Minikube Container. Two options :

- **1st option :** You can load the image into minikube with `minikube image load <image>` or using `docker pull <repo/image>`. You can setup a local docker registry and push your image into it before pulling it from minikube.

- **2nd option :** Also, you can build it directly from the [minikube container itself](https://minikube.sigs.k8s.io/docs/commands/docker-env/) (this option requires to re-download everything)

    ```bash
    eval $(minikube docker-env) # You are now inside gcr.io/k8s-minikube/... container
    docker build -t image .
    docker images # To check for your image to be built
    ```

### Launch a deployement

Once your minikube instance is up and your image is accessible from it, it's time for deployement.

Have a look at `./k8s/` as `.yaml` config files are there.

You can then run the following 

```bash
kubectl apply -f ./k8s/
```

Check for things to be running with 

```bash
$kubectl describe ingress sd
>Name:             sd
Labels:           <none>
Namespace:        default
Address:          192.168.XXX.XXX # Exposed IP Address 
Ingress Class:    nginx
Default backend:  <default>
Rules:
  Host        Path  Backends
  ----        ----  --------
  *           
              /   sd:7860 (xxx.xxx.xxx.xxx:7860)
Annotations:  <none>
Events:
  Type    Reason  Age                From                      Message
  ----    ------  ----               ----                      -------
  Normal  Sync    38m (x2 over 38m)  nginx-ingress-controller  Scheduled for sync

```

Go visit your running app in your browser with http://adress:7860 !

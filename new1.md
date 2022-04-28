```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC4nM7qR8NvVbm5dWqwyOtXh7vMehLRbtquqTGQMbvg5ZELHTiPxjtpCH4DZVhXtSRaVwVomg686kWRF0T100tEh08IzK1k+0SSEpmdcb93g+pfQlKR68vsepS28aOq1D2aNsl55LE8wr9xEwi0cYSKEmI3buEaNYYH7QeQOTmN4u7GSwNuWoFOjSJnanu6V8zQCya+G/twslm6wvKnnetV44q+IO7iJfIpji5O0ZjBcaLhtY1kROhn2JHtxXBP6zjGU+EERWe9EE+62jkj1BgOiquvcKUebhHU1Qg6YdwgQGAz5fJmh3Jeo/qQGieNaj47ocKUZhLRUYxaJrpt4/O7 imported-openssh-key

```


# install firewalld
- for all VMs

```
sudo apt-get -y update
sudo apt-get -y install firewalld
sudo systemctl enable firewalld 
sudo firewall-cmd --state
sudo firewall-cmd --permanent --zone=public --add-port=6443/tcp
sudo firewall-cmd --permanent --zone=public --add-port=10248/tcp
sudo firewall-cmd --permanent --zone=public --add-port=10250/tcp
sudo firewall-cmd --permanent --zone=public --add-port=5000/tcp
sudo firewall-cmd --permanent --zone=public --add-port=80/tcp
sudo firewall-cmd --permanent --zone=public --add-port=8080/tcp
sudo firewall-cmd --permanent --zone=public --add-port=31000/tcp
sudo firewall-cmd --permanent --zone=public --add-port=6783/tcp
sudo firewall-cmd --permanent --zone=public --add-port=6783/udp
sudo firewall-cmd --permanent --zone=public --add-port=6784/udp
sudo firewall-cmd --reload
sudo firewall-cmd --list-all
```

# install Docker
- for all VMs
```
sudo apt-get update

sudo apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

sudo apt-get update

sudo apt-get install docker.io
sudo docker version
sudo systemctl enable docker
sudo systemctl status docker
sudo systemctl daemon-reload
sudo systemctl restart docker
```

# install kubernetes
- for all VMs
```
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add
sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"
sudo apt-get install kubeadm kubelet kubectl
sudo apt-mark hold kubeadm kubelet kubectl
kubeadm version
```


# create kubernetes cluster
- for all VMs

```
kubeadm version
sudo hostnamectl set-hostname master-node
sudo nano /etc/hosts <host-IP> master-node
sudo swapoff -a

# solve Docker cgroup for all VMs
sudo docker info | grep Cgroup
sudo nano /etc/systemd/system/kubelet.service.d/10-kubeadm.conf

Environment="KUBELET_KUBECONFIG_ARGS=--bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf --cgroup-driver=cgroupfs"

sudo kubeadm reset
```


- only run on master node

``` 
sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=<private-ip-address>

rm -r $HOME/.kube
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config



sudo kubeadm token create --print-join-command


```

- only run on worker nodes

```
sudo kubeadm join 10.0.0.223:6443 --token 9lndni.2k03uqf5aa8f3pzn \
        --discovery-token-ca-cert-hash sha256:3053dab84fa01a60360d4284ccb8a726d103ce3f846008848b81e01c1f96b0b2
```

# install weave for nodes network connection
kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"

sudo rm -r /var/lib/weave/weave-netdata.db

# docker pull
sudo docker login
sudo docker pull haoxucode/iweblens_app:latest

#!!!!!!!!

## reset kubernetes
kubectl drain worker-node01 --ignore-daemonsets --delete-local-data
kubectl drain worker-node02 --ignore-daemonsets --delete-local-data
kubectl delete node worker-node01
kubectl delete node worker-node02
sudo kubeadm reset


# kubernete orchestra


kubectl create namespace myapp
kubectl get nodes,deployments,svc,pods -n=myapp -o wide
kubectl apply -f deployment.yml -n=myapp
kubectl apply -f service.yml -n=myapp

kubectl scale deployment iweblens-deployment --replicas=0 -n=myapp
kubectl delete deployment -n=myapp iweblens-deployment
kubectl logs -n=myapp pod-name


kubectl delete deployment -n=myapp iweblens-deployment
kubectl delete service -n=myapp iweblens-service

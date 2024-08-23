## SSH

Per Terminal sich auf die VM Verbinden

```bash
ssh theship@192.168.100.21
``` 
Password: theship

## Kubernetes
Alle Pods bekommen

```bash
k3s kubectl get pods --all-namespaces
```

Externl IP setzen
```bash
k3s kubectl patch svc rabbitmq-cluster-scanner -p '{"spec":{"externalIPs":["192.168.100.21"]}}'
```

## RabbitMQ

URL

```bash
http://192.168.100.21:15672/
```
| Username                         |             Password             |
|----------------------------------|:--------------------------------:|
| default_user_b2EKgD6Id6Hp989VC_8 | J_4rUCXcnlYgGb7JBqqohpdEdI1_ULe4 |
| guest                            |              guest               |

## SSH

Per Terminal sich auf die VM Verbinden

```bash
ssh theship@192.168.100.21
``` 
Password: theship

## Kubernetes
> **_INFO:_**  Grundsätzlich würden alle Befehle mit **k3s kubectl** starten. Jedoch haben wir ein alias gesetzt, daher funktioniert alles mit k!
> Ein Alias kann mit **alias <Abchürzig>=<"Befehl">** im Terminal erstellt werden.

```bash
k get pods --all-namespaces
```

External IP setzen
```bash
k patch svc rabbitmq-cluster-scanner -p '{"spec":{"externalIPs":["192.168.100.21"]}}'
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


## Widget Development

TBD
## SSH

Per Terminal sich auf die VM Verbinden

```bash
ssh theship@192.168.100.21
``` 
Password: theship

## Kubernetes
> **_INFO:_**  Grundsätzlich würden alle Befehle mit **k3s kubectl** starten. Jedoch haben wir ein alias gesetzt, daher funktioniert alles mit k!
> Ein Alias kann mit **alias <Abchürzig>=<"Befehl">** im Terminal erstellt werden.

Alle Pods anzeigen
```bash
k get pods --all-namespaces
```

External IP setzen
```bash
k patch svc rabbitmq-cluster-scanner -p '{"spec":{"externalIPs":["192.168.100.21"]}}'
```

Der Befehl kubectl apply -f <dateipfad> wird verwendet, um Kubernetes-Ressourcen aus einer Datei zu erstellen oder zu aktualisieren.
```bash
k apply -f <dein Yaml FILE>.yaml
```

Ein Pod löschen:
```bash
k delete pod <pod-name>
```

## RabbitMQ

Webinterface

```bash
http://192.168.100.21:15672/
```
| Username                         |             Password             |
|----------------------------------|:--------------------------------:|
| default_user_b2EKgD6Id6Hp989VC_8 | J_4rUCXcnlYgGb7JBqqohpdEdI1_ULe4 |
| guest                            |              guest               |

### Installation
> **_INFO:_**  Sollte RabbitMQ nicht laufen, kann folgendes versucht werden:

```bash
k delete rabbitmqclusters.rabbitmq.com hello-world
```

Im Pfad: XXX
```bash
kubectl apply -f rabbitMq.yaml
```

## Widget Development

TBD
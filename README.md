# C'est quoi?

Image docker exposant des métriques des comptes Crédit Agricole pour Prometheus 

## Docker run

Execution de l'image docker

```
sudo docker run -d --env-file ./env.list --name=ca_exporter creditagricole-exporter:latest
```

## Docker build

Contruction de l'image docker

```
sudo docker build . --file Dockerfile -t creditagricole-exporter
```

## Variables

| Variables | Description |
| ------------- | ------------- |
| CREDITAGRICOLE_EXPORTER_DEBUG | debug mode 1 or 0 |
| CREDITAGRICOLE_EXPORTER_DELAY | le délai entre chaque appel, la valeur par défaut est 3600s |
| CREDITAGRICOLE_EXPORTER_PORT | port d'écoute serveur http, valeur par défaut 8080 |
| CREDITAGRICOLE_EXPORTER_USERNAME | numéro de compte bancaire |
| CREDITAGRICOLE_EXPORTER_PASSWORD | mot de passe, code pin |
| CREDITAGRICOLE_EXPORTER_DEPARTMENT | numéro de département de la caisse régionale |

## Exécution depuis les sources

```
python3 -c "import creditagricole_exporter as lib; lib.start_monitor();"
```
## EDCA _Records_ (_Python version_)
Genera [_Records_](http://standard.open-contracting.org/latest/en/schema/records_reference/) y
  [_Record Packages_](http://standard.open-contracting.org/latest/en/schema/record_package/)

 ### Dependencias
 - [MongoDB](https://www.mongodb.com/)
 - [Python](https://www.python.org/downloads/) v3.4 or later
 - [jq](https://stedolan.github.io/jq/)

### Creación de entorno
 - Creamos ambiente de Python con versión v3.4
   conda create --name edca_env

 ### Instalación de paquetes
 `cd edca-records/ && pip install -r requirements.txt`

 ### Importar JSON (_Release Packages_)

 ```bash import_json.sh <dir_name>```

 ### Inicio rápido

 ### Instalación Docker
 
 #### Construcción de la imagen docker
 `docker built -t mxabierto/edca_records:development .`

 #### Construcción contenedor
 `docker run --name edca_dashboard -e TZ='America/Mexico_City' -d mxabierto/edca_records:develpment`

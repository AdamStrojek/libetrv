

# libetrv


**La biblioteca está actualmente en desarrollo y no está diseñada para ser utilizada por el usuario final**

Monitoree y controle su eTRV desde Python. Recientemente, Danfoss ha lanzado nuevos TRVs que pueden controlarse a través de Bluetooth Low Energy. Esta biblioteca permitirá conectar estos dispositivos y controlarlos.

La aplicación fue desarrollada en un Raspberry Pi B+, pero debería funcionar correctamente en cualquier sistema basado en Linux con un dispositivo Bluetooth LE.

## Dispositivos compatibles

Todos los dispositivos compatibles y probados:

- Danfoss Eco Bluetooth LE - WIP

## Registro de cambios

### Versión 0.6
- Migración de los procesos de CI/CD a flujos de trabajo de GitHub Actions.
- Se actualizó la versión mínima requerida de Python a 3.9.
- Se actualizaron los scripts de configuración para usar `setuptools`.
- Se añadió la funcionalidad para establecer el número PIN de los dispositivos.
- Se actualizó el README con nuevas instrucciones de instalación y ejemplos de uso.
- Se eliminó la insignia de CircleCI obsoleta del README.

## Instalación
Este software requiere al menos Python 3.5. Todos los paquetes requeridos se encuentran listados en el archivo `requirements.txt`.

Dado que el software está en desarrollo, no hay una forma directa de instalarlo en el sistema y configurarlo como un servicio del sistema.

Para desarrollo, simplemente cree un entorno virtual e instale todos los requisitos.

```bash
$ mkdir -p ~/venv/libetrv
$ python3 -m venv ~/venv/libetrv
$ source ~/venv/libetrv/bin/activate
$ pip3 install -r requirements.txt
```
  

## Permisos de Bluetooth
Se recomienda no iniciar esta aplicación como usuario `root`. Para evitarlo, puede permitir que python3 acceda a la interfaz de Bluetooth:

```bash
$ sudo apt-get install libcap2-bin
$ sudo setcap 'cap_net_raw,cap_net_admin+eip' `readlink -f \`which python3\``
$ sudo setcap 'cap_net_raw+ep' `readlink -f \`which hcitool\``
```

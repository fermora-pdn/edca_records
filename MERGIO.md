1. meter los releases de SFP (paquetes 1,2,3) en Releases_SFP, lo puedes hacer con import_Releases.sh pero tienes que copiar de Releases a Releases_SFP y borrar Releases

2. updatear Releases_SFP con el nuevo paquete de Compranet_JSONR usando update_releases_sfp.py

3. copiar Releases_SFP de nuevo a Releases y ahora ya meter los datos de hacienda

4. ahora que ya tieenes los datos completos en Releases, ya puedes generar los records y exportar todas las colecciones normalment
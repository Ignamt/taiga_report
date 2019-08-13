# Generador de reportes de Taiga

Este programa tiene como finalidad generar reportes de manera automática en base
a las UserStories cargadas en Taiga siguiendo unos lineamientos generales que se
incluyen con el proyecto.

El proyecto está armado con `Python 3.6+`.

Para poder probar y desarrollarlo, hay que armar un entorno virtual (Venv, que 
viene incluido con Python 3) con el cual se corre. [Tutorial para entornos 
virtuales](https://docs.python-guide.org/dev/virtualenvs/)

Una vez instalado el entorno virtual hay que activarlo. Con el entorno virtual 
activo, instalar las dependencias que vienen en el archivo `requirements.txt`.
El comando para hacer esto automáticamente es:

    cd path\a\donde\clonaste\el\repo
    pip install -r requirements.txt
    
Una vez acá, la mejor forma de ir probando es pararte sobre la carpeta superior
del repo y ejecutar un intérprete de python. Ahí 
podés ir importando los módulos y objetos para explorarlos e interactuar con 
ellos.

También desde este nivel (sin el intérprete de Python) podés correr el siguiente
comando para ejecutar todos los tests automáticamente:

    python -m pytest
    
Enjoy!

## Conversión del reporte en markdown a docx

Usamos [subprocess](https://docs.python.org/3/library/subprocess.html) 
de python junto con [pandoc](https://pandoc.org/) para realizar la conversión de
md a docx. Estado de prueba: solamente convierte `template_report.md` y es 
necesario correr `md_to_docx.py` en el mismo lugar que el mencionado .md, dando
por resultado `template_report.docx` también en el mismo directorio.  

## Ejecutar tests

Para correr las tests nos paramos en taiga_report/ y hacemos:

    pytest

Si queremos correr tests específicas podemos usar pytest de la siguiente manera:

    pytest -k "String representativa de la/s test/s que queremos correr, puede 
    ser el nombre de la clase"
    
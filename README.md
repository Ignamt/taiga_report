# Generador de reportes de Taiga

Este programa tiene como finalidad generar reportes de manera automática en base
a las UserStories cargadas en Taiga siguiendo unos lineamientos generales que se
incluyen con el proyecto.

El proyecto está armado con `Python 3.6+`. NO JODAN, ACTUALICENSE.

El proyecto en su estado actual no se puede ejecutar todavía. 

Para poder probar y desarrollarlo, hay que armar un entorno virtual (Venv, que 
viene incluido con Python 3) con el cual se corre. [Tutorial para entornos 
virtuales](https://docs.python-guide.org/dev/virtualenvs/)

Una vez instalado el entorno virtual y activado, instalar las dependencias que 
vienen en el archivo `requirements.txt`. El comando para hacer esto automáticamente
es (en la consola con el venv activado) es:

    cd path\a\donde\clonaste\el\repo
    pip install -r requirements.txt
    
Una vez acá, la mejor forma de ir probando es pararte sobre la carpeta superior
del repo y ejecutar un intérprete de python (o ipython si tenés la posta). Ahí 
podés ir importando los módulos y objetos para explorarlos e interactuar con 
ellos.

También desde este nivel (sin el intérprete de Python) podés correr el siguiente
comando para ejecutar todos los tests automáticamente:

    python -m pytest
    
Enjoy!

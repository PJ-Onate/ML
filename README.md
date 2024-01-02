# ML

2-Después de instalar Docker, ejecutar en terminal "sudo groupadd -f docker"

3-Luego "sudo usermod -aG docker $USER"

4-Después "newgrp docker"

5-Si no tiene interfaz grafica en sus sistema Debian:
	"sudo apt install tasksel"
	"sudo tasksel"
	(elija GNOME y espere instalación)

6-En el terminal de comandos local, ejecute (no con usuario root):
	"xhost +"
	comando que permite el uso del socket X11 a todos los hosts que se conecten via ssh

 9-El proyecto de Git incluye el Dockerfile dentro de Prueba 1. Una vez que el Dockerfile esté nuestro sistema local, vaya a la carpeta donde se encuentra la imagen dentro del terminal 
de Linux y ejecute "docker build -t "nombre_de_imagen" ." (No con usuario root)

9-ejecute "docker run -ti --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix "nombre-imagen"" (No con usuario root)

10-Dentro del contenedor, podremos ejecutar de nuevo git clone https://github.com/PJ-Onate/TESIS_2023.git para "dockerizar" la app. Para iniciar la aplicación, se debe ir a la carpeta 
"Prueba 1" y se debe ejecutar "python3 main.py", e iniciará la aplicación y su interfaz gráfica.


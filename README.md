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

# Partir desde una imagen base de Ubuntu
FROM ubuntu

# Instalar las herramientas necesarias
RUN apt-get update -y 
RUN apt-get install curl -y 
RUN apt-get install python3 -y

# Descargar archivos
COPY archivoacopiar.txt /tmp/archivo.txt
RUN curl https://raw.githubusercontent.com/mdn/learning-area/main/javascript/introduction-to-js-1/assessment-start/raw-text.txt -o raw-text.txt
RUN echo "hola " > prueba.txt

# Sentencia de ejecución que se ejecutará cuando se inicie el contenedor
CMD sh -c "cat prueba.txt && sleep 1000"

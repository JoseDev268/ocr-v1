# Para clonar este proyecto se necesita lo siguiente: 
## Pyhthon >= 10.0.x 
```
git clone https://github.com/JoseDev268/ocr-v1.git
```

### Crear un entorno virtual con venv en el directorio base del proyecto 
```
python virtualvenv p1
.\p1\Scripts\activate
```
### Una vez instalado el entorno virtual procedemos a instalar los requerimientos necesarios.
```pip install flask matplotlib numpy pandas pillow ``` 
### Para evitar breacking changes y error de version se desinstala en el entorno virtual tensorflow
``` pip uninstall -y tensorflow ```

### Se instala biblioteca OCR Doctr ( en mi caso trabajo con la version por PyTORCH)
``` pip install python-doctr[torch,viz]@git+https://github.com/mindee/doctr.git ```

### Para la maquetacion parte del frontend se usó tailwindcss 
```
npm install -D tailwindcss
npx tailwindcss init
```

## Ejecutar el programa 
### En la terminal ejecutar el comando:
``` .\p1\Scripts\activate ``` para ejecutar el entorno virtual
### Levantamos el servidor: 
``` python .\app.py ``` nos redirigira a hacia un entorno local ``Running on http://127.0.0.1:5000``
### abrimos otra terminal paralela para ejecutar tailwind 
```npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch ```



# rucpy
```
$ pip o pip3 install -r requirements.txt
$ Ejecutar la funcion `ImportData` ubicada en ruc.py
$ FLASK_APP=rucapi.py flask run
Go to http://127.0.0.1:5000/api/<CI/RUC> O <nombre/s> o <apellido/s> 
```
# API

La API esta alojada en https://rucs.datospy.org

# Ejemplo de Uso con Javascript
```js
var xhr = new XMLHttpRequest();
var url = 'https://rucs.datospy.org/api/1234567';
xhr.open('GET', url, true);       
xhr.onreadystatechange = function(){
   if (this.readyState == 4 && this.status == 200) {
      console.log(JSON.parse(invocation.responseText))
   }
}
xhr.send() 
```
**Repuesta**
```json
[
  {
    "_id": {"$oid": "5fb46e9694275e426db580bd"}, 
    "documento": "1234567", 
    "dv": "9", 
    "razonsocial": 
    "Nombre Apellido"
  }
]
```
**Obs.** Los datos se actualizan periodicamente.

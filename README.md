### DB Exporter
This project uses flask as web framework to support 
DB exporter aims to get metrics from mariadb database according to configuration and format it as prometheus metric.

---

### Usage
Install python3, then `pip install requirements.txt`

For win:

    set FLASK_APP=app.py
    set FLASK_ENV=development
    set FLASK_DEBUG=1

flask run:  
`flask run --host=0.0.0.0`  
--host=0.0.0.0 允许其他用户访问，如果没有的话，只可以本机访问。

---

### Reference Links
- [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/)
- [Prometheus Python Client with Flask](https://github.com/prometheus/client_python#flask)    
- [DBUtils User's Guide](https://webwareforpython.github.io/DBUtils/main.html)    
- [PEP 249 -- Python Database API Specification v2.0](https://www.python.org/dev/peps/pep-0249/)
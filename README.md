<!-- start backend -->

uvicorn app:app --reload

<!-- start frontend -->

navigate to new terminal containing index.html

```
python -m http.server 8001
```

Access the frontend at http://localhost:8001/index.html
cmd + shift + r to force reload

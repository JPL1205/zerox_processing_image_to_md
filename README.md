<!-- start backend -->

uvicorn app:app --reload

<!-- start frontend -->

navigate to new terminal containing index.html

```
python -m http.server 8001
```

Access the frontend at http://127.0.0.1:8001

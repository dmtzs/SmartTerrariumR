try:
    from flask import render_template
except ImportError as eImp:
    print(f"Ocurrió el error de importación: {eImp}")

# ------------------Admin routes------------------
# Below routes
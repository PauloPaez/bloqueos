rsync -av \
--exclude=node_modules \
--exclude=venv \
--exclude=.venv \
--exclude=.env \
--exclude=__pycache__ \
--exclude='*.py[cod]' \
--exclude='.pytest_cache' \
--exclude='.mypy_cache' \
back fastapi-user@10.2.133.193:/home/fastapi-user/testBloqueos

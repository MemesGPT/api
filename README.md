
# MemesGPT API
[![CI](https://github.com/MemesGPT/api/actions/workflows/tests.yml/badge.svg?branch=developer)](https://github.com/MemesGPT/api/actions/workflows/tests.yml)
### Запустить Dev локально

```bash
cp docker/compose/.env.dev docker/compose/.env
vi docker/compose/.env  # добавить значения переменных
cd ./backend
make init
make dev-server-start
```
риквайрементс:
- Python3.11
- poetry

свагер будет примерно тут:  
http://localhost:8081/docs

---

### Запуск приложения на докерах локально

требуется докер и докер-компоуз на машине

```bash
cd ./docker
make dev-build
make dev-start
```
свагер будет примерно тут:  
http://localhost:8081/docs

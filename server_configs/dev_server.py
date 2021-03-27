import uvicorn
import os


def export_variables(filename):
    with open(filename, mode='r') as env_file:
        for line in env_file.readlines():
            row = line.partition('=')
            os.environ[row[0]] = row[2].rstrip("\n")


if __name__ == '__main__':
    export_variables('.env')
    uvicorn.run("server_configs.asgi:app", loop="uvloop", reload=True, host="0.0.0.0", port=8000)


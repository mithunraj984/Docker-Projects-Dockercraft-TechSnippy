import os
import subprocess

def setup_minecraft_server(minecraft_version, memory_limit):
    os.makedirs('docker-craft', exist_ok=True)

    clone_repo_command = 'git clone https://github.com/BretFisher/docker-craft.git'
    subprocess.run(clone_repo_command, shell=True, check=True)

    with open('docker-craft/Dockerfile', 'w') as dockerfile:
        dockerfile.write(f'''
        FROM bretfisher/java-node
        RUN curl -L https://github.com/Bukkit/mc-dev-server/archive/refs/tags/{minecraft_version}.tar.gz | tar xzf - -C /mc-dev-server --strip-components=1
        RUN ln -s /mc-dev-server /mc
        EXPOSE 25565
        CMD ["java", "-Xmx{memory_limit}M", "-jar", "/mc-dev-server/target/mc-dev-server.jar", "nogui"]
        ''')

    build_docker_image_command = 'docker build -t minecraft-server:latest .'
    subprocess.run(build_docker_image_command, shell=True, check=True, cwd='docker-craft')

    run_docker_container_command = 'docker run -d -p 25565:25565 --name minecraft-server minecraft-server:latest'
    subprocess.run(run_docker_container_command, shell=True, check=True, cwd='docker-craft')


setup_minecraft_server('1.17.1', '1024')
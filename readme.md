Running Zato with Docker
Step 1: Pull and Run the Zato Container
To start a Zato container, use the following command in your terminal:

```bash
sudo docker run --pull=always -it --rm \
-p 22022:22 -p 8183:8183 -p 11223:11223 -p 17010:17010 \
--name zato-3.2-quickstart -e Zato_Log_Env_Details=True \
ghcr.io/zatosource/zato-3.2-quickstart
```

This command does several things:

    Pulls the latest Zato image from the GitHub Container Registry.
    Maps ports for SSH (22022), the web dashboard (8183), and other necessary services.
    Names the container zato-3.2-quickstart for easy reference.

Step 2: Accessing the Zato Dashboard
Once the container is running, you can access the Zato dashboard by navigating to http://localhost:8183 in your web browser. The default login credentials are:

    Username: admin
    Password: You will find this in the container's environment details2
    .

Step 3: SSH into the Container
To manage the Zato instance or perform administrative tasks, you can SSH into the container using:

bash
ssh zato@localhost -p 22022

The password for SSH access can also be found in the environment details file within the container2
.
Step 4: Customizing Your Environment
If you need to install additional Python libraries or customize your configuration:

    Create a requirements.txt file locally with your desired packages.
    Use a bind mount to map this file into the container during startup:

bash
sudo docker run \
--rm \
--name zato \
--pull=always \
-p 22022:22 \
-p 8183:8183 \
-p 17010:17010 \
--mount type=bind,source=/path/to/your/requirements.txt,target=/opt/hot-deploy/python-reqs/requirements.txt \
ghcr.io/zatosource/zato-3.2-quickstart

Replace /path/to/your/requirements.txt with the actual path to your requirements file on your local machine1
2
.
Step 5: Stopping and Restarting the Container
If you need to stop the container, use:

bash
sudo docker stop zato-3.2-quickstart

To restart it, simply run the initial docker run command again.
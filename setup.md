### 1. Keycloak

#### Steps
1. Start a new detached screen session for Keycloak:
   ```bash
   screen -S keycloak
   ```
2. Navigate to the Keycloak installation directory:
   ```bash
   cd /opt/keycloak/bin
   ```
3. Start Keycloak in development mode:
   ```bash
   ./kc.sh start-dev
   ```
   
### 2. Long-Range Communicator

#### Steps
1. Go to the setup directory:
   ```bash
   cd /TheShip/setup
   ```
2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
3. Set the `PYTHONPATH` to include the application directory:
   ```bash
   export PYTHONPATH=$PYTHONPATH:/TheShip
   ```

### 3. MinIO

#### Steps
1. Start the MinIO server:
   ```bash
   minio server /home/shared --console-address :9090 --address :2016
   ```

### 4. MongoDB

#### Steps
1. Start the MongoDB service:
   ```bash
   sudo systemctl start mongod
   ```
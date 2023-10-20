
# DreamCraft
- A Minecraft Server for DreamCraft Result Visualization
- New York University | Game Innovation Lab

## 1. How to Install to Minecraft (Windows Version)

### Download Minecraft
You need to have a Microsoft account that has purchased Minecraft (not free version, because you need `multiplayer` feature)

Download `Minecraft Launcher` and `Minecraft Java Edition`
  - Suggest directly download it from official website of [Minecraft](https://www.minecraft.net/en-us/download-dungeons)
  - Do not directly download from Microsoft or Xbox!
- You also need to install [Java8](https://www.java.com/download/ie_manual.jsp) in your computer


### Install Compatible Version
`Minecraft Java Edition` **MUST** have a **compatible version** ()
  1. `Installations`
  2. `New`
  3. Give it a name
  4. Select version **1.12.2**
  5. `Create`

You can reference this [link](https://help.minecraft.net/hc/en-us/articles/360034754852-Change-Game-Version-for-Minecraft-Java-Edition#:~:text=Click%20Installations%20on%20the%20launcher,Play%20on%20the%20top%20menu.) to see how to install different version of Minecraft

### Launch Server and Connect

Launch server: `java -jar spongevanilla-1.12.2-7.3.0.jar` (we will introduce it in the later section).

Open **Minecraft Java version**, under the `Multiplayer` selection, add the server: `localhost`.

Login and you are connected to the [Evocraft](https://github.com/real-itu/Evocraft-py) server.

## 2. How to Launch the Server
### Server Initialization
You have to follow the README of [Evocraft](https://github.com/real-itu/Evocraft-py) to correctly initialize the server.

### Launch the Server
The majority of the server source files are contained in the `server` code. After initialization, you will get many new files.

Under the root directory, enter the `server` folder and execute `java -jar spongevanilla-1.12.2-7.3.0.jar`.

This can be written as the terminal command: 

```
cd server
java -jar spongevanilla-1.12.2-7.3.0.jar 
```
### Execute Server Commands

Evocraft supports multiple commands to set up Minecraft environment.

After you successfully launch Minecraft Server, you can enter `\help` to check different commands. Evocraft README also contains some common
 commands.

### Execute Python code
Evocraft supports executing python code. When you launch the server, you can open up a new terminal to execute the python code.

```
python <your_python_file_name>.py
```

You can also check Evocraft README to get the idea of how to write your own python code.

### Reset Server Environment

To reset the server. Execute the `reset_server.py`.
```
python server/reset_server.py
```



## 3. How to Generate Data in Minecraft

### Collect the data
Download your training data `<name>.npz` from the [training repo](https://github.com/smearle/dreamcraft).

Copy and paste them under the `object_data` folder.




## 4. How to Record a Video of the Result




## Data generation
Make sure you have java installed, then launch a modded Minecraft server with:
```
cd server
java -jar spongevanilla-1.12.2-7.3.0.jar 
``` 

Now open minecraft. Download and install version `1.12.2`. Launch the game, select Multiplayer, Direct Connect, and join the server `localhost`.

Now you can run:
```
python clients/python/data_gen.py
```
This will generate a dataset of [screenshot <--> block layout] pairs by teleporting your player around the map in a square spiral, recording a chunk of blocks roughly in front of you, then taking a screenshot.

The latter is done very hackishly via screen captures. You will need to tweak `BBOX` in this script to ensure the screenshots contain your Minecraft window, which you will want to stick in, e.g., the top-left corner of your screen. For Mac users, you can press `cmd`+`shift`+`4` to enter screenshot mode, then put the mouse at the bottom right of the Minecraft window to have the coordinates in pixels displayed.



Change `options.text`, (in your minecraft directory. Mac OS: `~/Library/Application Support/minecraft/options.txt`), settings `OverrideWidth:512` and `OverrideHeight:512` so that we collect screenshots of an approriate size. You'll probably also want to edit the line `pauseOnLostFocus:false` so that you can change focus from the Minecraft client while collecting data, without bringing up the pause screen.

You will also need to change the name of the player being teleported around in `MinecraftRPC.java` to match your player name (or change your player name to "boopchie"). See "Build the Minecraft Mod" below.

## Training
_Under construction_

```
python train.py
```

We use hydra. The config can be found at `conf/config.yaml`

**TODO: Checkpointing, validation, loading, etc.**

See below for details about how we have hacked `minecraft-rpc` to interact with a modded Minecraft server via python.

## How to Add new Python Command (Minecraft RPC)

This is adoped by A [gRPC](https://grpc.io) interface for Minecraft. 


We will be editing `./src/main/proto/minecraft.proto` and `./src/main/java/dk/itu/real/ooe/services/MinecraftService.java`, to add new python commands via which we can interact with our modded Minecraft server. (E.g., we'd like to have a command to remove all collectible items, and add certain block types.) We will test functionality in `clients/python/example.py`.


## Install Dependencies

### Java (for building the mod)
* Install Java 1.8 (You can check your version with `java -version`)
  * unix: `sudo apt-get install openjdk-8-jre`
  * osx: [mkyong.com/java/how-to-install-java-on-mac-osx](https://mkyong.com/java/how-to-install-java-on-mac-osx/)  

### Python (for compiling grpc)
After creating a new conda environment, install dependencies:
```
python -m pip install grpcio
python -m pip install grpcio-tools
```

## Build the Minecraft Mod
Modify the mod:
* Go to `./src/main/java/dk/itu/real/ooe/services/MinecraftService.java`
* Overwrite your favorite function :D
* Build the minecraft mod as a jar:
```
mvn install
```
The `minecraft-rpc-0.0.5.jar` will be available in `target/` after this. Put this `jar` file inside `./server/mods`
```
mv target/minecraft-rpc-0.0.5.jar server/mods/
```

## Overwrite and Compile the grpc script (python api)
* Add your favorite Minecraft item in `./minecraft-rpc/src/main/proto/minecraft.proto`
* Navigate to the `./` of this repo. Then generate the grpc python files as follow:
```
python -m grpc_tools.protoc -I./ --python_out=./clients/python/ --grpc_python_out=./clients/python/ ./src/main/proto/minecraft.proto
```
The `minecraft_pb2_grpc.py` and `minecraft_pb2.py` will be available in `./clients/python/src/main/proto` folder. You can copy them into the folder in which you place the `mc_render.py` (or any other python script you're working on).


## One-line compilation

Alternatively, here is a one-line command for rebuilding the mode after changes are made:
```
python -m grpc_tools.protoc -I./ --python_out=./clients/python/ --grpc_python_out=./clients/python/ ./src/main/proto/minecraft.proto && mvn install && mv target/minecraft-rpc-0.0.5.jar server/mods/
```


## Run 
* Go to `./server`
* Start the server with 
```
java -jar spongevanilla-1.12.2-7.3.0.jar
```
* The first time you start the server you must accept the Minecraft EULA by modifying eula.txt
* You can change the properties of the world by modifying `server.properties`
* You should see a bunch of output including `[... INFO] [minecraft_rpc]: Listening on 5001`. 
This means it's working and the server is ready for commands on port 5001.

Note that if you run `java -jar ./server/spongevanilla-1.12.2-7.3.0.jar` inside the `./` folder, new `eula.txt` and `server.properties` will be generated and applied. So we recommand you not being too lazy to go to `./server` folder :D


# Reference 
For more information, see [Evocraft](https://github.com/real-itu/Evocraft-py) and the original [Minecraft RPC](https://github.com/real-itu/minecraft-rpc)
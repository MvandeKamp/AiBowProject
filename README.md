Running this on your own:

Setting up a Minecraft Forge Development Environment is quite challenging if you are not well versed in gradle.

Going with Intelji is quite recommended. Ecplises Gradle integration is a pain.

Here is a full guide from their Docs: https://docs.minecraftforge.net/en/1.20.x/gettingstarted/

Traningprocess runs via Python. Communication is done via gRPC.

Inference not setupped nor planned because its just used for research purposes.

If your IDE is fully functional -> No Erros while running gradle sync changes

You can build the mod via gradle -> shadow -> shadowjar after that install forge 1.21 and put the mod inside the default .minecraft/mods folder.

Some setup is needed with RunClients.py to use the locally aviable instance of Minecraft and a valid Minecraft Token.

Also a void world is required and the Player needs to be positioned at 0 60 0 with a bow in the first inventory slot. 

Place the world Path under Runclients.py => original_world_dir variable

Via IDE use the run config for the main.py if you setupped a valid Python venv with all required packages. Or create your own run config with your local python installation.

Execute your main.py run config. After that start the RunClients.py. If everything is setupped corretly the trainingsprocess should start automagically.

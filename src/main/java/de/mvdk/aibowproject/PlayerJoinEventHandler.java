package de.mvdk.aibowproject;

import net.minecraftforge.event.entity.player.PlayerEvent.PlayerLoggedInEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber
public class PlayerJoinEventHandler {
    public  PlayerJoinEventHandler(TargetManager targetManager) {
        this.targetManager = targetManager;
    }
    private TargetManager targetManager;

    @SubscribeEvent
    public void onPlayerLoggedIn(PlayerLoggedInEvent event) {
        targetManager.Start(event);
    }
}
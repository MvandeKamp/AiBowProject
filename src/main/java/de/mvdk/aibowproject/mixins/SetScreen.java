package de.mvdk.aibowproject.mixins;

import com.mojang.serialization.Dynamic;
import net.minecraft.Util;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.TitleScreen;
import net.minecraft.client.resources.server.DownloadedPackSource;
import net.minecraft.commands.Commands;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.Registries;
import net.minecraft.server.WorldLoader;
import net.minecraft.server.WorldStem;
import net.minecraft.server.packs.repository.PackRepository;
import net.minecraft.server.packs.repository.ServerPacksSource;
import net.minecraft.world.level.dimension.LevelStem;
import net.minecraft.world.level.storage.LevelDataAndDimensions;
import net.minecraft.world.level.storage.LevelResource;
import net.minecraft.world.level.storage.LevelStorageSource;
import net.minecraft.world.level.storage.LevelSummary;
import org.jetbrains.annotations.Nullable;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;

@Mixin(Minecraft.class)
public abstract class SetScreen {

    @Shadow
    public abstract boolean allowsMultiplayer();

    @Unique
    private static boolean wasLoaded;

    @Inject(method = "setScreen", at = @At("TAIL"))
    private void autoLoadLevel(@Nullable Screen screen, CallbackInfo info) throws IOException, InterruptedException {
        if (screen instanceof TitleScreen && !wasLoaded) {
            wasLoaded = true;

            Minecraft client = Minecraft.getInstance();
            if (client != null && client.getLevelSource().levelExists("aiTrain")) {
                try {
                    LevelStorageSource.LevelStorageAccess access = client.getLevelSource().createAccess("aiTrain");

                    Dynamic<?> dynamic;
                    LevelSummary levelsummary;

                    dynamic = access.getDataTag();
                    levelsummary = access.getSummary(dynamic);
                    PackRepository packrepository = ServerPacksSource.createPackRepository(access);

                    WorldLoader.PackConfig worldloader$packconfig = LevelStorageSource.getPackConfig(dynamic, packrepository, false);

                    WorldStem stem = loadWorldDataBlocking(worldloader$packconfig, p_308270_ -> {
                        Registry<LevelStem> registry = p_308270_.datapackDimensions().registryOrThrow(Registries.LEVEL_STEM);
                        LevelDataAndDimensions leveldataanddimensions = LevelStorageSource.getLevelDataAndDimensions(dynamic, p_308270_.dataConfiguration(), registry, p_308270_.datapackWorldgen());
                        return new WorldLoader.DataLoadOutput<>(leveldataanddimensions.worldData(), leveldataanddimensions.dimensions().dimensionsRegistryAccess());
                    }, WorldStem::new);

                    for (LevelStem levelstem : stem.registries().compositeAccess().registryOrThrow(Registries.LEVEL_STEM)) {
                        levelstem.generator().validate();
                    }

                    DownloadedPackSource downloadedpacksource = client.getDownloadedPackSource();

                    this.loadBundledResourcePack(downloadedpacksource, access).thenApply(p_233177_ -> true).thenAcceptAsync(p_325451_ -> {
                        if (p_325451_) {
                            client.doWorldLoad(access, packrepository, stem, false);
                        } else {
                            downloadedpacksource.popAll();
                            stem.close();
                            access.safeClose();
                        }
                    });
                    client.doWorldLoad(access, packrepository, stem, false);

                } catch (IOException e) {
                    throw new RuntimeException(e);
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }
            }
        }

    }

    private <D, R> R loadWorldDataBlocking(WorldLoader.PackConfig p_250997_, WorldLoader.WorldDataSupplier<D> p_251759_, WorldLoader.ResultFactory<D, R> p_249635_) throws Exception {
        Minecraft minecraft = Minecraft.getInstance();

        WorldLoader.InitConfig worldloader$initconfig = new WorldLoader.InitConfig(p_250997_, Commands.CommandSelection.INTEGRATED, 2);
        CompletableFuture<R> completablefuture = WorldLoader.load(worldloader$initconfig, p_251759_, p_249635_, Util.backgroundExecutor(), minecraft);
        minecraft.managedBlock(completablefuture::isDone);
        return completablefuture.get();
    }
    private static final UUID WORLD_PACK_ID
            = UUID. fromString("640a6a92-b6cb-48a0-b391-831586500359");
    private CompletableFuture<Void> loadBundledResourcePack(DownloadedPackSource p_312230_, LevelStorageSource.LevelStorageAccess p_310544_) {
        Path path = p_310544_.getLevelPath(LevelResource.MAP_RESOURCE_FILE);
        if (Files.exists(path) && !Files.isDirectory(path)) {
            p_312230_.configureForLocalWorld();
            CompletableFuture<Void> completablefuture = p_312230_.waitForPackFeedback(WORLD_PACK_ID);
            p_312230_.pushLocalPack(WORLD_PACK_ID, path);
            return completablefuture;
        } else {
            return CompletableFuture.completedFuture(null);
        }
    }
}
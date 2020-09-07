package dk.itu_real.open_evolution.MinecraftExtendedCommands;

import org.spongepowered.api.plugin.Plugin;
import org.spongepowered.api.text.Text;
import org.spongepowered.api.Game;
import org.spongepowered.api.command.args.GenericArguments;
import org.spongepowered.api.command.spec.CommandSpec;
import org.spongepowered.api.event.Listener;
import org.spongepowered.api.event.game.state.GamePreInitializationEvent;

import dk.itu_real.open_evolution.MinecraftExtendedCommands.command.GetBlockTypeAt;
import dk.itu_real.open_evolution.MinecraftExtendedCommands.command.GetTaggedAecCoordinate;
import dk.itu_real.open_evolution.MinecraftExtendedCommands.command.AddAecAtCoordinate;
import dk.itu_real.open_evolution.MinecraftExtendedCommands.command.BulkBlockSet;
import dk.itu_real.open_evolution.MinecraftExtendedCommands.command.DeleteTaggedAec;

// Imports for logger
import com.google.inject.Inject;

import java.util.HashMap;
import java.util.Map;
import org.spongepowered.api.entity.Entity;
import java.util.UUID;

import org.slf4j.Logger;

@Plugin(id = "minecraft_extended_commands", name = "Minecraft Extended Commands", version = "1.0", description = "Adding extra commands to help Python")

public class MinecraftExtendedCommands {
    @Inject
    private Game game;
    @Inject
    private Logger logger;
    
    private Map<Text, UUID> entity_dict;

    /**
     * Called on server startup.
     * 
     * @param event The server startup event
     */
    @Listener
    public void onPreInitialization(GamePreInitializationEvent event) {

    	this.entity_dict = new HashMap<Text, UUID>();
    	
        // get_block_type command
        CommandSpec getBlockTypeCommand = CommandSpec.builder()
        .permission("extended_block_api.read")
        .arguments(GenericArguments.onlyOne(GenericArguments.location(Text.of("location"))))
        .description(Text.of("Get block type from a coordinate"))
        .extendedDescription(Text.of("Gets the type of block at the specified coordinate"))
        .executor(new GetBlockTypeAt(logger)) // <-- command logic is in there
        .build();

        // Register the blockType-at-coordinate command
        this.game.getCommandManager().register(this, getBlockTypeCommand, "get_block_type");
        
        // get_block_type command
        CommandSpec getEntityCommand = CommandSpec.builder()
        .permission("extended_block_api.read")
        .arguments(GenericArguments.onlyOne(GenericArguments.string(Text.of("entity_tag"))), GenericArguments.onlyOne(GenericArguments.location(Text.of("location"))))
        .description(Text.of("Add an AEC"))
        .extendedDescription(Text.of("Add the tag to the block at the "))
        .executor(new AddAecAtCoordinate(logger, entity_dict)) // <-- command logic is in there
        .build();
        
        // Register the entity-at-coordinate command
        this.game.getCommandManager().register(this, getEntityCommand, "tag_coord");
        
        // get_tagged_aec Coordinate
        CommandSpec getTaggedAecCoordinaesCommand = CommandSpec.builder()
        		.permission("extended_block_api.read")
        		.arguments(GenericArguments.onlyOne(GenericArguments.string(Text.of("entity_tag"))))
        		.description(Text.of("Get AEC coordinate"))
        		.extendedDescription(Text.of("Get the tagged AEC coordinate"))
        		.executor(new GetTaggedAecCoordinate(logger, entity_dict))
        		.build();
        
        // Register get_tagged_aec coordinate
        this.game.getCommandManager().register(this, getTaggedAecCoordinaesCommand, "get_tagged_aec_coordinate");
        
        // Delete_tag
        CommandSpec deleteEntityTag = CommandSpec.builder()
        		.permission("extended_block_api_read")
        		.arguments(GenericArguments.onlyOne(GenericArguments.string(Text.of("entity_tag"))), GenericArguments.string(Text.of("new_block_type")))
        		.description(Text.of("Remove the AEC by tag"))
        		.extendedDescription(Text.of("Provide a tag and the AEC entity that will be deleted"))
        		.executor(new DeleteTaggedAec(logger, this.entity_dict))
        		.build();
        
        // Register delete_tagged_aec
        this.game.getCommandManager().register(this, deleteEntityTag, "delete_tagged_aec");
        
        CommandSpec bulkSetBlock = CommandSpec.builder()
        		.permission("extended_block_api_read")
        		.arguments(GenericArguments.onlyOne(GenericArguments.string(Text.of("json_package"))))
        		.description(Text.of("Send a bulk of blocks and place them server-side"))
        		.extendedDescription(Text.of("Send a bulk of blocks and place them server-side by sending a JSON string over MCRcon"))
        		.executor(new BulkBlockSet(logger))
        		.build();
        
        this.game.getCommandManager().register(this, bulkSetBlock, "bulk_set_block");
        

    }
}

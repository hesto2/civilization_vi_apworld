import asyncio
import logging
import traceback
from typing import Dict, List

from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, logger, server_loop, gui_enabled
from NetUtils import ClientStatus, NetworkItem
import Utils
from .CivVIInterface import CivVIInterface
from .Enum import CivVICheckType
from .Items import CivVIItemData, generate_item_table
from .Locations import generate_era_location_table
from .ProgressiveItems import get_progressive_items
from .TunerClient import TunerErrorException


class CivVICommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_deathlink(self):
        """Toggle deathlink from client. Overrides default setting."""
        if isinstance(self.ctx, CivVIContext):
            new_value = True
            if (self.tags["DeathLink"]):
                new_value = False
            Utils.async_start(self.ctx.update_death_link(
                new_value), name="Update Deathlink")

    def _cmd_resync(self):
        """Resends all items to client, and has client resend all locations to server. This can take up to a minute if the player has received a lot of items"""
        if isinstance(self.ctx, CivVIContext):
            logger.info("Resyncing...")
            asyncio.create_task(self.ctx.resync())


class CivVIContext(CommonContext):
    is_pending_death_link_reset = False
    command_processor = CivVICommandProcessor
    game = "Civilization VI"
    items_handling = 0b111
    tuner_sync_task = None
    game_interface: CivVIInterface
    location_name_to_civ_location = {}
    location_name_to_id = {}
    item_id_to_civ_item: Dict[int, CivVIItemData] = {}
    item_table: Dict[str, CivVIItemData] = {}
    processing_multiple_items = False
    disconnected = False
    progressive_items_by_type = get_progressive_items()
    item_name_to_id = {
        item.name: item.code for item in generate_item_table().values()}

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game_interface = CivVIInterface(logger)
        location_by_era = generate_era_location_table()
        self.item_table = generate_item_table()

        # Get tables formatted in a way that is easier to use here
        for era, locations in location_by_era.items():
            for item_name, location in locations.items():
                self.location_name_to_id[location.name] = location.code
                self.location_name_to_civ_location[location.name] = location

        for item_name, item in self.item_table.items():
            self.item_id_to_civ_item[item.code] = item

    async def resync(self):
        if self.processing_multiple_items:
            logger.info(
                "Waiting for items to finish processing, try again later")
            return
        await self.game_interface.resync()
        await handle_receive_items(self, -1)
        logger.info("Resynced")

    def on_deathlink(self, data: Utils.Dict[str, Utils.Any]) -> None:
        super().on_deathlink(data)
        # TODO: Implement deathlink handling

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(CivVIContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            if "death_link" in args["slot_data"]:
                Utils.async_start(self.update_death_link(
                    bool(args["slot_data"]["death_link"])))


async def tuner_sync_task(ctx: CivVIContext):
    logger.info("Starting CivVI connector")
    while not ctx.exit_event.is_set():
        try:
            if ctx.processing_multiple_items == True:
                logger.debug("Waiting for items to finish processing")
                await asyncio.sleep(3)
            elif await ctx.game_interface.is_in_game():
                await _handle_game_ready(ctx)
            else:
                await asyncio.sleep(3)
        except Exception as e:
            if isinstance(e, TunerErrorException):
                logger.error(str(e))
            else:
                logger.error(traceback.format_exc())

            logger.info("Attempting to reconnect to Civ VI...")
            ctx.disconnected = True
            await asyncio.sleep(3)
            continue


async def handle_checked_location(ctx: CivVIContext):
    checked_locations = await ctx.game_interface.get_checked_locations()
    checked_location_ids = [location.code for location_name, location in ctx.location_name_to_civ_location.items(
    ) if location_name in checked_locations]

    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": checked_location_ids}])


async def handle_receive_items(ctx: CivVIContext, last_received_index_override: int = None):
    try:
        last_received_index = last_received_index_override or await ctx.game_interface.get_last_received_index()
        if len(ctx.items_received) - last_received_index > 1:
            logger.debug("Multiple items received")
            ctx.processing_multiple_items = True

        # Handle non progressive items
        progressive_items: List[CivVIItemData] = []
        for index, network_item in enumerate(ctx.items_received):

            item: CivVIItemData = ctx.item_id_to_civ_item[network_item.item]
            if index > last_received_index:
                if item.item_type == CivVICheckType.PROGRESSIVE:
                    # if the item is progressive, then check how far in that progression type we are and send the appropriate item
                    count = sum(
                        1 for count_item in progressive_items if count_item.name == item.name)

                    if count >= len(ctx.progressive_items_by_type[item.name]):
                        logger.error(
                            f"Received more progressive items than expected for {item.name}")
                        continue

                    item_name = ctx.progressive_items_by_type[item.name][count]
                    item = ctx.item_table[item_name]

                sender = ctx.player_names[network_item.player]
                await ctx.game_interface.give_item_to_player(item, sender)
                await asyncio.sleep(0.02)

            if item.item_type == CivVICheckType.PROGRESSIVE:
                progressive_items.append(item)

        if ctx.processing_multiple_items:
            logger.debug("DONE")
        ctx.processing_multiple_items = False
    finally:
        # If something errors out, then unblock item processing
        ctx.processing_multiple_items = False


async def handle_check_goal_complete(ctx: CivVIContext):
    # logger.debug("Sending Goal Complete")
    result = await ctx.game_interface.check_victory()
    if result:
        logger.info("Sending Victory to server!")
        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])


async def handle_check_deathlink(ctx: CivVIContext):
    # TODO: Implement deathlink handling
    pass


async def _handle_game_ready(ctx: CivVIContext):
    if ctx.server:
        if not ctx.slot:
            await asyncio.sleep(3)
            return
        if ctx.disconnected == True:
            ctx.disconnected = False
            logger.info("Reconnected to Civ VI")
        await handle_receive_items(ctx)
        await handle_checked_location(ctx)
        await handle_check_goal_complete(ctx)

        if "DeathLink" in ctx.tags:
            await handle_check_deathlink(ctx)
        await asyncio.sleep(3)
    else:
        logger.info("Waiting for player to connect to server")
        await asyncio.sleep(3)


def main(connect=None, password=None, name=None):
    Utils.init_logging("Civilization VI Client")

    async def _main(connect, password, name):
        ctx = CivVIContext(connect, password)
        ctx.auth = name
        ctx.server_task = asyncio.create_task(
            server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        await asyncio.sleep(1)

        ctx.tuner_sync_task = asyncio.create_task(
            tuner_sync_task(ctx), name="DolphinSync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.tuner_sync_task:
            await asyncio.sleep(3)
            await ctx.tuner_sync_task

    import colorama

    colorama.init()
    asyncio.run(_main(connect, password, name))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser()
    parser.add_argument('--name', default=None,
                        help="Slot Name to connect as.")
    args = parser.parse_args()
    logger.setLevel(logging.DEBUG)
    main(args.connect, args.password, args.name)

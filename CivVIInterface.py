from logging import Logger
from typing import List

from .Items import CivVIItemData
from .TunerClient import TunerClient, TunerConnectionException, TunerTimeoutException


class CivVIInterface:
    logger: Logger
    tuner: TunerClient

    def __init__(self, logger: Logger):
        self.logger = logger
        self.tuner = TunerClient(logger)

    async def is_in_game(self) -> bool:
        command = "IsInGame()"
        try:
            result = await self.tuner.send_game_command(command)
            return result == "true"
        except TunerTimeoutException:
            self.logger.info(
                "Not connected to game, waiting for connection to be available")
            return False
        except TunerConnectionException as e:
            if "The remote computer refused the network connection" in str(e):
                self.logger.info(
                    "Unable to connect to game. Verify that the tuner is enabled")
            else:
                self.logger.info(
                    "Not connected to game, waiting for connection to be available")
            return False
        except Exception as e:
            if "attempt to index a nil valuestack traceback" in str(e) \
                    or ".. is not supported for string .. nilstack traceback" in str(e):
                self.logger.info(
                    "Connected to game,  waiting for game to start")
                return False

    async def give_item_to_player(self, item: CivVIItemData, sender: str = ""):
      # fmt: off
        command = f"HandleReceiveItem({item.civ_vi_id}, \"{item.name}\", \"{item.item_type.value}\", \"{sender}\")"
      # fmt: on
        await self.tuner.send_game_command(command)

    async def resync(self) -> None:
        """Has the client resend all the checked locations"""
        command = "Resync()"
        await self.tuner.send_game_command(command)

    async def check_victory(self) -> bool:
        command = "ClientGetVictory()"
        result = await self.tuner.send_game_command(command)
        return result == "true"

    async def get_checked_locations(self) -> List[str]:
        command = "GetUnsentCheckedLocations()"
        result = await self.tuner.send_game_command(command, 1024 * 4)
        return result.split(",")

    async def get_deathlink(self) -> str:
        """returns either "false" or the name of the unit that killed the player's unit"""
        command = "ClientGetDeathLink()"
        result = await self.tuner.send_game_command(command)
        return result

    async def kill_unit(self, message: str) -> None:
        command = f"KillUnit(\"{message}\")"
        await self.tuner.send_game_command(command)

    async def get_last_received_index(self) -> int:
        command = "ClientGetLastReceivedIndex()"
        result = await self.tuner.send_game_command(command)
        return int(result)

    async def send_notification(self, item: CivVIItemData, sender="someone") -> None:
        # fmt: off
        command = f"GameCore.NotificationManager:SendNotification(GameCore.NotificationTypes.USER_DEFINED_2, \"{item.name} Received\", \"You have received {item.name} from \" .. \"{sender}\", 0, {item.civ_vi_id})"
        # fmt: on
        await self.tuner.send_command(command)

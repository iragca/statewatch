from typing import override

import questionary

from .menu import Menu
from .asset_manager import AssetManagerMenu


class RootMenu(Menu):
    menu_name = "Main Menu"

    @override
    def menu(self) -> None:
        previous_choice = None
        while True:
            menu_option = questionary.select(
                self.breadcrumbs,
                choices=[
                    "🔙 Exit",
                    "Manage Assets",
                ],
                default=previous_choice,
            ).ask()

            if menu_option is None or menu_option.startswith("🔙"):
                break
            previous_choice = menu_option

            match menu_option:
                case "Manage Assets":
                    AssetManagerMenu(parent=self.menu_name)()
                case _:
                    print("Exiting application.")
                    break

import questionary

from .menu import Menu


class AssetManagerMenu(Menu):
    menu_name = "Manage Assets"

    def __init__(self, parent: str | None = None) -> None:
        self.parent_name = parent

    def menu(self) -> None:
        previous_choice = None
        while True:
            char_nav = questionary.select(
                self.breadcrumbs,
                choices=[
                    f"🔙 Back to {self.parent_name}",
                    "Add Asset",
                ],
                default=previous_choice,
            ).ask()
            if char_nav is None or char_nav.startswith("🔙"):
                break

            previous_choice = char_nav

            match char_nav:
                case "Add Asset":
                    self.add_asset()
                case _:
                    break

    def add_asset(self) -> None:
        pass

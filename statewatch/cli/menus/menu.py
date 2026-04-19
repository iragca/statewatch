class Menu:
    menu_name = "Generic Menu"
    parent_name = None

    def __call__(self, parent_breadcrumbs: list[str] = []) -> None:
        self.breadcrumb_path = parent_breadcrumbs + [self.menu_name]
        self.menu()

    def menu(self) -> None:
        """Override this method to implement the menu logic."""
        pass

    @property
    def breadcrumbs(self) -> str:
        return " > ".join(self.breadcrumb_path)

import customtkinter


class WelcomeScreen(customtkinter.CTk):
    """Welcome screen class"""

    def __init__(self, app_callback) -> None:
        """Initialize the welcome screen"""

        super().__init__()

        self.app_callback = app_callback
        self.title("Synapse")
        self.geometry("400x250")
        self.center_window(400, 250)

        self.label = customtkinter.CTkLabel(
            self, text="Welcome to Synapse!", font=("Arial", 26, "bold")
        )
        self.label.pack(pady=20)

        self.welcome_message = customtkinter.CTkLabel(
            self,
            text="Explore the capabilities of MindsDB\nwith our interactive playground.",
            font=("Arial", 16),
        )
        self.welcome_message.pack(pady=20)

        self.start_button = customtkinter.CTkButton(
            self,
            text="Start Exploring",
            command=self.start_app,
            height=40,
            font=("Arial", 14, "bold"),
        )
        self.start_button.pack(pady=20)

        self.after(5000, self.start_app)  # Automatically start after 5 seconds

    def start_app(self):
        """Start the main application"""
        self.destroy()
        self.app_callback()

    def center_window(self, width, height) -> None:
        """Center the window on the screen

        Args:
            width (int): The width of the window
            height (int): The height of the window
        """
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

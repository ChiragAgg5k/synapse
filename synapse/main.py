import customtkinter

from chatapp import ChatApp
from welcome_screen import WelcomeScreen

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


def start_main_app():
    """Start the main chat application"""
    app = ChatApp()
    app.mainloop()


if __name__ == "__main__":
    welcome_screen = WelcomeScreen(start_main_app)
    welcome_screen.mainloop()

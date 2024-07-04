import customtkinter
import mindsdb_sdk
import mindsdb_sdk.databases
import pandas as pd

server = mindsdb_sdk.connect()
project = server.get_project("mindsdb")
model = server.get_model("openai_model")


def list_models():
    res = []
    for model in server.list_models():
        res.append(model.name)
    return res


class ChatApp(customtkinter.CTk):
    """Main application class"""

    def __init__(self) -> None:
        """Initialize the application"""

        super().__init__()

        self.title("Synapse - General Room")
        self.geometry("805x300")
        self.center_window(805, 300)

        self.current_model = "openai_model"
        self.current_chatroom = "General"
        self.chat_history = {"General": []}

        self.chatroom_frame = customtkinter.CTkFrame(self, width=100, height=280)
        self.chatroom_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")

        self.chatroom_label = customtkinter.CTkLabel(
            self.chatroom_frame, text="Chatrooms"
        )
        self.chatroom_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")

        self.chatroom_buttons = []
        button = customtkinter.CTkButton(
            self.chatroom_frame,
            text="General",
            command=lambda: self.switch_chatroom("General"),
        )
        button.grid(row=1, column=0, padx=10, pady=(5, 5), sticky="ew")
        self.chatroom_buttons.append(button)

        self.create_button = customtkinter.CTkButton(
            self.chatroom_frame,
            text="Create New Chat",
            command=self.create_chatroom,
            fg_color=("black"),
        )
        self.create_button.grid(
            row=len(self.chatroom_buttons) + 2,
            column=0,
            padx=10,
            pady=(10, 10),
            sticky="ew",
        )

        self.chat_display = customtkinter.CTkTextbox(self, width=400, height=280)
        self.chat_display.grid(row=0, column=1, padx=(10, 5), pady=10)

        self.input_frame = customtkinter.CTkFrame(self, width=200, height=280)
        self.input_frame.grid(row=0, column=2, padx=(5, 10), pady=10, sticky="nsew")

        self.input_field = customtkinter.CTkEntry(
            self.input_frame, width=180, placeholder_text="Ask Synapse"
        )
        self.input_field.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")

        self.send_button = customtkinter.CTkButton(
            self.input_frame, text="Send", command=self.send_message
        )
        self.send_button.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="ew")

        self.model_label = customtkinter.CTkLabel(
            self.input_frame, text="Select Model:"
        )
        self.model_label.grid(row=2, column=0, padx=10, pady=(10, 5), sticky="ew")

        self.model_button = customtkinter.CTkOptionMenu(
            self.input_frame,
            values=list_models(),
            command=self.switch_model,
        )
        self.model_button.grid(row=3, column=0, padx=10, pady=(5, 10), sticky="ew")

        self.bind("<Return>", self.send_message)  # Bind Enter key to send message

    def switch_chatroom(self, chatroom) -> None:
        """Switch to a different chatroom"""

        self.chat_history[self.current_chatroom] = self.chat_display.get(
            "1.0", customtkinter.END
        )

        self.current_chatroom = chatroom
        self.title(f"Synapse - {chatroom} Room")
        self.chat_display.delete("1.0", customtkinter.END)
        self.chat_display.insert(
            customtkinter.END, self.chat_history[self.current_chatroom]
        )

    def switch_model(self, choice) -> None:
        """Switch to a different model

        Args:
            choice (str): The name of the model to switch to
        """

        if choice == self.current_model:
            return

        self.current_model = choice
        global model
        model = server.get_model(choice)
        self.chat_display.insert(customtkinter.END, f"Switched to model: {choice}\n")

    def create_chatroom(self) -> None:
        """Create a new chatroom"""

        input_dialog = customtkinter.CTkInputDialog(
            text="Enter the name of the new chatroom:", title="Create Chatroom"
        )
        new_room_name = input_dialog.get_input()
        if new_room_name:
            if new_room_name not in self.chat_history:
                self.chat_history[new_room_name] = []
                button = customtkinter.CTkButton(
                    self.chatroom_frame,
                    text=new_room_name,
                    command=lambda c=new_room_name: self.switch_chatroom(c),
                )
                button.grid(
                    row=len(self.chatroom_buttons) + 1,
                    column=0,
                    padx=10,
                    pady=(5, 5),
                    sticky="ew",
                )
                self.chatroom_buttons.append(button)

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

    def send_message(self, event=None) -> None:
        """Send a message to the chatbot

        Args:
            event (event, optional): The event that triggered the function. Defaults to None.
        """

        message = self.input_field.get()
        if message.strip() != "":
            self.chat_display.insert(customtkinter.END, f"You: {message}\n")
            self.input_field.delete(0, customtkinter.END)
            self.reply_message(message)

    def reply_message(self, message) -> None:
        """Reply to a message with the chatbot's response

        Args:
            message (str): The message to reply to
        """
        prediction_df = pd.DataFrame(
            model.predict(
                {
                    "question": message,
                }
            )
        )
        data = prediction_df["answer"][0]
        self.chat_display.insert(customtkinter.END, f"Bot: {data}\n")
        self.chat_display.insert(customtkinter.END, "\n")

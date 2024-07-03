import customtkinter
import mindsdb_sdk
import mindsdb_sdk.databases
import pandas as pd

server = mindsdb_sdk.connect()
project = server.get_project("mindsdb")
model = server.get_model("openai_model")

# Set the appearance mode and color theme
customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (default), "Light", "Dark"
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (default), "dark-blue", "green"


def list_models():
    res = []
    for model in server.list_models():
        res.append(model.name)
    return res


class ChatApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Synapse - General Room")
        self.geometry("805x300")  # Adjusted width to accommodate chatrooms column
        self.center_window(805, 300)

        self.current_model = "openai_model"
        self.current_chatroom = "General"
        self.chat_history = {"General": []}

        # Create chatroom selection area
        self.chatroom_frame = customtkinter.CTkFrame(self, width=100, height=280)
        self.chatroom_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")

        # Add label for chatroom selection
        self.chatroom_label = customtkinter.CTkLabel(
            self.chatroom_frame, text="Chatrooms"
        )
        self.chatroom_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")

        # Add chatroom buttons
        self.chatroom_buttons = []
        button = customtkinter.CTkButton(
            self.chatroom_frame,
            text="General",
            command=lambda: self.switch_chatroom("General"),
        )
        button.grid(row=1, column=0, padx=10, pady=(5, 5), sticky="ew")
        self.chatroom_buttons.append(button)

        # Add Create button
        self.create_button = customtkinter.CTkButton(
            self.chatroom_frame,
            text="Create",
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

        # Create chat display area
        self.chat_display = customtkinter.CTkTextbox(self, width=400, height=280)
        self.chat_display.grid(row=0, column=1, padx=(10, 5), pady=10)

        # Create input field and send button frame
        self.input_frame = customtkinter.CTkFrame(self, width=200, height=280)
        self.input_frame.grid(row=0, column=2, padx=(5, 10), pady=10, sticky="nsew")

        # Add input field to the frame
        self.input_field = customtkinter.CTkEntry(self.input_frame, width=180)
        self.input_field.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")

        # Add send button to the frame
        self.send_button = customtkinter.CTkButton(
            self.input_frame, text="Send", command=self.send_message
        )
        self.send_button.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="ew")

        # Add label for model selection
        self.model_label = customtkinter.CTkLabel(
            self.input_frame, text="Select Model:"
        )
        self.model_label.grid(row=2, column=0, padx=10, pady=(10, 5), sticky="ew")

        # Add a toggle button to switch between different models
        self.model_button = customtkinter.CTkOptionMenu(
            self.input_frame,
            values=list_models(),
            command=self.switch_model,
        )
        self.model_button.grid(row=3, column=0, padx=10, pady=(5, 10), sticky="ew")

        self.bind("<Return>", self.send_message)  # Bind Enter key to send message

    def switch_chatroom(self, chatroom):
        # Save current chat history
        self.chat_history[self.current_chatroom] = self.chat_display.get(
            "1.0", customtkinter.END
        )

        # Switch to new chatroom
        self.current_chatroom = chatroom
        self.title(f"Synapse - {chatroom} Room")
        self.chat_display.delete("1.0", customtkinter.END)
        self.chat_display.insert(
            customtkinter.END, self.chat_history[self.current_chatroom]
        )

    def switch_model(self, choice):
        self.current_model = choice
        global model
        model = server.get_model(choice)
        self.chat_display.insert(customtkinter.END, f"Switched to model: {choice}\n")

    def create_chatroom(self):
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

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def send_message(self, event=None):
        message = self.input_field.get()
        if message.strip() != "":
            self.chat_display.insert(customtkinter.END, f"You: {message}\n")
            self.input_field.delete(0, customtkinter.END)
            self.reply_message(message)

    def reply_message(self, message):
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


if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()

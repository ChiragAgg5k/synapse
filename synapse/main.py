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


def list_models() -> list:
    """List all available models."""

    res = []
    for model in server.list_models():
        res.append(model.name)
    return res


class ChatApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Synapse")
        self.geometry("630x300")
        self.center_window(630, 300)

        self.current_model = "openai_model"

        # Create chat display area
        self.chat_display = customtkinter.CTkTextbox(self, width=400, height=280)
        self.chat_display.grid(row=0, column=0, padx=(10, 5), pady=10)

        # Create input field and send button frame
        self.input_frame = customtkinter.CTkFrame(self, width=200, height=280)
        self.input_frame.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="nsew")

        # Add input field to the frame
        self.input_field = customtkinter.CTkEntry(
            self.input_frame, width=180, placeholder_text="Ask Synapse"
        )
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

    def switch_model(self, choice):
        self.current_model = choice
        global model
        model = server.get_model(choice)
        self.chat_display.insert(customtkinter.END, f"Switched to model: {choice}\n")

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

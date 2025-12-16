import modal
import os
import sys

# Define the image with necessary dependencies
# We copy requirements.txt to the image and install them
image = (
    modal.Image.debian_slim()
    .copy_local_file("requirements.txt")
    .pip_install_from_requirements("requirements.txt")
)

app = modal.App("whatsapp-todo-bot")

# Define the secret from the .env file
# Ensure you have a .env file locally relative to this script
secrets = modal.Secret.from_dotenv()

@app.function(
    image=image,
    secrets=[secrets],
    mounts=[
        modal.Mount.from_local_dir(".", remote_path="/root")
    ]
    # NOTE: Removed keep_warm=1 to avoid $20-30/month cost
    # Cold start ~300-500ms is acceptable for WhatsApp webhook
)
@modal.wsgi_app()
def flask_app():
    from app_twilio import app
    return app

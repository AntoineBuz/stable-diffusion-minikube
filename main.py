from diffusers import StableDiffusionPipeline
import safetensors
import torch
import gradio as gr
import json


class App:
    def __init__(self, config) -> None:
        self.model_id = config["model_id"]
        pipe = StableDiffusionPipeline.from_pretrained(
            self.model_id,
            torch_dtype=torch.float16,
            use_safetensors=True,
        )
        self.pipe = pipe.to("cuda")

    def sd(self, prompt):
        return self.pipe(prompt).images[0]

    def front(self) -> gr.Interface:
        return gr.Interface(fn=self.sd, inputs="textbox", outputs="image")


with open("config.json", "r") as config_file:
    config = json.load(config_file)

app = App(config)
app.front().launch(server_name="0.0.0.0")

from diffusers import StableDiffusionPipeline
import torch
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)

model_id = config["model_id"]
pipe = StableDiffusionPipeline.from_pretrained(
    model_id, torch_dtype=torch.float16, use_safetensors=True)

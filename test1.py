import matplotlib.pyplot as plt
import torch
from diffusers import FluxPipeline
import streamlit as st
pipe = FluxPipeline.from_pretrained("/home/eric/anaconda3/envs/py311", torch_dtype=torch.bfloat16)
pipe.enable_sequential_cpu_offload() 

def generate_image(prompt):
    image = pipe(
        prompt,
        guidance_scale=3.5,
        output_type="pil",
        num_inference_steps=4,
        max_sequence_length=256,
        generator=torch.Generator("cuda")
    ).images[0]
    return image

# Streamlit 用戶界面
st.title("flux.1 Schnell Demo")

prompt = st.text_input("Enter your prompt:", "prompt")

if st.button("Generate"):
    with st.spinner("Generating image..."):
        image = generate_image(prompt)
        st.image(image, caption="Generated Image")



# streamlit run test1.py
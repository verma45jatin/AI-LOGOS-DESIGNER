
import gradio as gr
from diffusers import StableDiffusionPipeline
import torch
import random
import os

# Load the Stable Diffusion model
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
pipe.to("cuda" if torch.cuda.is_available() else "cpu")

# Function to generate logos and save the first image for download
def generate_logos(prompt):
    images = [pipe(prompt).images[0] for _ in range(3)]  # Generate 3 logo variations
    
    # Save the first generated image for download
    save_path = "generated_logo.png"
    images[0].save(save_path)

    return images, save_path  # Return images and file path

# List of example prompts
example_prompts = [
    "Minimalist tech startup logo in blue and white",
    "Futuristic AI-inspired logo with a neon glow",
    "Nature-inspired eco-friendly brand logo",
    "Luxury brand logo with gold and black theme",
    "Modern gaming company logo with a cyberpunk feel"
]

# Custom CSS with animations and a better gallery display
custom_css = """
h1 {
    text-align: center;
    color: #ffffff;
    font-size: 42px;
    font-weight: bold;
    text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.7);
}

body {
    background-color: #000000 !important;
    font-family: 'Poppins', sans-serif;
}



/* Animated Buttons */
.gradio-container .button {
    transition: 0.3s;
    background: linear-gradient(to right, #ff8c00, #ff3b3b);
    border-radius: 10px;
    color: white !important;
    font-weight: bold;
}

.gradio-container .button:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 15px rgba(255, 165, 0, 0.8);
}

/* Stylish Prompt Box */
/* Stylish Prompt Box */
#prompt_box {
    background-color: #282828 !important;
    padding: 12px;
    border-radius: 12px;
    color: #00ff00 !important; /* Green color */
    font-size: 16px;
}


/* Animated Gallery */
#output_gallery {
    display: flex;
    overflow-x: auto;
    gap: 15px;
    padding: 15px;
    animation: fadeIn 1s ease-in-out;
}

#output_gallery img {
    border-radius: 12px;
    transition: 0.3s;
}

#output_gallery img:hover {
    transform: scale(1.08);
    box-shadow: 0px 0px 20px rgba(255, 255, 255, 0.3);
}

/* File Download Styling */
#download_container {
    background: rgba(255, 255, 255, 0.1);
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    font-weight: bold;
    animation: fadeIn 1.2s ease-in-out;
}
/* Ensure white text for specific sections */
h2, h3, #download_text {
    color: white !important;
}


/* Keyframe Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
"""

# UI Components
with gr.Blocks(css=custom_css) as iface:
    # Hero Section
    gr.Markdown("# 🎨 AI Logo Designer ")
    gr.HTML("""
    <h1 style="
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        background: linear-gradient(90deg, #ff8a00, #e52e71);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    ">
        🎨 Create Stunning & Unique Logos Instantly with AI! 🚀
    </h1>
    """)

    # Background Image
    gr.Image("/content/cy image.png", elem_id="banner_image", width=800)

    with gr.Row():
        with gr.Column(scale=2):
           prompt = gr.Textbox(label="🔍 Enter Logo Prompt", placeholder="e.g., 'Modern gaming logo with cyberpunk feel'", lines=2, elem_id="prompt_box")
        with gr.Column(scale=1):
            example_btn = gr.Button("🎲 Random Example")

    with gr.Row():
        generate_btn = gr.Button("🚀 Generate Logos", variant="primary")
        clear_btn = gr.Button("❌ Clear")

    # Animated Output Section
    gr.Markdown("## ✨ Your AI-Generated Logos ✨", elem_id="output_text")

    # Gallery with enhanced animations
    output_images = gr.Gallery(label="🖼️ Generated Logos", columns=[3], rows=[1], height=400, object_fit="contain", elem_id="output_gallery")

    # Styled Download Section
    with gr.Row(elem_id="download_container"):
        gr.Markdown("📥 **Download Your Logo**", elem_id="download_text")
        download_btn = gr.File()

    # Footer
    gr.Markdown("### ✨ Built with Stable Diffusion & Gradio ✨")

    # Button Actions
    def get_example():
        return random.choice(example_prompts)

    example_btn.click(get_example, outputs=prompt)
    generate_btn.click(generate_logos, inputs=prompt, outputs=[output_images, download_btn])
    clear_btn.click(lambda: "", outputs=prompt)

# Launch the UI
iface.launch(share=True)

import gradio as gr
from logic import get_cli_command, validate_command_wrapper
from prompts import SYSTEM_PROMPT_V1

def process_request(user_input, history):
    raw_command, updated_history = get_cli_command(user_input, SYSTEM_PROMPT_V1, history)
    is_safe, result = validate_command_wrapper(raw_command)
    
    if not is_safe:
        return "", updated_history, updated_history, gr.update(value=result, visible=True)
    
    return result, updated_history, updated_history, gr.update(visible=False)


def clear_session():
    return [], [], "", gr.update(visible=False)


def handle_request(user_input, history):
    if not user_input:
        return "", history, history
    return process_request(user_input, history)


THEME = gr.themes.Base(
    primary_hue="emerald",
    secondary_hue="cyan",
    neutral_hue="slate"
)

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

.gradio-container { 
    background: linear-gradient(135deg, #0a0e1a 0%, #0f1419 50%, #0d1117 100%) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

#main-title { 
    text-align: center; 
    font-size: 3.5em !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #00ff87 0%, #60efff 50%, #00d4ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.3em !important;
    text-shadow: 0 0 40px rgba(0, 255, 135, 0.3);
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: -0.02em;
}

#subtitle {
    text-align: center;
    color: #8b92a8;
    font-size: 1.1em;
    margin-bottom: 2em !important;
    font-weight: 400;
}

.input-section {
    background: linear-gradient(135deg, rgba(20, 26, 38, 0.9) 0%, rgba(15, 20, 30, 0.95) 100%) !important;
    border: 1px solid rgba(0, 255, 135, 0.2) !important;
    border-radius: 20px !important;
    padding: 25px !important;
    box-shadow: 0 8px 32px rgba(0, 255, 135, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px) !important;
}

.output-section {
    background: linear-gradient(135deg, rgba(15, 20, 30, 0.95) 0%, rgba(20, 26, 38, 0.9) 100%) !important;
    border: 1px solid rgba(96, 239, 255, 0.25) !important;
    border-radius: 20px !important;
    padding: 20px !important;
    box-shadow: 0 8px 32px rgba(96, 239, 255, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
}

.history-section {
    background: linear-gradient(135deg, rgba(20, 26, 38, 0.8) 0%, rgba(15, 20, 30, 0.9) 100%) !important;
    border: 1px solid rgba(139, 146, 168, 0.2) !important;
    border-radius: 20px !important;
    padding: 20px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
}

.generate-btn {
    background: linear-gradient(135deg, #00ff87 0%, #00d4ff 100%) !important;
    color: #0a0e1a !important;
    font-weight: 700 !important;
    font-size: 1.1em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 16px 32px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    box-shadow: 0 4px 20px rgba(0, 255, 135, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    transition: all 0.3s ease !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.generate-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 30px rgba(0, 255, 135, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
}

.clear-btn {
    background: rgba(239, 68, 68, 0.15) !important;
    color: #ef4444 !important;
    font-weight: 600 !important;
    border: 1px solid rgba(239, 68, 68, 0.3) !important;
    border-radius: 10px !important;
    padding: 12px 24px !important;
    transition: all 0.3s ease !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.clear-btn:hover {
    background: rgba(239, 68, 68, 0.25) !important;
    border: 1px solid rgba(239, 68, 68, 0.5) !important;
}

label {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
    font-size: 0.95em !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    margin-bottom: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.input-field textarea {
    background: rgba(15, 20, 30, 0.6) !important;
    border: 1px solid rgba(0, 255, 135, 0.3) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1em !important;
    padding: 14px !important;
}

.input-field textarea:focus {
    border: 1px solid rgba(0, 255, 135, 0.6) !important;
    box-shadow: 0 0 20px rgba(0, 255, 135, 0.2) !important;
}

.code-output {
    background: rgba(10, 14, 26, 0.9) !important;
    border: 1px solid rgba(96, 239, 255, 0.3) !important;
    border-radius: 12px !important;
    font-family: 'Fira Code', monospace !important;
    font-size: 1.05em !important;
    color: #00ff87 !important;
    padding: 18px !important;
    box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.5) !important;
}

.history-box {
    background: rgba(10, 14, 26, 0.6) !important;
    border: 1px solid rgba(139, 146, 168, 0.2) !important;
    border-radius: 12px !important;
    padding: 12px !important;
}

.history-title {
    color: #60efff !important;
    font-weight: 700 !important;
    font-size: 1.2em !important;
    margin-bottom: 15px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    display: flex !important;
    align-items: center !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.section-label {
    color: #00d4ff !important;
    font-weight: 700 !important;
    font-size: 0.85em !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    margin-bottom: 12px !important;
    display: flex !important;
    align-items: center !important;
}

.feature-badge {
    display: inline-block;
    background: rgba(0, 255, 135, 0.15);
    color: #00ff87;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 0.75em;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-left: 10px;
    border: 1px solid rgba(0, 255, 135, 0.3);
}

footer {
    text-align: center !important;
    color: #64748b !important;
    margin-top: 3em !important;
    font-size: 0.9em !important;
}

.warning-container {
    background: rgba(239, 68, 68, 0.1) !important;
    border: 2px solid #ef4444 !important;
    border-radius: 12px !important;
    padding: 15px !important;
    margin-bottom: 15px !important;
    animation: pulse-red 2s infinite;
}

@keyframes pulse-red {
    0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
    70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
    100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}

#main-title { 
    background: linear-gradient(135deg, #00ff87 0%, #60efff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3em !important;
    text-align: center;
}

.input-section, .output-section, .history-section {
    background: rgba(15, 23, 42, 0.8) !important;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 20px !important;
}
"""

with gr.Blocks(theme=THEME, css=CUSTOM_CSS) as demo:
    history_state = gr.State([])

    gr.Markdown("# ⚡ TERMINAL ARCHITECT", elem_id="main-title")
    gr.Markdown("### Advanced AI Command Generation & Security Shield", elem_id="subtitle")
    
    with gr.Row():
        with gr.Column(scale=3):
            warning_box = gr.Markdown(
                visible=False, 
                elem_classes="warning-container"
            )

            with gr.Group(elem_classes="input-section"):
                gr.Markdown("#### 💬 Mission Objective")
                input_field = gr.Textbox(
                    label="", placeholder="How can I help you automate your terminal?", 
                    lines=3
                )
                submit_btn = gr.Button("🚀 Generate Command", elem_classes="generate-btn")
            
            with gr.Group(elem_classes="output-section"):
                gr.Markdown("#### 🖥️ Verified Output")
                output_code = gr.Code(language="shell", lines=5)
            
        with gr.Column(scale=2):
            with gr.Group(elem_classes="history-section"):
                gr.Markdown("#### 📜 Session History")
                history_display = gr.Chatbot(height=500, show_label=False)
                clear_btn = gr.Button("🗑️ Reset", elem_classes="clear-btn")

    event_params = {
        "fn": handle_request,
        "inputs": [input_field, history_state],
        "outputs": [output_code, history_display, history_state, warning_box]
    }
    
    submit_btn.click(**event_params)
    input_field.submit(**event_params)
    
    clear_btn.click(
        fn=clear_session,
        outputs=[history_display, history_state, output_code, warning_box]
    )

if __name__ == "__main__":
    demo.launch()




# # Custom theme with programming aesthetic
# THEME = gr.themes.Base(
#     primary_hue="emerald",
#     secondary_hue="cyan",
#     neutral_hue="slate",
#     font=gr.themes.GoogleFont("JetBrains Mono"),
#     font_mono=gr.themes.GoogleFont("Fira Code")
# )



# # Create the Gradio interface
# with gr.Blocks(theme=THEME, css=CUSTOM_CSS) as demo:
#     history_state = gr.State([])

#     # Header
#     gr.Markdown("# ⚡ TERMINAL ARCHITECT", elem_id="main-title")
#     gr.Markdown("*Transform natural language into Windows CMD commands*", elem_id="subtitle")
    
#     # Main layout
#     with gr.Row():
#         # Left column - Input and Output
#         with gr.Column(scale=3):
#             # Input section
#             with gr.Group(elem_classes="input-section"):
#                 gr.Markdown("### 💬 Describe Your Command", elem_classes="section-label")
#                 input_field = gr.Textbox(
#                     label="",
#                     placeholder="Example: Find all Python files larger than 1MB in the current directory...",
#                     lines=4,
#                     elem_classes="input-field"
#                 )
#                 submit_btn = gr.Button(
#                     "🚀 Generate Command",
#                     elem_classes="generate-btn",
#                     size="lg"
#                 )
            
#             # Output section
#             with gr.Group(elem_classes="output-section"):
#                 gr.Markdown("### 🖥️ Generated CMD Command", elem_classes="section-label")
#                 output_code = gr.Code(
#                     label="",
#                     language="shell",
#                     elem_classes="code-output",
#                     lines=6
#                 )
            
#         # Right column - History
#         with gr.Column(scale=2):
#             with gr.Group(elem_classes="history-section"):
#                 gr.Markdown("### 📜 Session History", elem_classes="history-title")
#                 history_display = gr.Chatbot(
#                     label="",
#                     height=500,
#                     elem_classes="history-box",
#                     show_label=False
#                 )
#                 clear_btn = gr.Button(
#                     "🗑️ Clear History",
#                     elem_classes="clear-btn",
#                     size="sm"
#                 )

#     # Footer
#     gr.Markdown(
#         "---\n*Powered by Gemini AI • Secure command validation enabled*",
#         elem_id="footer"
#     )

#     # Event handlers
#     submit_btn.click(
#         fn=handle_request,
#         inputs=[input_field, history_state],
#         outputs=[output_code, history_display, history_state]
#     )
    
#     input_field.submit(
#         fn=handle_request,
#         inputs=[input_field, history_state],
#         outputs=[output_code, history_display, history_state]
#     )
    
#     clear_btn.click(
#         fn=lambda: ([], []),
#         inputs=None,
#         outputs=[history_display, history_state]
#     )

# if __name__ == "__main__":
#     demo.launch()

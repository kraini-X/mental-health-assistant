from rag import rag_with_history
import gradio as gr
print("Gradio version:", gr.__version__)

DESCRIPTION = """
<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align: center;">
    <img src="https://cdn-icons-png.flaticon.com/512/3203/3203856.png" alt="MindMate Logo" width="80" style="margin-bottom: 10px;">
    <h2 style="margin-bottom: 0;">MindMate: Your Empathetic Mental Health Assistant</h2>
    <p style="font-size: 1.1em; color: #555;">
        MindMate provides supportive, evidence-based responses to your mental health questions.<br>
        <b>All conversations are private and confidential.</b>
    </p>
</div>
"""

FOOTER = """
<div style="text-align: center; color: #888; font-size: 0.95em; margin-top: 20px;">
    &copy; 2025 MindMate &mdash; For informational purposes only. Not a substitute for professional help.
</div>
"""

chat = gr.ChatInterface(
    fn=rag_with_history,
    title="MindMate: Mental Health Assistant",
    description=DESCRIPTION+FOOTER,
    theme=gr.themes.Soft(
        primary_hue="indigo",
        secondary_hue="blue",
        neutral_hue="slate"
    ),
    examples=[
        "I'm feeling low lately.",
        "What can I do when I'm anxious?",
        
    ],
    type="messages",
    additional_inputs=[]
 
    
   
)
if __name__ == "__main__":
    chat.launch(
        share=True,
        server_name="0.0.0.0",
        server_port=7860  # Change this to any free port you prefer
    )

   

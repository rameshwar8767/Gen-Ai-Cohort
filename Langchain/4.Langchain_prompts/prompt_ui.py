from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

st.header("Research Tool")

paper_input = st.selectbox(
    "Select Research Paper Name",
    [
        "Attention Is All You Need",
        "BERT: Pre-training of Deep Bidirectional Transformers",
        "GPT-3: Language Models are Few-Shot Learners",
        "Diffusion Models Beat GANs on Image Synthesis"
    ]
)

style_input = st.selectbox(
    "Select Explanation Style",
    ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"]
)

length_input = st.selectbox(
    "Select Explanation Length",
    ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"]
)

# Initialize the chat model
model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

# Define the prompt template
template = PromptTemplate(
    input_variables=["paper_input", "style_input", "length_input"],
    template="""
Explain the research paper titled "{paper_input}" in a {style_input} style.
Make the explanation {length_input}.
"""
)

# Format the prompt
prompt_text = template.format(
    paper_input=paper_input,
    style_input=style_input,
    length_input=length_input
)

if st.button("Summarize"):
    # Pass prompt as a HumanMessage
    result = model([HumanMessage(content=prompt_text)])
    st.write(result.content)  # result.content now works

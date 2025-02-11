import streamlit as st
from langchain_groq import ChatGroq
import json

# Initialize the LLM model
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    groq_api_key="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"  # Replace with your actual API key
)

# Streamlit UI
st.set_page_config(page_title="Python Code Reviewer", page_icon="🐍")
st.title("🐍 AI-Powered Python Code Reviewer")

st.write(
    "Upload a Python script or enter Python code below. "
    "The AI will analyze the code for errors, suggest improvements, and provide an optimized version."
)

# Code Input Section
uploaded_file = st.file_uploader("Upload a Python file", type=["py"])
if uploaded_file:
    python_code = uploaded_file.read().decode("utf-8")
else:
    python_code = st.text_area("Or, paste your Python code below:", height=200)

# Process when "Analyze Code" button is clicked
if st.button("🔍 Analyze Code") and python_code.strip():
    # Construct structured prompt
    code_review_prompt = f"""
    You are a professional Python code reviewer.
    Analyze the following function and provide a structured review.

    Return the response in strict JSON format with three keys:
    - "errors": A list of syntax or logical errors.
    - "suggestions": A list of improvements.
    - "optimized_code": The corrected and optimized version of the function.

    Ensure your response is **valid JSON only**. Do not include any explanation outside JSON format.

    ```python
    {python_code}
    ```
    """

    # Invoke LLM
    response = llm.invoke(code_review_prompt)

    try:
        # Parse JSON response
        review_result = json.loads(response.content)

        st.subheader("📌 Code Review Summary")
        if review_result.get("errors"):
            st.error("🚨 Errors Found:")
            for error in review_result["errors"]:
                st.write(f"- {error}")

        if review_result.get("suggestions"):
            st.warning("💡 Suggestions for Improvement:")
            for suggestion in review_result["suggestions"]:
                st.write(f"- {suggestion}")

        if review_result.get("optimized_code"):
            st.success("✅ Optimized Code:")
            st.code(review_result["optimized_code"], language="python")

    except json.JSONDecodeError:
        st.error("❌ Failed to parse the AI response. Try again.")

# Footer
st.markdown("---")
st.write("🔹 **Powered by Groq AI & Streamlit** 🚀")

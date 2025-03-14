from agent import CollaborativeAgent
import ollama
import asyncio
import json
from sandbox import SecureSandbox, Tool

# Define the tools available to the agent as actual functions
def summarize(text):
    # Implement the summarization logic here
    return f"Summary of: {text[:50]}..."

def classify(text):
    # Implement the classification logic here
    return "Classification: informational"

def generate(prompt):
    # Implement the text generation logic here
    return f"Generated content based on: {prompt}"

def translate(text, target_language):
    # Implement the translation logic here
    return f"Translated to {target_language}: {text[:30]}..."

def qa(question, context):
    # Implement the question answering logic here
    return f"Answer to '{question}' based on context"

# Define the main function to demonstrate the multi-agent runner
async def main():
    """
    Demonstrate the multi-agent runner with SecureSandbox.
    """
    # Specify a model that exists in your Ollama installation
    model_name = "qwen2.5:0.5b"  # Update this to a model you have installed
    
    # Simulate language model and tools
    llm = ollama.Client(host='http://localhost:11434')
    
    # Create secure sandbox for tool execution with proper security constraints
    sandbox = SecureSandbox(
        allowed_modules=["json", "re", "string"],
    )
    
    # Wrap tools with secure sandbox
    tools = {
        "summarize": LLMTool(
            summarize, 
            name="summarize", 
            description="Summarize a given text"
        ),
        "classify": LLMTool(
            classify, 
            name="classify", 
            description="Classify a given text"
        ),
        "generate": LLMTool(
            generate, 
            name="generate", 
            description="Generate text based on a prompt"
        ),
        "translate": LLMTool(
            translate, 
            name="translate", 
            description="Translate text to a target language"
        ),
        "qa": LLMTool(
            qa, 
            name="qa", 
            description="Answer a question based on a given context"
        )
    }
    
    # Create properly structured multi-agent system
    agents = {
        "research_agent": GoalOrientedAgent(
            llm.chat(model=model_name), 
            sandbox,
            tools,
            name="ResearchAgent",
            description="Researches current AI trends"
        ),
        "analysis_agent": GoalOrientedAgent(
            llm.chat(model=model_name), 
            sandbox,
            tools,
            name="AnalysisAgent",
            description="Analyzes and synthesizes AI trend information"
        )
    }
    
    # Initialize runner with proper agents
    

if __name__ == "__main__":
    asyncio.run(main())
import os

from dotenv import load_dotenv
from aiohttp import web
from ragtools import attach_rag_tools
from rtmt import RTMiddleTier
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential

if __name__ == "__main__":
    load_dotenv()
    provider = os.environ.get("PROVIDER", "azure")

    if provider == "azure":
        llm_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        llm_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
        llm_key = os.environ.get("AZURE_OPENAI_API_KEY")
        credentials = DefaultAzureCredential() if not llm_key else None
        llm_credentials = AzureKeyCredential(llm_key) if llm_key else credentials
    elif provider == "openai":
        llm_endpoint = os.environ.get("OPENAI_API_ENDPOINT")
        llm_key = os.environ.get("OPENAI_API_KEY")
        llm_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
        llm_credentials = llm_key
    else:
        raise ValueError(f"Unknown provider {provider}")

    search_endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT")
    search_index = os.environ.get("AZURE_SEARCH_INDEX")
    search_key = os.environ.get("AZURE_SEARCH_API_KEY")
    search_credentials = AzureKeyCredential(search_key) if search_key else None

    app = web.Application()

    rtmt = RTMiddleTier(llm_endpoint, llm_deployment, llm_credentials, provider=provider)
    rtmt.system_message = "You are a helpful assistant. Only answer questions based on information you searched in the knowledge base, accessible with the 'search' tool. " + \
                          "The user is listening to answers with audio, so it's *super* important that answers are as short as possible, a single sentence if at all possible. " + \
                          "Never read file names or source names or keys out loud. " + \
                          "Always use the following step-by-step instructions to respond: \n" + \
                          "1. Always use the 'search' tool to check the knowledge base before answering a question. \n" + \
                          "2. Always use the 'report_grounding' tool to report the source of information from the knowledge base. \n" + \
                          "3. Produce an answer that's as short as possible. If the answer isn't in the knowledge base, say you don't know."
    attach_rag_tools(rtmt, search_endpoint, search_index, search_credentials)

    rtmt.attach_to_app(app, "/realtime")

    app.add_routes([web.get('/', lambda _: web.FileResponse('./static/index.html'))])
    app.router.add_static('/', path='./static', name='static')
    web.run_app(app, host='0.0.0.0', port=8000)

from langchain_classic.chains.question_answering import load_qa_chain 
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

def get_answer(vector_store, search_query, question_with_history):
    match = vector_store.similarity_search(search_query, k=4) 

    llm = OllamaLLM(temperature=0, model="llama3.2:latest")
    
    # Custom prompt to force the AI to be honest and factual
    template = """
    You are an official, exact HR Salary Assistant. 
    Use the following pieces of context to answer the question at the end. 
    If you do not know the answer, or if it is not explicitly mentioned in the context, 
    say "I am sorry, but I cannot find that information in the official company documents." 
    Do not try to make up an answer or assume rules.

    Context:
    {context}

    {question}
    
    Answer:""" 
    
    QA_CHAIN_PROMPT = PromptTemplate(
        input_variables=["context", "question"],
        template=template,
    )
    
    # Pass our custom strict prompt into the chain
    chain = load_qa_chain(llm, chain_type="stuff", prompt=QA_CHAIN_PROMPT)
    response = chain.run(input_documents=match, question=question_with_history)
    return response

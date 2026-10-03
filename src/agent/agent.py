
from src.agent.intent_classifier import classify_intent

from src.tools.pdf_tool import search_pdf
from src.tools.summary_tool import summarize_document
from src.tools.quiz_tool import generate_quiz

from src.prompts.prompt_builder import build_prompt


MAX_HISTORY =10 ; 



def answer_question(question,history, index,chunks,llm_function):

    conversation = ""
    recent_history= history[-MAX_HISTORY: ]
    for chat in recent_history:
        conversation+=(
            f"User:{chat['question']}\n"
            f"Assistant: {chat['answer']}\n\n"
        )

    intent = classify_intent(question )
    if (intent=="summmary"):
        return summarize_document(chunks, llm_function)
    elif (intent=="quiz"):
        return  generate_quiz(chunks , llm_function)
    else :
        context= search_pdf(question , index , chunks)
        context = "\n\n".join(context)
        prompt = build_prompt(question,context,conversation)
        return llm_function(prompt); 
 
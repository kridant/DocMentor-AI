def classify_intent(question):

    question = question.lower()

    if any(word in question for word in ["summarize", "summary"]):
        return "summary"

    if any(word in question for word in ["quiz", "mcq", "questions"]):
        return "quiz"

    if any(word in question for word in ["keyword", "keywords"]):
        return "keyword"

    return "retrieve"
# DocMentor AI — Detailed Interview Questions in Simple English

> This guide contains 40 important questions instead of many short questions. The answers are detailed enough for a strict interview, but use simple English. Technical terms are kept because interviewers may use them.

## Resume points you can safely use

- Built a Python and Streamlit PDF question-answering prototype using a Retrieval-Augmented Generation (RAG) pipeline, Sentence Transformer embeddings, FAISS vector search, and Gemini.
- Separated PDF processing, retrieval, prompts, model calls, tools, and routing into different modules, and used Streamlit session state to reuse a processed document during a session.

Do not claim that the project is production-ready, highly accurate, scalable, secure, or hallucination-free. These claims have not been measured. Also, do not claim that the current version supports OCR, citations, authentication, permanent storage, or multiple documents.

---

## 1. Project overview and architecture

### Q1. Tell me about DocMentor AI.

**Strong answer:**

DocMentor AI is a PDF question-answering prototype. A user uploads a PDF and asks questions in normal language. The application extracts the text, divides it into overlapping chunks, converts those chunks into embeddings, and stores the embeddings in a FAISS index.

When the user asks a question, the app converts that question into an embedding and uses FAISS to find the three closest PDF chunks. It sends those chunks, the question, and recent conversation history to Gemini 2.5 Flash. Gemini then creates the final answer using the retrieved text as evidence.

The project also contains simple intent routing for quiz and summary requests. However, the summary route currently has a spelling bug, so I would describe the project as a working RAG prototype with known limitations—not as a production system.

### Q2. What problem does this project solve?

**Strong answer:**

The project helps users find and understand information in a PDF without reading the complete document. A student, for example, can upload study material and ask focused questions or request practice questions.

Normal keyword search works only when the user knows the exact words used in the document. My application uses semantic search, so it can find related text even when the question uses different wording. This makes document search more natural.

The main limitation is that the answer depends on the quality of retrieval. If the correct PDF chunk is not found, Gemini may not have enough evidence to answer correctly.

### Q3. Walk me through the complete data flow.

**Strong answer:**

The flow has two parts. During **document ingestion**, PyPDF extracts text from every page. LangChain’s recursive text splitter creates chunks of 500 characters with 100 characters of overlap. The `all-MiniLM-L6-v2` model converts every chunk into a vector, and FAISS stores those vectors in an exact L2 index.

During **question answering**, the same embedding model converts the user’s question into a vector. FAISS returns the three closest chunk vectors. The corresponding text is joined into context and added to a prompt with up to ten recent chat turns. Gemini reads that prompt and generates the answer.

The index and chunks stay in Streamlit session state, so the app does not process the same filename again on every Streamlit rerun.

### Q4. Why did you separate the project into different modules?

**Strong answer:**

I separated the project by responsibility. PDF loading, chunking, embeddings, vector storage, retrieval, prompts, Gemini calls, tools, and orchestration live in different modules. This makes the system easier to understand and change.

For example, the agent receives the LLM function as an argument. This means I can replace Gemini with another provider or pass a fake model during testing without changing the retrieval logic. This is a simple form of dependency injection.

The structure creates good boundaries, but modular code alone does not guarantee quality. The current project still needs proper automated tests to confirm that the modules work correctly together.

### Q5. Is this really an AI agent?

**Strong answer:**

It is only agent-like in a basic sense. It checks the user’s words and chooses from a few fixed actions, such as normal retrieval or quiz generation. It does not make a multi-step plan, examine tool results, correct itself, or dynamically select new tools.

I would describe it as a **routed RAG workflow** or an **orchestrator**. Calling it a fully autonomous agent would be an overstatement. A more advanced agent could plan several steps, call tools repeatedly, check the results, and decide whether more information is needed.

Being honest about this difference is important because interviewers often challenge the word “agent” on a resume.

---

## 2. RAG and retrieval

### Q6. What is RAG?

**Strong answer:**

RAG means Retrieval-Augmented Generation. It works like an open-book exam. Before the language model answers, the application searches an external source—in this case, the uploaded PDF—and finds the most relevant passages. Those passages are then given to the model as evidence.

This is different from asking Gemini a question directly. Without RAG, Gemini mainly depends on information learned during training. With RAG, the answer can use information from a new private document without training the model again.

RAG can reduce hallucination and make answers easier to verify, but it does not guarantee correctness. The search can retrieve the wrong text, and the model can still misunderstand the correct text.

### Q7. Why not send the complete PDF to Gemini?

**Strong answer:**

For a small PDF, sending the complete document may actually be simpler. It avoids the risk that retrieval misses the page containing the answer.

For a large PDF, however, sending everything increases the number of input tokens, response time, and API cost. The document may exceed the model’s context limit, and irrelevant sections may distract the model. RAG sends only a few likely-relevant chunks, which usually makes the prompt smaller and more focused.

The trade-off is that RAG can leave out useful information. Therefore, I should measure how often the correct passage appears in the retrieved results instead of assuming retrieval always works.

### Q8. Why use RAG instead of fine-tuning?

**Strong answer:**

Fine-tuning changes how a model behaves by training it on examples. It is useful for teaching a style, format, or repeated task. It is not the best way to give a model facts from every newly uploaded PDF.

RAG can use a new document immediately. It does not require training, and it can keep a connection between the answer and the original source passage. This is cheaper and more flexible when the knowledge changes often.

Fine-tuning and RAG are not direct opposites. A company could fine-tune a model to follow a specific answer style and still use RAG to provide current document information.

### Q9. What are the main ways a RAG system can fail?

**Strong answer:**

The first type is **retrieval failure**. The answer exists in the PDF, but the search does not return the correct chunk. Gemini cannot use evidence that it never receives.

The second type is **generation failure**. The correct chunk is present in the prompt, but Gemini ignores it, misunderstands it, or adds unsupported information.

These failures need different solutions. Retrieval failure may require better chunking, embeddings, top-k values, hybrid search, or reranking. Generation failure may require clearer prompts, a better model, citations, or answer verification. I would evaluate these stages separately so I know which part needs improvement.

### Q10. What happens when the answer is not in the PDF?

**Strong answer:**

The prompt tells Gemini to say that the answer is unavailable in the document. However, this is only an instruction, not a guarantee. A language model can still guess or use its general knowledge.

There is another problem: FAISS always returns the closest three chunks, even if all three are unrelated to the question. The current project does not use a minimum similarity threshold. Therefore, irrelevant text may still be sent to Gemini.

In a production design, I would check retrieval scores first. If every result has low relevance, the app should refuse before calling Gemini. I would also display the source passages and page numbers so the user can verify the answer.

### Q11. Does RAG remove hallucinations?

**Strong answer:**

No. RAG reduces the chance of hallucination by giving the model relevant evidence and telling it to answer only from that evidence. It does not completely control the model.

The model may still invent details, combine unrelated passages, or use information from its training. Retrieval can also return incomplete or incorrect context. Even a confident answer may be unsupported.

To improve trust, I would return citations, show the exact retrieved passages, test questions whose answers are absent, and measure faithfulness. For important use cases, I could also add a second verification step that checks whether every claim in the answer is supported by the context.

---

## 3. PDF processing and chunking

### Q12. Which PDFs can the project process?

**Strong answer:**

The project works best with PDFs that contain selectable digital text, such as a Word document exported to PDF. PyPDF reads the text layer from these documents.

A scanned PDF may contain only images of pages. A human can see the words, but PyPDF may extract little or no text because the words are not stored as digital characters. The project does not currently use OCR, so scanned documents may fail.

A better pipeline would measure the amount of text extracted from each page. If a page has very little text, it could run OCR. It should also keep the page number, heading, and document ID with every chunk.

### Q13. What information is lost during PDF extraction?

**Strong answer:**

The loader joins all page text into one long string. It does not keep page numbers or document structure with the chunks. It may also lose table rows, columns, headings, image captions, and the correct reading order in multi-column documents.

This creates two problems. First, the model may misunderstand structured information such as tables. Second, the app cannot reliably display citations such as “page 12” because page metadata has already been removed.

I would store every chunk as text plus metadata: document ID, page number, section heading, and chunk position. For tables, I would use a layout-aware parser rather than treating the PDF as plain text.

### Q14. Why divide the document into chunks?

**Strong answer:**

If I create one embedding for the complete document, that one vector must represent many unrelated ideas. Its meaning becomes too broad, so it is difficult to find the exact passage that answers a question.

Chunks create smaller units, with each vector representing a more focused section. The retriever can then return only the parts that are likely to contain the answer. Smaller context also reduces the number of tokens sent to Gemini.

Chunks should not be too small because they may lose important surrounding information. They should not be too large because their meaning becomes less focused. The correct size must be tested.

### Q15. Why use 500-character chunks with 100-character overlap?

**Strong answer:**

The values are starting heuristics, not proven best settings. A 500-character chunk is small enough to focus on a limited idea, while 100 characters of overlap help when a useful sentence crosses a chunk boundary.

Overlap improves continuity, but it also creates repeated text, more embeddings, and sometimes duplicate search results. Larger chunks give more context but may reduce search precision. Smaller chunks improve precision but may remove necessary context.

I would create questions with known source passages and test several chunk sizes and overlap values. I would compare retrieval success, answer quality, prompt size, latency, and cost before selecting the final values.

### Q16. Why can summaries and quizzes fail on large PDFs?

**Strong answer:**

The current summary and quiz tools join every chunk and send the complete document text to Gemini. This can exceed the model’s context limit for large documents and can increase latency and cost.

For summarization, I would use hierarchical or map-reduce summarization. The app would summarize smaller sections first and then combine those summaries into a final document summary.

For quiz generation, I would generate questions from different sections, combine them, remove duplicates, and check topic coverage. This gives more balanced questions than asking the model to process an entire large document in one prompt.

---

## 4. Embeddings and FAISS

### Q17. What is an embedding?

**Strong answer:**

An embedding is a list of numbers that represents the meaning of text. Texts with similar meanings should receive vectors that are close to each other, even when they use different words.

For example, “How does RAG work?” and “Explain retrieval-augmented generation” may produce similar embeddings. This allows semantic search to find related ideas instead of only exact keyword matches.

The PDF chunks and the user’s question must use the same embedding model. Otherwise, their vectors may not belong to the same meaningful space and should not be compared.

### Q18. Why use `all-MiniLM-L6-v2`?

**Strong answer:**

`all-MiniLM-L6-v2` is a relatively small and fast Sentence Transformer model. It can run locally and is a practical starting point for a prototype. Using it locally also avoids making an embedding API request for every document chunk and question.

The model may be weaker for specialized fields, very long passages, or some languages. I did not compare it with other embedding models, so I should not call it the best choice.

I would compare models using the same set of questions and known answer passages. I would select one based on retrieval quality, speed, memory use, language support, and cost.

### Q19. What does FAISS do?

**Strong answer:**

FAISS is a vector-search library. It stores the embeddings created from PDF chunks. When it receives the question embedding, it returns the positions of the nearest chunk vectors.

FAISS does not read PDFs, create embeddings, understand language, or generate answers. Those jobs belong to PyPDF, the Sentence Transformer model, and Gemini. FAISS only solves the nearest-neighbor search problem.

The project uses `IndexFlatL2`, which performs exact search using Euclidean distance. This is simple and accurate for a small number of chunks but does more work as the number of vectors grows.

### Q20. What is exact search, and will it scale?

**Strong answer:**

Exact search compares the question vector with every stored vector and returns the closest results. This gives exact results for the chosen distance measurement and is a sensible choice for one PDF with a limited number of chunks.

Its search work grows roughly in direct proportion to the number of vectors. Keeping all vectors in memory also becomes expensive at large scale.

For millions of chunks, I would consider approximate methods such as HNSW or IVF. They search much faster by avoiding a full comparison, but they may occasionally miss the true nearest vector. That is another trade-off between speed, memory, and retrieval accuracy.

### Q21. Why use L2 distance instead of cosine similarity?

**Strong answer:**

The project uses FAISS `IndexFlatL2`, so it compares vectors using Euclidean—or straight-line—distance. Cosine similarity instead compares the direction of vectors.

If vectors are normalized to length one, L2 distance and cosine similarity produce closely related rankings. However, the current project does not explicitly normalize embeddings, so I cannot claim the two methods are equivalent here.

I would test both methods on a retrieval dataset. If I wanted cosine-style search in FAISS, I would normalize document and question vectors and use inner-product search.

### Q22. Why retrieve only three chunks?

**Strong answer:**

Three is a starting value, not a value proven by testing. Retrieving fewer chunks keeps the prompt small and focused, but it may miss supporting information. Retrieving many chunks gives wider coverage, but it increases tokens and may distract Gemini with irrelevant or repeated text.

I would test different values of k and measure how often the correct passage appears in the results. I would also measure final answer quality, because finding the correct chunk is useful only if the model uses it properly.

One current edge case is that if a document has fewer than three chunks, FAISS may return `-1` for missing results. Python can treat that as the final list item, causing repeated text. The app should cap k to the actual chunk count.

### Q23. How would you improve retrieval?

**Strong answer:**

I would first create a small evaluation dataset instead of changing the system blindly. Each question would have a known correct page or chunk. I would measure whether that passage appears in the top results.

Then I could test better chunking, another embedding model, normalized cosine similarity, or a larger first-stage search followed by a reranker. A reranker reads the question and candidate chunks together and orders them more carefully.

I could also combine semantic search with keyword search. Embeddings are good for meaning, while keyword search is useful for exact names, codes, formulas, and rare terms. I would keep only improvements that provide enough measured benefit to justify extra complexity and latency.

---

## 5. Gemini, prompts, and conversation

### Q24. What does Gemini do in this project?

**Strong answer:**

Gemini 2.5 Flash is the answer-generation model. It receives the user’s question, the retrieved PDF chunks, recent conversation history, and instructions. It turns that information into a clear natural-language answer.

Gemini does not perform the vector search. MiniLM creates embeddings, and FAISS retrieves chunks. Gemini is used only after retrieval has selected the likely evidence.

I chose a fast model because document Q&A is interactive and the evidence is already provided. However, I did not benchmark different Gemini models, so I would describe it as a practical choice rather than an optimal one.

### Q25. What information is placed in the prompt?

**Strong answer:**

The prompt contains the current question, the three retrieved chunks, and up to ten recent question-answer turns. It also tells Gemini to use only the provided context, remain concise, and say when the answer is not available.

Separating prompts from application logic makes the instructions easier to change and test. However, prompt instructions are not guarantees. The model may still use unsupported information.

The prompt also treats PDF text as normal content. A harmful PDF could contain instructions for the model. A stronger design would clearly mark the PDF as untrusted data and test prompt-injection attacks.

### Q26. Why include conversation history?

**Strong answer:**

Conversation history helps with follow-up questions such as “Explain the second point.” Without history, the model may not know what “the second point” refers to. The project limits history to ten turns so the prompt does not grow forever.

History increases token use and can carry an earlier wrong answer into later responses. It can also expose more conversation content to the model provider.

Another limitation is that retrieval uses only the latest question. An unclear follow-up may produce a poor embedding. A better system would first rewrite the follow-up into a complete standalone search question using the conversation history.

### Q27. What is prompt injection in this project?

**Strong answer:**

A PDF may contain text such as “ignore all earlier instructions.” Because the app places PDF text inside the model prompt, Gemini may treat that text as an instruction rather than as untrusted document content. This is called prompt injection.

I would clearly separate system instructions from document data, mark the PDF content as untrusted, limit which tools and data the model can access, and validate the output. I would also create malicious test PDFs.

Prompt wording alone cannot provide complete security. Real protection must come from access controls and limits outside the language model.

---

## 6. Routing, state, and correctness

### Q28. How does intent classification work?

**Strong answer:**

The classifier changes the question to lowercase and searches for words such as “summary,” “quiz,” or “keyword.” It then returns a fixed intent. This approach is fast, free, deterministic, and easy to understand.

The weakness is that it depends on exact words. It may miss a request such as “give me the main points,” and it can create false matches when a keyword appears in a different meaning.

For a small number of intents, rules are a reasonable starting point. I would first improve tests and phrase coverage. If real usage requires more flexibility, I could use embedding similarity or a structured-output LLM classifier.

### Q29. What important routing bugs exist?

**Strong answer:**

The classifier returns `summary`, but the agent checks for `summmary` with an extra “m.” Therefore, a summary request does not reach the summary tool and instead falls into normal retrieval.

The classifier can also return `keyword`, but the agent has no keyword branch or keyword tool. That request also falls into normal retrieval. This means the feature contract between the classifier and agent is incomplete.

I would fix the values, remove unfinished intents, use a typed enum or constant instead of repeated strings, and write a parameterized test covering every possible intent. This shows why automated contract tests are important even when the individual functions look simple.

### Q30. How does Streamlit session state help?

**Strong answer:**

Streamlit reruns the script when the user interacts with the page. Session state keeps the current filename, FAISS index, chunks, and chat history across those reruns. Without it, the app might process and embed the PDF again for every question.

This is not permanent caching. The data exists only during the active session and is not shared safely across servers or application restarts.

The project also identifies the document only by filename. Two different files can have the same name, causing the wrong index to be reused. I would use a content hash as the document ID and include the embedding and chunking versions in the cache key.

### Q31. What happens when the user uploads a new PDF?

**Strong answer:**

If the new filename is different, the project processes it and replaces the current index and chunks. However, it does not clear the existing chat history.

This means questions and answers from the previous PDF may be included in prompts for the new PDF. That can confuse the model and cause information from one document to affect another.

I would reset history when the active document changes or store separate history for each document ID. In a multi-user system, every document, chunk, history record, and cache entry would also need a tenant or user ID to prevent data leakage.

---

## 7. Testing and evaluation

### Q32. How did you test the project?

**Strong answer:**

The repository contains small smoke scripts for configuration, PDF extraction, chunking, embedding shape, FAISS retrieval, and a live Gemini request. These scripts helped me check each component while building the prototype.

They print results but do not contain assertions, mocks, fixtures, or reliable automatic pass/fail results. Therefore, I would not call them a complete test suite.

The summary spelling bug is a good example of why manual checks are not enough. I would convert these scripts into unit and integration tests that run automatically without requiring a paid Gemini call for normal test runs.

### Q33. What tests would you add first?

**Strong answer:**

I would first test every routing result so the summary bug and missing keyword action are caught. I would test empty PDFs, scanned PDFs, pages where `extract_text()` returns `None`, and documents containing fewer chunks than the requested top-k.

I would test that prompt context contains the retrieved chunks, that history is limited to ten turns, and that history resets when the document changes. I would also test different files with the same filename.

Most tests should use fake embeddings and a fake LLM so they remain fast and predictable. A smaller number of integration tests can process a real sample PDF, and live Gemini tests can run separately.

### Q34. How would you measure retrieval quality?

**Strong answer:**

I would create a set of realistic questions and mark the page or chunk containing each answer. Then I would run the retriever and measure how often the correct passage appears in the top one, top three, or top five results. This is commonly measured with hit rate or recall@k.

I could also measure ranking quality using mean reciprocal rank, which gives more credit when the correct result appears near the top.

This dataset would let me compare chunk sizes, overlap, embedding models, distance methods, and top-k values using evidence instead of guesses.

### Q35. How would you measure final answer quality?

**Strong answer:**

Retrieval quality is only one part. For final answers, I would measure correctness, relevance, faithfulness to the source, citation correctness, and whether the system properly refuses questions that the PDF cannot answer.

I would also track response time, token use, API cost, and failure rates. Human reviewers can judge a smaller high-quality test set. An LLM judge can help evaluate more examples, but it should be checked against human ratings because it can also make mistakes.

I would never claim the system is accurate without defining a test dataset and reporting these results.

---

## 8. Scale, security, and production design

### Q36. What are the main production limitations?

**Strong answer:**

The index exists only in memory, there is no OCR, page metadata or citations are missing, and large summary prompts can exceed context limits. Intent routing is brittle, testing is weak, and model or file errors are not handled carefully.

There is also no authentication, user isolation, monitoring, rate limiting, retry logic, or data-retention policy. PDF text is sent to an external model provider, which creates privacy concerns for sensitive documents.

These limitations do not make the prototype useless. They show the difference between proving an idea and operating a safe, reliable product.

### Q37. How would you scale the system?

**Strong answer:**

I would separate document ingestion from question serving. Uploads would go to object storage, and a background job would extract text, create embeddings, and save chunks and vectors in persistent storage. The user would see a processing status instead of waiting on one web request.

Query servers would remain mostly stateless and search a persistent vector store using user and document filters. For very large datasets, I would evaluate approximate search and reranking.

I would add caching, timeouts, retries, rate limits, monitoring, and autoscaling. Important measurements would include p95 response time, retrieval time, model time, error rate, token use, and cost per successful answer.

### Q38. FAISS or a vector database—which would you choose?

**Strong answer:**

FAISS is a library for vector search. It is simple, fast, and useful for a local prototype. However, it does not automatically provide a distributed service, user authentication, backups, metadata management, or multi-tenant access controls.

A vector database or pgvector becomes useful when indexes must survive restarts, be shared by many servers, support metadata filters, and isolate users. It adds infrastructure and operating cost.

I would keep FAISS for a small local application. I would choose a database when persistence, sharing, filtering, and operations become more important than local simplicity.

### Q39. What security and privacy issues should you consider?

**Strong answer:**

Uploaded PDFs and conversation context are sent to Gemini, so users must know that an external provider may process their data. A real system needs authentication, authorization, encrypted storage and transport, deletion rules, secret management, and careful logging that avoids saving private document content.

For multiple users, every document and chunk needs an owner or tenant ID. The server must enforce these filters before retrieval. A prompt saying “do not show other users’ data” is not access control.

The system also needs file-size limits, file validation, rate limiting, prompt-injection testing, and API key rotation. Sensitive organizations may require a private or self-hosted model.

### Q40. What would you improve first if you had one more week?

**Strong answer:**

First, I would fix correctness issues: the summary typo, the unfinished keyword intent, empty-text handling, top-k edge cases, document identification, and history leakage between PDFs. I would also correct and pin the Gemini dependency because the code imports `google.genai` while the requirements list a different package line.

Second, I would create assertion-based tests and a small evaluation dataset. This would give me real retrieval and answer-quality measurements and prevent old bugs from returning.

Third, I would keep page metadata and show verified source citations. These changes would improve correctness and user trust more than adding another feature. After that, I would work on persistence, OCR, and stronger retrieval.

---

## Final points to remember

- Clearly separate **what the project has now** from **what you would build later**.
- Do not say “accurate,” “fast,” or “scalable” unless you have numbers to prove it.
- Explain each decision as: **what you chose → why → weakness → how you would test it**.
- Be honest about the summary bug, weak tests, and missing evaluation.
- FAISS performs vector search; MiniLM creates embeddings; Gemini writes the answer.
- RAG reduces hallucination risk, but it does not guarantee correct answers.
- If you did not measure something, say so and explain the experiment you would run.

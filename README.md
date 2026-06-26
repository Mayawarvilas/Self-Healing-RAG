# Self-Healing RAG System Workflow

This project implements a Self-Healing Retrieval-Augmented Generation (RAG) architecture that dynamically decides whether external knowledge retrieval is required and continuously evaluates the quality of retrieved information and generated answers. The system can automatically recover from poor retrieval results, irrelevant documents, and low-quality responses by reformulating the query and retrying the retrieval process.

1. Query Input and Retrieval Decision

The workflow begins at the Start node, where the user submits a question.

The decide_retrieval component analyzes the query and determines whether external knowledge is necessary:

If the question can be answered using the LLM's internal knowledge, the system routes directly to generate_direct.
If external information is needed, the system proceeds to the retrieve stage.

This optimization reduces unnecessary vector database searches and improves response speed.

2. Document Retrieval

When retrieval is required, the retrieve node searches the vector database and returns the most relevant document chunks based on semantic similarity.

These retrieved documents are then passed to the is_relevant evaluator.

3. Relevance Verification

The is_relevant node acts as a document quality checker.

Its responsibilities are:

Verify whether the retrieved documents actually contain information useful for answering the user's question.
Filter out irrelevant or noisy retrieval results.
Prevent hallucinations caused by unrelated context.
Outcomes

Relevant Documents Found

Continue to generate_from_context.

Documents Not Relevant

Move to rewrite_question.
Reformulate the user's query.
Retry retrieval with a more optimized search query.

This creates the first self-healing loop.

4. Context-Based Answer Generation

The generate_from_context component generates an answer using the retrieved documents as grounding context.

The generated answer is then evaluated rather than immediately returned to the user.

5. Support Verification (Grounding Check)

The is_sup node determines whether the generated answer is supported by the retrieved context.

It verifies:

Factual consistency
Grounding in retrieved documents
Absence of unsupported claims
Outcomes
Supported Answer

The answer proceeds to accept_answer.

Unsupported Answer

The answer moves to revise_answer.

6. Answer Revision

The revise_answer node attempts to repair the generated response.

Possible actions include:

Removing hallucinated information
Rewriting unsupported statements
Improving factual alignment with retrieved documents

After revision, the answer is sent back to is_sup for re-evaluation.

This forms the second self-healing loop.

7. Usefulness Evaluation

Once an answer passes the support verification stage, it reaches accept_answer and then proceeds to is_use.

The is_use node evaluates whether the answer is:

Complete
Helpful
Relevant
Sufficiently detailed

An answer can be factually correct yet still fail to adequately address the user's question.

8. Final Decision
Useful Answer

If the answer is useful:

is_use → END

The response is delivered to the user.

Not Useful

If the answer is incomplete or unsatisfactory:

is_use → no_answer_found
9. Query Rewriting and Recovery

The no_answer_found node indicates that:

No relevant documents were found,
The generated answer was not useful,
Or retrieval quality was insufficient.

The system then routes to rewrite_question, which:

Rephrases the user's question.
Expands keywords.
Improves semantic search intent.
Sends the rewritten query back to retrieve.

This forms the third self-healing loop.

10. Direct Generation Path

For general knowledge questions that do not require retrieval:

Start
   ↓
decide_retrieval
   ↓
generate_direct
   ↓
END

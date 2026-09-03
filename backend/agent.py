import re

from backend.llm import ask_llm
from backend.tools import calculator
from backend.rag import search_documents
from backend.audit import write_audit


MAX_CONTEXT_LENGTH = 6000


# =========================================================
# DETECT CALCULATION TASK
# =========================================================

def is_calculation_task(task: str) -> bool:

    calculation_words = [

        "calculate",
        "solve",
        "multiply",
        "divide",
        "addition",
        "subtraction",
        "percentage",
        "sum",
    ]


    task_lower = task.lower()


    if any(
        word in task_lower
        for word in calculation_words
    ):

        return True


    if re.search(
        r"\d+\s*[\+\-\*/]\s*\d+",
        task
    ):

        return True


    return False


# =========================================================
# EXTRACT MATHEMATICAL EXPRESSION
# =========================================================

def extract_expression(task: str) -> str:

    match = re.search(
        r"\d+(?:\s*[\+\-\*/]\s*\d+)+",
        task
    )


    if match:

        return match.group(0)


    return ""


# =========================================================
# RUN AGENT
# =========================================================

def run_agent(task: str):

    trace = []


    trace.append(
        "Task received"
    )


    calculation_result = ""

    context = ""

    source_documents = []


    # =====================================================
    # CALCULATION WORKFLOW
    # =====================================================

    if is_calculation_task(task):


        trace.append(
            "Agent identified a calculation task"
        )


        expression = extract_expression(task)


        if expression:


            trace.append(
                f"Calculator tool selected: {expression}"
            )


            calculation_result = calculator(
                expression
            )


            trace.append(
                f"Calculation result: {calculation_result}"
            )


        else:


            trace.append(
                "No mathematical expression found"
            )


    # =====================================================
    # PRIVATE KNOWLEDGE BASE WORKFLOW
    # =====================================================

    else:


        trace.append(
            "Searching private knowledge base"
        )


        try:

            results = search_documents(
                task
            )


        except Exception as error:


            trace.append(
                f"Knowledge base search failed: {error}"
            )


            answer = (
                "The private knowledge base "
                "could not be accessed."
            )


            write_audit(
                task,
                trace,
                answer
            )


            return {

                "answer":
                    answer,

                "trace":
                    trace,

                "sources":
                    []
            }


        documents = results.get(
            "documents",
            [[]]
        )[0]


        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]


        scores = results.get(
            "relevance_scores",
            [[]]
        )[0]


        trace.append(
            f"Relevant documents found: {len(documents)}"
        )


        # =================================================
        # NO RELEVANT INFORMATION
        # =================================================

        if not documents:


            trace.append(
                "No sufficiently relevant private information found"
            )


            trace.append(
                "Private knowledge base cannot answer this question"
            )


            answer = (
                "I couldn't find relevant information "
                "in the private knowledge base."
            )


            write_audit(
                task,
                trace,
                answer
            )


            return {

                "answer":
                    answer,

                "trace":
                    trace,

                "sources":
                    []
            }


        # =================================================
        # SELECT CONTEXT
        # =================================================

        selected_documents = []

        current_length = 0


        for index, document in enumerate(documents):


            remaining = (
                MAX_CONTEXT_LENGTH
                - current_length
            )


            if remaining <= 0:

                break


            document_text = document[
                :remaining
            ]


            selected_documents.append(
                document_text
            )


            current_length += len(
                document_text
            )


            if index < len(metadatas):


                source = metadatas[index].get(
                    "source",
                    "Unknown"
                )


                if source not in source_documents:

                    source_documents.append(
                        source
                    )


        context = "\n\n".join(
            selected_documents
        )


        trace.append(
            f"Context accepted: {len(context)} characters"
        )


        if scores:


            best_score = max(
                scores
            )


            trace.append(
                f"Best relevance score: {best_score:.2f}"
            )


    # =====================================================
    # GENERATE FINAL ANSWER
    # =====================================================

    trace.append(
        "Generating final answer with local AI"
    )


    prompt = f"""

You are a secure sovereign on-premise AI assistant.

The AI model is running locally.

USER QUESTION:
{task}

PRIVATE KNOWLEDGE BASE:
{context}

CALCULATION RESULT:
{calculation_result}

STRICT INSTRUCTIONS:

1. Answer the user's question directly and clearly.

2. If the PRIVATE KNOWLEDGE BASE contains
   information relevant to the question, use
   that information to answer.

3. Do NOT use unrelated information from the
   PRIVATE KNOWLEDGE BASE.

4. Do NOT invent facts.

5. Do NOT claim that information exists in the
   private knowledge base when it does not.

6. For calculations, use the CALCULATION RESULT.

7. Keep the answer concise.

8. If the knowledge base information is relevant,
   answer using that information only.

"""


    try:

        answer = ask_llm(
            prompt
        )


    except Exception as error:


        trace.append(
            f"Local AI generation failed: {error}"
        )


        answer = (
            "The local AI model could not "
            "generate an answer."
        )


        write_audit(
            task,
            trace,
            answer
        )


        return {

            "answer":
                answer,

            "trace":
                trace,

            "sources":
                source_documents
        }


    trace.append(
        "Final answer generated"
    )


    # =====================================================
    # AUDIT LOG
    # =====================================================

    write_audit(
        task,
        trace,
        answer
    )


    return {

        "answer":
            answer,

        "trace":
            trace,

        "sources":
            source_documents
    }
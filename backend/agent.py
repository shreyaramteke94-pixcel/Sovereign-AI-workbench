import re

from backend.llm import ask_llm
from backend.tools import calculator
from backend.rag import search_documents
from backend.audit import write_audit


MAX_CONTEXT_LENGTH = 6000


# =========================================
# TASK TYPE DETECTION
# =========================================

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

def is_policy_task(task: str):

    policy_words = [
        "policy",
        "policies",
        "allowed",
        "allow",
        "permission",
        "approval",
        "approve",
        "compliance",
        "compliant",
        "violate",
        "violation",
        "rule",
        "rules",
        "remote work",
        "work remotely",
        "company policy",
        "employee",

        # Security and data-protection terms
        "confidential",
        "personal cloud",
        "personal device",
        "google drive",
        "cloud storage",
        "data protection",
        "security incident",
        "external sharing",
        "external organization",
        "share confidential",
        "company documents",
    ]

    task_lower = task.lower()

    return any(
        word in task_lower
        for word in policy_words
    )


# =========================================
# CALCULATOR
# =========================================

def extract_expression(task: str) -> str:

    match = re.search(
        r"\d+(?:\s*[\+\-\*/]\s*\d+)+",
        task
    )

    if match:
        return match.group(0)

    return ""


# =========================================
# AUDIT
# =========================================

def save_audit(
    task: str,
    trace: list,
    answer: str
):

    try:

        write_audit(
            task=task,
            trace=trace,
            answer=answer
        )

    except Exception as error:

        print(
            f"Audit logging failed: {error}"
        )


# =========================================
# MAIN AGENT
# =========================================

def run_agent(task: str):

    trace = []

    trace.append(
        "Task received"
    )

    calculation_result = ""

    context = ""

    source_documents = []

    task_type = "knowledge"

    # =========================================
    # CALCULATION ROUTING
    # =========================================

    if is_calculation_task(task):

        task_type = "calculation"

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


    # =========================================
    # POLICY / COMPLIANCE ROUTING
    # =========================================

    else:

        if is_policy_task(task):

            task_type = "policy"

            trace.append(
                "Agent identified a policy/compliance task"
            )

            trace.append(
                "Searching private policy knowledge base"
            )

        else:

            trace.append(
                "Searching private knowledge base"
            )


        # =========================================
        # PRIVATE KNOWLEDGE SEARCH
        # =========================================

        try:

            results = search_documents(task)

        except Exception as error:

            trace.append(
                f"Knowledge base search failed: {error}"
            )

            answer = (
                "The private knowledge base "
                "could not be accessed."
            )

            save_audit(
                task,
                trace,
                answer
            )

            return {
                "answer": answer,
                "trace": trace,
                "sources": []
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


        # =========================================
        # NO RELEVANT INFORMATION
        # =========================================

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

            save_audit(
                task,
                trace,
                answer
            )

            return {
                "answer": answer,
                "trace": trace,
                "sources": []
            }


        # =========================================
        # BUILD PRIVATE CONTEXT
        # =========================================

        selected_documents = []

        current_length = 0


        for index, document in enumerate(documents):

            remaining = (
                MAX_CONTEXT_LENGTH
                - current_length
            )

            if remaining <= 0:
                break


            document_text = document[:remaining]

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

            best_score = max(scores)

            trace.append(
                f"Best relevance score: {best_score:.2f}"
            )


        # =========================================
        # POLICY VERIFICATION STEP
        # =========================================

        if task_type == "policy":

            trace.append(
                "Relevant policy evidence identified"
            )

            trace.append(
                "Evaluating request against organizational policy"
            )


    # =========================================
    # LOCAL AI GENERATION
    # =========================================

    trace.append(
        "Generating final answer with local AI"
    )


    if task_type == "policy":

        prompt = f"""
You are a secure enterprise policy compliance assistant
running entirely on a local on-premise AI system.

USER REQUEST:
{task}

PRIVATE COMPANY POLICY:
{context}

IMPORTANT INSTRUCTIONS:

1. Evaluate the user's request ONLY against the
   provided private company policy.

2. Do not use outside knowledge.

3. Do not invent company rules.

4. Clearly state whether the request is:
   - Allowed
   - Requires Approval
   - Not Allowed
   - Cannot Be Determined

5. If approval is required, identify what approval
   the policy requires.

6. Explain the relevant policy rule briefly.

7. If the policy does not contain enough information,
   say that it cannot be determined from the policy.

8. Mention the relevant source document when possible.

9. Keep the answer concise and professional.

10. Do not claim that a policy rule exists unless it
    is present in the PRIVATE COMPANY POLICY.
"""


    else:

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


    # =========================================
    # LOCAL MODEL
    # =========================================

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

        save_audit(
            task,
            trace,
            answer
        )

        return {
            "answer": answer,
            "trace": trace,
            "sources": source_documents
        }


    # =========================================
    # POLICY COMPLETION
    # =========================================

    if task_type == "policy":

        trace.append(
            "Policy compliance evaluation completed"
        )


    # =========================================
    # COMPLETION
    # =========================================

    trace.append(
        "Final answer generated"
    )


    # =========================================
    # AUDIT LOGGING
    # =========================================

    save_audit(
        task,
        trace,
        answer
    )


    return {
        "answer": answer,
        "trace": trace,
        "sources": source_documents
    }
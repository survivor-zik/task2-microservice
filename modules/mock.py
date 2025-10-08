from typing import Literal

from modules.prompt import *


async def get_prompt(request, total, mode) -> Literal[dict, str]:
    if mode == "mock":
        lang = request["client"].get("lang", "ar")
        if lang == "ar":
            prompt = MOCK_LLM_AR.format(
                client_name=request["client"]["name"],
                currency=request["currency"],
                items="\n".join(
                    [
                        f"- {item['qty']} x {item['sku']}"
                        for item in request["items"]
                    ]
                ),
                grand_total=total,
                delivery_terms=request["delivery_terms"],
                notes=request["notes"],
            )
            subject = MOCK_LLM_SUBJECT_AR.format(client_name=request["client"]["name"])
            return {"subject": subject, "body": prompt}
        else:
            prompt = MOCK_LLM_EN.format(
                client_name=request["client"]["name"],
                currency=request["currency"],
                items="\n".join(
                    [
                        f"- {item['qty']} x {item['sku']}"
                        for item in request["items"]
                    ]
                ),
                grand_total=total,
                delivery_terms=request["delivery_terms"],
                notes=request["notes"],
            )
            subject = MOCK_LLM_SUBJECT_EN.format(client_name=request["client"]["name"])
            prompt = {"subject": subject, "body": prompt}
            return prompt
    elif mode == "openai":
        lang = request["client"].get("lang", "ar")
        prompt = LLM_PROMPT.format(
            lang=lang,
            delivery_terms=request["delivery_terms"],
            currency=request["currency"],
            items="\n".join(
                [
                    f"- {item['qty']} x {item['sku']}"
                    for item in request["items"]
                ]
            ),
            grand_total=total,
            client_name=request["client"]["name"],
            notes=request["notes"],
        )
        return prompt

    else:
        raise ValueError("Unsupported mode")

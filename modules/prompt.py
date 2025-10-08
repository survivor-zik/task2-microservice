MOCK_LLM_EN="""
Dear {client_name},
Please find our quotation below for your requested items:

• Delivery Terms: {delivery_terms}
• Total Amount: {grand_total} {currency}
• Items: {items}
• Notes: {notes}

We remain at your disposal for any clarification.


Best regards,
Alrouf Lighting Team

"""

MOCK_LLM_SUBJECT_EN="Quotation for {client_name}"

MOCK_LLM_SUBJECT_AR="عرض سعر لـ {client_name}"
MOCK_LLM_AR="""
النص:
عزيزي {client_name}،
يرجى الاطلاع على عرض الأسعار التالي للعناصر المطلوبة:

• شروط التسليم: {delivery_terms}
• الإجمالي: {grand_total} {currency}
• ملاحظات: {notes}
• العناصر: {items}


مع خالص التحية،
فريق الروف للإضاءة

"""


LLM_PROMPT="""
    You are an Expert Assistant that generates professional email drafts in both English and Arabic for business quotations.
    Given the following details, create a concise and professional email draft in both languages.
    Ensure the drafts are clear, polite, and suitable for business communication.
        NOTE:
            Look at the language preference of the client and generate the email draft accordingly.
        
        Details:
            Lang: {lang}
            Delivery Terms: {delivery_terms}
            Items: {items}
            Grand Total: {grand_total} {currency}
            Client Name: {client_name}
            Notes: {notes}

    Return the response email without any markdown formatting."""



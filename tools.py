import json
from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool

from prompts import (
    send_profile_via_email_tool_name,
    send_profile_via_email_tool_desc,
    retrieve_company_information_tool_name,
    retrieve_company_information_tool_desc
)
from KnowledgeBase.response import get_query_result

class SendProfileViaEmailInput(BaseModel):
    email: str = Field(..., description="email address of the user to send the profile to")
    
class SendProfileViaEmail(BaseTool):
    name: str = send_profile_via_email_tool_name
    description: str = send_profile_via_email_tool_desc

    def _run(self, input_str: str="", **kwargs):
        print("\nSend Profile Via Email tool recieved input")
        print(f"Kwargs: `{kwargs}`", end="\n")
        print(f"Input: `{input_str}`", end="\n\n")

        if "email" in kwargs:
            email = kwargs["email"]
        else:
            try:
                input_dict = json.loads(input_str)
                email = input_dict.get("email", "")
            except json.JSONDecodeError:
                return "Invalid input format. Please provide a valid JSON."

        return "Check your email for the company profile. Profile sent to " + email
    
    def _arun(self, email: str):
        raise NotImplementedError("This tool does not support async execution")
    
    
class RetrieveCompanyInformation(BaseTool):
    name: str = retrieve_company_information_tool_name
    description: str = retrieve_company_information_tool_desc

    def _run(self, input_str: str="", **kwargs):

        print("\nRetreive Company Information tool recieved input")
        print(f"Kwargs: `{kwargs}`", end="\n")
        print(f"Input: `{input_str}`", end="\n\n")

        if "query" in kwargs:
            query = kwargs["query"]
        else:
            try:
                input_dict = json.loads(input_str)
                query = input_dict.get("query", "")
            except json.JSONDecodeError:
                return "Invalid input format. Please provide a valid JSON."

        result = get_query_result(
            query=query
        )

        return result
    
    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async execution")
        return query
    


from pydantic import BaseModel 


class JobsQuery(BaseModel): 
    job_search_text: str 
    job_location: str
    email: str

    class Config: 
        schema_example = {
            'example': {
                'job_search_text': 'Junior Software Engineer', 
                'job_location': 'Remote', 
                'email': 'example@example.com'
            }
        } 




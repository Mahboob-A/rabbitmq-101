
from fastapi import FastAPI 
from fastapi.exceptions import HTTPException 


from rabbitmq import cloudamqp_jobpublisher
from validators import is_valid_email
from schema import JobsQuery


app = FastAPI()


@app.get('/')
async def root(): 
    return {'message': 'hello world!'}


@app.post('/jobs/new')
async def post_job_query(job_data: JobsQuery):
    job_search_text = job_data.job_search_text
    job_location = job_data.job_location
    email = job_data.email 


    if not job_search_text or not job_location or not email: 
        return HTTPException(
            detail={'message: all the parameters are needed!'}, 
            status=400
        )

    if not is_valid_email(email=email): 
        return HTTPException(
            detail={'message':'email is not valid'}, 
            status=400
        )
    
    data = {
        'job_search_text':job_search_text, 
        'job_location':job_location, 
        'email':email
    }

    # push/publish to rabbitmq queue 
    await cloudamqp_jobpublisher.publish_jobs(
        data=data
    )

    return('your job search post has been queued! you will get resualts shortly!')








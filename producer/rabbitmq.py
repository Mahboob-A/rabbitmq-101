import os, json 
import pika 
from dotenv import load_dotenv

load_dotenv()




class CloudAMQPHelper: 
    class Config: 
        EXCHANGE_NAME='job_search_exchange'
        EXCHANGE_TYPE='direct'
        QUEUE_NAME='job_search_queue'
        BINDING_KEY='job_search'
        ROUTING_KEY='job_search'
    
    def __init__(self) -> None: 
        url = os.environ.get('CLOUD_AMQP_URL')
        params = pika.URLParameters(url)

        self.__connection = pika.BlockingConnection(params)

    async def __get_channel_helper(self) -> pika.BlockingConnection: 
        channel = self.__connection.channel()
        return channel 
    
    async def __set_or_create_exchange_and_queue_helper(self) -> None: 
        channel = await self.get_channel()

        # declare exchange 
        channel.exchange_declare(
            exchange=self.Config.EXCHANGE_NAME, 
            exchange_type=self.Config.EXCHANGE_TYPE
        )

        # declare queue 
        channel.queue_declare(
            queue=self.Config.QUEUE_NAME
        )

        # bind exchange and queue 
        channel.queue_bind(
            self.Config.QUEUE_NAME, 
            self.Config.EXCHANGE_NAME, 
            self.Config.BINDING_KEY
        )

    # methods to interact from child class 
    async def set_or_create_exchange_and_queue(self): 
        await self.__set_or_create_exchange_and_queue_helper()
    
    async def get_channel(self): 
        return await self.__get_channel_helper()

    def close_connection(self): 
        self.__connection.close()



class JobPublisher(CloudAMQPHelper):
    
    async def publish_jobs(self, data) -> None: 
        
        await self.set_or_create_exchange_and_queue()

        channel = await self.get_channel()

        channel.basic_publish(
            exchange=self.Config.EXCHANGE_NAME, 
            routing_key=self.Config.ROUTING_KEY, 
            body=json.dumps(data)
        )

        print ("Info: Message sent to consumer")

        # self.close_connection()



# if __name__ == '__main__': 
cloudamqp_jobpublisher = JobPublisher()
















# ###################################################

# class Demo: 
#     class Config: 
#         EXCHANGE_NAME='job_search_exchange'
#         EXCHANGE_TYPE='direct'
#         QUEUE_NAME='job_search_queue'
#         BINDING_KEY='job_search'
#         ROUTING_KEY='job_search'
    
#     def test(self) -> str: 
#         string = f'{self.Config.EXCHANGE_NAME} and {self.Config.EXCHANGE_TYPE}'
#         return string


# d = Demo()

# print(d.test())





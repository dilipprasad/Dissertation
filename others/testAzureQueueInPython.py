#Run the below command to install azure related services
#   pip install azure
# https://docs.microsoft.com/en-us/azure/storage/queues/storage-python-how-to-use-queue-storage?tabs=python2%2Cenvironment-variable-windows
# https://pypi.org/project/azure-data-tables/

from azure.storage.queue import (
        QueueService,
        QueueMessageFormat
)

crawledUrlInsertQueueConStr = "DefaultEndpointsProtocol=https;AccountName=artifactsdatastorage;AccountKey=FPoDnacbEV1KRm1zZxAdqS6k8HI6VLHeRGwDsjm113Y+cvfXV5SyuAE8X/0kdBodhjqqxW5YpxnHCZuKbVzjNA==;EndpointSuffix=core.windows.net"

# Retrieve the connection string from an environment
# variable named AZURE_STORAGE_CONNECTION_STRING
#connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
connect_str = crawledUrlInsertQueueConStr

# Create a unique name for the queue
# queue_name = "queue-" + str(uuid.uuid4())
queue_name = "queue-crawledarchiveurls"

# Create a QueueService object which will
# be used to create and manipulate the queue
# print("Creating queue: " + queue_name)
queue_service = QueueService(connection_string=connect_str)

# Create the queue
# queue_service.create_queue(queue_name)

# Setup Base64 encoding and decoding functions
# queue_service.encode_function = QueueMessageFormat.binary_base64encode
# queue_service.decode_function = QueueMessageFormat.binary_base64decode

message = u"Hello, World"
print("Adding message: " + message)
queue_service.put_message(queue_name, message)

metadata = queue_service.get_queue_metadata(queue_name)
count = metadata.approximate_message_count
print("Message count: " + str(count))

messages = queue_service.get_messages(queue_name)

for message in messages:
    print("Dequeueing message: " + message.content)
    queue_service.delete_message(queue_name,message.id, message.pop_receipt)
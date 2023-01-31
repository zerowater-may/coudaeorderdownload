# from boto3 import client

# def remove_prefix(text, prefix):
#     if text.startswith(prefix):
#         return text[len(prefix):]
#     return text

# def get_directory_size_bytes():
# #   s3_client = client('s3')
# #   bucket_name = remove_prefix(s3Url, "s3://").split('/',1)[0]
# #   prefix = remove_prefix(s3Url, "s3://").split('/',1)[1]

# #   dir_info = s3_client.list_objects(Bucket=bucket_name, Prefix=prefix)['Contents']

# #   total_size = 0

# #   for object_in_dir in dir_info:
# #     total_size = total_size + object_in_dir['Size']

# #   return total_size
#     s3_client = client('s3')
#     bucket_name = "bucket"
#     prefix = "coudae/"
#     dir_info = s3_client.list_objects(Bucket=bucket_name, Prefix=prefix, Delimiter='/')['CommonPrefixes']
#     print(dir_info)
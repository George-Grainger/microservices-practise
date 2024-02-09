import pika, json

def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
    # Catching all exceptions - surely bad practice?
    except Exception as err:
        return "internal server error", 500
    
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        # Username must be unique so uniquely identifies user
        "username": access["username"],
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                # Ensures the messages are maintained if the pod crashes
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except:
        fs.delete(fid)
        return "internal server error", 500
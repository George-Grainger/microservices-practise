import pika
import os
import json
import tempfile
import moviepy.editor
from bson.objectid import ObjectId


def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)

    # empty temp file
    tf = tempfile.NamedTemporaryFile()

    # video contents
    out = fs_videos.get(ObjectId(message["video_fid"]))

    # add video contents to empty file
    tf.write(out.read())

    # convert temp video file into audio
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()

    # write audio to its own file
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path)

    # Save file to mongo
    f = open(tf, "rb")
    data = f.read()
    fid = fs_mp3s.put(data)
    f.close()
    os.remove(tf_path)

    # Update our message
    message["mp3_fid"] = str(fid)

    # add new message to mp3 queue
    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
        )
    except Exception as err:
        fs_mp3s.delete(fid)
        return "failed to publish message"

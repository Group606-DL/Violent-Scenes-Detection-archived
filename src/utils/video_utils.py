
# # TODO: add video file class?
# class VideoFile(str):
#     @staticmethod
#     def get_name():
#         return VideoFile.split(".")[0]


def get_video_name(video_file):
    return video_file.split(".")[0]

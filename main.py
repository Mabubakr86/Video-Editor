#########################################
#
# Script for video editing with python
#
########################################

# import packages
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import *
from PIL import Image
import os


def get_video_info(video_path=''):
    """
    function to extract main informations from video
    input : video path
    return -> size, fps, duration
    """
    try:
        clip = VideoFileClip(video_path)        # convert to videoclip object
        fps = clip.reader.fps                   # frames per second
        n_frames = clip.reader.nframes          # total number of frames  
        duration = int(clip.reader.duration)    # video duration
        size = clip.size                        # video size (width, height)
        print(f'Video size is : {size}',
            f'\nVideo fps is : {fps}',
            f'\nVideo duration is : {duration} seconds')
        return size, fps, duration
    except Exception as e:
        print(e)

def get_thumbnails(video_path='', output_dir='thumbnails',all=True,**kwargs):
    """
    function to extract thumbnails from video
    input : video path
    return -> thumnails of video
    """
    try:
        base_path = os.path.abspath(__file__)
        base_dir = os.path.dirname(base_path)
        os.makedirs(output_dir, exist_ok=True)
        output_dir = os.path.join(base_dir, output_dir)
        clip = VideoFileClip(video_path)
        if all == True:
            duration = int(clip.reader.duration)
            start = 0
            end = duration 
        else:
             start = 60 * int(kwargs['start_min']) + kwargs['start_sec']
             end = 60 * int(kwargs['end_min']) + kwargs['end_sec']
        for i in range(start, end + 1):
            frame = clip.get_frame(i)           # get numpy array of pixels 
            frame_img = Image.fromarray(frame)
            image_path = os.path.join(output_dir,f'{i}.png')
            print(f'created {i}.png')
            frame_img.save(image_path)
    except Exception as e:
        print(e)

def get_subclip(video_path='', start_min=0, start_sec=0, end_min=1, end_sec=1, output_path=''):
    """
    function to extract subclip from video
    input : video path
    return -> subclip of video
    """
    try:
        start = 60 * int(start_min) + start_sec
        end = 60 * int(end_min) + end_sec
        return ffmpeg_extract_subclip (video_path,t1=start, t2=end, targetname=output_path)
    except Exception as e:
        print(e)


def get_video_audio_merged(video_path='', audio_path='', output_path=''):
    try:
        return ffmpeg_merge_video_audio(video=video_path, audio=audio_path, output=output_path)
    except Exception as e:
        print(e)

def get_resized_video(video_path='', output_path='', size=()):
    try:
        return ffmpeg_resize(video=video_path, output=output_path, size=size)
    except Exception as e:
        print(e)


def get_audio(video_target='', audio_source='',output_path='' ):
    """
    function to extract audio from one video and apply it to other video
    input : source_audio: the path of video from where we will extract audio
            video_target: the path of video to where we will apply audio
            output_path : the path to where merged video saved
    return-> merged video
    """
    try:
        #select video
        clip1 = VideoFileClip(audio_source)
        #extract the audio from clip1
        audioclip1 = clip1.audio
        #select the video we want to add music to
        clip2 = VideoFileClip(video_target)
        #add music to clip2 
        new_video = clip2.set_audio(audioclip1)
        #output  mp4
        new_video.write_videofile(output_path) 
        return new_video
    except Exception as e:
        print(e)


def add_video(video1_path='', video2_path='', output_path=''):
    """
    function to add to videos
    input : video1_path : the path of 1st video 
            video2_path: the path of 2nd video 
            output_path : the path to where merged video saved
    return-> merged video
    """
    try:
        #Read video and select from 10s~20s
        clip1 = VideoFileClip(video1_path)
        #Scale the video size to 60%
        clip2 = VideoFileClip(video2_path)
        #Merge the video(clip1&clip2)
        final_clip = concatenate_videoclips([clip1,clip2])
        #Output the video file
        final_clip.write_videofile(output_path)
    except Exception as e:
        print(e)

def add_logo(video_path='',logo_path='', output_path='',
             opts={'start':0,'height':200, 'width':200, 'pos':("right","top")}):
    """
    function to add logo to videos
    input : video_path : the path of  video 
            logo_path: the path to logo
            output_path : the path to where merged video saved
    return-> merged video
    """
    try:
        video = VideoFileClip(video_path)
        logo = (ImageClip(logo_path).set_start(opts['start'])
                  .set_duration(video.duration)
                  .resize(height=opts['height'], width=opts['width']) # if you need to resize...
                  .set_pos(opts['pos']))

        final = CompositeVideoClip([video, logo])
        final.write_videofile(output_path, codec='libx264')
    except Exception as e:
        print(e)

def add_text(text='', video_path='' ,output_path='', **kwargs):
    """
    function to add text to video
    input : text : the text taht will be added
            video_path : the path of  video 
            **kwargs : involve some main control options (fontsize, fontcolor, position)
            output_path : the path to where merged video saved
    return-> merged video
    """
    text = TextClip(text,font='Arial',fontsize=kwargs['fontsize'],color=kwargs['color']).set_start(kwargs['start']).set_pos(kwargs['pos']).set_duration(kwargs['duration'])
    clip = VideoFileClip(video_path)
    final_clip = CompositeVideoClip([clip, text])
    final_clip.write_videofile(output_path, codec='libx264', fps=25)


if __name__ == '__main__':
    video_path='corey.mp4'
    audio_path='audio.mp3'
    output_path='results.mp4'
    # get_video_info(video_path)
    # get_thumbnails(video_path=video_path, output_dir='thumbnails', all=False, start_min=12, start_sec=10,end_min=15, end_sec=20)
    # get_subclip (video_path=video_path, start_min=10, start_sec=0, end_min=10, end_sec=10, output_path=output_path)
    # get_video_audio_merged(video_path='results.mp4', audio_path='audio.mp3', output_path='merged2.mp4')
    # get_resized_video(video_path='other2.ts', output_path='other3.ts', size=(320,320))
    # get_audio(video_target='', audio_source='', output_path='')
    # add_video(video1_path='sub.ts', video2_path='y2.mkv', output_path='mix.mp4')
    # add_logo(video_path='results.mp4', logo_path='me.jpg', output_path='with_photo.mp4', opts={'start':2,'height':150, 'width':150, 'pos':("left","top")})
    add_text(text='Mbakr',video_path='results.mp4',output_path='with_text.mp4',fontsize=70, color='red', start=1, pos=('right','center'), duration=3 )

import streamlit as st
import os
import json
import subprocess

def download_song(url):
    result = subprocess.call(['yt-dlp', url])
    return result == 0

def download_twitch_video(url, quality=None, auth_token=None):
    command = ['twitch-dl', 'download', url]
    if quality:
        command.extend(['-q', quality])
    if auth_token:
        command.extend(['--auth-token', auth_token])
    result = subprocess.call(command)
    return result == 0

def get_json_files():
    json_files = [pos_json for pos_json in os.listdir() if pos_json.endswith('.info.json')]
    return json_files

def read_metadata(json_file):
    with open(json_file, 'r') as fp:
        data = json.load(fp)
    return data

def main():
    st.title('Media Downloader')
    
    platforms = ['SoundCloud', 'Twitch']
    selected_platform = st.selectbox('Select Platform', platforms)
    
    if selected_platform == 'SoundCloud':
        st.subheader('SoundCloud Downloader')
        url = st.text_input('Enter SoundCloud URL')
        if st.button('Download'):
            if download_song(url):
                st.success('Download successful!')
                json_files = get_json_files()
                if json_files:
                    metadata = read_metadata(json_files[0])
                    thumb = metadata.get('thumbnail', 'No thumbnail found')
                    title = metadata.get('fulltitle', 'No title found')
                    st.image(thumb, caption=title)
                    st.write(f"**Title:** {title}")
                    st.write(f"**Thumbnail URL:** {thumb}")
                    for json_file in json_files:
                        try:
                            os.remove(json_file)
                        except Exception as e:
                            st.error(f'Error removing JSON file: {e}')
            else:
                st.error('Download failed. Please check the URL and try again.')
    
    elif selected_platform == 'Twitch':
        st.subheader('Twitch Video Downloader')
        url = st.text_input('Enter Twitch Video URL')
        quality = st.selectbox('Select Quality', ('source', '720p', '480p', '360p', 'audio_only'))
        auth_token = st.text_input('Enter Auth Token (optional)')
        if st.button('Download'):
            if download_twitch_video(url, quality, auth_token):
                st.success('Download successful!')
            else:
                st.error('Download failed. Please check the URL and try again.')

if __name__ == '__main__':
    main()
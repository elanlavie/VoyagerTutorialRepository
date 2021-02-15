import os

from tqdm.notebook import tqdm as tqdm_notebook
from tqdm import tqdm
import requests

def download_file_with_progress_bar(url, filename=None, download_dir=os.curdir, mkdir=True, redownload=False):
    # From https://stackoverflow.com/a/37573701/4228052
    
    # Use the filename from the end of the URL by default
    if filename is None:
        filename = os.path.basename(url)
        
    # Make sure the download directory exists
    if not os.path.exists(download_dir):
        if mkdir:
            os.makedirs(download_dir)
        else:
            raise FileNotFoundError("Download directory '{}' does not exist, and `mkdir` option is disabled.".format(download_dir))
    elif not os.path.isdir(download_dir):
        raise NotADirectoryError("Download directory '{}' exists, but is not actually a directory!".format(download_dir))
        
    download_path = os.path.join(download_dir, filename)
    None
    
        
    if os.path.exists(download_path) and not redownload:
        print("File '{}' already exists - not re-downloading {}".format(download_path, url))
        return
        
    # Streaming, so we can iterate over the response.
    response = requests.get(url, stream=True)
    # Quit early if there's an error
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise requests.exceptions.HTTPError("Failed to download {} to {}".format(url, download_path)) from e
    
    # Create the progress bar
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024 #1 Kibibyte
    try:
        progress_bar = tqdm_notebook(total=total_size_in_bytes, unit='iB', unit_scale=True, desc=download_path)
    except ImportError:
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc=download_path, mininterval=5)
    
    # Write the file
    with open(download_path, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    
    # Make sure the download completed
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        progress_bar.clear()
        raise ValueError("Unexpected error: failed to completely download {}".format(url))
        
    progress_bar.close()
    return response
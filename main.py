import py_cui
from youtubesearchpython import *
import sys
import os

all_videos = []  # global dict that contains all videos

if len(sys.argv):
    print('Usage: python3 main.py /path/to/browser/executable')
    sys.exit()

browser_path = str(sys.argv[1])


class YtSearcher:
    def __init__(self, master: py_cui.PyCUI):
        self.master = master

        self.search = ''

        self.search_textbox = self.master.add_text_box('Search:', 0, 0, column_span=6)
        self.videos_list = self.master.add_scroll_menu('Videos', 2, 0, column_span=6, row_span=5)

        self.search_textbox.add_key_command(py_cui.keys.KEY_ENTER, self.search_videos)
        self.videos_list.add_key_command(py_cui.keys.KEY_ENTER, self.list_handler)

    def search_videos(self, next_page=False):
        global all_videos

        query = self.search_textbox.get()
        if not next_page:  # if next_page is False - rewrites object
            self.search = VideosSearch(query, limit=20)
            all_videos.clear()  # clears global dict if user enters a new query
        result = self.search.result(mode=ResultMode.dict)
        videos = {}  # local dict to parse new videos
        for i in range(0, 20):
            try:
                vid = result['result'][i]['id']
                title = result['result'][i]['title']
                videos[vid] = title

                all_videos.append(vid + '-:split:-' + title)
            except:
                break
        if not next_page:
            self.videos_list.clear()
        else:
            self.videos_list.remove_selected_item()  # removes 'Load more [Press Enter]' from the list
        self.videos_list.add_item_list(list(videos.values()))
        self.videos_list.add_item('Load more [Press Enter]')

    def list_handler(self):
        selected = self.videos_list.get()
        if selected == 'Load more [Press Enter]':  # bad code
            try:
                self.search.next()
                self.search_videos(next_page=True)
            except:
                pass
        else:
            for video in all_videos:
                if selected in video:
                    vid = video.split('-:split:-')[0]  # ugly but works
                    os.system(browser_path + ' https://www.youtube.com/watch?v=' + vid)


root = py_cui.PyCUI(7, 6)

if browser_path == '-h' or browser_path == '--help':
    print('Usage: python3 main.py /path/to/browser/executable')
    sys.exit()
elif not os.path.exists(browser_path):
    print('Error! Path ' + browser_path + ' does not exists')
    sys.exit()

root.toggle_unicode_borders()
root.set_title('YouTube Searcher')
yt = YtSearcher(root)
root.start()


import py_cui
from youtubesearchpython import *


class YtSearcher:
    def __init__(self, master: py_cui.PyCUI):
        self.master = master

        self.search = ''

        self.search_textbox = self.master.add_text_box('Search:', 0, 0, column_span=6)
        self.videos_list = self.master.add_scroll_menu('Videos', 2, 0, column_span=6, row_span=5)

        self.search_textbox.add_key_command(py_cui.keys.KEY_ENTER, self.search_videos)
        self.videos_list.add_key_command(py_cui.keys.KEY_ENTER, self.list_handler)

    def search_videos(self, next_page=False):
        query = self.search_textbox.get()
        if not next_page:
            self.search = VideosSearch(query, limit=20)
        result = self.search.result(mode=ResultMode.dict)
        videos = {}
        for i in range(0, 20):
            try:
                vid = result['result'][i]['id']
                title = result['result'][i]['title']
                videos[vid] = title
            except Exception as ex:  # bad code
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


root = py_cui.PyCUI(7, 6)

root.toggle_unicode_borders()
root.set_title('YouTube Searcher')
yt = YtSearcher(root)
root.start()

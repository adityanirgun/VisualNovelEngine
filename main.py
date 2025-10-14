import pyglet
import sys
import os
from pyglet.window.event import WindowEventLogger
from pyglet.window import mouse
from pyglet.window import key
#import classes
import time
from datetime import datetime
import json
from pyglet import image
from pyglet.graphics import Batch
from pyglet.gl import *

from dataclasses import dataclass, field
from typing import List, Dict, Any


class Window(pyglet.window.Window):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        print('Window created')
        self.game_state = 0
        print('window test')
        self.togglefullscreen = 0  # initial toggle state
        self._prev_fullscreen = self.togglefullscreen  # track previous state
        self.skip_on = 0

    def on_key_press(self, KEY, MOD):
        print(KEY)
        if KEY == key.LCTRL:
            print('LCTRL pressed in window')
            print(KEY)
            self.skip_on = 1
            #self.on_key_press(1,[])
        if KEY == key.C:
            print('C Key Pressed')
        if KEY == 65307:
            #ESCAPE key pressed
            #music_player.delete()

            if self.game_state == 3:

                self.game_state = 0
                if music_player.playing:
                    # print('AUDIO IS PLAYING')
                    music_player.pause()
                #audioPlayer.stop()
                #audioPlayer.end()
                # music = pyglet.resource.media("theme0.wav")
                #music_player.queue(pyglet.resource.media("theme0.wav"))
                # setattr(music_player,'loop',True)


            if self.game_state == 1:
                pyglet.app.exit()

        if KEY == 65470:
            #F1 pressed
            if self.game_state ==3:
                memory.save()
        if KEY == 65471:
            #F2 pressed
            if self.game_state ==1:
                memory.load()
        if KEY == 32:
            #space key pressed
            self.on_mouse_release(0,0,1,0)



        if KEY == 102 :
            # F key pressed
            if self.togglefullscreen == 0:
                self.togglefullscreen = 1
                print('Fullscreen"d')
            else:
                if self.togglefullscreen == 1:
                    self.togglefullscreen = 0
                    print('Small screened')
        #if KEY == key.L:
        if KEY == 108 :
            print("L Key pressed")
            if reader.log == 0:
                reader.log = 1
                print('log turned on')
            else:
                if reader.log == 1:
                    reader.log = 0
                    print('log turned off')
        '''
        if KEY  == 65507:
            #CTRL pressed
            print('CTRL pressed, window')
            #window.on_mouse_release(0, 0, 1, 0)
            #reader.skip = 1
        '''
    def on_key_release(self, KEY, MOD):
        if KEY == 65507:
            print('CTRL released')
            self.skip_on = 0

    def on_mouse_scroll(self,x,y,scroll_x,scroll_y):
        print(scroll_y)
        if self.game_state == 3:
            #reader.log =0
            if scroll_y > 0 and reader.current_page > 0 and reader.current_page < reader.total_pages:
                reader.current_page = reader.current_page - 1
                reader.timeline_read(reader.current_page)
            if scroll_y < 0 and reader.current_page < reader.latest_page-1 and reader.current_page < reader.total_pages:
                reader.current_page = reader.current_page + 1
                reader.timeline_read(reader.current_page)

    def on_mouse_release(self,x,y,button, modifiers):
        '''Might need to abstract a function here like load new page or something for clarity. like make everything after gamestate check a method within reader possibly '''
        print(button)
        print(x)
        print(y)
        if button == 1:
            #print('left click mouse')

            if self.game_state == 3:
                #if game in play mode
                #print stats
                print('COMPLETION:%s'%completion.report())
                print("DATA LENGTH %s"%reader.total_chapters)
                print("CURRENT PAGE %s"%reader.current_page)
                print("CURRENT LATEST %s"%reader.latest_page)
                print("CURRENT CHAPTER %s"%reader.current_chapter)
                print('TOTAL PAGES:%s'%reader.total_pages)
                #reader.build_log_text(data)

                if reader.current_page < reader.latest_page:
                #if Backlog
                    reader.label_content = ""
                    #turn page with BACKLOG
                    reader.current_page += 1

                    reader.timeline_read(reader.current_page)
                    ''' PLAY AUDIO when backlog'''
                    audioPlayer.stop()
                    if reader.audio_que:
                        audioPlayer.play(reader.audio_que)
                    else:
                        print("No audio que'd")

                #if Current
                else:
                    #if currently letter loading
                    if reader.label_content_index < len(reader.timeline_array)-1:

                        print('skipping letterloading')
                        #time.sleep(0.1)
                        #skip letterloading
                        #reader.label_content_index = 0
                        #reader.label_content = ""
                        reader.label_content = reader.timeline_content
                        #reader.label_content_index = len(reader.timeline_array)

                        #reader.latest_page = reader.latest_page + 1

                        reader.label_content_index = len(reader.timeline_array)-1
                        '''PLAY AUDIO on mouse release when letterload'''

                        audioPlayer.stop()
                        if reader.audio_que:
                            audioPlayer.play(reader.audio_que)
                        else:
                            print("No audio que'd")



                    #being Latest, if letterloading will load all the text without doing anything else,  increase
                    #reader.latest_page = reader.latest_page + 1


                    #if letter loading finished
                    if reader.label_content_index > len(reader.timeline_array)-1:
                        if reader.current_page < reader.total_pages:
                            #not last page of chapter
                            print('turn page')
                            reader.label_content_index = 0
                            reader.label_content = "";
                            #if reader.current_page < reader.latest_page:

                            reader.current_page += 1
                            '''Turn Page'''

                            if reader.current_page > reader.latest_page:
                                #new page

                                reader.latest_page += 1


                            # if reader.current_page > reader.latest_page:
                            #     reader.latest_page = reader.latest_page + 1

                            #reader.latest_page = reader.latest_page + 1
                            if reader.latest_page == reader.total_pages:
                                #last page of chapter
                                print('CHAPTER END')
                                reader.save_label_draw(reader.inversion)


                        if reader.current_page == reader.total_pages:
                            #last page in chapter
                             reader.current_chapter += 1
                             reader.latest_page = 0
                             reader.current_page = 0
                             #reader.current_page = -1
                             print('new chapter started')

                        reader.timeline_read(reader.current_page)
                        '''
                        mouse release after letter loading finished (normal click)'''
                        audioPlayer.stop()
                        #stop ongoing sound fx from last page
                        if reader.audio_que:
                            audioPlayer.play(reader.audio_que)
                        else:
                            print("No audio que'd")
                        #start sound fx from new page on mouseclicka



                    if reader.current_chapter >= reader.total_chapters:
                        #last chapter in route
                        completion.route_finish()
                        pyglet.app.exit()




    def on_draw(self):
        self.clear()
        #print('COMPLETION:%s'%completion.report())
        #print("DATA LENGTH %s"%reader.total_chapters)
        #print("CURRENT CHAPTER %s"%reader.current_chapter)
        #print('TOTAL PAGES:%s'%reader.total_pages)
        #pyglet.graphics.Batch().draw()
        clock = pyglet.clock
        cfreq = clock.get_frequency()
        #print(f"{cfreq} since last draw")
        #mouse click logic; detecting mouse on every draw frame
        if self.game_state == 1:
            r = reader
            r.menu_draw()
        if self.game_state == 2:
            if music_player.playing == True:
                #print('AUDIO IS PLAYING')
                music_player.pause()
            return


        if self.game_state == 3:
            #if key.LCTRL:
            #    reader.skip = 1
            #    print('CTRL on draw')
            r = reader #cache
            # Draw page content
            r.img_draw()
            r.character_draw()
            r.letter_load()
            r.label_draw(r.inversion)
            r.speaker_label_draw(r.inversion)
            if r.log:
                #r.build_log_text(data)
                r.log_draw()

                #print('Log drawing in on_draw')
            if self.skip_on == 1:
                r.skip = 1
                print('CTRL on draw')
            # if r.current_chapter==0 and r.current_page==0 and not hasattr(AudioPlayer, "player"):
            #     print('play music on first page')
            #     audioPlayer.stop()
            #     audioPlayer.play(r.audio_que)


            is_latest_page = r.current_page >= r.latest_page
            at_last_page = r.current_page + 1 > r.total_pages
            if is_latest_page and at_last_page: #should not show
                r.current_chapter += 1
                if r.current_chapter >= r.total_chapters:
                    completion.route_finish()
                    pyglet.app.exit()
                r.current_page = 0
                r.latest_page = 0
                print("New chapter started")

                #new chapter
            if is_latest_page and r.label_content_index > len(r.timeline_array)-1 and r.current_page == 0 and r.current_chapter > 0:
                #if reader.current_page == 0:
                #if new chapter AND not chapter 0
                r.save_label_draw(r.inversion)

        #reader.speaker_label_draw(reader.inversion)


            if r.audio_que and r.audio_que[1]:

                    music_que, music_file = r.audio_que[0], r.audio_que[1]
                    #music = pyglet.resource.media(music_file)
                    if r.current_page == r.latest_page:
                        if music_player.playing:
                            #print('MUSiC is playing')
                            if music_que == 'STOP':
                                if music_player.playing:
                                    music_player.pause()
                            if not music_que == 'STOP' and not music_que == 'PLAY':
                                print("Unhandled command:{}".format(music_que))

                        else:
                            if music_que == 'PLAY':
                                music = pyglet.resource.media(music_file)
                                if music:
                                    music_player.queue(music)
                                music_player.next_source()
                                music_player.play()
                            if not music_que == 'STOP' and not music_que == 'PLAY':
                                print("Unhandled command:{}".format(music_que))


    def on_close(self):
        pass
                #if mousebuttons[mouse.LEFT] is False and reader.current_page == reader.total_pages:
                #print('last page in chapter')
                #reader.timeline_read(reader.current_page)
'''
            if reader.current_page == reader.total_pages:
                print('last page in chapter')
                reader.timeline_read(reader.current_page)
                time.sleep(0.1)
                reader.current_page = reader.current_page + 1
            if mousebuttons[mouse.LEFT] is True and reader.current_page > reader.total_pages:
                print('new chapter')
                reader.current_chapter = reader.current_chapter + 1
                reader.current_page = 0
                reader.latest_page = 0
                reader.timeline_read(reader.current_page)
'''
''' CLASSES.PY MERGE'''
'''
@dataclass
class Reader:
    name: str = "Reader"
    current_page: int = 0
    current_chapter: int = 0

    # timeline-related/ letter load and label draw
    timeline_content: str = "" (for letterload)
    label_content: str = "" (for label draw)
    speaker_content: str = ""
    label_content_index: int = 0
    latest_page: int = 0
    total_pages: int = 0
    total_chapters: int = 1
    wait_duration: float = 0
    #page_date[0](timeline_que) is ["speaker_content","timeline_content", inversion bool],

    timeline_content: list[Any] = field(default_factory=list)
    audio_que: list[Any] = field(default_factory=list)
    animation_frames: list[Any] = field(default_factory=list)
    image_array: list[Any] = field(default_factory=list)
    timeline_meta: dict[str, Any] = field(default_factory=dict)


    # audio
    audio_tracks: List[str] = field(default_factory=list)
    audio_meta: Dict[str,str] = field(default_factory=dict)
    # audio metas:
    audio_meta:
    {
        "FADE": True,
        "Loop": True,
        "Loop Duration" : 3,
        "command": "PLAY"

    }
    timeline_read logic:
    fade = bool(self.audio_meta.get("FADE",False))
    #False is the default value wherever timeline.json doesn't specify one. For this case, fade effect is not enabled where unspecified
    command = str(self.audio_meta.get("command",))
    command = audio_meta.get("command", "")
    # str() not needed if its always going to be a string
    if command == "PLAY":
        print("Starting playback...")
        #send play command to audioplayer,
        as in run audioplayer method here?
    elif command == "STOP":
        print("Stopping playback...")

    command [play, start, stop, pause]


    # animation — split into more descriptive pieces
    animation_frames: List[str] = field(default_factory=list)   # list of frame file paths
    animation_meta: Dict[str, str] = field(default_factory=dict)  # e.g., duration, loop, easing,
    # animation metas:
    wait
    FADE
    Loop (if false playthough)
    loop_duration

    logic:
    loop_duration = float(self.animation_meta.get("duration", 0.1))
    loop = bool(self.animation_meta.get("loop", False))



    animation_counter: int = 0

    # images
    image_array: List[str] = field(default_factory=list)

    # timeline progression
    timeline_array: List[str] = field(default_factory=list)

    # characters — split too
    character_frames: List[str] = field(default_factory=list)   # filenames of character sprites
    character_positions: List[str] = field(default_factory=list) # e.g., "left", "right"
    character_meta: Dict[str, str] = field(default_factory=dict) # emotion, expression, etc.

    # display/flags
    inversion: int = 0
    special_scroll: int = 0


    actually it might not be worth it to use dataclasses, might be too much work and might diverge from the vision too much
    but it is worth it to reorganize the que into a dictionary for the pros of default values and easy extensibility
    converting all to dataclasses does allow default values for safety and error prevention in the json to a wild degree

    def load_page_data(self, page_data: list[Any]) -> None:
    mapping = [
        ("timeline_content", []),
        ("audio_que", []),
        ("animation_frames", []),
        ("image_array", []),
        ("timeline_meta", {}),
    ]

    for i, (attr, default) in enumerate(mapping):
        value = page_data[i] if i < len(page_data) else default
        setattr(self, attr, value)   # assign dynamically


'''


class Reader():
    def __init__(self):
        self.name = 'Reader'
        self.current_page = 0
        self.current_chapter=0
        #current page and chapter code for save/load
        self.timeline_content = ""
        self.label_content = ""
        self.speaker_content =""
        #timeline content uploaded from timeline.json, transfer to label content for display
        self.label_content_index = 0
        self.latest_page = 0
        #latest page set to 0 every chapter. part of save load data?
        self.total_pages = 0
        #comes from timeline.json, how many pages in a chapter
        self.total_chapters = 1
        self.audio_que = []
        self.audio_meta = {}
        self.animation_que = {}
        self.animation_meta = {}
        self.loop_duration = 0.1
        self.loop_bool = 0
        self.playthrough = 0
        self.timeline_meta = {}

        self.animation_counter = 0
        self.image_array = []
        self.timeline_array = []
        self.character_que = {}
        self.character_meta ={}
        self.inversion = 0
        self.specialscroll = 0 #future function which allows for backtracking into a different timeline
        self.skip = 0
        self.menu_count = 0
        self.menu_anim_array=['010901.png','010902.png']
        self.log = 0
        self.timeline_text = ""
        self.timeline_buffer = []
        #self.page_location = 720
        print('Reader created')
    def timeline_read(self,timeline_id):
        self.current_page = timeline_id
        #chapter_num = 'chapter'+str(self.current_chapter)
        chapter_num = self.current_chapter
        print("current chapter:%d" % self.current_chapter)
        page_num = str(self.current_page)
        #with open('timeline.json') as f:
        #    data = json.load(f)
        #print(timeline_id)
        #print(data)
        #print(data[0])
        #print(data[chapter_num]['page%s'%page_num])
        #print(data[chapter_num][page_num])
        # print("DATA LENGTH %s"%len(data))
        # print("CURRENT CHAPTER %s"%self.current_chapter)
        self.total_chapters = len(data)

        if self.current_chapter >= self.total_chapters:
            print('Chapter_num =' + str(chapter_num))
            print('exiting from timeline read: current chapter is greater than total chapters')
            return  # no more chapters

        self.total_pages = len(data[chapter_num])-1

        if self.current_page >= self.total_pages:
            print('Page_num =' + page_num)
            print('exiting from timeline read: current page is greater than total pages')
            return
        #if self.current_page >= self.total_pages:
        #    return  # no more pages in this chapter
        page_data = data[chapter_num]['page%s'%page_num]
        print("Page data: %s -- Page data end" % page_data)
        #[chapter_num][page_num]
        if self.current_chapter == self.total_chapters + 1:
            completion.route_finish()
            print("route:%d" % completion.report())
            pyglet.app.exit()
            #route completion



        #pass
        #self.total_pages = len(data[chapter_num])-1

        #for i in data['content']:
        #    print(timeline_id)
        #    print(i)

        '''Removing page num: Using demo_timeline_test, Scroll does not work and chapters and save/load would need to be fixed'''
        # timeline_que = data[int(chapter_num)][int(page_num)][0]
        # audio_que = data[int(chapter_num)][int(page_num)][1]
        # animation_que = data[int(chapter_num)][int(page_num)][2]
        # print(animation_que)
        # print(len(animation_que))
        # character_que = data[int(chapter_num)][int(page_num)][3]

        #add new functionalities to mapping here
        mapping = [
        ("timeline_que", []),
        ("audio_que", []),
        ("animation_que", []),
        ("character_que", []),
        ("timeline_meta", {}),
        ("audio_meta", {}),
        ("animation_meta", {}),
        ("character_meta", {})
        ]

        for i, (attr, default) in enumerate(mapping):
            value = page_data[i] if i < len(page_data) else default
            setattr(self, attr, value)   # assigns self.timeline_content, etc.

        ''' Timeline Breakdown
        '''
        #timeline unpacking
        speaker, content= (self.timeline_que + ["",""])[:2] #adding empty string and truncating for safety to reduce index errors
        #this only works for when timeline_que is completely missing, missing elements or elements in wrong order will cause errant display
        self.speaker_content = speaker
        self.timeline_content = content
        self.loop_bool = getattr(self, "animation_meta", {}).get("loop", True)
        self.playthrough = getattr(self,"animation_meta", {}).get("playthrough", False)
        if len(self.timeline_que) > 2:
            self.inversion = self.timeline_que[2]

        self.audio_que = (self.audio_que + ["", "", ""])[:3]

        self.build_log_text()



        '''
        loop, loop_duration, fade, low pass, high pass, distortions = self.audio_meta
        but maybe this ^ all happens in the audioplayer? audio_meta surely passed on wholesale to audioplayer class

        fade (white, back, none), fade duration, loop, loop_duration, auto advance, screen shake etc, = self.animation_meta

        fade, shake, emote, accessory features (frustration lines), multiple characters, etc = self.character_meta

        '''
        print('timeline read')

        #f.close()
    def label_draw(self, inversion):
        #print("CURRENT PAGE:%s"%self.current_page)
        #print("LATEST PAGE:%s"%self.latest_page)

        # document_content = "{.margin_left '150px'}{font_name 'Chrono Cross'}{font_size 28}"+self.label_content+"{color (0, 0, 0, 255)}"
        if inversion == 1:
            #print("INVERTED")
            document_content = "{.margin_left '150px'}{font_name 'Chrono Cross'}{font_size 28}{color (255, 255, 255, 255)}{background_color (0,0,0,255)}"+self.label_content
        else:
            document_content = "{.margin_left '150px'}{font_name 'Chrono Cross'}{font_size 28}{background_color (255,255,255,255)}"+self.label_content

        document = pyglet.text.decode_attributed(document_content)
        width = window.width//1.35
        height = window.height//3

        layout = pyglet.text.layout.TextLayout(document, width ,height,  wrap_lines=True, multiline=True)

        #label.draw()
        layout.draw()

        #letter loading: label draws character array built from timeline content by method when LATEST
        #print(self.timeline_content)
        #print('label drew')
        #print('timeline_id')
    def save_label_draw(self, inversion):

        if inversion == 1:
            document_content = "{.margin_left '10px'}{font_name 'Chrono Cross'}{font_size 20}{color (255, 255, 255, 255)}{background_color (0,0,0,255)}New Chapter: Press F1 to SAVE game"
        else:
            document_content = "{.margin_left '10px'}{font_name 'Chrono Cross'}{font_size 20}{background_color (255,255,255,255)}New Chapter: Press F1 to SAVE game"

        document1 = pyglet.text.decode_attributed(document_content)

        width = window.width//1.35
        height = 50
        layout1 = pyglet.text.layout.TextLayout(document1, width ,height, wrap_lines=True, multiline=True)

        #label.draw()
        layout1.draw()
    def speaker_label_draw(self, inversion):
        if len(self.speaker_content) == 0:
            pass
        else:
            if inversion == 1:
                #print("INVERTED")
                document_content2 = "{.margin_left '10px'}{font_name 'Chrono Cross'}{font_size 20}{bold True}{color (255, 255, 255, 255)}"+self.speaker_content+":"

            else:
                document_content2 = "{.margin_left '10px'}{font_name 'Chrono Cross'}{font_size 20}{bold True}"+self.speaker_content+":"



            document2 = pyglet.text.decode_attributed(document_content2)

            width = window.width//1.35
            height = window.height//2
            layout2 = pyglet.text.layout.TextLayout(document2, width ,height, wrap_lines=True, multiline=True)

            #label.draw()
            layout2.draw()
    def build_log_text(self):
        """Build timeline string from the last 10 pages including the current_page."""
        chapter_data = data[self.current_chapter]

        # Compute the window of pages to show
        start_page = max(0, self.current_page - 9)   # 9 previous + current = 10
        end_page = self.current_page + 1             # include current page

        timeline_pages = []
        for page in range(start_page, end_page):
            page_key = f"page{page}"
            if page_key not in chapter_data:
                continue

            page_lines = []
            for sublist in chapter_data[page_key]:
                if (
                    isinstance(sublist, list)
                    and len(sublist) > 1
                    and isinstance(sublist[1], str)
                    and sublist[1].strip()
                ):
                    safe_text = sublist[1].replace("{", "{{").replace("}", "}}")
                    page_lines.append(safe_text.strip())

            if page_lines:
                timeline_pages.append("\n".join(page_lines))

        # Store directly instead of appending
        self.timeline_buffer = timeline_pages
        self.timeline_text = "\n\n".join(self.timeline_buffer)

    def log_draw(self):
        if reader.log and reader.latest_page > 1:
            #reader.log_content
            #page_data = self.timeline_content

            #page_data = str(data[self.current_chapter]['page%s'%self.current_page][0])
            '''
            if (int(self.current_page)) > 0:
                print('more than 1 page')
                page_data = str(data[self.current_chapter]['page%d'% (int(self.current_page)-1)][0][0])+'\n'+page_data
            '''

            #curr_page = int(self.current_page)
            #prev_page = curr_page - 1
            '''
            prev_text = ""
            if prev_page >= 0:  # must be non-negative
                chapter_data = data[self.current_chapter]
                page_key = f'page{prev_page}'
                if page_key in chapter_data:
                    page_content = chapter_data[page_key]
                    if isinstance(page_content, list) and len(page_content) > 0:
                        first_item = page_content[0]
                        if isinstance(first_item, list) and len(first_item) > 0:
                            prev_text = str(first_item[0])

            # Build final page_data safely
            if prev_text:
                page_data = prev_text + '\n' + page_data

            '''
            '''
            prev_lines = []
            if prev_page >= 0:
                chapter_data = data[self.current_chapter]
                page_key = f'page{prev_page}'
                if page_key in chapter_data:
                    for sublist in chapter_data[page_key]:
                        prev_lines.append(str(sublist))

            if prev_lines:
                page_data = "\n".join(prev_lines) + "\n" + page_data
            '''
            #print(page_data)

            document_content3 = "{.margin_left '10px'}{font_name 'Chrono Cross'}{font_size 20}{bold False}{wrap True}{color (0, 255, 0, 255)}"+self.timeline_text
            #print(document_content3)
            document3 = pyglet.text.decode_attributed(document_content3)
            #width = window.width//1.35
            width = window.width//2
            height = window.height-100
            layout3 = pyglet.text.layout.TextLayout(document3, width ,height, wrap_lines=True, multiline=True)
            layout3.draw()
            #log_label = pyglet.text.Label(page_data,
            #          font_name='Chrono Cross',
            #          font_size=20,
            #          x=10, y=window.height//3,
            #          color=(0, 255, 0, 255),
            #          )
            #log_label.draw()


    def letter_load(self):
        #print(self.current_page)
        #print('Label content index:' + str(self.label_content_index))
        if self.current_page < self.latest_page:
            #print('BACKLOG')
            self.label_content_index = 0
            self.label_content = self.timeline_content
        if self.current_page == self.latest_page and self.latest_page != self.total_pages:
            #print('LATEST')
            self.timeline_array = list(self.timeline_content);
            #print(self.timeline_array)
            if self.label_content_index > len(self.timeline_array)-1:
                #print('letter loading finished')
                self.label_content = self.timeline_content
                #turn page animation trigger

                return
            else:
                current_character = self.timeline_array[self.label_content_index]
                #print('CURRENT CHARACTER: %s' % current_character)
                if current_character == "{":
                    self.label_content_index = self.label_content_index + 10
                    current_character = self.timeline_array[self.label_content_index]
                self.label_content = self.label_content + current_character
                #print(self.label_content)
                self.label_content_index = self.label_content_index + 1

    def img_draw(self):
        #timeline cues direct reader to load and blit and animate everything inside img_draw. img_draw must be made more robust and image files must draw from elsewhere

        #print('img_draw called')
        frames = self.animation_que
        #print(len(frames))

        count = self.animation_counter
        #print(len(frames))
        #print(count)

        if count < len(frames) and frames:
            #print(count)
            ''' THIS IS THE SLOW DOWN'''
            #current_pic = pyglet.resource.image(frames[count-1])
            #For local running
            current_pic = pyglet.image.load('resources/frames/'+frames[count-1])
            #for pyinstaller
            #current_pic = pyglet.image.load('_internal/resources/frames/'+frames[count-1])
            #print(f"{current_pic} = CURRENT PIC")
            #pic = image.load(current_pic)

            # height, width = 800, 600
            #
            # current_pic.scale = min(current_pic.height, height)/max(current_pic.height, height), max(min(width, current_pic.width)/max(width, current_pic.width))
            #
            # current_pic.width = width
            # current_pic.height = height
            # current_pic.texture.width = width
            # current_pic.texture.height = height
            current_pic.blit(0,0)

            # target_width, target_height = 1920, 1080
            #
            # # Create sprite
            # sprite = pyglet.sprite.Sprite(current_pic)
            # draw_objects = [sprite]
            #
            # # Compute uniform scale (fit to smaller dimension)
            # scale = min(target_width / sprite.width, target_height / sprite.height)
            #
            # # Apply uniform scale
            # sprite.scale = scale
            #
            # # Optional: center it
            # #sprite.x = (target_width - sprite.width * scale) // 2
            # #sprite.y = (target_height - sprite.height * scale) // 2
            #
            # # Draw
            # sprite.draw()
            # #global sprite
            # if sprite in draw_objects:
            #     print('deleting')
            #     sprite.delete()
            #     draw_objects.remove(sprite)
            #

            #pass
        #Test reaction images below
        #test_pic = pyglet.image.load('picture.png')
        #test_pic.blit(0,0)

    def character_draw(self):
        #two options here:
            #have a naming convention for file names
            #have character name[0] pull a seperate json of filenames based on emotion[1]
        #for the beta let us stick with the first option while including the design for the second
        if len(self.character_que) != 0:
            character_frames = self.character_que[0]
            character_side = self.character_que[1]
            test_pic = pyglet.resource.image(character_frames)
            glEnable(GL_BLEND)

            if character_side == "left":
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                test_pic.blit(0,0)
            if character_side == "right":
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                test_pic.blit(1000,0)


    def page_turn_draw(self):
        print('page_turn_draw called')
        '''
    def autoplayer():
        pass
        '''
    def specialScroll(self, specialScroll):
        pass
    def menu_draw(self):

        menu_label = pyglet.text.Label('Press SPACE to begin, F2 to LOAD chapter, ESC to Exit',
                      font_name='Chrono Cross',
                      font_size=36,
                      x=10, y=10,
                      color=(0, 255, 0, 255))
        #dynamic menu label
        current_progress_label = f"Chapter {self.current_chapter} Page {self.current_page}"
        menu_label2 = pyglet.text.Label(current_progress_label,
                font_name = 'Times New Roman',
                font_size = 200,
                x=10, y =250,
                color=(0, 0, 0, 255))

        #chrono_cross = menu_label.get_style("Chrono Cross")
        # menu_label.set_style(0,
        #
        # {
        #     "color": (255, 255, 255,1)
        # })
        #menu_label.set_style("Chrono Cross",color=(255,255,255,1))
        #self.menu_anim_array=['white.png','black.png']
        menu_pic = pyglet.image.load('resources/frames/'+self.menu_anim_array[self.menu_count])
        menu_pic.blit(0,0)
        #print('menu count =' + str(self.menu_count))
        menu_label.draw()
        menu_label2.draw()

class Memory():
    def __init__(self):
        #there needs to be an if else that looks for exisitng save file upon start up, perhaps new method. this method will trigger at game_state
        self.dictionary = {
            "name":"autosave",
            "chapter":"",
            "completion":0,
            "date_saved":""
        }
    def save(self):
        self.dictionary['chapter'] = reader.current_chapter
        print(datetime.now())
        self.dictionary['date_saved'] = str(datetime.now())
        self.dictionary['completion'] = 0 #to be added
        with open('save_data.json', 'w') as outfile:
            json.dump(self.dictionary, outfile)
        #print(self.dictionary)
    def load(self):
        with open('save_data.json', 'r') as openfile:
            json_object = json.load(openfile)
        #print(json_object)
        self.dictionary['chapter'] = json_object['chapter']
        self.dictionary['completion'] = json_object['completion']
        reader.current_chapter = self.dictionary['chapter']
        reader.latest_page = 0
        reader.current_page = 0
        #print(self.dictionary)

class Completion():
    def __init__(self):
        self.current_route = Memory().dictionary['completion']
    def route_finish(self):
        self.current_route = self.current_route + 1
        Memory().dictionary['completion'] = self.current_route
    def report(self):
        return Memory().dictionary['completion']

class AudioPlayer():
    # def __init__(self):
    #     audio_player = pyglet.media.Player()
    #     music = pyglet.resource.media("theme0.wav")
    #     music_player.queue(music)
    #     #music_player.eos_action = pyglet.media.SourceGroup.loop
    #     music_player.play()

    def play(self,audio_que):
        if reader.audio_que != None and reader.audio_que[2] != "":
            print('AUDIO QUE:'+str(audio_que[2]))

            # player = pyglet.media.Player()
            source = pyglet.resource.media(audio_que[2])
            audio_player.queue(source)
            #using
            #setattr(player,'loop',True)
            audio_player.play()
        #check que string for commands: STOP, START, FADE, VOICE, BGM
        #VOICE LINE stop currently playing and play new ones
    def stop(self):
        if hasattr(self, "player") and self.player:
            self.player.pause()
            self.player.delete()
            self.player = None

        #if audio_player.playing == True:
        #    audio_player.pause()
    def end(self):
        audio_player.delete()

class AnimPlayer():
    def play():
        pass

if __name__ == '__main__':
    #pyglet.resource.path = ['resources/media','resources/frames', 'resources/fonts']
    pyglet.resource.path = ['resources/media','resources/frames','resources/fonts']

    pyglet.resource.reindex()

    clock = pyglet.clock
    window = Window(style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS, vsync=False)
    #window.set_size(1786, 1086)
    window.set_size(1920,1080)
    if window.fullscreen == 1:
        window.set_fullscreen(True)
    if window.fullscreen == 0:
        window.set_fullscreen(False)
    with open('timeline.json') as f:
        data = json.load(f)

    # cursor = pyglet.image.load('cursor.png')
    # image_cursor = pyglet.window.ImageMouseCursor(cursor, 16, 8)
    # window.set_mouse_cursor(image_cursor)

    print('main test')
    mousebuttons = mouse.MouseStateHandler()
    keys = key.KeyStateHandler()

    music_player = pyglet.media.Player()
    music = pyglet.resource.media("theme0.wav")
    music_player.queue(music)
    setattr(music_player,'loop',True)

    audio_player = pyglet.media.Player()
    audioPlayer = AudioPlayer()

    #music_player.eos_action = pyglet.media.SourceGroup.loop
    music_player.play()
    #intros in game state 0, click to skip
    #if game_state = 0:
    #play intros
    #time.sleep()->game_state = 1
    #when game state 0 reaches end, switch to game state 1 and begin menu
    #load save data somewhere in here
    #if game_state = 1
    #load menu buttons
    #reader = classes.Reader()
    reader = Reader()
    memory = Memory()
    completion = Completion()
    print('COMPLETION:%s'%completion.report())
    #print('reader test')
    #page = classes.Page()
    #start_menu = classes.Start_menu()

    #pyglet.sprite.Sprite(img=pyglet.image.load('picture.png')).draw()
    #pyglet.font.add_file('resources/fonts/times.ttf')
    pyglet.resource.add_font('times.ttf')
    pyglet.font.load('Times New Roman')
    pyglet.resource.add_font('Chrono Cross.ttf')
    pyglet.font.load('Chrono Cross')
    os.environ["PYGLET_AUDIO_DRIVER"] = "openal"
    def on_close():
        pyglet.font.quit()
    # Get the font name used at character index 0
    #font_name = document.get_style('Chrono Cross', 0)

    # Set the font name and size for the first 5 characters
    #document.set_style(0, 5, dict(font_name='Chrono Cross', font_size=12))

    # def callback(dt):
    #     print(f"{dt} seconds since last callback")
    # def drawFrames(dt):
    #     print("frame drawn")
    def tick(dt):
        #print(window.togglefullscreen)
        #print(window.game_state)

        if window.togglefullscreen != window._prev_fullscreen:
            window.set_fullscreen(window.togglefullscreen)
            window._prev_fullscreen = window.togglefullscreen

        #print('tick')
        #print(f"{dt} seconds since last callback")

        if window.game_state == 0:
            # Bootup → move to start menu
            window.game_state = 1

        elif window.game_state == 1:
            #Start menu
            reader.menu_count = (reader.menu_count + 1) % (len(reader.menu_anim_array))
            if music_player.playing:
                print('STARTING AUDIO IS PLAYING')
            if keys[key.SPACE]:
                #if mousebuttons[mouse.LEFT] is True:
                window.game_state = 2
                if music_player.playing:
                    #print('AUDIO IS PLAYING')
                    music_player.pause()

        elif window.game_state == 2:
            #main menu to game mode
            window.game_state = 3
            #get load information from main to present menus
            reader.timeline_read(reader.current_page)


        elif window.game_state == 3:
            #Game mode
            '''
            ---Animation code below. frame of animation count is called every draw frame, if timeline->reader->image_array variable is not empty,
            and count incremented ever callback tick
            '''
            #frames = []
            frames = reader.animation_que
            frames_length = len(frames)
            #image_array = reader.image_array
            #print(image_array)
            #print(frames)
            count = reader.animation_counter
            '''Menu Anim code below'''
            #reader.menu_count = (reader.animation_counter if frames_length else 0)% len(reader.menu_anim_array)
            #reader.menu_count = (reader.menu_count + 1) % (len(reader.menu_anim_array)+1)
            reader.menu_count = (reader.menu_count + 1)
            #% (len(reader.menu_anim_array))
            if reader.skip:
                print('CTRL pressed, in tick')
                window.on_mouse_release(0, 0, 1, 0)
                reader.skip = 0

            if frames_length:
                if reader.loop_bool:
                    reader.animation_counter = (reader.animation_counter + 1) % frames_length
                else:
                    reader.animation_counter = min(reader.animation_counter + 1, frames_length - 1)

                if reader.menu_anim_array:
                    reader.menu_count = reader.animation_counter % len(reader.menu_anim_array)

                if reader.playthrough and reader.animation_counter >= frames_length -1:
                    print("Playthrough flag detected")
                    window.on_mouse_release(0, 0, 1, [])

            # if frames_length:
            #     reader.animation_counter = (
            #         (reader.animation_counter + 1) % frames_length
            #         if reader.loop_bool
            #         else
            #         min(reader.animation_counter + 1, frames_length - 1)
            #     )
            #     if reader.menu_anim_array:
            #         reader.menu_count = reader.animation_counter % len(reader.menu_anim_array)


            '''
            if frames_length:
                #print('images present')
                if count < frames_length:
                    #print(count)

                    count = count + 1
                    reader.animation_counter = count
                    #print('new count: {}'.format(count))
                    #reader.img_draw()


                if count >= frames_length:
                    if reader.loop_bool:
                        count = 0
                        reader.animation_counter = count
                    else:
                        if reader.playthrough:
                            print("Playthrough flag detected")
                            window.on_mouse_release(0,0,1,[])
                        reader.animation_counter = count -1

                    #print('loop reset')



            '''
            '''Menu Anim code below
            #reader.menu_count = (reader.animation_counter if frames_length else 0)% len(reader.menu_anim_array)
            reader.menu_count = (reader.menu_count + 1) % (len(reader.menu_anim_array)+1)
            '''
    clock.schedule_interval(tick, 1/24)


    #clock.schedule_interval(tick, 0.001)
    window.push_handlers(mousebuttons)
    window.push_handlers(keys)
    #glClearColor(0.5,1,0.7,1)
    print('app will run')
    pyglet.app.run()
    print('app ran')

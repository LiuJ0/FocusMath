from datetime import datetime
import image_utils

start_import = datetime.now()
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty, Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.event import EventDispatcher
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.network.urlrequest import UrlRequest
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.properties import NumericProperty
from kivy.graphics import *
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView

print(f"Kivy Imports: {datetime.now() - start_import}")
start_import = datetime.now()
# PEP 8 Crying rn

import os.path
from os import path
import configparser
import requests
import os
import glob
import StepPyStep
from Mathpix import mathpix
import imagesize
import json
import urllib
import cProfile
import certifi
import glob
from functools import partial
from theme import themeConfig
import imghdr

import shutil
import cv2
from plyer import filechooser as native_file_chooser

print(f"StepPyStep Imports: {datetime.now() - start_import}")

Builder.load_file("main.kv")

# global filepath for each run


# declare screens
class SolutionStep(Button):
    pass


class HomeScreen(Screen):

    def capture(self):
        directory_file = open("curdir.tmp", 'w')
        # Creates a folder for the solution and stores it's relative name in self.filepath
        filepath = StepPyStep.create_zip().create_directory(App.get_running_app().user_data_dir)
        # print("Filepath: ", filepath)
        directory_file.write(filepath)
        directory_file.close()

        try:
            camera = self.ids["proxy"]
            image_path = os.path.join(App.get_running_app().user_data_dir, "Solutions", filepath, "image.png")

            camera.export_to_png(image_path)
            image_utils.crop_transparent(image_path, image_path)
            print("captured successfully")
            self.on_image_get()
        except KeyError:
            self.image_input_error()
        except Exception as e:
            print("Camera capture exception: " + str(e))

        # link = solution().step_by_step(f"Solutions/{self.filepath}/image{self.count}.png", f"Solutions/{self.filepath}/solution.txt")[0]
        # print(link)

        # self.manager.transition.direction = 'right'
        # self.manager.current = 'mathpixDisplay'

        # link = solution().check(f"Solutions/{self.filepath}/image{self.count}.png", f"Solutions/{self.filepath}/solution.txt")
        # if link != None:
        #     print(link)

    def image_input_error(self):
        error = ImageErrorPopup()
        error.open()

    def on_resize(self):
        try:
            self.window_width_relative = (Window.width / 1080)
            self.window_height_relative = (Window.height / 1920)
            self.relative_size = ((self.window_width_relative + self.window_height_relative) / 2)
            self.image_container.height = min(self.image_size[1] * self.relative_size, Window.height - (
                    (120 + 60 + 150 + 30 + 30 + 145) * self.relative_size) - self.title_label.height)
            self.display_latex_image.size_hint = (None, None)
            self.display_latex_image.height = max(self.image_container.height, self.image_size[1] * self.relative_size)
            self.display_latex_image.width = max(Window.width - 240 * self.relative_size,
                                                 self.image_size[0] * self.relative_size)
            self.capture_popup.height = self.image_container.height + (
                    (60 + 150 + 30 + 30 + 145) * self.relative_size) + self.title_label.height
        except AttributeError:
            pass

    def open_image(self):
        print("open")
        try:
            open_image_path = native_file_chooser.open_file(title="Choose an image: ", filters=[(
                "Image Files(*.jpg, *.jpeg, *.png, *.tiff, *.pjp, *.jfif, *.gif, *.svg, *.raw)",
                "*.jpg", "*.jpeg",
                "*.png", "*.tiff",
                "*.pjp", "*.jfif",
                "*.gif", "*.svg",
                "*.raw"), (
                "All Files(*.*)", "*.*")])[0]
            print(open_image_path)
            destination_filepath = StepPyStep.create_zip().create_directory(App.get_running_app().user_data_dir)
            print("Filepath: ", destination_filepath)
            directory_file = open("curdir.tmp", 'w')
            directory_file.write(destination_filepath)
            directory_file.close()
            shutil.copy2(open_image_path,
                         os.path.join(App.get_running_app().user_data_dir, "Solutions", destination_filepath,
                                      "image.png"))
            try:
                self.on_image_get()
            except KeyError:
                self.image_input_error()

        except TypeError:
            pass

    def on_image_get(self):

        dir_file = open("curdir.tmp", "r")
        self.solve_file_path = dir_file.read()
        dir_file.close()
        latex = solution().call_mathpix(self.solve_file_path)
        latex_file = open(
            os.path.join(App.get_running_app().user_data_dir, "Solutions", self.solve_file_path, "latex.txt"), 'w+')
        print(latex)
        latex_file.write(latex["latex_simplified"])
        self.open_capture_popup()

    def open_capture_popup(self):
        render_path = os.path.join(App.get_running_app().user_data_dir, "Renders", self.solve_file_path,
                                   "capture_render.png")
        self.capture_popup = CapturePopup()

        self.window_width_relative = (Window.width / 1080)
        self.window_height_relative = (Window.height / 1920)
        self.relative_size = ((self.window_width_relative + self.window_height_relative) / 2)

        self.image_container = self.capture_popup.ids["image_scroll_view"]
        self.title_label = self.capture_popup.ids["title_label"]
        max_latex_height = Window.height - ((150 + 30 + 30 + 145) * self.relative_size)
        self.image_size = imagesize.get(render_path)
        self.display_latex_image = Image()
        self.display_latex_image.source = render_path
        self.display_latex_image.allow_stretch = True
        self.display_latex_image.color = App.get_running_app().theme.color_neutral
        self.image_container.add_widget(self.display_latex_image)

        self.image_container.height = min(self.image_size[1] * self.relative_size, Window.height - (
                (120 + 60 + 150 + 30 + 30 + 145) * self.relative_size) - self.title_label.height)
        self.display_latex_image.size_hint = (None, None)
        self.display_latex_image.height = max(self.image_container.height, self.image_size[1] * self.relative_size)
        self.display_latex_image.width = max(Window.width - 240 * self.relative_size,
                                             self.image_size[0] * self.relative_size)
        self.title_label.texture_update()
        self.capture_popup.height = self.image_container.height + (
                (60 + 150 + 30 + 30 + 145) * self.relative_size) + self.title_label.height
        self.capture_popup.open()


class CapturePopup(ModalView):

    def solve(self):
        dir_file = open("curdir.tmp", "r")
        self.solve_file_path = dir_file.read()
        dir_file.close()
        latex_file = open(
            os.path.join(App.get_running_app().user_data_dir, "Solutions", self.solve_file_path, "latex.txt"))
        solved_solution = solution().step_by_step(latex_file.read(),
                                                  os.path.join(App.get_running_app().user_data_dir, "Solutions",
                                                               self.solve_file_path, "solution.txt"),
                                                  self.solve_file_path)
        self.dismiss()
        App.get_running_app().sm.transition.direction = 'left'
        App.get_running_app().sm.current = 'solveequ'

    def retake(self):
        # Cleans up on the event of a retake
        dir_file = open("curdir.tmp", "r")
        solve_file_path = dir_file.read()
        dir_file.close()
        shutil.rmtree(os.path.join(App.get_running_app().user_data_dir, "Solutions", solve_file_path))
        shutil.rmtree(os.path.join(App.get_running_app().user_data_dir, "Renders", solve_file_path))
        self.dismiss()

    def check(self):
        dir_file = open("curdir.tmp", "r")
        solve_file_path = dir_file.read()
        dir_file.close()
        latex_file = open(os.path.join(App.get_running_app().user_data_dir, "Solutions", solve_file_path, "latex.txt"))
        latex = latex_file.read()
        solution().check(latex, solve_file_path)
        self.dismiss()
        App.get_running_app().sm.transition.direction = 'left'
        App.get_running_app().sm.current = 'check'


class ImageErrorPopup(ModalView):

    def retake(self):
        # Cleans up on the event of a retake
        dir_file = open("curdir.tmp", "r")
        solve_file_path = dir_file.read()
        dir_file.close()
        shutil.rmtree(os.path.join(App.get_running_app().user_data_dir, "Solutions", solve_file_path))
        shutil.rmtree(os.path.join(App.get_running_app().user_data_dir, "Renders", solve_file_path))
        self.dismiss()


class FileOpenPopup(ModalView):
    pass


class CorrectionLabel(Label):
    pass


class CheckWorkScreen(Screen):

    def back(self):
        try:
            App.get_running_app().screen_history.pop()
        except IndexError:
            pass
        try:
            return App.get_running_app().screen_history[len(App.get_running_app().screen_history) - 1]
        except IndexError:
            return "home"


    def on_enter(self, *args):
        self.setup_checked_solution()
        self.bind(size=self.on_resize)

    def setup_checked_solution(self):

        dir_file = open("curdir.tmp", "r")
        self.solve_file_path = dir_file.read()
        dir_file.close()
        self.check = configparser.ConfigParser()
        self.check.read(
            os.path.join(App.get_running_app().user_data_dir, "Solutions", self.solve_file_path, "check.txt"))

        os.mkdir(os.path.join(App.get_running_app().user_data_dir, "Renders", self.solve_file_path, "checksteps"))
        working_directory = os.path.join(App.get_running_app().user_data_dir, "Renders", self.solve_file_path,
                                         "checksteps")
        self.check_steps = self.check.sections()
        step_number = 0
        for section in self.check_steps:
            if "STEP" in section:
                # Prepares by rendering the math

                image_utils.render_text(self.check[section]["step"].replace("|", ""),
                                        os.path.join(working_directory, f"step{step_number}.png"))
            else:
                correction_number = section.replace("CORRECTION", "")
                # Prepares by rendering the math

                image_utils.render_text(self.check[section]["operation"].replace("|", ""),
                                        os.path.join(working_directory, f"step{step_number}.png"))
            step_number +=1

        self.build()

    def build(self):
        self.window_width_relative = (Window.width / 1080)
        self.window_height_relative = (Window.height / 1920)
        self.relative_size = ((self.window_width_relative + self.window_height_relative) / 2)

        self.check_step_widgets = []
        self.comment_labels = [0, 0, 0]
        check_steps_layout = self.ids['check_steps_layout']

        solution_title_label = self.ids['check_title_label']
        solution_title_label.text = self.solve_file_path

        cumulative_height = 0

        for s in range(len(self.check_steps)):

            # Creates widget object
            self.check_step_widgets.append(
                SolutionStep(x=30 * self.relative_size, width=Window.width - 60 * self.relative_size))

            # Links KV objects
            latex_image = self.check_step_widgets[s].ids['latex_image']
            latex_image_scrollview = self.check_step_widgets[s].ids["latex_image_scroll"]
            instructions_label = self.check_step_widgets[s].ids["instructions_label"]

            # Is it a step or correction?

            # Yes, is a step
            if "STEP" in self.check_steps[s]:
                padding_height = 60
                # Step is correct
                if self.check[self.check_steps[s]]["iscorrect"] == "True":
                    self.check_step_widgets[s].background_color = App.get_running_app().theme.color_neutral_muted
                # Step is incorrect
                else:
                    self.comment_labels[0] = CorrectionLabel(text="Here's what you did wrong:")
                    self.comment_labels[0].width = check_steps_layout.width
                    self.comment_labels[0].text = "Here's what you did wrong:"
                    check_steps_layout.add_widget(self.comment_labels[0])
                    self.comment_labels[0].texture_update()

                    self.check_step_widgets[s].background_color = App.get_running_app().theme.color_wrong
            # No, is a correction
            else:
                if self.check_steps[s] == "CORRECTION0":
                    self.comment_labels[1] = CorrectionLabel()
                    self.comment_labels[1].width = check_steps_layout.width
                    self.comment_labels[1].text = "Solution:"
                    check_steps_layout.add_widget(self.comment_labels[1])
                    self.comment_labels[1].texture_update()

                padding_height = 90
                self.check_step_widgets[s].background_color = App.get_running_app().theme.color_right
                instructions_label.text = self.check[self.check_steps[s]]["instruction"].replace("text: ", "")

            latex_image.color = App.get_running_app().theme.color_neutral
            instructions_label.color = App.get_running_app().theme.color_neutral

            latex_image.source = os.path.join(App.get_running_app().user_data_dir, "Renders", self.solve_file_path,
                                              "checksteps", f"step{s}.png")

            latex_image_size = imagesize.get(latex_image.source)

            latex_image.texture_update()
            instructions_label.texture_update()
            print(instructions_label.height)
            latex_image.height = 75 * (latex_image_size[1] / 75) * self.relative_size
            latex_image.width = max(latex_image_scrollview.width,
                                    latex_image.height * (latex_image_size[0] / latex_image_size[1]))
            self.check_step_widgets[s].height = latex_image.height + instructions_label.height + padding_height * self.relative_size
            check_steps_layout.add_widget(self.check_step_widgets[s])

        try:
            if self.check[self.check_steps[len(self.check_steps) - 1]]["iscorrect"] == "True":
                self.check_step_widgets[len(self.check_step_widgets) - 1].background_color = App.get_running_app().theme.color_right
                self.comment_labels[2] = CorrectionLabel()
                self.comment_labels[2].width = check_steps_layout.width
                self.comment_labels[2].text = "All correct!"
                check_steps_layout.add_widget(self.comment_labels[2])
                self.comment_labels[2].texture_update()
                cumulative_height += self.comment_labels[2].height + 40 * self.relative_size
        except KeyError:
            pass

        for s in range(len(self.check_step_widgets)):
            cumulative_height += self.check_step_widgets[s].height
            cumulative_height += 40 * self.relative_size
        check_steps_layout.height = cumulative_height

    def on_leave(self):
        self.ids['check_steps_layout'].clear_widgets()

    def on_resize(self, instance, value):

        self.window_width_relative = (Window.width / 1080)
        self.window_height_relative = (Window.height / 1920)
        self.relative_size = ((self.window_width_relative + self.window_height_relative) / 2)

        check_steps_layout = self.ids['check_steps_layout']

        cumulative_height = 0

        for comment in range(3):
            try:
                self.comment_labels[comment].width = check_steps_layout.width
                self.comment_labels[comment].texture_update()
                cumulative_height += self.comment_labels[2].height + 40 * self.relative_size
            except AttributeError:
                pass



        for s in range(len(self.check_steps)):

            # Links KV objects
            latex_image = self.check_step_widgets[s].ids['latex_image']
            latex_image_scrollview = self.check_step_widgets[s].ids["latex_image_scroll"]
            instructions_label = self.check_step_widgets[s].ids["instructions_label"]

            # Is it a step or correction?

            # Yes, is a step
            if "STEP" in self.check_steps[s]:
                padding_height = 60
            # No, is a correction
            else:
                padding_height = 90

            latex_image_size = imagesize.get(latex_image.source)

            latex_image.texture_update()
            instructions_label.texture_update()
            latex_image.height = 75 * (latex_image_size[1] / 75) * self.relative_size
            latex_image.width = max(latex_image_scrollview.width,
                                    latex_image.height * (latex_image_size[0] / latex_image_size[1]))
            self.check_step_widgets[s].height = latex_image.height + instructions_label.height + padding_height * self.relative_size
            self.check_step_widgets[s].width = Window.width - 60 * self.relative_size

        for s in range(len(self.check_step_widgets)):
            cumulative_height += self.check_step_widgets[s].height
            cumulative_height += 40 * self.relative_size
        check_steps_layout.height = cumulative_height


class SolveEquScreen(Screen):

    def back(self):
        try:
            App.get_running_app().screen_history.pop()
        except IndexError:
            pass
        try:
            return App.get_running_app().screen_history[len(App.get_running_app().screen_history) - 1]
        except IndexError:
            return "home"

    def on_enter(self):
        dir_file = open("curdir.tmp", "r")
        self.solve_file_path = dir_file.read()
        dir_file.close()
        self.create_build_objects()
        self.bind(size=self.on_resize)

    def on_leave(self):
        self.ids['solution_steps_layout'].clear_widgets()

    def create_build_objects(self):
        self.solution = configparser.ConfigParser()
        solution_file = os.path.join(App.get_running_app().user_data_dir, "Solutions", self.solve_file_path,
                                     "solution.txt")
        self.solution.read(solution_file)
        self.solution_steps = self.solution.sections()
        print(f"create_build: {self.solution_steps}")
        self.build()

    def build(self):

        self.window_width_relative = (Window.width / 1080)
        self.window_height_relative = (Window.height / 1920)
        self.relative_size = ((self.window_width_relative + self.window_height_relative) / 2)

        self.solution_step_widgets = []
        solution_step_layout = self.ids['solution_steps_layout']

        solution_title_label = self.ids['solution_title_label']
        solution_title_label.text = self.solve_file_path

        for s in range(len(self.solution_steps)):
            self.solution_step_widgets.append(
                SolutionStep(x=30 * self.relative_size, width=Window.width - 60 * self.relative_size))
            self.solution_step_widgets[s].background_color = App.get_running_app().theme.color_neutral_muted
            latex_image = self.solution_step_widgets[s].ids['latex_image']
            latex_image_scrollview = self.solution_step_widgets[s].ids["latex_image_scroll"]
            if s == len(self.solution_steps) - 1:
                self.solution_step_widgets[s].background_color = App.get_running_app().theme.color_right
            else:
                self.solution_step_widgets[s].background_color = App.get_running_app().theme.color_neutral_muted
            instructions_label = self.solution_step_widgets[s].ids["instructions_label"]
            latex_image.color = App.get_running_app().theme.color_neutral
            instructions_label.color = App.get_running_app().theme.color_neutral
            latex_image.source = os.path.join(App.get_running_app().user_data_dir, "Renders", self.solve_file_path,
                                              "steppysteps", f"step{s}.png")
            latex_image_size = imagesize.get(latex_image.source)
            instructions_label.text = self.solution[self.solution_steps[s]]['instruction'].replace("text: ", "")
            if instructions_label.text == "":
                padding_height = 60
            else:
                padding_height = 90
            latex_image.texture_update()
            instructions_label.texture_update()
            latex_image.height = 75 * (latex_image_size[1] / 75) * self.relative_size
            latex_image.width = max(latex_image_scrollview.width,
                                    latex_image.height * (latex_image_size[0] / latex_image_size[1]))
            self.solution_step_widgets[
                s].height = latex_image.height + instructions_label.height + padding_height * self.relative_size
            solution_step_layout.add_widget(self.solution_step_widgets[s])

        cumulative_height = 0
        for s in range(len(self.solution_step_widgets)):
            cumulative_height += self.solution_step_widgets[s].height
            cumulative_height += 40 * self.relative_size
        solution_step_layout.height = cumulative_height

    def on_resize(self, instance, value):

        self.window_width_relative = (Window.width / 1080)
        self.window_height_relative = (Window.height / 1920)
        self.relative_size = ((self.window_width_relative + self.window_height_relative) / 2)

        solution_step_layout = self.ids['solution_steps_layout']

        for s in range(len(self.solution_steps)):
            latex_image = self.solution_step_widgets[s].ids['latex_image']
            latex_image_scrollview = self.solution_step_widgets[s].ids["latex_image_scroll"]
            instructions_label = self.solution_step_widgets[s].ids['instructions_label']

            instructions_label.font_size = 60 * self.relative_size

            latex_image_size = imagesize.get(latex_image.source)
            latex_image.height = 75 * (latex_image_size[1] / 75) * self.relative_size
            latex_image.width = max(latex_image_scrollview.width - 5,
                                    latex_image.height * (latex_image_size[0] / latex_image_size[1]))
            if instructions_label.text == "":
                padding_height = 60
            else:
                padding_height = 90
            latex_image.texture_update()
            instructions_label.texture_update()
            self.solution_step_widgets[s].height = latex_image.height + instructions_label.height + padding_height * self.relative_size
            self.solution_step_widgets[s].width = Window.width - 60 * self.relative_size
            latex_image.width = max(Window.width - 120 * self.relative_size,
                                    latex_image.height * (latex_image_size[0] / latex_image_size[1]))
        cumulative_height = 0
        for s in range(len(self.solution_step_widgets)):
            cumulative_height += self.solution_step_widgets[s].height
            cumulative_height += 40 * self.relative_size
        solution_step_layout.height = cumulative_height


class FileScreen(Screen):

    def on_enter(self):
        App.get_running_app().screen_history.append("files")
        self.build()
        self.bind(size=self.on_resize)
        self.popup = FileOpenPopup()

    def on_leave(self):
        file_chooser = self.ids["file_chooser"]
        file_chooser.clear_widgets()

    def back(self):
        try:
            App.get_running_app().screen_history.pop()
        except IndexError:
            pass
        try:
            return App.get_running_app().screen_history[len(App.get_running_app().screen_history) - 1]
        except IndexError:
            return "home"

    def open(self):
        # if file is selected
        try:
            # Get full filepath of selected
            selected_file = self.file_labels[len(self.file_labels) - self.selected_file_index - 1].text
            selected_file_path = os.path.join(App.get_running_app().user_data_dir, "Solutions", selected_file)
            self.selected_file_path = selected_file_path
            # print(self.selected_file_path)

            # Set popup title text
            self.popup.ids["filename_label"].text = selected_file

            # Compute maximum image height and maximum popup size based on window size
            max_image_height_raw = (120 + 120 + 150 + 30 + 30 + 145)
            max_image_height = Window.height - max_image_height_raw * self.relative_size
            max_image_width = self.popup.width - 120 * self.relative_size
            image_size = imagesize.get(os.path.join(self.selected_file_path, "image.png"))

            # Fit image
            if image_size[0] / image_size[1] < max_image_width / max_image_height:
                image_height = max_image_height
            else:
                image_height = (Window.size - 240 * self.relative_size) * image_size[1] / image_size[0]

            # Popup height to image and window
            self.popup.height = image_height + (max_image_height_raw - 120) * self.relative_size
            selected_file_image_params = {
                "source": os.path.join(self.selected_file_path, "image.png"),
                "size_hint": (None, None),
            }

            # Create image and build
            self.selected_file_image = Image(**selected_file_image_params)
            self.popup_layout = self.popup.ids["popup_layout"]
            self.popup_layout.add_widget(self.selected_file_image)
            self.selected_file_image.size = image_size[0] / image_size[1] * image_height, image_height
            self.popup.bind(on_dismiss=self.clean_up_popup)
            self.popup.open()

        # if nothing is selected
        except:
            pass

        # Update so elements are in correct position
        try:
            max_image_height_raw = (120 + 120 + 150 + 30 + 30 + 145)
            max_image_height = Window.height - max_image_height_raw * self.relative_size
            max_image_width = self.popup.width - 120 * self.relative_size
            image_size = imagesize.get(os.path.join(self.selected_file_path, "image.png"))
            if image_size[0] / image_size[1] < max_image_width / max_image_height:
                image_height = max_image_height
            else:
                image_height = (Window.size[0] - 240 * self.relative_size) * image_size[1] / image_size[0]
            self.popup.height = image_height + (max_image_height_raw - 120) * self.relative_size
            self.selected_file_image.x = self.popup.x + (self.popup.width / 2) - (self.selected_file_image.width / 2)
            self.selected_file_image.y = self.popup.y + (320 * self.relative_size)
            self.selected_file_image.size = image_size[0] / image_size[1] * image_height, image_height
        except AttributeError:
            pass

    def clean_up_popup(self, instance):
        self.popup_layout.remove_widget(self.selected_file_image)
        print(self.selected_file_image)

    def delete(self):
        selected_file = self.file_labels[len(self.file_labels) - self.selected_file_index - 1].text
        print(selected_file)
        selected_file_path = os.path.join(App.get_running_app().user_data_dir, "Solutions", selected_file)
        shutil.rmtree(selected_file_path)
        file_chooser = self.ids["file_chooser"]
        file_chooser.clear_widgets()
        self.build()

    def on_selected(self, instance, value):
        # change color when selected, using only one texture
        if value == "down":
            instance.background_color = App.get_running_app().theme.color_right
            self.selected_file_index = self.file_buttons.index(instance)
        else:
            instance.background_color = App.get_running_app().theme.color_neutral_muted
            self.selected_file_index = None

    def on_resize(self, obj, value):
        # Define new window dimensions
        self.window_width_relative = (Window.width / 1080)
        self.window_height_relative = (Window.height / 1920)
        self.relative_size = ((self.window_width_relative + self.window_height_relative) / 2)

        # Define new scrollview layout height
        file_chooser = self.ids["file_chooser"]
        self.chooser_height = ((len(self.files) * 240) * (
                (self.window_width_relative + self.window_height_relative) / 2)) + (
                                      (40 * (len(self.files) - 1)) * (
                                      (self.window_width_relative + self.window_height_relative) / 2))
        file_chooser.height = self.chooser_height

        # Update height of file entries, namely labels and their font
        for current_entry in range(len(self.file_buttons)):

            # Update size and position of labels
            self.file_labels[current_entry]._label.refresh()
            self.file_labels[current_entry].pos = self.file_labels[current_entry]._label.texture.size[
                                                      0] / 2 + 230 * self.relative_size, current_entry * (
                                                          280 * self.relative_size) + 120 * self.relative_size
            self.file_labels[
                current_entry].text_size = 790 * self.window_width_relative - 32 * self.relative_size, 60 * self.relative_size
            self.file_labels[current_entry].font_size = 60 * (
                    (self.window_width_relative + self.window_height_relative) / 2)

            # Update size and position of images
            if self.file_images[current_entry].source == self.default_file_image:
                self.file_image_size = 100
            else:
                self.file_image_size = 200
            self.file_images[current_entry].pos = (
                (15 * self.window_width_relative) + (100 * self.relative_size) - self.file_images[
                    current_entry].width / 2,
                current_entry * (
                        280 * self.relative_size) + (120 * self.relative_size) - self.file_images[
                    current_entry].height / 2)
            self.file_image_params["height"] = self.file_image_size * self.relative_size
            self.file_image_params["width"] = self.file_image_size * self.relative_size
            icon_width, icon_height = imagesize.get(self.file_images[current_entry].source)
            if icon_width > icon_height:
                self.file_image_params["height"] *= icon_height / icon_width
            else:
                self.file_image_params["width"] *= icon_width / icon_height
            self.file_images[current_entry].height = self.file_image_params["height"]
            self.file_images[current_entry].width = self.file_image_params["width"]
            # Update popup image compute image size
            try:
                max_image_height_raw = (120 + 120 + 150 + 30 + 30 + 145)
                max_image_height = Window.height - max_image_height_raw * self.relative_size
                max_image_width = self.popup.width - 120 * self.relative_size
                image_size = imagesize.get(os.path.join(self.selected_file_path, "image.png"))
                if image_size[0] / image_size[1] < max_image_width / max_image_height:
                    image_height = max_image_height
                else:
                    image_height = (Window.size[0] - 240 * self.relative_size) * image_size[1] / image_size[0]
                self.popup.height = image_height + (max_image_height_raw - 120) * self.relative_size
                self.selected_file_image.x = self.popup.x + (self.popup.width / 2) - (
                        self.selected_file_image.width / 2)
                self.selected_file_image.y = self.popup.y + (320 * self.relative_size)
                self.selected_file_image.size = image_size[0] / image_size[1] * image_height, image_height
            except AttributeError:
                pass

    def build(self):
        # Find files
        self.data_path = os.path.join(App.get_running_app().user_data_dir, "Solutions")
        self.files = glob.glob(os.path.join(self.data_path, "*/"))

        # Sort by recent
        self.files.sort(key=os.path.getmtime)

        file_chooser = self.ids["file_chooser"]

        # Define window dimensions
        self.window_width_relative = (Window.width / 1080)
        self.window_height_relative = (Window.height / 1920)
        self.relative_size = ((self.window_width_relative + self.window_height_relative) / 2)

        self.chooser_height = ((len(self.files) * 240) * self.relative_size) + (
                (40 * (len(self.files) - 1)) * self.relative_size)
        file_chooser.height = self.chooser_height

        # Parameters for button and label for file entry
        self.default_file_image = os.path.join("themes", App.get_running_app().theme.theme_folder, "icons",
                                               "file_empty.png")
        self.file_image_size = 100
        self.file_image_params = {
            "source": self.default_file_image,
            "height": self.file_image_size * self.relative_size,
            "width": self.file_image_size * self.relative_size,
            "pos": (0, 0),
            "allow_stretch": True,
        }
        self.file_entry_params = {
            "text": "",
            "group": "files",
            "background_normal": os.path.join("themes", App.get_running_app().theme.theme_folder, "boxes", "empty.png"),
            "background_down": os.path.join("themes", App.get_running_app().theme.theme_folder, "boxes", "empty.png"),
            "background_color": App.get_running_app().theme.color_neutral_muted,
            "border": [20] * 4,
        }
        self.label_entry_params = {
            "text": "world",
            "shorten": True,
            "shorten_from": "right",
            "text_size": (700 * self.window_width_relative, 60 * self.relative_size),
            "font_name": "main",
            "font_size": 60 * self.relative_size,
            "pos": (0, 0),
        }

        self.file_buttons = []
        self.file_labels = []
        self.file_images = []

        # Create file list from parameters
        for file in self.files:
            try:
                source_image = os.path.join(file, "image.png")
                self.file_image_size = 200
                icon_width, icon_height = imagesize.get(source_image)
                if imghdr.what(source_image) != "png":
                    source_image = self.default_file_image
                    icon_width, icon_height = imagesize.get(source_image)
                    self.file_image_size = 100
            except FileNotFoundError:
                source_image = self.default_file_image
                icon_width, icon_height = imagesize.get(source_image)
                self.file_image_size = 100

            self.file_image_params["source"] = source_image
            self.file_image_params["height"] = self.file_image_size * self.relative_size
            self.file_image_params["width"] = self.file_image_size * self.relative_size
            if icon_width > icon_height:
                self.file_image_params["height"] *= icon_height / icon_width
            else:
                self.file_image_params["width"] *= icon_width / icon_height
            # Create labels for file
            self.label_entry_params["text"] = file.replace(self.data_path, "").replace("/", "")
            self.file_buttons.append(ToggleButton(**self.file_entry_params))

            current_entry = len(self.file_buttons) - 1
            # Position relative
            self.file_image_params["pos"] = (
                (15 * self.window_width_relative) + (100 * self.relative_size) - self.file_image_params["width"] / 2,
                current_entry * (
                        280 * self.relative_size) + (120 * self.relative_size) - self.file_image_params["height"] / 2)
            self.file_images.append(Image(**self.file_image_params))

            self.file_labels.append(Label(**self.label_entry_params))

            self.file_labels[current_entry].size = self.file_labels[current_entry].texture_size
            self.file_labels[current_entry]._label.refresh()
            self.file_labels[current_entry].pos = self.file_labels[current_entry]._label.texture.size[
                                                      0] / 2 + 230 * self.relative_size, current_entry * (
                                                          280 * self.relative_size) + 120 * self.relative_size
            self.file_buttons[current_entry].add_widget(self.file_labels[current_entry])
            self.file_buttons[current_entry].add_widget(self.file_images[current_entry])
            if self.file_images[current_entry].source == self.default_file_image:
                self.file_images[current_entry].color = App.get_running_app().theme.color_neutral_muted
            file_chooser.add_widget(self.file_buttons[current_entry])

            self.file_buttons[current_entry].bind(state=self.on_selected)


class SettingsScreen(Screen):
    pass


class FocusMath(App):

    def __init__(self):
        App.__init__(self)
        try:
            os.mkdir(os.path.join(self.user_data_dir, "Solutions"))
        except FileExistsError:
            pass
        self.theme = themeConfig()
        self.theme.read_theme()
        self.screen_history = ["home"]
        os.environ['SSL_CERT_FILE'] = certifi.where()

    def clean_saved_images(self):
        files = glob.glob(os.path.join(App.get_running_app().user_data_dir, "Solutions", "*/"))
        for file in files:
            try:
                image = os.path.join(file, "image.png")
                print(image)
                if imghdr.what(image) == "png":
                    image_utils.crop_transparent(image, image)
                else:
                    os.remove(image)
            except FileNotFoundError:
                pass

    def build(self):
        start_load = datetime.now()
        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(FileScreen(name='files'))
        self.sm.add_widget(SolveEquScreen(name='solveequ'))
        self.sm.add_widget(CheckWorkScreen(name='check'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        print(f"GUI Load: {datetime.now() - start_load}")
        return self.sm

    def on_start(self):
        self.profile = cProfile.Profile()
        self.profile.enable()
        LabelBase.register(name="main", fn_regular=App.get_running_app().theme.font_info)

    def on_stop(self):
        self.profile.disable()
        self.profile.dump_stats('debug.prof')


class solution(object):
    def __init__(self):
        try:
            os.mkdir(os.path.join(App.get_running_app().user_data_dir, "Solutions", "Outputs"))
        except Exception:
            pass

    def call_mathpix(self, filepath):
        # Creates render directories
        try:
            os.mkdir(os.path.join(App.get_running_app().user_data_dir, "Renders"))
        except Exception as e:
            print(e)
        try:
            os.mkdir(os.path.join(App.get_running_app().user_data_dir, "Renders", filepath))
            os.mkdir(os.path.join(App.get_running_app().user_data_dir, "Renders", filepath, "steps"))
        except Exception as e:
            print(e)

        # Checks if an internet connection exists.
        try:
            urllib.request.urlopen('https://www.google.com', timeout=3)
        except Exception as e:
            return f"[ERROR]{e} Sorry! We encountered an issue. Check your internet connection and try again!"

        try:
            source_filepath = os.path.join(App.get_running_app().user_data_dir, "Solutions", filepath, "image.png")
        # Handles a failure to get a reply from mathpix
        except ConnectionAbortedError:
            # return "\\text[ERROR<ConnectionAbortedError> This could be because of \n[http_unauthorized], [http_max_requests] \nCheck https://mathpix.github.io/docs/#errors]"
            pass

        # if 'latex_simplified' not in r:
        #     r['latex_simplified'] = "OCR_ERROR"
        self.ocr_latex = mathpix.latex(
            {'src': mathpix.image_uri(f'{source_filepath}'), 'formats': ['latex_simplified']})
        print(self.ocr_latex)
        print(self.ocr_latex['latex_simplified'])
        print(filepath)
        image_utils.render_text(
            self.ocr_latex['latex_simplified'],
            os.path.join(App.get_running_app().user_data_dir, "Renders", filepath, "capture_render.png"),
            os.path.join(App.get_running_app().user_data_dir, "Renders", filepath, "steps", "steps_render.png")
        )
        return self.ocr_latex

    def step_by_step(self, input_latex, writepath, input_filepath):

        try:
            os.mkdir(os.path.join(App.get_running_app().user_data_dir, "Renders", input_filepath, "steppysteps"))
        except Exception as e:
            print(e)
        input_latex = StepPyStep.parse_tex().replaceBackSlash(input_latex)

        # What the OCR detected in the image.
        engine = StepPyStep.solve_equation()
        self.solution_link = engine.wolfram_alpha(input_latex, image=False)
        print(self.solution_link)
        temp = []
        solution_list = []
        for i in range(len(self.solution_link)):
            temp.append(self.solution_link[i])
            if i % 2 == 1:
                solution_list.append(temp)
                print(f"temp: {temp}")
                temp = []
        print(solution_list)
        with open(f"{writepath}", "w+", encoding='utf-8') as steps_file:
            print(solution_list)
            write_steps = configparser.ConfigParser()
            for i in range(len(solution_list)):
                write_steps[f"STEP{i}"] = {
                    "instruction": solution_list[i][0],
                    "operation": solution_list[i][1]
                }
            write_steps.write(steps_file)
        for i in range(len(solution_list)):
            filename = f"step{i}.png"
            render_text = solution_list[i][1].replace('|', '')
            print(f"Rendering {render_text}")
            image_utils.render_text(render_text,
                                    os.path.join(App.get_running_app().user_data_dir, "Renders", input_filepath,
                                                 "steppysteps", filename), delete_intermediate=True)
        print(solution_list)
        return solution_list

    def check(self, input_latex, writepath):
        tex = input_latex
        tex = str(tex)
        engine = StepPyStep.solve_equation()
        # error here
        latex_list = StepPyStep.parse_tex().split_array(input_latex)
        print(latex_list)
        if not isinstance(latex_list, list):
            return "NOT_MULTILINE"
        for i in range(len(latex_list)):
            latex_list[i] = latex_list[i].replace("{", "(")
            latex_list[i] = latex_list[i].replace("}", ")")
            latex_list[i] = latex_list[i].replace("^", "**")
            latex_list[i] = StepPyStep.parse_tex().replaceBackSlash(latex_list[i])
        a = engine.get_answer(latex_list[0])
        results = []
        dirFile = open("curdir.tmp", "r")
        solveFilePath = dirFile.read()
        dirFile.close()
        with open(os.path.join(App.get_running_app().user_data_dir, "Solutions", solveFilePath, "check.txt"), "w+",
                  encoding='utf-8') as check_file:

            for i in range(len(latex_list)):
                write_steps = configparser.ConfigParser()
                print(f"latex_list[{i}]: {latex_list[i]}")

                truth = StepPyStep.check_equation().check_eq(latex_list[i], a, precision=5, step=i,
                                                             writepath=os.path.join(App.get_running_app().user_data_dir,
                                                                                    "Solutions", solveFilePath))

                truth = truth.replace("**", "^")
                results.append(truth)
                if ("False" in truth):
                    print(truth)
                    if (i == 0):
                        print(f"latex_list[i]: {latex_list[i]}")
                        result = StepPyStep.solve_equation().wolfram_alpha(latex_list[i], writepath)

                        print(f"result: {result}")
                        results.append(result)
                    else:
                        print(f"latex_list[i-1]: {latex_list[i - 1]}")
                        result = StepPyStep.solve_equation().wolfram_alpha(latex_list[i - 1], writepath)
                        print(f"result: {result}")
                        results.append(result)
                    print(f"STEP{i}")
                    truth = truth.replace("(False)", "")
                    write_steps[f"STEP{i}"] = {
                        "step": truth,
                        "isCorrect": False
                    }
                    temp = []
                    correction_list = []
                    for i in range(len(result)):
                        temp.append(result[i])
                        if i % 2 == 1:
                            correction_list.append(temp)
                            temp = []
                    for correction in correction_list:
                        write_steps[f"CORRECTION{correction_list.index(correction)}"] = {
                            "instruction": correction[0],
                            "operation": correction[1]
                        }
                    write_steps.write(check_file)
                    return results
                else:
                    write_steps[f"STEP{i}"] = {
                        "step": truth,
                        "isCorrect": True
                    }
                    write_steps.write(check_file)

        results.append("All correct!")
        return results


if __name__ == '__main__':
    FocusMath().run()

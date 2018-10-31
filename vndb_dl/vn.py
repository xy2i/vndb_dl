# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

import os
import json
import requests
import textwrap

class VN:
    """
    Represents a visual novel.
    Each instance contains metadata about the visual novel
    and screenshot links of the visual novel.
    """
    __slots__ = ["id", "metadata", "soup", "url_screenshots"]

    def __init__(self, id):
        """
        Initialize the class.
        From the ID of the VN, get the metadata and screenshot links.
        """
        # The ID refers to the number in each vndb v-url: https://vndb.org/v###
        # where ### is the id.
        self.id = id
        self.soup = self.__make_soup()
        self.metadata = self.__extract_metadata()
        self.url_screenshots = self.__extract_screenshots_url()

    def __make_soup(self):
        """
        Creates the soup from the vndb page.
        """
        # Creates the entire URL for the VN. This type of URL is prefixed with a v
        # for "visual novel", and is the vn info page.
        url = "https://vndb.org/v" + str(self.id)

        # Parse the content into an adressable tree with BeautifulSoup.
        content = requests.get(url).content 
        soup = BeautifulSoup(content, features="html.parser")

        return soup

    def __extract_metadata(self):
        """
        Gets the metadata from the soup, returned as a dict.
        """
        # We have to deal with either an HTML table with two columns, that 
        # can be fitted into a key:value dicttionary for later traversal, and
        # a single column containing the description at the end.
        # The metadata table can be of variable size and contain any of various tags.
        # We don't worry about this, just fit all the tags we can find into the dict.
        
        metadata = {}
        # Get a list of all the rows, separated by td tags
        rows = self.soup.table.find_all('tr')

        for row in rows:
            # Does an h2 element exist in this row's first column? 
            # If so, the row has one element: the description
            if row.td.h2:
                # The description text is contained within the <p> tags
                desc = row.td.p

                # Convert linebreaks
                for br in desc.find_all("br"):
                    br.replace_with("\n" + br.text)

                desc = desc.text
                metadata["Description"] = desc
                
            # Otherwhise, it is a list of two columns: the first is the key,
            # the second is the value
            else:
                column = row.find_all("td")
                column = [element.text for element in column]
                metadata[column[0]] = column[1]

        return metadata

    def __extract_screenshots_url(self):
        """
        Gets each screenshot link from the vndb page.
        """
        # Confusingly enough, a vndb page can host multiple different revisions
        # of a VN, which are called "games" here.
        # For pages with multiple games, we need to get the list for each game,
        # then extract the screenshots for each.
        
        # Get the list of game. Each game is delimited with a <div scr..> tag.
        game_list = self.soup.findAll("div", attrs="scr")

        # We are interested in the href tag of each, which gives us the direct
        # link to each screenshot.
        # No list comprehensions here! 
        screenshot_url_list = []
        for game in game_list:
            for ele in game:
                screenshot_url_list.append(ele["href"])

        return screenshot_url_list

    def __extract_screenshots(self):
        """
        Generator that yields each successive screenshot on use.
        Each screenshot is given back ordered in the same order as on vndb.
        """
        for screenshot_url in self.url_screenshots:
            screenshot = requests.get(screenshot_url).content
            yield screenshot

    def extract(self, directory):
        """
        Extracts all data from the VN object in human-readable form
        to the specified directory, in its own named folder.
        """ 
        folder_name = str(self.id) + " - " + self.metadata["Title"]
        path = os.path.join(directory, folder_name)
        
        if not os.path.exists(path):
            os.mkdir(path)

        # Each time the generator is called, the screenshot is downloaded.
        for counter, screenshot in enumerate(self.__extract_screenshots()):
            filename = self.metadata["Title"] + "_screenshot" + str(counter+1) + ".jpg"
            with open(os.path.join(path, filename), "wb") as file:
                file.write(screenshot)

        # TODO: arg parser flags to check json/plain
        filename = "metadata.json"
        with open(os.path.join(path, filename), "w", encoding="utf-8") as file:
            file.write(json.dumps(self.metadata, indent=4, separators=(',', ': ')))

        filename = "metadata.txt"
        with open(os.path.join(path, filename), "w", encoding="utf-8") as file:
            for key, value in self.metadata.items():
                file.write(key + ": " + textwrap.fill(value, width=80) + "\n\n")
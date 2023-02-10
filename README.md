<p align="center">
  <a href="https://www.ros.org/">
    <img src="https://media.tenor.com/5K72-R8R8s0AAAAC/ice-scraping-winter.gif" alt="Logo" width=72 height=72>
  </a>

  <h3 align="center">News Scraper Project</h3>

  <p align="center">
    A web scraper integration using RPA from Robocorp
    <br>
  </p>
</p>


## Table of contents

- [Guide to install and run](#guide-to-install-and-run)
- [Explanation of each excel rows](#frontend)

## Guide to install and run

Please follow step by step, all these commands, and run from base folder


- Run env_vars.sh file, inside it are the environment variables such phrase, months and section.

  ```
  source ./env_vars.sh
  ```
- Install your virtual env (conda)

- To run

  ```
  python main.py
  ```

## Explanation of each excel rows

- **title**: The news main title.

- **description**: The news main description.

- **date**: Date of publish of the news.

- **has_money**: If the title or description has some money pattern like $11 or $11.11.

- **phrase_in_title**: Number of times the phrase searched appears in title.

- **phrase_in_description**: Number of times the phrase searched appears in description.

- **picture_filename**: src of the image file.

#### I wish I could have asked my questions about each data requested for the excel, I wanted an example of the generated excel file, but I couldn't get it, so each data is as I thought it should be, sorry if it was not exactly what was asked to extract , I did my best :)

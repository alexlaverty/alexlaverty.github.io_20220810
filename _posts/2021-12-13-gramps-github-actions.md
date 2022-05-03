---
layout: post
title: Generating a Gramps Website with Github Actions Workflow
date: 2021-12-12 11:33:00 +0800
categories: [tech]
tags: [
  gramps,
  python,
  ]
image:
  src: /assets/img/deploying-gramps-on-github-pages-using-github-action-workflow/2021-10-11-21-51-24.png
---

- [Introduction](#introduction)
- [Download and install Gramps](#download-and-install-gramps)
- [Add Your Family Members to Gramps](#add-your-family-members-to-gramps)
- [Export Gramps Family Tree as a GEDCOM file](#export-gramps-family-tree-as-a-gedcom-file)
- [Generate Gramps Narrated Website Locally](#generate-gramps-narrated-website-locally)
- [Encrypt GEDCOM file](#encrypt-gedcom-file)
- [Create a Github Pages Website](#create-a-github-pages-website)
- [Set the ZIP Password as a Repository Secret](#set-the-zip-password-as-a-repository-secret)
- [Create Github Action Workflow YML Config](#create-github-action-workflow-yml-config)
- [Docker Image with Gramps Depenencies Installed](#docker-image-with-gramps-depenencies-installed)
- [Viewing the Github Actions Workflow Build Status](#viewing-the-github-actions-workflow-build-status)
- [Browsing Your Generated Gramps Website](#browsing-your-generated-gramps-website)
- [Other Options When Generating Gramps Website](#other-options-when-generating-gramps-website)
- [Updating Your Gramps Website](#updating-your-gramps-website)

## Introduction

I have recently been looking into my genealogy and wanted to put together a family tree and see how far back I could go.
I came across the opensource genealogy software called [Gramps](https://gramps-project.org/), 
Gramps provides a GUI to be able to add in your Family members and the ability to output reports, charts, and also compile what they call a [Narrated Website](https://gramps-project.org/wiki/index.php/Howto:_Make_a_genealogy_website_with_Gramps) for you to browse your family tree.

[Github Pages](https://pages.github.com/) allows you to host a static website free of charge, and [Github Actions](https://docs.github.com/en/actions) provides you with a build system to be able to build/compile your github project based on a Schedule or via pushing commits to the repo.

I combined Gramps with Github Pages and Github Actions to put together an automated CICD pipeline to build and host my Family Tree Gramps website.

## Download and install Gramps

Download Gramps here [Gramps Download](https://gramps-project.org/blog/download/)

## Add Your Family Members to Gramps

How to create a family tree is out of scope for this document so I will refer you to the [Gramps - Getting Started Guide](https://gramps-project.org/wiki/index.php/Gramps_5.1_Wiki_Manual_-_Getting_started)

## Export Gramps Family Tree as a GEDCOM file

Once you have all your family members added into gramps and are ready to generate the website, export the family tree as a GEDCOM file :

![](/assets/img/gramps-github-actions/2021-10-10-16-15-07.png)

![](/assets/img/gramps-github-actions/2021-10-10-16-18-35.png)

## Generate Gramps Narrated Website Locally

To test your GEDCOM file locally you can run the following command :

```
gramps -i gramps.ged -a report -p name=navwebpage,incl_private=False,living_people=2,target=./
```

* `-i` should point to your gedcom file 
* `-p name=navwebpage` specifies you want to generate the Narrated Website 
  
* For security reasons I am excluding private info from the webpage and also hiding the birthdays of living members for security reasons, do this with the following parameters :

```
incl_private=False,living_people=2
```
* `target=./` means to generate the webpage in the current directory

Once it's finished generating you can open the index.html page and browse the site, verify you can not see birthdays of living members.


## Encrypt GEDCOM file

A family tree contains information about living people, including birthdates and fullnames etc. This information can be used by unsavioury characters for identity fraud,
as I am pushing this file up into a public github repository I have chosen to zip and encrypt the GEDCOM file with a password using 7zip :

Right click the gedcom file and select Add To Archive

![](/assets/img/gramps-github-actions/2021-10-10-16-24-39.png)

Enter a strong password to encrypt the zip with 

![](/assets/img/gramps-github-actions/2021-10-10-16-25-21.png)

## Create a Github Pages Website

Follow instructions on how to configure a Github Pages Website this will allow you to host a static html website for free on Github

[Getting Started with GitHub Pages](https://guides.github.com/features/pages/)

For me I have created a github repo named [alexlaverty.github.io ](https://github.com/alexlaverty/alexlaverty.github.io) which can be browsed here <https://alexlaverty.github.io/>

## Set the ZIP Password as a Repository Secret

During the Github build we want to decrypt the 7Zip file with our password so go into your repositories `Settings -> Secrets -> Repository Secrets`
Create a `GRAMPS_ZIP_PASSWORD` secret and enter your zips password as the value. We will reference this secret in the build yml.

![](/assets/img/gramps-github-actions/2021-10-10-16-47-59.png)

## Create Github Action Workflow YML Config

Github Actions allows you to define build steps by creating yml build definitions in the root of the repository at `.github/workflows`

Here is my github workflow yml for generating the gramps website, i have added comments to the file below 

<https://github.com/alexlaverty/alexlaverty.github.io/blob/main/.github/workflows/genealogy.yml>

```
# Give the Github Action Workflow a Name 
name: Genealogy

# Trigger the build when a file is checked into the folder paths genealogy or the github workflow is updated 
# when the checkin is to the main branch
on:
  push:
    paths:
      - 'genealogy/**'
      - '.github/workflows/genealogy.yml'
    branches:
      - main
jobs:
  build:
    # Run on a ubuntu build agent
    runs-on: ubuntu-latest

    # Run in a docker container with the required build dependencies installed 
    container: alexlaverty/alexlaverty:1.0.2

    # Run commands from within the genealogy website
    env:
      working-directory: ./genealogy
    steps:
      # Checkout the github repo
      - name: checkout repo content
        uses: actions/checkout@v2 # checkout the repository content to github runner
         
      # Decrypt the 7Zip gedcom file, 
      # do a small workaround for a bug, 
      # generate the Gramps website and then clean up the decrypted gedcom file
      - name: Generate Gramps Narrated Website
        run: |
          7z x gramps.7z -p$GRAMPS_ZIP_PASSWORD -y
          # Workaround for bug in database name in Gramps generic.py
          sed -i 's/name.txt/database.txt/g' /usr/lib/python3/dist-packages/gramps/gen/db/generic.py
          gramps -i gramps.ged -a report -p name=navwebpage,incl_private=False,living_people=2,target=./
          rm -f gramps.ged
        working-directory: ${{env.working-directory}}
        # The ZIP file password is stored as a github repo secret
        env:
          GRAMPS_ZIP_PASSWORD: ${{ secrets.GRAMPS_ZIP_PASSWORD }}

      # Commit the generated files and push them up to the github repo
      - name: commit files
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add -A
          git commit -m "Genealogy Update" -a
        working-directory: ${{env.working-directory}}
          
      - name: push changes
        uses: ad-m/github-push-action@v0.6.0
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          branch: main
```

## Docker Image with Gramps Depenencies Installed

The `alexlaverty/alexlaverty:1.0.2` docker image that I am referecing in the build has gramps, 7zip and git installed in it, the dockerfile is :

https://github.com/alexlaverty/alexlaverty.github.io/blob/main/Dockerfile

```
FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y \
            python3-pip \
            p7zip-full \
            gramps \
            git
```

I plan on using that container for some other builds so will probably add in extra dependecies in there for my other projects later.

## Viewing the Github Actions Workflow Build Status

Once you've pushed your encrypted gedcom zip into your github pages repo and have pushed your Github Actions Workflow YML config you should then be able to go see your build run and view the status and build log for it.

In your github pages repo, click `Actions --> Genealogy` Then click on a build

![](/assets/img/gramps-github-actions/2021-10-10-17-02-42.png)

From here you can see the status of each step and click each step and see the build log output 

![](/assets/img/gramps-github-actions/2021-10-10-17-03-24.png)

## Browsing Your Generated Gramps Website

Once you build is successful you should be able to view your Gramps Github Pages website, for example mine is :

<https://alexlaverty.github.io/genealogy/>

## Other Options When Generating Gramps Website

To view other available parameters you can use while generating the Gramps Narrated Website run the following commands :

```
gramps -i gramps.ged -a report -p name=navwebpage,show=all

Performing action: report.
Using options string: name=navwebpage,show=all
   Available options:
      ancestortree      Whether to include an ancestor graph on each individual page ()
      archive           Whether to store the web pages in an archive file ()
      birthorder        Whether to display children in birth order or in entry order? ()
      caluri            Where do you place your web site ? default = /WEBCAL ()
      citationreferents Determine the default layout for the Source Page's Citation Referents section ()
      cmsuri            Where do you place your web site ? default = /NAVWEB ()
      contactimg        An image to be used as the publisher contact.
If no publisher information is given,
no contact page will be created ()
      contactnote       A note to be used as the publisher contact.
If no publisher information is given,
no contact page will be created ()
      coordinates       Whether to display latitude/longitude in the places list? ()
      create_thumbs_only        This option allows you to create only thumbnail images instead of the full-sized images on the Media Page. This will allow you to have a much smaller total upload size to your web hosting site. ()
      cright            The copyright to be used for the web files ()
      css               The stylesheet to be used for the web pages ()
      date_format       The format and language for dates, with examples ()
      dl_descr1         Give a description for this file. ()
      dl_descr2         Give a description for this file. ()
      down_fname1       File to be used for downloading of database ()
      down_fname2       File to be used for downloading of database ()
      encoding          The encoding to be used for the web files ()
      ext               The extension to be used for the web files ()
      extrapage         Your extra page path without extension ()
      extrapagename     Your extra page name like it is shown in the menubar ()
      familymappages    Whether or not to add an individual page map showing all the places on this page. This will allow you to see how your family traveled around the country. ()
      filter            Select filter to restrict people that appear on web site ()
      footernote        A note to be used as the page footer ()
      gallery           Whether to include a gallery of media objects ()
      googlemapkey      The API key used for the Google maps ()
      googleopts        Select which option that you would like to have for the Google Maps Family Map pages... ()
      graphgens         The number of generations to include in the ancestor graph ()
      headernote        A note to be used as the page header ()
      homeimg           An image to be used on the home page ()
      homenote          A note to be used on the home page ()
      inc_addressbook   Whether or not to add Address Book pages,which can include e-mail and website addresses and personal address/ residence events. ()
      inc_events        Add a complete events list and relevant pages or not ()
      inc_families      Whether or not to include family pages. ()
      inc_gendex        Whether to include a GENDEX file or not ()
      inc_id            Whether to include Gramps IDs ()
      inc_places        Whether or not to include the places Pages. ()
      inc_repository    Whether or not to include the Repository Pages. ()
      inc_sources       Whether or not to include the sources Pages. ()
      inc_stats         Whether or not to add statistics page ()
      incdownload       Whether to include a database download option ()
      incl_private      Whether to include private data ()
      introimg          An image to be used as the introduction ()
      intronote         A note to be used as the introduction ()
      linkhome          Include a link to the active person (if they have a webpage) ()
      living_people     How to handle living people ()
      mapservice        Choose your choice of map service for creating the Place Map Pages. ()
      maxinitialimageheight     This allows you to set the maximum height of the image shown on the media page. Set to 0 for no limit. ()
      maxinitialimagewidth      This allows you to set the maximum width of the image shown on the media page. ()
      name_format       Select the format to display names ()
      navigation        Choose which layout for the Navigation Menus. ()
      notes             Include narrative notes just after name, gender and age at death (default) or include them just before attributes. ()
      of                Output file name. MANDATORY (=filename)
      off               Output file format. (=format)
      papermb           Bottom paper margin (=number)
      paperml           Left paper margin (=number)
      papermr           Right paper margin (=number)
      papermt           Top paper margin (=number)
      papero            Paper orientation number. (=number)
      papers            Paper size name. (=name)
      pid               The centre person for the filter ()
      placemappages     Whether to include a place map on the Place Pages, where Latitude/ Longitude are available. ()
      prevnext          Add previous/next to the navigation bar. ()
      reference_sort    Sort the places references by date or by name. Not set means by date. ()
      relation          For each person page, show the relationship between this person and the active person. ()
      securesite        Whether to use http:// or https:// ()
      showbirth         Whether to include a birth column ()
      showdeath         Whether to include a death column ()
      showhalfsiblings  Whether to include half and/ or step-siblings with the parents and siblings ()
      showparents       Whether to include a parents column ()
      showpartner       Whether to include a partners column ()
      style             Style name. (=name)
      target            The destination directory for the web files ()
      title             The title of the web site ()
      trans             The translation to be used for the report. ()
      unused            Whether to include unused or unreferenced media objects ()
      usecal             ()
      usecms             ()
      years_past_death  Whether to restrict data on recently-dead people ()
   Use 'show=option' to see description and acceptable values
Cleaning up.
```

To view help around a specific command what the accepted values are, 
for example I needed to know what value to pass in for  `show=living_people`, so run the command like :

```
gramps -i gramps.ged -a report -p name=navwebpage,show=living_people

Performing action: report.
Using options string: name=navwebpage,show=living_people
   Available values are:
      living_people     How to handle living people ()
      99        Included, and all data
      2 Full names, but data removed
      1 Given names replaced, and data removed
      3 Complete names replaced, and data removed
      0 Not included
```

## Updating Your Gramps Website 

Once you have this pipeline setup and configured and successfully building and publish, 
all you will need to do is push an updated encrypted 7Zip file with your updated GEDCOM file.
This will trigger the build to run and regenerate and publish your Gramps Narrated Website updates.


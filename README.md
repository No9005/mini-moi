<p align="center">
    <img src="https://user-images.githubusercontent.com/52833906/159451562-de17a088-1438-4198-8e90-0cda45ef307a.png" alt="Mini Moi" style="width:25%;">
</p>
<p style="color:gray" align="center"><em><a href='https://de.freepik.com/vektoren/design'>Checkout - freepik - </a></em></p>

<br>


# mini-moi
Little assistant to organizing deliveries. <br>



## <a name="top"></a> CONTENT
1. [Introduction](#whats-it)
2. [Features](#features)
2. [Installing](#install)
3. [Quickstart](#how)
4. [Manual](#manual)
5. [Additional infos](#why)
 

<br>

# <a name='whats-it'></a> Introduction <sub><sub>[Back to top](#top)</sub></sub> 

<b>Mini Moi</b> enables you to perform CRM light functions. The centerpiece though is the tracking of next-day deliveries. <br>
After creating your **sortiment, customers & abos**, the programm is automatically tracking and creating overviews for upcoming deliveries. <br>
Easy and reliable. What remains is more sparetime for you! <br>

<br>

<p align="center">
<img src="https://user-images.githubusercontent.com/52833906/160295657-8118154b-118f-4703-a539-785ba1f3067a.png" alt="mini-moi delivery screen" style="width:50%">
</p>

<br>

It also comes packed with three Languages: **English, German and French.** <br>
To use it you just have to install python, load the current release and install the requirements. For detailed instructions please refere to [Installing](#install).

<br>

# <a name='features'></a> Features <sub><sub>[Back to top](#top)</sub></sub> 

The core features are:
- Creation, editing & deleting of customers, products & abos either (`Management screen`):
    - The frontend: A HTML/javascript combination which is executed in the browser of your choice. 
    - Bulk editor: You can use (and create!) the excel blueprints to mass upload new table entries!
- Next delivery tracking (`Delivery screen`):
    - Check the deliveries for the next day
    - Download a excel report, which summarizes the to be shipped products & the delivery addresses of your customers.
    - Book the next deliveries. This logs the products for the next day and enables them for the reporting section
- Creating reports (`Report screen`):
    - Get an overview of your earnings, revenue and sold products for different time periods.
- Multi language support:
    - <b>Mini Moi</b> supports 3 languages:
        - English
        - German
        - French
- Database backup & rollback options 

<br>

<p align="center">
<img src="https://user-images.githubusercontent.com/52833906/160295206-e823d9e3-bd81-4441-8184-17e3fb2061e2.png" alt="mini-moi management screen" style="width:50%">
</p>

<br>

# <a name='install'></a> Installing <sub><sub>[Back to top](#top)</sub></sub> 

If you have already Python (at least 3.8) installed on your machine, you can directly download & install the app in a few steps:
- Download the latest release
- Install the `pip` requirements
- Run the app

<br>

## 1. Download the latest release

Download the latest (release)[https://github.com/No9005/mini-moi/releases] or `git clone` the project. It's up to you. <br>
After downloading (and unzipping the file) you are ready for: 

<br>

## 2. Install requirements

Jump into your terminal and `cd` into the project folder. There you use the command

<br>

```terminal
$ pip install -r requirements.txt
```

<br>

after the installation has finished, you are ready to run the app. Just write the following and the app is starting up (takes a few seconds depending on your system):

<br>

```terminal
$ python app.py
```

<br>

> _Note:_ <br>
> _If you have multiple python versions installed, you may need to use the `python3` command instead of `python`_

<br>

## FAQ: Tips during install

Below are some tips & tricks.

- **`venv` recommended**: <br> As with all python installations, you should not install packages directly into your main path. <br> It is recommended to use a virtual environment (`.venv`) to keep the main system clean. <br> You can use your virtual environment manager of your choice. I do prefere the `pipenv` manager. <br> If you use `pipenv` you can use the following commands to install (in your app directory) everything: <br>

<br>

```terminal
$ pipenv install -r requirements.txt
```

<br>

- **Windows user**: <br> You have to install the **Visual C++ build tools** to enable the wheel backwards compatible building.

<br>

# <a name='how'></a> Quickstart <sub><sub>[Back to top](#top)</sub></sub> 





 is a program based on python (in particular flask as backend) and the combination of HTML, CSS & javscript for the User Interface. <br>
It runs locally on your pc on **127.0.0.1:8080**. <br>
It supports adding, editing and deleting products, subscriptions & consumers. 
A bulk importer allows quick addition of multiple items. <br>

<br>




<br>
<br>

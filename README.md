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
4. [Additional infos](#why)
 

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

After setting up the app (you can set your prefered language in the **Settings** menu), you can start adding your service related data. <br>
You can use either the data **input masks** or the **bulk importert**. Both options are found in the **Management** tab.

<br>

<p align="center">
<img src="https://user-images.githubusercontent.com/52833906/160431860-46f87d87-13ea-483f-b39d-2eff0d808d71.png"/>
</p>

<br>

## A. Input mask
Click on one of the table buttons (`Customers`, `Categories`, `Subcategories`, `Products`, `Abos`) to fetch the current available data (which is - suprise, suprise - empty):

<br>


<p align="center">
<img src="https://user-images.githubusercontent.com/52833906/160432687-4e14ff54-2111-4b97-b37e-dd7bb041aa10.png"/>
</p>

<br>

Next, click on the `+` sign to create a new row and insert your data. If you do not like your data, you can remove the row by clicking on the `remove circle`on the right. <br>
If you are finished with your input, you can use the `cloud button` to send it to the database. <br>
Columns which are automatically added by the app are marked as **Auto.** 

<br>

<p align="center">

Add button |  Remove button | Upload button
:-------------------------:|:-------------------------:|:-------------------------:
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/circle-plus.svg" width="50" style="color:#070;" />  |  <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/circle-minus.svg" width="50" style="color:#700;" />  | <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/cloud.svg" width="66" style="color:#e67e22;"/> 

</p>

<br>
<br>


<p align="center">
<img src="https://user-images.githubusercontent.com/52833906/160436308-a4755ed9-876d-4820-be6d-db05040a80f9.png"/>
</p>

<br>

> _Note:_ <br>
> _Some tables are only editable once you have already filled the associated tables. If this is the case for the table you have selected, the app will inform you._

<br>

## B. Mass importer
Below the table buttons is the `Bulk upload` button in light gray. Clicking opens up a new window with the instructions. To use the bulk importing you have to follow in general these steps:

1. **Create a blueprint**: <br>
To create a blueprint you just have to click on the button naming the data you want to input. **Mini Moi** generates an excel file which is located in your home directory under `~/mini-moi/blueprints` . <br> 
Open the file and start inputting your data.

<br>

> _Note:_ <br>
> _Please do not change the name of the file!_

<br>

2. **Edit the excel**: <br>
Copy & paste your data into the excel sheet. As in the **input masks** you do not have to provide information for the `id`. The app will add these automatically. If you are unsure whether to insert data or not, you should do so. The app will automatically remove unneeded information. <br>

<br>

<p align="center">
<img src="https://user-images.githubusercontent.com/52833906/160438906-6a6b4abb-2e35-4688-b9c1-d928f3add3fa.png"/>
</p>

<br>

3. **Push the button**: <br>
Once you are done editing the file, save it and push the red button in the `bulk upload` menu.

<br>

<p align="center">
<img src="https://user-images.githubusercontent.com/52833906/160439321-0f385ad5-5689-49de-86e1-e05f0b7b8d44.png"/>
</p>

<br>

**Mini Moi** will scan your directory and import every blueprint within the folder. <br>
After the job is finished, the app will delete successfull imported blueprints automatically.

<br>


## Create a delivery report
After the data import is done, you can create the report for the next day. <br>
Switch to the `Delivery` tab and click on `Create`. The app will fetch the orders and show you a formatted overview of the next day.

<br>

<p align="center">

Summary |  Detailed overview
:-------------------------:|:-------------------------:
<img src="https://user-images.githubusercontent.com/52833906/160440407-27316c9c-09af-4175-b2c3-9a467a9583c4.png" width="250" />  |  <img src="https://user-images.githubusercontent.com/52833906/160440401-f08da6b3-c280-4077-8ed1-dc71098b81a3.png" width="275" /> 

</p>

<br>

If you want to, you can edit & customize the detailed overview (maybe a customer just called you and requested a little change for tomorrow?). After editing (or not) you can download the presented summary and overview by clicking on the `Download report` button and **Mini Moi** will save it as an excel in your home directory under `~/mini-moi/delivery`. <br>

<br>

You must have already seen the yellow button which says `Book`, right? This button saves the current overview (inclusive all your editing) to the 'Orders' table. This table tracks orders which where made in the past. It also triggers the calculation of the next delivery dates for your abos.

<br>

> _Note:_ <br>
> _After pressing `Book` you are not able to edit or redownload your deliveries for tomorrow! So handle with care!_

<br>

# <a name='why'></a> Additional info <sub><sub>[Back to top](#top)</sub></sub> 
This project was created to help out a frind of mine aaaaaaannnddd... also to check out what I am able to work in 48h. <br>
As you can already imagine, it didn't quite work out as expected. <br>
Anyway, to appreciate all the work and effort, you are also welcome to use the project! :-) <br>

<br>

If you want to know some more of those nitty-gritty technical aspects, please read on. For everyone else: <br>
<br>

Have fun using the app! :-)

<br>
<br>

## Technical details
The app is a combination of python/flask in the backend and HTML, CSS & java script for the UI. <br>
Personally I do not like the GUI tools of python, so it was just natural for me to create this project as the above described combination. <br>
<br>
For the sake of simplicity, the inbuilt **Werkzeug server** was used. The database, which stores the data, is a **sqlite3 lite** database instance. To interact the **sqlAlchemy** ORM is used. <br>
<br>
The rest is pretty straight forward. Bootstrap CSS was used to give myself a jumpstart (although the app is not mobile safe...) and java script was used to call the Flask Backend and populate the tables.
<br>
To stay within your local environment, the Werkzeug server runs on **localhost:8080**. <br>
<br>
<br>

If you have further questions, please do not hesitate to drop me a message. Else you are welcome to have a look at the source code. <br>

<br>

Cheers, Daniel

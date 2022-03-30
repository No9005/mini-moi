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
    1. [Windows](#win-install)
    2. [Linux](#linux-install)
    4. [From Source](#source-install)
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
Below are the instructions to use the app on **Windows 10** & **Linux** <br>
You can also download the source files, modify the project and execute them.

<br>

> _Note:_
> _Indepentend of your os of choice, you need a modern Browser installed on your system. **Mini Moi** was tested with Chrome, Firefox and IE_

<br>

## <a name='win-install'></a> 1. Windows <sub><sub>[Back to top](#top)</sub></sub>
If you are using **Windows 10** you can download the `.exe` which is a self running executable. <br>
The App is not installing anything. **Just plug and play!** <br>
You can find & download the newest release [here](https://github.com/No9005/mini-moi/releases).

<br>

## <a name='linux-install'></a> 2. Linux <sub><sub>[Back to top](#top)</sub></sub>
Download the `.pkg` for Debian, make it executable

<br>

```terminal
$ chmod +x miniMoi 
```

<br>

and start it.

<br>

```terminal
$ ./miniMoi
```

<br>

## <a name='source-install'></a> 4. From source <sub><sub>[Back to top](#top)</sub></sub>

If you have already Python (at least 3.8) installed on your machine, you can directly download & install the app in a few steps:
- Download the [latest](https://github.com/No9005/mini-moi/releases) release
- Install the `pip` requirements
- Run the app

<br>

### Download the latest release

Download the latest (release)[https://github.com/No9005/mini-moi/releases] or `git clone` the project. It's up to you. <br>
After downloading (and unzipping the file) you are ready for: 

<br>

### Install requirements

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

### FAQ: Tips during install from source

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

# <a name='manual'></a> Manual <sub><sub>[Back to top](#top)</sub></sub> 
The core functionality is already explained in the [Quickstart](#how) section. <br>

This section provides you additional infos for:
- Terminology
- `Reporting` tab
- Blueprint format
- Allowed types and formats
- How the next delivery date gets calculated & its options
- What the 'approach' column is for
- Nice to knows about the `Customers` & `Abo` input masks
- Columns & their meaning

<br>

## Terminology
**Mini Moi** is acutally a database with additional business logic. This business logic enables you to trach deliveries, download your overvies, etc. <br>
The graphical interface you see after starting the app is nothing more than a fancy input mask to perform typical database processes (which are `create`, `read`, `update`, `delete`). <br>
When we talk about tables, this means the data tables within the database.

## Reporting Tab
The `Reporting` tab summarizes all previous orders. These orders are displayed for the following time periods:
- **current week**: Orders between today and the last Sunday (inclusive)
- **last week**: Orders between Sunday to Sunday of last week (both)
- **current month**: Orders within the current month
- **current year**: Orders within the current year

For each of these periods you see:
- **Earnings**: Total income.
- **Revenue sources**: Revenues by product category.
- **Selling overview**: Number of sales per product.

<br>

## Blueprint format
The `Blueprint` (created in the `Bulk upload` menu on the `Management` tab) is a `.csv` file containing the column heads of the table you would like to write data to. Each row represents one database entry to create. <br>
The below table shows an example for the `Abo` table:<br>

<br>

id | Customer id | Update data | Cycle type | Interval | Next delivery | Product | Subcategory | Qnt.
:--:|:---------:|:-----------:|:-----------:|:--------:|:-------------:|:-------:|:-----------:|:-----------:
Auto. | Auto. | Auto. | Weekday | Monday | | Bread | cutted | 2
Auto. | Auto. | Auto. | Interval | 4 | | Milk | None | 1

<br>

As you can see, the `Blueprint` has two rows. This means the database will add two entries to the `Abo` table (after the blueprint was successfully uploaded you can see them in the `Abo` input mask on the `Management` tab.). <br>
You can add as many lines as you prefere. Upon uploading, all rows in the csv will be added to the database. <br>

<br>

It is recommended to create the `Blueprints` by using the `Bulk upload` menu (which you can find in the `Management` tab). However, you can also create a blueprint yourself by writing the table column names from the input mask (found in the `Management` tab) into the first row, followed by the database entries you would like to create. <br>

<br>

Please keep in mind, that you have to save the bluprint as `.csv` with semicolons (';') as separators.

<br>

The created file has to be named according to the name of the database table you want to manipulate and the addition *_blueprint* (e.g. for abo its *abo_blueprint.csv*). The database tables are named: <br>

<br>

**table name** | abo | category | subcategory | customers | products
:-------------:|:---:|:--------:|:-----------:|:---------:|:--------:
**file name** | abo_blueprint.csv | category_blueprint.csv | subcategory_blueprint.csv | customers_blueprint.csv | products_blueprint.csv 

<br>

To upload the file you have to move the created file(s) to your home directory `~/mini-moi/blueprints`and hit the red `Push me!` button in the `Bulk upload` menu (located in the `Management` tab). <br>

<br>

As soon as the file was successfully uploaded to your database it gets deleted from the blueprints folder. <br>

<br>

If you would like to see examples, you can check out the (examples)[https://github.com/No9005/mini-moi/tree/main/example] folder of this github project.

<br>

## Allowed types and formats
**Mini Moi** accepts only the following formats:
- Integers (int): whole numbers. Example: 5
- Floats (float): decimals. Example: .8 or 0.8
- Text (str): Normal text. Example: Michael
- python Datetime: A DateTime object. You do not need this type. If you want to provide dates (like 01.10.1988) you can just pass the value and **Mini Moi** tries to convert it to a DateTime object.

If you want to provide a date, you can do this by normally adding your date. However, **Mini Moi** needs one of the following formats to be able to understand it:
- **Year.Month.Day**, for example: 1988.08.20
- **Day.Month.Year**, for example: 20.08.1988
- **Year-Month-Day**, for example: 1988-08-20
- **Day-Month-Year**, for example: 20-08-1988

<br>
<br>

## How the next delivery Date gets calculated & its options
The next delivery date is calculated automatically after you booked the orders. <br>

<br>

> _Note_: <br>
> _Only customers in the current booking process are calculated. This means that customers with delivery dates in the past are not considered!_ <br>
> _To include these customers in future delivery tracking, you need to edit these dates so that they are in the futur!_

<br>

**Mini Moi** recognizes three types for the calculation process:
- Weekly on a specific weekday (e.g. every Friday)
- Every n-days (e.g. every 3 days)
- One time

<br>

Deliveries based on **one time** abonements (`abo`) are only tracked until they are booked. From on onwards they are inactive until you edit the **Next delivery** to be in the futur. <br>
These types of deliveries are market in the `abo` input mask of the `Management` tab as **Cycle type** None.

<br>

<p align="center">
<img src="https://user-images.githubusercontent.com/52833906/160556164-6335f4d3-4e59-4e5c-8d81-01202847bad3.png"/>
</p>

<br>

Other **Cycle types** trigger the calculation of a new delivery date. These are:
- Weekday: You have to provide the day for the delivery. The delivery is calculated to be on the next weeks indicated day.
- Interval: You have to provide the time period for the interval. The next delivery is calculated to be n-days after the current one, where n is the number you provided. <br>

<br>

To sum it all up:
- **Cycle type**: Sets the type of time period for the next delivery calculation
    - Weekday: Every week on the specified day in the **Interval** column.
    - Interval: Every n-days, where n is the specified number in the **Interval** column.
    - None: A one time delivery.

<br>

## What the 'approach' column is for
You can find this column in the `customers` input mask. This number in this column indicates the order of delivery addresses within one city. E.g. If you have two customers for the city of *Berlin* you can set the order of appearance in the delivery overviews as follows:

<br>

id | Date | Name | Surname | Street | Nr | Postal | City | ... | Approach | Notes
:-:|:---:|:-----:|:-------:|:------:|:--:|:------:|:----:|:----:|:-------:|:-----:
1 | - | Hans | Peter | Maximilianstraße | 5 | 83064 | Neuholm | ... | 2 | \<- This customer will be second in the delivery overview
2 | - | Michael | Meier | Baumstr. | 88 | 83064 | Neuholm | ... | 1 | \<- This customer will be first in the delivery overview

<br>

## Nice to knows about the `Customers` & `Abo` input masks
The `customers` input mask has a button in the column **special** which is linked to his abos.

<br>

Special button |  Customer's abos 
:-------------------------:|:-------------------------:
<img src="https://user-images.githubusercontent.com/52833906/160558479-f7c1e9f4-1d1a-42ef-b18b-6f6d43533bf0.png" width="250" />  |  <img src="https://user-images.githubusercontent.com/52833906/160559276-8fd2543b-5522-40aa-a362-6f52dcccfc28.png" width="200" /> 

<br>

If you are adding new entries to the `Abo` table (by the input mask or the bulk importer) you have to supply the **Customer_id**. You can either lookup the customer in the `Customers` input mask tab, or you can just click on **abo button**. <br>
The second method only works for you the selected customer has already at least one abonement.

<br>

## Columns & their meaning
Below is a list of each column (EN version of the app) and their meaning:
- `Customers`:
    - **id**: The unique identifier of the customer within the database. *Automatically assigned by the database*.
    - **date**: The date on which the customer was added. *Automatically added by the database*.
    - **Name**: The first name of the customer.
    - **Surname**: The last name of the customer.
    - **Street**: The street in which the customer lives.
    - **Nr**: The house nr. (as a number)
    - **Postal**: The postal code of the city
    - **City**: The name of the city
    - **Phone**: The phone number of your customer. *optional*
    - **Mobile**: The mobil number of your customer. *optional*
    - **Birthdate**: The Birthdate of your customer.
    - **Approach**: The ordering of appearance in the delivery overview. For further details see: 'What the 'approach' column is for'.
    - **Notes**: Space to add some notes. *optional*
- `Categories`:
    - **id**: The unique identifier. *Automatically added*
    - **name**: The category name. *Needs to be unique*
- `Subcategories`:
    - **id**: The unique identifier. *Automatically added*
    - **name**: The subcategory name. *Needs to be unique*
- `Products`:
    - **id**: The unique identifier. *Automatically added*
    - **Name**: The product name.
    - **Category**: The product category.
    - **Purchase price**: The purchase price of the product (needed for the reporting & overviews).
    - **Selling price**: The selling price of the product (-> your price; needed for the reporting & overview).
    - **Margin**: The margin of the product. **Automatically added*
    - **Store**: The name of the store you buy the product from. *optional*
    - **Phone**: The phone number of the store you buy the product from. *optional*
- `Abos`:
    - **id**: The unique identifier. *Automatically added*
    - **Customer id**: The unique identifier of the customer. _See `Customers`_ _**id**_
    - **Update date**: The date of the last update. *Automatically added*
    - **Cycle type**: The type of the abo interval. *For further information see: How the next delivery Date gets calculated & its options*
        - Options:
            - Weekday: deliveries are set to the specific weekday
            - Interval: deliveries are set to be every n-days.
            - None: One time deliveries.
    - **Interval**: The interval between deliveries. _Applies only if the **Cycle type** is either 'Weekday' or 'Interval'_
    - **Next delivery**: Date of the next delivery.
    - **Product**: The product to deliver.
    - **Subcategory**: The subcategory of the product to deliver (e.g. cutted, whole, etc).
    - **Qnt.**: The quantity of the product.

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

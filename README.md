SquadLog
==========


Crowd source a squad like dataset via a tampermonkey plugin

Contribute to build the dataset
-----------------

1. Install [Tampermonkey](https://tampermonkey.net/) on your browser.
2. Click on the plugin and then "new script".
3. Copy paste the [user script for this project](https://raw.githubusercontent.com/theSage21/SquadMarker/master/user.js) into that place.
4. Save (Ctrl + s)
5. Help build the dataset
    1. Visit a wikipedia page of your choice.
    2. Select some text on the page.
    3. Click on the button named "SQUADMARK" (it appears on the top right of your screen)
    4. Type in the question which would be answered by that text.
    5. Click OK / Press the Enter key
    6. Repeat for another selection of text


How much data has been collected?
--------------

Visiting the [status page](https://stark-springs-69888.herokuapp.com/) shows us basic statistics about the data.


Dataset Releases
----------------

The dataset will be released in the following places:

- Version tagged dataset in this repository itself.
- Kaggle


A new release will be made every 1000 new unique questions. Versions are denoted by `v.1k`, `v.2k`, `v.3k` and so on. Each release consists of

- full wikipedia context page
- question
- extracted answer string
- train, dev, test mask


Notes
------------

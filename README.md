**A Google Workspace Add-on Dataset and its Smart Use**

With the growing popularity of Google Workspace Marketplace, the number of available
applications has increased exponentially. While most of these applications are legitimate and
safe to use, there is also a growing concern about the presence of malicious, advertising and
unusable apps in the marketplace. Google Workspace Marketplace hosts many add-ons which
can be integrated with user's google workspace (e.g., Google drive, sheets, slides, docs ...), it
is increasingly important to detect and identify these addons and those the problematic
addons. In this project, I first use a crawler to regularly collect and maintain the dataset of all
add-ons listed in Google Workspace Marketplace, e. g. description, permission, developer,
privacy policy, demo usage, downloads and reviews, then use NLP and time series analysis to
identify problematic addons. A total of 7 problematic addons were detected among 4734
addons, with a recognition accuracy of 87.5%. In order to prove the migrability and accuracy
of the algorithm, I also crawled the dataset of all addons in the Zoho workspace marketplace,
and after analyzing them in the same way, a total of two problematic addons were detected,
with an accuracy of 100%.

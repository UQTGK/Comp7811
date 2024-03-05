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

随着 Google Workspace Marketplace 的日益普及，可用应用程序的数量呈指数级增长。 虽然这些应用程序中的大多数都是合法且可以安全使用的，但人们也越来越担心市场上存在恶意、广告和无法使用的应用程序。 Google Workspace Marketplace 托管许多可以与用户的 Google Workspace 集成的插件（例如 Google 云端硬盘、表格、幻灯片、文档...），检测和识别这些插件以及有问题的插件变得越来越重要。 在这个项目中，我首先使用抓取工具定期收集和维护 Google Workspace Marketplace 中列出的所有插件的数据集，例如。描述、许可、开发者、隐私政策、演示使用、下载和评论，然后使用 NLP 和时间序列分析来识别有问题的插件。 在4734个插件中，共检测到7个有问题的插件，识别准确率为87.5%。 为了证明算法的可迁移性和准确性，我还爬取了Zoho工作区市场中所有插件的数据集，用同样的方法分析后，总共检测到了两个有问题的插件，准确率100% 。

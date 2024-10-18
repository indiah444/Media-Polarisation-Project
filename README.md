# 📡 Media Polarisation Project

## ❓ Problem Statement

In today's society, the media landscape is highly polarised. Different groups of people often receive radically different information or narratives depending on the media sources they consume. This divergence in coverage can make it difficult for the public to trust any particular source or easily identify bias. This project addresses the challenge of understanding media bias across different outlets.

## 🎯 Project Goal

This project aims to create a service that tracks and analyses how different media outlets cover various topics. The service will allow users to compare the frequency and sentiment of topic coverage between different media sources, enabling them to see  _what_ is being covered and _how_ it is being discussed. This will provide valuable insights into media bias and narrative framing, helping users make more informed decisions about the information they consume.

The overall system will:

- Extract data from RSS feeds belonging to news sources every hour.
- Perform sentiment analysis on this data before storing it in an RDS for ease of access and querying.
- Use this data to create a visually appealing and informative dashboard displaying sentiment across time, topic, and news source.
- The option to receive daily and/or weekly email updates will be available through a subscription page on the dashboard.

## 🛠️ Installation and Setup

This project is split into multiple components, each housed in a separate subfolder. To correctly set up this project and deploy to the cloud, please follow the instructions detailed in the [terraform folder README.md](./terraform/README.md).

## 👥 Contributors

This project was made with major contributions from:

- India Howell ([@indiah444](https://github.com/indiah444))
- Aya Husseini ([@ayahusseini](https://github.com/ayahusseini))
- Megan Lester ([@megansam5](https://github.com/megansam5))
- Shayak Hussain ([@YakMan101](https://github.com/YakMan101))

## How to Contribute 
Additional contributions are welcome! Please fork this repository, write an issue using the [provided template](.github/ISSUE_TEMPLATE/user-story-issue-template.md), and submit a pull request with your proposed changes. Kindly ensure that your code adheres to a high standard (> 8.0 `pylint` score), is well documented, and all associated unit tests pass.

## 📜 License

This project is licensed under MIT License. Please see attached `LICENSE` file for more information.